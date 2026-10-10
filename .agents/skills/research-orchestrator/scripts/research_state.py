#!/usr/bin/env python3
"""Conservative, stdlib-only research records. No agent, shell or job execution.

The event journal is authoritative; state.json is its checked snapshot. Each
newline-terminated, hash-valid event is a commit. A malformed tail is never
discarded implicitly. Read references/record-cli.md for the trust boundary.
"""
from __future__ import annotations

import argparse
import copy
import csv
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import uuid

VERSION = 1
ROLES = ("literature_scout novelty_skeptic research_designer implementation_engineer "
         "experiment_optimizer confirmation_executor compute_scheduler analysis_agent "
         "artifact_author manuscript_author stage_verifier journal_stage_critic scientific_reviewer "
         "citation_auditor documentation_steward").split()
ACCEPTED = {"accepted", "conditionally_accepted"}
SEVERITIES = {"minor", "major", "critical"}
HEX = re.compile(r"^[0-9a-f]{64}$")


class RecordError(ValueError):
    """An invalid, stale or unsupported record; no speculative success is inferred."""


def require(condition, message):
    if not condition:
        raise RecordError(message)


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label}: nonempty string required")
    return value


def integer(value, label, minimum=0, maximum=None):
    require(type(value) is int and value >= minimum and (maximum is None or value <= maximum),
            f"{label}: true integer in range required (booleans are invalid)")
    return value


def fields(value, required, optional=()):
    require(isinstance(value, dict), "JSON object required")
    require(set(required) <= value.keys(), f"Missing fields: {sorted(set(required) - value.keys())}")
    require(value.keys() <= set(required) | set(optional),
            f"Unsupported fields: {sorted(value.keys() - set(required) - set(optional))}")


def strings(value, label, nonempty=True):
    require(isinstance(value, list) and (value or not nonempty), f"{label}: list required")
    for item in value:
        text(item, label)
    require(len(set(value)) == len(value), f"{label}: duplicates forbidden")
    return value


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def encoded(value):
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                          allow_nan=False).encode("utf-8")
    except (ValueError, TypeError) as exc:
        raise RecordError(f"Invalid JSON value: {exc}") from exc


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def hash_file(path):
    hasher = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON object key: {key}")
        result[key] = value
    return result


def loads(value):
    def bad_constant(token):
        raise RecordError(f"Nonfinite JSON number forbidden: {token}")
    try:
        return json.loads(value, object_pairs_hook=_pairs, parse_constant=bad_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RecordError(f"Malformed JSON: {exc}") from exc


def load_json(path):
    return loads(Path(path).read_bytes())


def atomic_write(path, data):
    path = Path(path)
    temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temp.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def write_json(path, value):
    atomic_write(path, encoded(value) + b"\n")


def safe_path(root, name):
    text(name, "path")
    require(not Path(name).is_absolute() and not re.match(r"^[A-Za-z]:", name), "Project-relative path required")
    require("\\" not in name and ":" not in name, "Use portable forward-slash relative paths")
    require(all(x not in ("", ".", "..") for x in name.split("/")), "Unsafe relative path")
    root = Path(root).resolve()
    candidate = root / name
    current = root
    for part in name.split("/"):
        current /= part
        require(not current.is_symlink() and not (hasattr(current, "is_junction") and current.is_junction()),
                "Symlink/junction artifact paths are unsupported")
    require(candidate.resolve().is_relative_to(root), "Path escapes project")
    return candidate


def file_binding(root, descriptor):
    fields(descriptor, ["path", "sha256", "format"], ["required_fields", "min_rows", "empty_reason"])
    require(isinstance(descriptor["sha256"], str) and HEX.fullmatch(descriptor["sha256"]), "sha256: lowercase digest required")
    require(descriptor["format"] in {"text", "json", "jsonl", "csv", "binary"}, "Unsupported format; YAML requires a real parser outside this helper")
    path = safe_path(root, descriptor["path"])
    require(path.is_file(), f"Missing file: {descriptor['path']}")
    require(hash_file(path) == descriptor["sha256"], f"Changed file: {descriptor['path']}")
    return path


def check_output(root, descriptor):
    path = file_binding(root, descriptor)
    require(path.stat().st_size > 0, f"Empty output file: {descriptor['path']}")
    fmt = descriptor["format"]
    required = strings(descriptor.get("required_fields", []), "required_fields", False)
    minimum = integer(descriptor.get("min_rows", 1), "min_rows")
    empty_reason = descriptor.get("empty_reason")
    if empty_reason is not None:
        text(empty_reason, "empty_reason")
        require(minimum == 0, "Declared empty results require min_rows: 0")
    rows = None
    if fmt != "binary":
        try:
            content = path.read_text(encoding="utf-8-sig")
        except UnicodeError as exc:
            raise RecordError("Text output is not valid UTF-8") from exc
        require(bool(content.strip()), "Whitespace-only output")
        if fmt == "text":
            substantive = "\n".join(line for line in content.splitlines()
                                    if line.strip() and not line.lstrip().startswith("#"))
            require(bool(substantive.strip()), "Headings-only output")
            require(substantive.strip().lower() not in {"todo", "tbd", "placeholder", "coming soon", "...", "n/a"},
                    "Recognized untouched placeholder")
            require(not required, "required_fields applies to structured outputs")
        elif fmt == "json":
            value = loads(content)
            require(isinstance(value, (dict, list)), "Structured JSON object/array required")
            rows = value if isinstance(value, list) else ([value] if value else [])
        elif fmt == "jsonl":
            require(content.endswith("\n"), "JSONL final line is not terminated")
            rows = [loads(line) for line in content.splitlines() if line.strip()]
        elif fmt == "csv":
            reader = csv.DictReader(io.StringIO(content), strict=True)
            require(reader.fieldnames and len(reader.fieldnames) == len(set(reader.fieldnames)), "CSV unique header required")
            rows = list(reader)
            require(all(None not in row and all(v is not None for v in row.values()) for row in rows), "Malformed CSV row width")
    if rows is not None:
        require(len(rows) >= minimum, f"Insufficient rows: need {minimum}, got {len(rows)}")
        require(rows or empty_reason, "Empty result requires an explicit reason and min_rows: 0")
        for row in rows:
            require(isinstance(row, dict), "Structured rows must be objects")
            require(all(k in row and row[k] is not None and row[k] != "" for k in required), "Missing meaningful required field")
    return {"valid": True, "path": descriptor["path"], "sha256": descriptor["sha256"],
            "rows": len(rows) if rows is not None else None,
            "scope": "structural-and-hash-only; binary open/render and scientific substance need independent inspection"}


def validate_profile(profile, launch=False, runtime=None):
    fields(profile, ["schema_version", "profile_name", "roles"],
           ["autonomy", "allow_silent_model_fallback", "max_parallel_workers", "swarm", "remote_compute",
            "negative_result_recovery", "completion_backup", "publication", "logging", "manuscript_quality", "external_frameworks"])
    require(type(profile["schema_version"]) is int and profile["schema_version"] == VERSION, "Unsupported profile schema")
    text(profile["profile_name"], "profile_name")
    require(isinstance(profile["roles"], dict) and set(profile["roles"]) == set(ROLES), "Exactly the 15 declared roles are required")
    require(profile.get("allow_silent_model_fallback", False) is False, "Silent model fallback is unsupported")
    integer(profile.get("max_parallel_workers", 3), "max_parallel_workers", 1, 99)
    for section in ("swarm", "remote_compute", "negative_result_recovery", "completion_backup", "publication", "logging", "manuscript_quality"):
        if section in profile: require(isinstance(profile[section], dict), f"{section}: object required")
    if "swarm" in profile:
        swarm = profile["swarm"]
        fields(swarm, [], ["enabled", "max_agents_per_swarm", "allocation", "overflow", "recursive_spawning"])
        integer(swarm.get("max_agents_per_swarm", 100), "max_agents_per_swarm", 1, 100)
        require(type(swarm.get("enabled", True)) is bool, "swarm.enabled must be boolean")
        for key in ("allocation", "overflow", "recursive_spawning"):
            if key in swarm: text(swarm[key], "swarm." + key)
    if runtime is not None:
        fields(runtime, ["models"])
        require(isinstance(runtime["models"], dict) and runtime["models"], "runtime.models must map model IDs to efforts")
        for model, efforts in runtime["models"].items():
            text(model, "runtime model"); strings(efforts, "runtime efforts")
    unresolved = []
    inherited = []
    for role, settings in profile["roles"].items():
        fields(settings, ["model", "effort"], ["inherit_authorized"])
        inherit = settings.get("inherit_authorized", False)
        require(type(inherit) is bool, "inherit_authorized must be boolean")
        model, effort = settings["model"], settings["effort"]
        if model is None or effort is None:
            require(model is None and effort is None, f"{role}: partial settings are ambiguous")
            if inherit:
                inherited.append(role)
            else:
                unresolved.append(role)
        else:
            text(model, role + " model"); text(effort, role + " effort")
            require(not inherit, "Choose explicit settings or authorized inheritance, not both")
            if launch:
                require(runtime is not None and model in runtime["models"] and effort in runtime["models"][model],
                        f"{role}: configured model/effort not supported by supplied current runtime")
    publication = profile.get("publication", {})
    if "critic_quality_gate" in publication:
        gate = publication["critic_quality_gate"]
        require(isinstance(gate, dict) and gate, "critic_quality_gate must be a nonempty object when supplied")
        fields(gate, [], ["minimum_criteria", "default_criteria", "score_min", "score_max", "aggregation", "pass_threshold",
                          "comparison", "max_reloop_iterations", "hard_blockers_override_score", "post_reloop_decision_owner", "minor_issue_conditional_advance"])
        for key, expected in {"minimum_criteria": 5, "score_min": 0, "score_max": 100,
                              "pass_threshold": 90, "max_reloop_iterations": 2}.items():
            require(type(gate.get(key, expected)) is int and gate.get(key, expected) == expected, f"Profile cannot change gate {key}")
        integer(gate.get("default_criteria", 7), "default_criteria", 5)
        require(gate.get("aggregation", "equal-weight-arithmetic-mean") == "equal-weight-arithmetic-mean", "Unsupported score aggregation")
        require(gate.get("comparison", ">=") == ">=", "Threshold comparison must be >=")
        require(gate.get("hard_blockers_override_score", True) is True, "Hard blockers cannot be disabled")
        require(gate.get("minor_issue_conditional_advance", True) is True, "Unsupported conditional advancement policy")
        require(gate.get("post_reloop_decision_owner", "main-orchestrator-or-explicitly-delegated-executor") ==
                "main-orchestrator-or-explicitly-delegated-executor", "Unsupported exception ownership policy")
    if launch:
        require(not unresolved, "Profile template is not launch-ready: " + ", ".join(unresolved))
    return {"valid": True, "configuration_complete": not unresolved,
            "launch_ready": launch and not unresolved and (runtime is not None or len(inherited) == len(ROLES)),
            "unassigned_roles": unresolved, "explicitly_inherited_roles": inherited,
            "runtime_checked": launch and runtime is not None,
            "scope": "configuration validation; actual launch/settings require runtime receipts"}


def rubric_check(rubric):
    fields(rubric, ["version", "criteria"])
    text(rubric["version"], "rubric version")
    require(isinstance(rubric["criteria"], list) and len(rubric["criteria"]) >= 5, "At least five criteria required")
    ids = []
    for c in rubric["criteria"]:
        fields(c, ["id", "definition", "evidence_expectation"])
        for k in c: text(c[k], k)
        ids.append(c["id"])
    require(len(ids) == len(set(ids)), "Rubric criterion IDs must be distinct")
    require(len({c["definition"].strip().casefold() for c in rubric["criteria"]}) == len(ids), "Rubric definitions must be distinct")


def review_binding(stage):
    rev = stage["revisions"][-1]
    return digest({"stage_instance_id": stage["id"], "revision_id": rev["id"],
                   "inputs": stage["inputs"], "outputs": rev.get("outputs", []),
                   "protocol_hash": stage["protocol_hash"], "rubric_hash": stage["rubric_hash"],
                   "operating_hash": stage.get("operating_hash"),
                   "required_checks": stage["required_checks"], "dependency_bindings": stage["dependency_bindings"]})


def verify_reviews(stage, verifier, critic, epoch):
    base = ["id", "actor", "binding", "revision_id", "epoch", "context", "evidence"]
    fields(verifier, base + ["verdict", "checks"])
    fields(critic, base + ["blockers", "scores"])
    actors = {r["producer"] for r in stage["revisions"]}
    require(verifier["actor"] != critic["actor"] and verifier["id"] != critic["id"], "Critic and verifier must be distinct")
    for receipt in (verifier, critic):
        text(receipt["id"], "receipt id"); text(receipt["actor"], "receipt actor")
        require(receipt["actor"] not in actors, "Producer cannot independently review its own lineage")
        require(receipt["context"] == "none", "Fresh review must record context: none")
        require(type(receipt["epoch"]) is int and receipt["epoch"] == epoch, "Stale receipt ownership epoch")
        require(receipt["binding"] == review_binding(stage), "Stale review input/output/rubric binding")
        require(receipt["revision_id"] == stage["current_revision"], "Wrong review revision")
        strings(receipt["evidence"], "receipt evidence")
    require(verifier["verdict"] in {"pass", "revise", "stop", "inconclusive"}, "Unsupported verifier verdict")
    require(isinstance(verifier["checks"], list), "checks must be a list")
    names = []
    for check in verifier["checks"]:
        fields(check, ["name", "result"], ["evidence"])
        text(check["name"], "check name")
        require(check["result"] in {"pass", "fail", "unknown"}, "Unsupported check result")
        if "evidence" in check: strings(check["evidence"], "check evidence")
        names.append(check["name"])
    require(len(names) == len(set(names)) and set(names) == set(stage["required_checks"]), "Frozen required checks must match exactly")
    strings(critic["blockers"], "critic blockers", False)
    require(isinstance(critic["scores"], list), "scores must be a list")
    ids, values = [], []
    for score in critic["scores"]:
        fields(score, ["criterion_id", "score", "justification", "evidence", "gap"])
        text(score["criterion_id"], "criterion_id")
        values.append(integer(score["score"], "score", 0, 100))
        text(score["justification"], "score justification"); strings(score["evidence"], "score evidence")
        require(isinstance(score["gap"], str), "gap must be a string")
        if score["score"] < 90: text(score["gap"], "Below-standard score needs concrete gap")
        ids.append(score["criterion_id"])
    require(len(ids) >= 5 and len(ids) == len(set(ids)) and set(ids) == {c["id"] for c in stage["rubric"]["criteria"]},
            "Scores must cover every distinct frozen criterion exactly once")
    total = sum(values)
    return {"verifier": copy.deepcopy(verifier), "critic": copy.deepcopy(critic),
            "score_sum": total, "criterion_count": len(values), "mean": total / len(values),
            "numeric_pass": total >= 90 * len(values)}


class Project:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.records = self.root / ".research"
        self.log = self.records / "events.jsonl"
        self.snapshot = self.records / "state.json"
        self.lockfile = self.records / "owner.lock"

    def initialize(self, original_input, profile=None, project_id=None):
        text(original_input, "original input")
        require(not self.records.exists(), "Existing .research is never overwritten; use status/resume")
        if profile is not None: validate_profile(profile)
        self.root.mkdir(parents=True, exist_ok=True)
        self.records.mkdir()  # Atomic mkdir prevents concurrent initializers.
        for directory in ("agents", "compute", "recovery", "reproduction", "delivery", "verification", "criticism",
                          "logs", "originality", "framework-jobs"):
            (self.records / directory).mkdir()
        contract = {"schema_version": VERSION, "project_id": project_id or str(uuid.uuid4()),
                    "original_input": original_input, "effective_profile": profile,
                    "operating_contract_status": "pending", "authorizations": [], "budgets": None,
                    "notice": "Initialization is intake only; no scientific, paid, launch or author authority is inferred."}
        text(contract["project_id"], "project_id")
        write_json(self.records / "contract.json", contract)
        state = {"schema_version": VERSION, "project_id": contract["project_id"], "original_input": original_input,
                 "created_at": stamp(), "sequence": 0, "epoch": 0, "status": "active", "contract_hash": digest(contract),
                 "stages": {}, "issues": {}, "task_ids": [], "receipt_ids": [],
                 "operating_contracts": [], "operating_contract_status": "pending"}
        self.log.touch(exist_ok=False)
        self._commit(state, "project.initialize", "0" * 64, {"original_input_preserved": True})
        return self.read()

    @contextmanager
    def _mutex(self):
        require(self.records.is_dir(), "Project is not initialized")
        path = self.records / "transaction.lock"
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise RecordError("Transaction lock exists; reconcile its process before any manual recovery; never auto-stolen") from exc
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(encoded({"pid": os.getpid(), "created_at": stamp()}))
                stream.flush(); os.fsync(stream.fileno())
            yield
        finally:
            path.unlink()

    def _scan(self):
        raw = self.log.read_bytes()
        head, state, offset = "0" * 64, None, 0
        result = {"head": head, "state": state, "valid_bytes": 0, "error": None, "tail_recoverable": False}
        lines = raw.splitlines(keepends=True)
        for idx, line in enumerate(lines):
            try:
                require(line.endswith(b"\n"), "Unterminated event tail")
                event = loads(line)
                fields(event, ["schema_version", "sequence", "previous_hash", "timestamp", "op", "details", "state", "hash"])
                require(type(event["schema_version"]) is int and event["schema_version"] == VERSION, "Unsupported event schema; explicit migration required")
                expected = 1 if state is None else state["sequence"] + 1
                require(type(event["sequence"]) is int and event["sequence"] == expected, "Broken journal sequence")
                require(event["previous_hash"] == head, "Broken event hash chain")
                body = {k: v for k, v in event.items() if k != "hash"}
                require(digest(body) == event["hash"], "Event hash mismatch")
                require(event["state"].get("schema_version") == VERSION and event["state"].get("sequence") == expected,
                        "Unsupported/broken event state")
                head, state = event["hash"], event["state"]
                offset += len(line)
                result.update(head=head, state=state, valid_bytes=offset)
            except (RecordError, AttributeError, TypeError) as exc:
                message = str(exc)
                # Only a final syntactically torn/malformed line can be quarantined.
                recoverable = idx == len(lines) - 1 and (not line.endswith(b"\n") or message.startswith("Malformed JSON:"))
                result.update(error=message, tail_recoverable=recoverable)
                break
        if state is None and result["error"] is None:
            result["error"] = "Missing initialization commit"
        return result

    def _snapshot_ok(self, scan):
        try:
            snap = load_json(self.snapshot)
            fields(snap, ["schema_version", "head_hash", "state"])
            return type(snap["schema_version"]) is int and snap["schema_version"] == VERSION and snap["head_hash"] == scan["head"] and snap["state"] == scan["state"]
        except (OSError, RecordError):
            return False

    def _healthy(self):
        scan = self._scan()
        require(scan["error"] is None, "Journal unavailable: " + str(scan["error"]))
        require(self._snapshot_ok(scan), "Snapshot missing/stale/malformed; explicit recover required")
        require(digest(load_json(self.records / "contract.json")) == scan["state"]["contract_hash"], "Contract changed; unsupported unrecorded amendment")
        return scan

    def read(self):
        return copy.deepcopy(self._healthy()["state"])

    def _commit(self, state, op, head, details=None):
        state["sequence"] += 1
        event = {"schema_version": VERSION, "sequence": state["sequence"], "previous_hash": head,
                 "timestamp": stamp(), "op": op, "details": details or {}, "state": state}
        event["hash"] = digest(event)
        with self.log.open("ab") as stream:
            stream.write(encoded(event) + b"\n")
            stream.flush(); os.fsync(stream.fileno())
        write_json(self.snapshot, {"schema_version": VERSION, "head_hash": event["hash"], "state": state})

    def acquire(self, owner, for_recovery=False):
        text(owner, "owner")
        with self._mutex():
            require(not self.lockfile.exists(), "Ownership lock exists; no automatic stale-lock takeover")
            scan = self._scan() if for_recovery else self._healthy()
            require(scan["state"] is not None, "No valid project state for ownership")
            lock = {"schema_version": VERSION, "owner": owner, "epoch": scan["state"]["epoch"] + 1,
                    "acquired_at": stamp(), "pid_observation": os.getpid(), "recovery_only": bool(for_recovery)}
            with self.lockfile.open("xb") as stream:
                stream.write(encoded(lock)); stream.flush(); os.fsync(stream.fileno())
            if not for_recovery:
                state = copy.deepcopy(scan["state"]); state["epoch"] = lock["epoch"]
                self._commit(state, "ownership.acquire", scan["head"], lock)
                return {**lock, "sequence": state["sequence"]}
            return {**lock, "sequence": scan["state"]["sequence"], "recovery_required": True}

    def _ownership(self, owner, epoch, expected, scan, recovery=False):
        require(self.lockfile.exists(), "Acquire project ownership before mutation")
        lock = load_json(self.lockfile)
        require(lock.get("owner") == owner and type(epoch) is int and lock.get("epoch") == epoch, "Wrong owner or stale epoch")
        require(type(expected) is int and expected == scan["state"]["sequence"], "Expected sequence conflict")
        if not recovery:
            require(not lock.get("recovery_only"), "Recovery-only ownership cannot mutate before recovery")
            require(scan["state"]["epoch"] == epoch, "State ownership epoch mismatch")
        return lock

    def release(self, owner, epoch, expected):
        with self._mutex():
            scan = self._healthy()
            self._ownership(owner, epoch, expected, scan)
            state = copy.deepcopy(scan["state"])
            self._commit(state, "ownership.release", scan["head"], {"owner": owner, "epoch": epoch})
            self.lockfile.unlink()
            return {"released": True, "sequence": state["sequence"]}

    def recover(self, owner, epoch, expected, quarantine_tail=False):
        with self._mutex():
            scan = self._scan()
            require(scan["state"] is not None, "Recovery needs a valid initialization prefix")
            lock = self._ownership(owner, epoch, expected, scan, recovery=True)
            details = {"snapshot_rebuilt": True}
            if self.snapshot.exists():
                try:
                    existing = load_json(self.snapshot)
                except RecordError:
                    existing = None
                if isinstance(existing, dict) and "schema_version" in existing:
                    require(type(existing["schema_version"]) is int and existing["schema_version"] == VERSION,
                            "Unsupported snapshot schema; explicit migration required")
                if not self._snapshot_ok(scan):
                    saved = self.records / "recovery" / (uuid.uuid4().hex + ".snapshot-original.bin")
                    with saved.open("xb") as stream:
                        stream.write(self.snapshot.read_bytes()); stream.flush(); os.fsync(stream.fileno())
                    details.update(preserved_snapshot=saved.relative_to(self.root).as_posix(),
                                   preserved_snapshot_sha256=hash_file(saved))
            if scan["error"]:
                require(quarantine_tail and scan["tail_recoverable"], "Cannot repair journal; only explicit malformed final-tail quarantine is supported")
                original = self.log.read_bytes()
                archive = self.records / "recovery" / (uuid.uuid4().hex + ".events-original.bin")
                with archive.open("xb") as stream:
                    stream.write(original); stream.flush(); os.fsync(stream.fileno())
                details.update(preserved_original=archive.relative_to(self.root).as_posix(),
                               preserved_sha256=hash_file(archive), valid_bytes=scan["valid_bytes"])
                atomic_write(self.log, original[:scan["valid_bytes"]])
            state = copy.deepcopy(scan["state"]); state["epoch"] = epoch
            self._commit(state, "records.recover", scan["head"], details)
            if lock.get("recovery_only"):
                lock["recovery_only"] = False
                write_json(self.lockfile, lock)
            return {"recovered": True, "sequence": state["sequence"], **details}

    def _artifact_list(self, artifacts, outputs=False):
        require(isinstance(artifacts, list) and artifacts, "Nonempty artifact list required")
        names = []
        for artifact in artifacts:
            (check_output if outputs else file_binding)(self.root, artifact)
            names.append(artifact["path"])
        require(len(names) == len(set(names)), "Duplicate artifact paths")

    def _protocol_inputs(self, artifacts, protocol_hash):
        self._artifact_list(artifacts)
        require(any(item["sha256"] == protocol_hash for item in artifacts),
                "protocol_hash must match an actual hash-verified declared input file; an early stage assignment or charter is sufficient")

    def _dependencies(self, state, stage):
        for dep in stage["dependencies"]:
            parent = state["stages"][dep]
            require(parent["status"] in ACCEPTED, f"Dependency not accepted: {dep}")
            self._fresh(state, parent)
            require(stage["dependency_bindings"][dep] == review_binding(parent), f"Changed dependency: {dep}")

    def _fresh(self, state, stage):
        require(digest(stage["rubric"]) == stage["rubric_hash"], "Frozen rubric changed")
        self._protocol_inputs(stage["inputs"], stage["protocol_hash"])
        if stage["revisions"][-1].get("outputs"):
            self._artifact_list(stage["revisions"][-1]["outputs"], outputs=True)
        self._dependencies(state, stage)

    def _invalidate(self, state, stage_id, reason):
        queue, seen = [stage_id], set()
        while queue:
            current = queue.pop()
            if current in seen: continue
            seen.add(current)
            stage = state["stages"][current]
            stage["status"] = "invalidated"
            stage.setdefault("invalidations", []).append({"reason": reason, "at": stamp()})
            for name, child in state["stages"].items():
                if current in child["dependencies"]: queue.append(name)
        return sorted(seen)

    def _blockers(self, state, stage):
        return [i for i in state["issues"].values() if i["stage_instance_id"] == stage["id"] and
                i["status"] != "verified_resolved" and (i["blocking"] or i["severity"] != "minor")]

    def _mandatory(self, state, stage):
        reviews = stage.get("reviews")
        require(reviews is not None, "Current independent reviews required")
        require(reviews["verifier"]["verdict"] == "pass", "Independent verifier did not pass")
        require(all(c["result"] == "pass" for c in reviews["verifier"]["checks"]), "Required check missing/failed/unknown")
        require(not reviews["critic"]["blockers"] and not self._blockers(state, stage), "Unresolved blocker overrides scores")

    def transact(self, owner, epoch, expected, operation):
        encoded(operation)  # Forbid NaN even through the Python API.
        with self._mutex():
            scan = self._healthy()
            self._ownership(owner, epoch, expected, scan)
            state = copy.deepcopy(scan["state"])
            require(isinstance(operation, dict) and type(operation.get("schema_version")) is int and
                    operation["schema_version"] == VERSION, "Unsupported transaction schema")
            text(operation.get("op"), "op")
            details = self._apply(state, operation, owner, epoch)
            self._commit(state, operation["op"], scan["head"], {"record": operation, **(details or {})})
            return copy.deepcopy(state)

    def _apply(self, state, op, owner, epoch):
        kind = op["op"]
        common = ["schema_version", "op"]
        def schema(required=(), optional=()): fields(op, common + list(required), optional)
        if kind in {"project.configure", "project.amend"}:
            if kind == "project.configure":
                schema(["operating_contract"])
                require(not state.get("operating_contracts"), "Existing configuration needs an explicit amendment")
            else:
                schema(["operating_contract", "previous_hash", "reason"], ["affected_stages"])
                require(state.get("active_operating_hash") == op["previous_hash"], "Stale operating-contract amendment")
                text(op["reason"], "amendment reason")
            record = op["operating_contract"]
            fields(record, ["id", "scope", "autonomy", "effective_profile", "budgets", "deliverables", "authorizations", "authorization"])
            text(record["id"], "operating contract ID"); text(record["scope"], "operating scope")
            require(record["autonomy"] in {"checkpointed", "bounded_autonomous", "plan_only"}, "Unsupported recorded autonomy")
            profile_result = validate_profile(record["effective_profile"])
            fields(record["budgets"], ["summary", "evidence"])
            text(record["budgets"]["summary"], "budget summary"); strings(record["budgets"]["evidence"], "budget evidence")
            strings(record["deliverables"], "deliverables")
            require(isinstance(record["authorizations"], list), "authorizations must be a list")
            for authority in record["authorizations"]:
                fields(authority, ["action", "scope", "evidence"])
                text(authority["action"], "authorized action"); text(authority["scope"], "authorization scope")
                strings(authority["evidence"], "authorization evidence")
            self._authorization(record["authorization"])
            versions = state.setdefault("operating_contracts", [])
            require(record["id"] not in {v["record"]["id"] for v in versions}, "Operating contract ID already used")
            versions.append({"record": record, "hash": digest(record), "recorded_at": stamp(), "epoch": epoch})
            state["active_operating_hash"] = digest(record)
            state["operating_contract_status"] = "configured" if profile_result["configuration_complete"] else "pending_profile"
            if kind == "project.amend":
                affected = strings(op.get("affected_stages", list(state["stages"])), "affected_stages", False)
                for sid in affected:
                    require(sid in state["stages"], "Unknown affected stage")
                    self._invalidate(state, sid, "Operating contract amendment: " + op["reason"])
            return
        if kind == "project.resume":
            schema(["reason", "authorization"])
            require(state["status"] == "stopped", "Only a stopped project can resume")
            text(op["reason"], "resume reason")
            self._authorization(op["authorization"], user_resume=True)
            state.setdefault("resumptions", []).append({"reason": op["reason"], "authorization": op["authorization"],
                "previous_stop_reason": state.get("stop_reason"), "recorded_at": stamp(), "epoch": epoch})
            state["status"] = "active"
            return
        if kind == "project.stop":
            schema(["reason"]); text(op["reason"], "stop reason")
            state["status"] = "stopped"; state["stop_reason"] = op["reason"]
            return
        if kind == "stage.replan":
            schema(["source_stage_instance_id", "stage_instance_id", "stage", "phase", "protocol_hash", "dependencies", "inputs",
                    "required_checks", "rubric", "task_id", "producer", "allocation", "amendment"])
            source_id = text(op["source_stage_instance_id"], "source_stage_instance_id")
            require(source_id in state["stages"], "Unknown replan predecessor")
            source = state["stages"][source_id]
            require(op["protocol_hash"] != source["protocol_hash"], "A new label does not constitute a changed protocol")
            amendment = op["amendment"]
            fields(amendment, ["actor", "authority_scope", "previous_binding", "reason", "material_change", "evidence", "independent_review"])
            require(amendment["actor"] == owner, "Only the current coordinator records the authorized replan")
            require(amendment["previous_binding"] == review_binding(source), "Stale predecessor binding")
            for key in ("authority_scope", "reason", "material_change"): text(amendment[key], key)
            strings(amendment["evidence"], "amendment evidence")
            independent = amendment["independent_review"]
            fields(independent, ["actor", "context", "verdict", "evidence"])
            text(independent["actor"], "independent replan reviewer")
            require(independent["actor"] not in {r["producer"] for r in source["revisions"]} | {owner, op["producer"]},
                    "Replan requires independent nonproducer material-change assessment")
            require(independent["context"] == "none" and independent["verdict"] == "substantive_replan", "Independent substantive replan receipt required")
            strings(independent["evidence"], "independent replan evidence")
            invalidated = self._invalidate(state, source_id, "Substantive authorized replan: " + amendment["reason"])
            create = {k: v for k, v in op.items() if k not in {"source_stage_instance_id", "amendment"}}
            create["op"] = "stage.create"
            self._apply(state, create, owner, epoch)
            new = state["stages"][op["stage_instance_id"]]
            new["predecessor"] = source_id
            new["root_lineage"] = source.get("root_lineage", source_id)
            new["amendment"] = amendment
            source.setdefault("successors", []).append(new["id"])
            return {"invalidated": invalidated, "new_lineage": new["id"], "preserved_predecessor": source_id}
        if kind == "stage.create":
            schema(["stage_instance_id", "stage", "phase", "protocol_hash", "dependencies", "inputs", "required_checks", "rubric", "task_id", "producer", "allocation"])
            require(state["status"] == "active", "Stopped project cannot reserve dispatch")
            sid = text(op["stage_instance_id"], "stage_instance_id")
            require(sid not in state["stages"], "Stage lineage already exists; renaming to evade revision caps is not authorized")
            integer(op["stage"], "stage", 1, 23); text(op["phase"], "phase")
            require(isinstance(op["protocol_hash"], str) and HEX.fullmatch(op["protocol_hash"]), "protocol_hash must be sha256")
            rubric_check(op["rubric"]); strings(op["required_checks"], "required_checks")
            dependencies = strings(op["dependencies"], "dependencies", False)
            for dep in dependencies: require(dep in state["stages"], "Unknown dependency")
            self._protocol_inputs(op["inputs"], op["protocol_hash"])
            stage = {"id": sid, "stage": op["stage"], "phase": op["phase"], "protocol_hash": op["protocol_hash"],
                     "operating_hash": state.get("active_operating_hash", state["contract_hash"]),
                     "dependencies": dependencies, "dependency_bindings": {dep: review_binding(state["stages"][dep]) for dep in dependencies},
                     "inputs": op["inputs"], "rubric": op["rubric"], "rubric_hash": digest(op["rubric"]),
                     "required_checks": op["required_checks"], "status": "producing", "reloop_count": 0, "revisions": [], "reviews": None}
            self._dependencies(state, stage)
            fields(op["allocation"], ["budget"]); text(op["allocation"]["budget"], "allocation budget")
            self._reserve(state, stage, op["task_id"], op["producer"], op["allocation"], epoch)
            state["stages"][sid] = stage
            return
        if kind.startswith("issue."):
            return self._issue(state, op, epoch)
        require(kind in {"stage.submit", "stage.review", "stage.reserve", "stage.gate", "stage.invalidate", "stage.stop", "stage.reconcile", "stage.reopen"}, "Unsupported operation")
        sid = text(op.get("stage_instance_id"), "stage_instance_id")
        require(sid in state["stages"], "Unknown stage instance")
        stage = state["stages"][sid]
        if kind == "stage.invalidate":
            schema(["stage_instance_id", "reason"]); text(op["reason"], "invalidation reason")
            return {"invalidated": self._invalidate(state, sid, op["reason"])}
        if kind == "stage.stop":
            schema(["stage_instance_id", "reason"]); text(op["reason"], "stop reason")
            stage["status"] = "stopped"; stage["stop_reason"] = op["reason"]
            for child in list(state["stages"].values()):
                if sid in child["dependencies"]: self._invalidate(state, child["id"], "Upstream stopped: " + sid)
            return
        require(state["status"] == "active", "Project is stopped")
        if kind == "stage.reopen":
            schema(["stage_instance_id", "inputs", "task_id", "producer", "plan", "remedy"], ["dependencies"])
            require(stage["status"] in {"invalidated", "stopped"}, "Reopen requires explicit invalidation or stop first")
            remedy = op["remedy"]
            fields(remedy, ["actor", "context", "previous_binding", "verdict", "reason", "evidence"])
            text(remedy["actor"], "remedy reviewer")
            require(remedy["actor"] not in {r["producer"] for r in stage["revisions"]} | {owner, op["producer"]},
                    "Remedy needs an independent nonproducer reviewer")
            require(remedy["context"] == "none" and remedy["previous_binding"] == review_binding(stage) and
                    remedy["verdict"] == "remedy_approved", "Current independently reviewed remedy required")
            text(remedy["reason"], "remedy reason"); strings(remedy["evidence"], "remedy evidence")
            self._plan(state, op["plan"])
            self._protocol_inputs(op["inputs"], stage["protocol_hash"])
            require(digest(stage["rubric"]) == stage["rubric_hash"], "Frozen rubric cannot change on reopen")
            stage["inputs"] = op["inputs"]
            stage["operating_hash"] = state.get("active_operating_hash", state["contract_hash"])
            if "dependencies" in op:
                deps = strings(op["dependencies"], "replacement dependencies", False)
                require(sid not in deps and all(dep in state["stages"] for dep in deps), "Invalid replacement dependency")
                # Every replacement must already be accepted; an invalidated descendant
                # cannot become a parent and create a cycle through this transaction.
                require(all(state["stages"][dep]["status"] in ACCEPTED for dep in deps), "Replacement dependency must be accepted")
                stage.setdefault("dependency_history", []).append({"dependencies": stage["dependencies"],
                    "bindings": stage["dependency_bindings"], "remedy": remedy})
                stage["dependencies"] = deps
            stage["dependency_bindings"] = {dep: review_binding(state["stages"][dep]) for dep in stage["dependencies"]}
            self._dependencies(state, stage)
            previous = stage["revisions"][-1]
            if previous.get("outputs"):
                require(stage["reloop_count"] < 2, "Two-reloop lineage cap exhausted; no third correction")
                stage["reloop_count"] += 1
                self._reserve(state, stage, op["task_id"], op["producer"], op["plan"], epoch)
            else:
                require(op["task_id"] == previous["task_id"] and op["producer"] == previous["producer"],
                        "Unreturned reservation must retain its existing task and producer")
                previous.setdefault("remedies", []).append({"old_inputs": previous["inputs"], "old_epoch": previous["epoch"], "remedy": remedy})
                previous.update(inputs=copy.deepcopy(stage["inputs"]), epoch=epoch, plan=op["plan"])
            stage.setdefault("remedies", []).append({"receipt": remedy, "recorded_at": stamp()})
            stage["reviews"] = None; stage["status"] = "producing"
            return
        require(stage["status"] not in {"stopped", "invalidated"}, "Stage requires supported remedy/replan; no automatic reset")
        self._fresh(state, stage)
        if kind == "stage.reconcile":
            schema(["stage_instance_id", "task_id", "previous_epoch", "disposition", "evidence"])
            require(stage["status"] == "producing", "Only existing producer reservations can be reconciled")
            rev = stage["revisions"][-1]
            require(type(op["previous_epoch"]) is int and op["previous_epoch"] == rev["epoch"] and rev["epoch"] < epoch,
                    "Reconciliation requires the precise earlier reservation epoch")
            require(op["task_id"] == rev["task_id"], "Reconcile the original task ID")
            require(op["disposition"] in {"not_started", "stopped", "completed_return_available"},
                    "Unresolved/live ownership cannot be reconciled for redispatch")
            strings(op["evidence"], "reconciliation evidence")
            rev.setdefault("ownership_reconciliations", []).append({"previous_epoch": rev["epoch"], "new_epoch": epoch,
                "disposition": op["disposition"], "evidence": op["evidence"], "recorded_at": stamp()})
            rev["epoch"] = epoch
        elif kind == "stage.submit":
            schema(["stage_instance_id", "revision_id", "task_id", "outputs", "evidence_kind", "scientific_outcome"])
            require(stage["status"] == "producing", "Only a reserved producing revision can submit")
            rev = stage["revisions"][-1]
            require(op["revision_id"] == rev["id"] and op["task_id"] == rev["task_id"], "Return does not match reservation")
            require(rev["epoch"] == epoch, "Stale reserved task epoch; explicit reconciliation is required")
            require(op["evidence_kind"] in {"unverified", "synthetic_fixture", "executed_simulation", "observed_real_system", "nonempirical"}, "Unsupported evidence kind; invented empirical evidence cannot submit")
            require(op["scientific_outcome"] in {"positive", "negative", "inconclusive", "not_applicable"}, "Unsupported scientific outcome")
            self._artifact_list(op["outputs"], outputs=True)
            if any(o["format"] == "binary" for o in op["outputs"]):
                require("open_or_render" in stage["required_checks"], "Binary output requires frozen open_or_render inspection check")
            rev.update(outputs=op["outputs"], evidence_kind=op["evidence_kind"], scientific_outcome=op["scientific_outcome"], status="submitted")
            for issue in state["issues"].values():
                if issue["stage_instance_id"] == sid and issue["status"] == "verified_resolved" and issue["verification"]["outputs"] != op["outputs"]:
                    self._reopen_issue(issue, "Corrected output binding changed; current independent verification required")
            stage["status"] = "reviewing"
        elif kind == "stage.review":
            schema(["stage_instance_id", "verifier", "critic"])
            require(stage["status"] == "reviewing", "Only current submitted output can be reviewed")
            prior = stage["reviews"]
            rev = stage["revisions"][-1]
            if prior is not None:
                require(prior["verifier"]["epoch"] < epoch and prior["critic"]["epoch"] < epoch,
                        "A current-epoch review cannot be replaced to shop for a higher score")
                require(rev.get("review_refresh_count", 0) < 2, "Bounded same-output review refresh allowance exhausted")
            reviews = verify_reviews(stage, op["verifier"], op["critic"], epoch)
            for r in (op["verifier"], op["critic"]):
                require(r["id"] not in state["receipt_ids"], "Receipt ID already used")
                state["receipt_ids"].append(r["id"])
            if prior is not None:
                rev.setdefault("review_history", []).append(prior)
                rev["review_refresh_count"] = rev.get("review_refresh_count", 0) + 1
            stage["reviews"] = reviews
            stage["revisions"][-1]["reviews"] = reviews
        elif kind == "stage.reserve":
            schema(["stage_instance_id", "task_id", "producer", "plan"])
            require(stage["status"] == "reviewing" and stage["reviews"] is not None, "A reviewed failed output is required before revision")
            require(stage["reloop_count"] < 2, "Two-reloop lineage cap exhausted")
            reviews = stage["reviews"]
            mandatory_ok = reviews["verifier"]["verdict"] == "pass" and all(c["result"] == "pass" for c in reviews["verifier"]["checks"]) and not reviews["critic"]["blockers"] and not self._blockers(state, stage)
            require(not reviews["numeric_pass"] or not mandatory_ok, "Passing output cannot consume a failure reloop")
            self._plan(state, op["plan"])
            stage["reloop_count"] += 1
            self._reserve(state, stage, op["task_id"], op["producer"], op["plan"], epoch)
            stage["status"] = "producing"; stage["reviews"] = None
        elif kind == "stage.gate":
            schema(["stage_instance_id", "decision"], ["exception"])
            require(stage["status"] == "reviewing", "Gate requires current reviewing state")
            require(stage["reviews"] is not None, "Missing critic/verifier receipts")
            reviews = stage["reviews"]
            verify_reviews(stage, reviews["verifier"], reviews["critic"], epoch)
            self._mandatory(state, stage)
            if op["decision"] == "advance":
                require("exception" not in op, "Ordinary advancement cannot carry an exception")
                require(reviews["numeric_pass"], "Unrounded mean is below 90")
                stage["status"] = "accepted"
            elif op["decision"] == "conditional_advance":
                self._conditional(state, stage, op.get("exception"), owner, epoch)
                stage["status"] = "conditionally_accepted"
                stage["exception"] = op["exception"]
            else: raise RecordError("Gate decision must be advance or conditional_advance")
            stage["accepted_binding"] = review_binding(stage)
            stage["revisions"][-1]["status"] = stage["status"]

    def _plan(self, state, plan):
        fields(plan, ["reason", "issue_ids", "expected_changes", "cheapest_check", "closure_criteria", "budget"])
        for key in ("reason", "expected_changes", "cheapest_check", "closure_criteria", "budget"): text(plan[key], key)
        strings(plan["issue_ids"], "plan issue_ids", False)
        for issue in plan["issue_ids"]: require(issue in state["issues"], "Unknown revision issue")

    def _authorization(self, authority, user_resume=False):
        fields(authority, ["source", "actor", "scope", "evidence"])
        allowed = {"user_decision"} if user_resume else {"user_decision", "standing_user_instruction", "delegated_project_authority"}
        require(authority["source"] in allowed, "Actual supplied authority record required; coordinator guesses are invalid")
        text(authority["actor"], "authority actor"); text(authority["scope"], "authority scope")
        strings(authority["evidence"], "authority evidence")

    def _reopen_issue(self, issue, reason):
        if issue["status"] == "verified_resolved":
            issue.setdefault("closure_history", []).append({"fix": copy.deepcopy(issue["fix"]),
                "verification": copy.deepcopy(issue["verification"]), "closed_at": issue["closed_at"]})
        issue["status"] = "open"
        issue.setdefault("reopenings", []).append({"reason": reason, "recorded_at": stamp()})

    def _reserve(self, state, stage, task, producer, plan, epoch):
        text(task, "task_id"); text(producer, "producer")
        require(task not in state["task_ids"], "Task ID already reserved; reconcile existing task rather than duplicate")
        state["task_ids"].append(task)
        rid = f"{stage['id']}:r{stage['reloop_count']}"
        stage["current_revision"] = rid
        stage["revisions"].append({"id": rid, "task_id": task, "producer": producer, "epoch": epoch,
                                   "inputs": copy.deepcopy(stage["inputs"]), "reserved_at": stamp(), "plan": plan, "status": "reserved"})

    def _conditional(self, state, stage, receipt, owner, epoch):
        require(stage["reloop_count"] == 2 and len(stage["revisions"]) == 3 and
                all(r.get("reviews") for r in stage["revisions"]), "Conditional advancement requires three actually scored versions and reloop 2")
        require(not stage["reviews"]["numeric_pass"], "Numerically passing outputs use ordinary advancement")
        fields(receipt, ["actor", "decision_owner", "binding", "epoch", "revision_ids", "reason", "options_considered",
                         "accepted_limitations", "scope_claim_changes", "resource_implications", "downstream_effects", "next_action", "minor_disposition"], ["delegation"])
        actors = {r["producer"] for r in stage["revisions"]}
        require(receipt["actor"] not in actors, "Producer cannot approve unresolved faults")
        require(receipt["binding"] == review_binding(stage) and type(receipt["epoch"]) is int and receipt["epoch"] == epoch, "Stale exception binding")
        require(receipt["revision_ids"] == [r["id"] for r in stage["revisions"]], "Exception must retain all three revision IDs")
        if receipt["decision_owner"] == "coordinator":
            require(receipt["actor"] == owner and "delegation" not in receipt, "Coordinator exception must identify current owner")
        elif receipt["decision_owner"] == "delegated_executor":
            delegation = receipt.get("delegation")
            fields(delegation, ["by", "to", "scope", "evidence"])
            require(delegation["by"] == owner and delegation["to"] == receipt["actor"], "Invalid coordinator delegation")
            text(delegation["scope"], "delegation scope"); strings(delegation["evidence"], "delegation evidence")
        else: raise RecordError("Exception owner must be coordinator or delegated_executor")
        for key in ("reason", "scope_claim_changes", "resource_implications", "downstream_effects", "next_action"):
            text(receipt[key], key)
        strings(receipt["options_considered"], "options_considered"); strings(receipt["accepted_limitations"], "accepted_limitations")
        proof = receipt["minor_disposition"]
        fields(proof, ["actor", "context", "binding", "epoch", "issue_ids", "severity", "blocking", "downstream_satisfied", "rationale", "evidence"])
        require(proof["actor"] not in actors | {receipt["actor"]}, "Minor disposition requires an independent nonproducer assessor")
        require(proof["actor"] == stage["reviews"]["verifier"]["actor"], "Minor disposition must come from current independent verifier")
        require(proof["context"] == "none" and proof["binding"] == review_binding(stage) and proof["epoch"] == epoch, "Stale minor-disposition proof")
        require(proof["severity"] == "minor" and proof["blocking"] is False and proof["downstream_satisfied"] is True, "Only independently nonblocking minor limitations are eligible")
        text(proof["rationale"], "severity rationale"); strings(proof["evidence"], "minor disposition evidence")
        expected = {i["id"] for i in state["issues"].values() if i["stage_instance_id"] == stage["id"] and i["status"] != "verified_resolved"}
        strings(proof["issue_ids"], "minor issue_ids", False)
        require(set(proof["issue_ids"]) == expected, "Exception must retain every unresolved stage issue")

    def _issue(self, state, op, epoch):
        base = ["schema_version", "op", "issue_id"]
        iid = text(op.get("issue_id"), "issue_id")
        if op["op"] == "issue.open":
            fields(op, base + ["stage_instance_id", "severity", "blocking", "owner", "description", "affected", "reproduction", "expected_behavior"])
            require(iid not in state["issues"], "Issue ID already exists")
            require(op["stage_instance_id"] in state["stages"], "Unknown issue stage")
            require(op["severity"] in SEVERITIES and type(op["blocking"]) is bool, "Invalid issue severity/blocking")
            if op["severity"] in {"major", "critical"}: require(op["blocking"], "Major/critical issues cannot be declared nonblocking")
            for key in ("owner", "description", "reproduction", "expected_behavior"): text(op[key], key)
            self._artifact_list(op["affected"])
            issue = {k: copy.deepcopy(v) for k, v in op.items() if k not in {"schema_version", "op", "issue_id"}}
            issue.update(id=iid, status="open", opened_at=stamp())
            state["issues"][iid] = issue
            if op["blocking"] and state["stages"][op["stage_instance_id"]]["status"] in ACCEPTED:
                self._invalidate(state, op["stage_instance_id"], "New blocking issue: " + iid)
            return
        require(iid in state["issues"], "Unknown issue")
        issue = state["issues"][iid]
        if op["op"] == "issue.reopen":
            fields(op, base + ["reason"]); text(op["reason"], "issue reopening reason")
            require(issue["status"] == "verified_resolved", "Issue already unresolved")
            self._reopen_issue(issue, op["reason"])
            if issue["blocking"] and state["stages"][issue["stage_instance_id"]]["status"] in ACCEPTED:
                self._invalidate(state, issue["stage_instance_id"], "Reopened blocking issue: " + iid)
            return
        require(issue["status"] != "verified_resolved", "Closed issue cannot be silently rewritten")
        if op["op"] == "issue.fix":
            fields(op, base + ["fix"])
            fix = op["fix"]
            fields(fix, ["actor", "description", "outputs", "evidence"])
            require(fix["actor"] == issue["owner"], "Fix receipt must name assigned owner")
            text(fix["description"], "fix description"); strings(fix["evidence"], "fix evidence")
            self._artifact_list(fix["outputs"], outputs=True)
            current = state["stages"][issue["stage_instance_id"]]["revisions"][-1].get("outputs")
            require(fix["outputs"] == current, "Issue correction must bind current submitted stage outputs")
            issue["fix"] = fix; issue["status"] = "awaiting_verification"
        elif op["op"] == "issue.close":
            fields(op, base + ["verification"])
            require(issue["status"] == "awaiting_verification", "Recorded fix required before closure")
            verify = op["verification"]
            fields(verify, ["actor", "context", "outputs", "correction", "regression", "original_reproduction", "close_reason"])
            producers = {r["producer"] for r in state["stages"][issue["stage_instance_id"]]["revisions"]}
            text(verify["actor"], "closure verifier")
            require(verify["actor"] not in producers | {issue["owner"], issue["fix"]["actor"]}, "Producer/fixer cannot close its own issue")
            require(verify["context"] == "none", "Closure requires fresh independent inspection")
            current = state["stages"][issue["stage_instance_id"]]["revisions"][-1].get("outputs")
            require(verify["outputs"] == issue["fix"]["outputs"] == current, "Stale issue correction outputs")
            self._artifact_list(verify["outputs"], outputs=True)
            for name in ("correction", "regression", "original_reproduction"):
                check = verify[name]; fields(check, ["result", "evidence"])
                require(check["result"] == ("reproduced" if name == "original_reproduction" else "pass"), "Independent correction, original reproduction and regression must be established")
                strings(check["evidence"], name + " evidence")
            text(verify["close_reason"], "close_reason")
            issue["verification"] = verify; issue["status"] = "verified_resolved"; issue["closed_at"] = stamp()
        else: raise RecordError("Unsupported issue operation")

    def status(self):
        try:
            scan = self._scan()
            snapshot_ok = self._snapshot_ok(scan)
            state = scan["state"] or {}
            errors = [scan["error"]] if scan["error"] else []
            if not snapshot_ok: errors.append("Snapshot missing/stale/malformed")
            try:
                if digest(load_json(self.records / "contract.json")) != state.get("contract_hash"):
                    errors.append("Contract hash mismatch")
            except (OSError, RecordError) as exc: errors.append(str(exc))
            stale = {}
            for sid, stage in state.get("stages", {}).items():
                try: self._fresh(state, stage)
                except (RecordError, OSError) as exc: stale[sid] = str(exc)
            lock = None
            if self.lockfile.exists():
                try: lock = load_json(self.lockfile)
                except (OSError, RecordError) as exc: errors.append("Unreadable owner lock: " + str(exc))
            return {"schema_version": VERSION, "healthy": not errors and not stale,
                    "sequence": state.get("sequence"), "epoch": state.get("epoch"), "project_id": state.get("project_id"),
                    "status": state.get("status", "unknown"), "errors": errors, "stale_stages": stale,
                    "operating_contract_status": state.get("operating_contract_status", "pending"),
                    "active_operating_hash": state.get("active_operating_hash"),
                    "stages": {sid: {"stage": s["stage"], "phase": s["phase"], "status": s["status"],
                                "effective_status": "invalidated" if sid in stale else s["status"],
                                "reloop_count": s["reloop_count"], "revision_id": s["current_revision"],
                                "mean": s["reviews"]["mean"] if s.get("reviews") else None} for sid, s in state.get("stages", {}).items()},
                    "unresolved_issues": [iid for iid, i in state.get("issues", {}).items() if i["status"] != "verified_resolved"],
                    "ownership": lock, "tail_recoverable": scan["tail_recoverable"], "read_only": True,
                    "notice": "Recorded identities/authority/checks are assertions requiring independent runtime and scientific evidence."}
        except (OSError, RecordError) as exc:
            return {"healthy": False, "status": "unknown", "sequence": None, "errors": [str(exc)], "read_only": True}

    def review_packet(self, stage_id):
        state = self.read()
        require(stage_id in state["stages"], "Unknown stage instance")
        stage = state["stages"][stage_id]
        require(stage["status"] == "reviewing", "Review packet requires submitted outputs")
        self._fresh(state, stage)
        return {"schema_version": VERSION, "stage_instance_id": stage_id,
                "revision_id": stage["current_revision"], "epoch": state["epoch"],
                "binding": review_binding(stage), "inputs": stage["inputs"],
                "outputs": stage["revisions"][-1]["outputs"], "rubric": stage["rubric"],
                "rubric_hash": stage["rubric_hash"], "required_checks": stage["required_checks"],
                "read_only": True,
                "notice": "Send the scoped evidence separately to fresh verifier and critic; this packet contains no verdict."}

    def validate(self):
        result = self.status()
        return {"valid": result["healthy"], **result}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Preserve one scientific input; no execution authority inferred")
    init.add_argument("project")
    inp = init.add_mutually_exclusive_group(required=True)
    inp.add_argument("--input"); inp.add_argument("--input-file")
    init.add_argument("--profile"); init.add_argument("--project-id")
    profile = sub.add_parser("profile-validate", help="Check profile template or actual runtime model/effort configuration")
    profile.add_argument("profile"); profile.add_argument("--launch", action="store_true"); profile.add_argument("--runtime")
    hashed = sub.add_parser("hash", help="SHA-256 of a file")
    hashed.add_argument("path")
    output = sub.add_parser("check-output", help="Validate a JSON artifact descriptor and actual file")
    output.add_argument("project"); output.add_argument("descriptor")
    acquire = sub.add_parser("lock-acquire", help="Exclusive cooperative ownership; never steals locks")
    acquire.add_argument("project"); acquire.add_argument("--owner", required=True)
    acquire.add_argument("--for-recovery", action="store_true")
    for command in ("lock-release", "transact", "recover"):
        cmd = sub.add_parser(command)
        cmd.add_argument("project"); cmd.add_argument("--owner", required=True)
        cmd.add_argument("--epoch", type=int, required=True); cmd.add_argument("--expected-sequence", type=int, required=True)
        if command == "transact": cmd.add_argument("--record", required=True)
        if command == "recover": cmd.add_argument("--quarantine-tail", action="store_true")
    for command in ("status", "validate"):
        sub.add_parser(command).add_argument("project")
    packet = sub.add_parser("review-packet", help="Read current hash-bound scoped review inputs without a verdict")
    packet.add_argument("project"); packet.add_argument("stage_instance_id")
    args = parser.parse_args(argv)
    try:
        if args.command == "profile-validate":
            result = validate_profile(load_json(args.profile), args.launch, load_json(args.runtime) if args.runtime else None)
        elif args.command == "hash": result = {"path": args.path, "sha256": hash_file(args.path)}
        elif args.command == "check-output": result = check_output(Path(args.project), load_json(args.descriptor))
        else:
            project = Project(args.project)
            if args.command == "init":
                original = Path(args.input_file).read_text(encoding="utf-8") if args.input_file else args.input
                result = project.initialize(original, load_json(args.profile) if args.profile else None, args.project_id)
            elif args.command == "lock-acquire": result = project.acquire(args.owner, args.for_recovery)
            elif args.command == "lock-release": result = project.release(args.owner, args.epoch, args.expected_sequence)
            elif args.command == "transact": result = project.transact(args.owner, args.epoch, args.expected_sequence, load_json(args.record))
            elif args.command == "recover": result = project.recover(args.owner, args.epoch, args.expected_sequence, args.quarantine_tail)
            elif args.command == "status": result = project.status()
            elif args.command == "review-packet": result = project.review_packet(args.stage_instance_id)
            else: result = project.validate()
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
        return 1 if args.command == "validate" and not result["valid"] else 0
    except (RecordError, OSError, csv.Error) as exc:
        print(json.dumps({"error": str(exc), "type": type(exc).__name__}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
