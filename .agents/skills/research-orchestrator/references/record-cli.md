# Deterministic research record helper

`scripts/research_state.py` runs with Python 3.10+ and the standard library. It records and checks project state; it never launches agents, executes experiments, manages Git, calls providers, purchases compute, uploads files, or schedules wakeups. Native orchestration remains responsible for these actions and their actual receipts.

## Trust and enforcement boundary

Mechanically enforced: exact input preservation; immutable contract hash; strict supported transaction schemas; portable project-relative file paths; SHA-256 checks; basic output structure; duplicate-key/NaN rejection; frozen distinct rubrics; true integer scores; exact unrounded threshold; distinct declared actors; receipt/revision/ownership bindings; applicable declared required-check results; recorded blockers; persistent revision reservations; two same-lineage reloops; dependency invalidation; independent correction/regression closure records; exclusive cooperative local writing; epoch/sequence conflicts; hash-chained commits; explicit evidence-preserving tail recovery.

Independently verified by agents: scientific substance, source support, meaningful criterion differences, adequate required-check inventory, correct route/DAG selection, actual execution, actual identity/model settings/fresh context, permission and resource sufficiency, truth of evidence locators, whether a protocol change is substantive, external process fencing, and author decisions. Passing structural records is **not** scientific validation or runtime attestation. A string saying that a check passed does not establish the check occurred. Bind actual inspection/execution receipts in the relevant input/output descriptors and supply their precise evidence locators.

No false model defaults: the installed profile is a template. Initialization with that template is allowed; designated launches require the separate profile/runtime checks and actual configured launch arguments. `stage.create` reserves a record; it does not grant execution or spending authority.

The helper is intended for bounded, local project metadata on a filesystem with reliable exclusive creation, replace and flush semantics. Each event contains the complete resulting state, favoring inspectability over large-database efficiency. A network sync directory is not a demonstrated distributed lock. Anyone with unrestricted filesystem access can alter records or impersonate an actor; this is cooperative integrity, not an adversarial security boundary.

## CLI and exit codes

Run from any directory using the actual installed helper path. Examples below use `$rsHelper` and `$rsProject` as PowerShell variables:

```powershell
$rsHelper = 'C:/Users/eshan/.agents/skills/research-orchestrator/scripts/research_state.py'
$rsProject = 'C:/path/to/project'
python $rsHelper --help
python $rsHelper init $rsProject --input 'Investigate a bounded retrieval question.' --profile 'C:/path/to/configured-profile.json'
python $rsHelper status $rsProject
python $rsHelper validate $rsProject
```

Use `--input-file INPUT.txt` instead of `--input` to preserve multiline text verbatim. `--project-id ID` is optional; otherwise a UUID is generated. `.research` must not already exist. Existing project import is a separate reviewed workflow, never reinitialization.

| Command | Behavior |
| --- | --- |
| `init PROJECT (--input TEXT \| --input-file PATH) [--profile PATH] [--project-id ID]` | Write the intake contract, initialization event and snapshot; create scoped record directories. No fabricated completed stages or authorizations. |
| `profile-validate PROFILE [--launch] [--runtime RUNTIME_JSON]` | Validate template/configuration; launch mode additionally requires assignments or explicitly authorized inheritance and actual supplied runtime compatibility. |
| `hash PATH` | Return SHA-256 of an actual file. |
| `check-output PROJECT DESCRIPTOR_JSON` | Check the declared artifact's path, hash and supported structure. |
| `lock-acquire PROJECT --owner OWNER [--for-recovery]` | Atomically acquire ownership; return epoch and sequence. Never steal an existing lock. |
| `transact PROJECT --owner OWNER --epoch N --expected-sequence N --record OP_JSON` | Validate and commit one typed operation under exclusive ownership and sequence comparison. |
| `review-packet PROJECT STAGE_ID` | Read the current scoped input/output/rubric binding without a verdict. |
| `lock-release PROJECT --owner OWNER --epoch N --expected-sequence N` | Record release and remove the matching ownership lock. External work must already be reconciled. |
| `status PROJECT` | Read-only status of the latest valid prefix, snapshot health, stale artifacts, counts, issues and ownership observations. |
| `validate PROJECT` | Same inspection with a failing exit code for unhealthy records/stale artifacts. |
| `recover PROJECT --owner OWNER --epoch N --expected-sequence N [--quarantine-tail]` | Explicitly rebuild a stale/missing snapshot, or preserve and quarantine a malformed final journal tail. Never executes historical events. |

Successful commands emit JSON to stdout. Invalid commands/records emit a JSON error to stderr and exit 2. `validate` exits 1 when its report has `valid:false`. `status` exits 0 even for an unhealthy project so a caller can inspect its structured report; always inspect `healthy`, `errors`, and `stale_stages`.

Ownership example:

```powershell
$rsLock = python $rsHelper lock-acquire $rsProject --owner 'coordinator-run-001' | ConvertFrom-Json
$rsStatus = python $rsHelper status $rsProject | ConvertFrom-Json
python $rsHelper transact $rsProject --owner 'coordinator-run-001' --epoch $rsLock.epoch --expected-sequence $rsStatus.sequence --record 'C:/path/to/stage-create.json'
```

Refresh the sequence after each successful transaction. A conflict means reconcile the actual newer state; do not blindly retry an already-dispatched action. Owners should be unique run identifiers. Record the helper's intended task ID before dispatch, and reconcile that ID after interruption.

## On-disk commit schema

`.research/contract.json` contains `schema_version:1`, `project_id`, exact `original_input`, optional `effective_profile`, and initially pending operating-contract metadata. This intake snapshot remains immutable. Use `project.configure`/`project.amend` below to preserve later user answers and effective settings as versioned canonical records. The protocol, author decisions and detailed receipts can be immutable, versioned input artifacts referenced by stages; the coordinator retains their own supported carriers.

`.research/events.jsonl` is authoritative. Every event has exactly `schema_version`, `sequence`, `previous_hash`, `timestamp`, `op`, `details`, `state`, and `hash`. The hash is SHA-256 of canonical UTF-8 JSON for all fields except `hash` (`sort_keys=True`, compact separators, no NaN). Sequences start at 1; the first predecessor hash is 64 zeros. A complete newline-terminated, schema-valid, hash-valid event is the commit boundary. The resulting full state has the same sequence. The event is flushed before atomically replacing the snapshot.

`.research/state.json` contains exactly `{schema_version:1, head_hash, state}` and must equal the valid journal head. Core state keys are `schema_version`, `project_id`, `original_input`, `created_at`, `sequence`, `epoch`, `status`, `contract_hash`, `stages`, `issues`, `task_ids`, `receipt_ids`, `operating_contracts`, and `operating_contract_status`. Each operating version retains `{record,hash,recorded_at,epoch}`; `active_operating_hash` identifies the current version. All stage/issue changes are journaled; do not maintain a second mutable issue ledger. Optional `stop_reason` and `resumptions` preserve stop/resume history.

`owner.lock` records `schema_version`, `owner`, `epoch`, `acquired_at`, `pid_observation`, and `recovery_only`. PID is an observation, not proof of a live coordinator or stopped external job. `transaction.lock` is a short exclusive critical-section marker carrying `pid` and `created_at`. Its presence blocks competing transactions even from the same owner. A crashed critical-section marker is never deleted automatically; verify process termination and preserve the marker before a deliberate operator recovery. No time expiry, heartbeat or PID reuse grants takeover.

Do not edit snapshots, counters or historical events. The helper rejects unsupported versions for mutation; no schema-migration engine is supplied. Preserve unsupported bytes and write an explicitly reviewed migration if one becomes necessary.

## Profiles

Use `assets/role-profile.json` as the complete template. All 15 role keys must exist. Each role is exactly `{"model":null,"effort":null}` until configured, or has nonempty model/effort strings. Partial assignments are rejected. Explicit user authorization to inherit can be represented as `{"model":null,"effort":null,"inherit_authorized":true}`. Never add that authorization because configuration is inconvenient.

`profile-validate` reports `configuration_complete` separately from `launch_ready`. Plain template validation never claims runtime launch readiness. Explicit launch validation consumes a current runtime capability record such as:

```json
{"models":{"actual-model-id-from-runtime":["low","medium","high"]}}
```

This example names no real model. Copy actual supported values from the current runtime. Run:

```powershell
python $rsHelper profile-validate 'C:/path/to/profile.json'
python $rsHelper profile-validate 'C:/path/to/profile.json' --launch --runtime 'C:/path/to/runtime-capabilities.json'
```

Silently falling back is rejected. Known rubric threshold/reloop policy fields cannot change the native 90/2 contract. Other profile policy sections are coordinator instructions, not mechanically executed budgets or provider adapters. A successful launch check still needs actual dispatch arguments and observed settings where exposed.

## Artifact descriptors

An artifact is a JSON object with `path`, `sha256`, `format`, and optionally `required_fields`, `min_rows`, `empty_reason`:

```json
{"path":"analysis/results-v1.json","sha256":"ACTUAL_64_CHARACTER_LOWERCASE_HASH","format":"json","required_fields":["status","count"],"min_rows":1}
```

The hash token above must be replaced with `hash` output. Paths are project-relative with forward slashes, no traversal/absolute paths, and no symlink/junction components. Formats are `text`, `json`, `jsonl`, `csv`, `binary`. JSON/JSONL rows must be objects; required fields must exist and not be null/empty strings. JSONL must end in newline. CSV requires unique column names and consistent row widths. Text rejects empty/whitespace, headings only and recognized whole-file placeholders. These are preliminary checks; a meaningful scientific document still needs inspection.

For a genuinely empty structured result: set `min_rows:0` and a nonempty `empty_reason`, for example no matches under a prespecified query. A zero-byte file still fails. Binary files are hashed and must be nonempty; submitted binary artifacts require a frozen `open_or_render` check and an actual independent open/render inspection receipt. YAML parsing, image/PDF decoding, plotting and semantic text inspection are outside this helper.

## Stage transactions

Every operation is a JSON file containing `schema_version:1` and `op`. Unknown fields are rejected. The schemas below name all operation fields. Quoted examples are record shapes; evidence, hashes, settings and verdicts must come from the real corresponding work. Synthetic tests must remain clearly marked `synthetic_fixture`.

### Record the operating contract after intake

`project.configure` requires `operating_contract` and is valid once. The complete operating record has exactly `id`, `scope`, `autonomy` (`checkpointed`, `bounded_autonomous`, `plan_only`), `effective_profile` (complete profile object), `budgets:{summary,evidence}`, `deliverables` (nonempty list), `authorizations` (possibly empty list of `{action,scope,evidence}`), and `authorization:{source,actor,scope,evidence}`. Every summary/scope/action is nonempty; evidence is a nonempty locator list pointing to actual supplied decisions or budget records. Authorization source is `user_decision`, `standing_user_instruction`, or `delegated_project_authority`. Those labels record a decision; they do not establish its provenance without the referenced original.

Configured null assignments remain `operating_contract_status:"pending_profile"`; a structurally complete assigned/explicitly inherited profile becomes `configured`. Runtime compatibility and actual launch settings still require the independent launch check. This permits scientific input and known operating answers to be recorded before the user has supplied models, without inventing them.

`project.amend` requires `previous_hash` equal to the current active operating hash, a new unique full `operating_contract`, and `reason`. Optional `affected_stages` lists the instances whose obligations changed; their descendants are invalidated. Omission conservatively invalidates every existing stage. An explicit empty list is appropriate only when independently established that current evidence and obligations remain valid. Original intake and every operating version remain intact. Budgets are evidence references; this helper does not debit or enforce a remote spending ledger.

### Create and reserve the original revision

`stage.create` additionally requires: `stage_instance_id` (unique), `stage` (true integer 1–23), `phase` (nonempty project-defined phase), `protocol_hash`, `dependencies` (IDs), `inputs` (nonempty descriptor list), `required_checks` (distinct names), `rubric`, `task_id` (unique), `producer`, `allocation:{budget}`.

```json
{
  "schema_version":1,"op":"stage.create","stage_instance_id":"s09-protocol-v1","stage":9,"phase":"planning",
  "protocol_hash":"ACTUAL_PROTOCOL_HASH","dependencies":[],
  "inputs":[{"path":"protocol/protocol-v1.json","sha256":"ACTUAL_PROTOCOL_HASH","format":"json"}],
  "required_checks":["substance","scope_controls","scientific_support","protocol_validity"],
  "rubric":{"version":"1","criteria":[
    {"id":"fidelity","definition":"Protocol follows the declared research question","evidence_expectation":"Question-to-outcome mapping"},
    {"id":"rigor","definition":"Comparison and independent units are valid","evidence_expectation":"Controls and unit specification"},
    {"id":"alternatives","definition":"Rival explanations can be tested","evidence_expectation":"Rivals and disconfirmation tests"},
    {"id":"reproducibility","definition":"Protocol is executable from declared inputs","evidence_expectation":"Pinned data, code and commands"},
    {"id":"feasibility","definition":"Plan fits agreed compute and time","evidence_expectation":"Bounded estimate and protected confirmation allocation"}
  ]},
  "task_id":"protocol-producer-001","producer":"actual-producer-id","allocation":{"budget":"Reference the actual bounded project allocation"}
}
```

Use actual route dependencies, not the empty illustrative list when predecessors are required. The helper checks declared dependencies, not a universal hard-coded DAG: applicability and phase-specific obligations are independently reviewed. It freezes the rubric/checks/protocol, captures dependency and operating-contract hash bindings, sets `reloop_count:0`, and reserves `<stage_instance_id>:r0` before any producer dispatch. Criteria must have distinct IDs and definitions, at least five, with a version and evidence expectations. **The protocol hash must equal the SHA-256 of at least one actual declared input file.** The example deliberately uses the same `ACTUAL_PROTOCOL_HASH` for `protocol_hash` and its protocol input descriptor; replace both with the result of `hash`. For intake or early research stages, that file can be the current stage assignment or charter; no future experiment protocol is required. Hash checks continue on review, gating and status, so changed protocol bytes block stale acceptance.

### Submit the reserved output

`stage.submit` requires `stage_instance_id`, `revision_id`, `task_id`, nonempty `outputs`, `evidence_kind`, `scientific_outcome`. It accepts only the current producing reservation and current ownership epoch. Example:

```json
{"schema_version":1,"op":"stage.submit","stage_instance_id":"s09-protocol-v1","revision_id":"s09-protocol-v1:r0","task_id":"protocol-producer-001","outputs":[{"path":"protocol/final-v1.json","sha256":"ACTUAL_OUTPUT_HASH","format":"json"}],"evidence_kind":"nonempirical","scientific_outcome":"not_applicable"}
```

Evidence kinds: `unverified`, `synthetic_fixture`, `executed_simulation`, `observed_real_system`, `nonempirical`. Outcomes: `positive`, `negative`, `inconclusive`, `not_applicable`. These are recorded classifications requiring inspection; a valid null/negative/inconclusive result is eligible for quality acceptance. Invented placeholder evidence has no accepted submission class.

### Independently inspect and score

Run `review-packet PROJECT STAGE_ID`. It returns current `binding`, `revision_id`, `epoch`, `inputs`, `outputs`, `rubric`, `rubric_hash`, and `required_checks`, without an intended verdict. Give scoped packets to fresh distinct verifier/critic agents using actual `fork_turns="none"` and configured settings.

`stage.review` requires `stage_instance_id`, `verifier`, `critic`. Both receipts have exactly these common fields:

```json
{"id":"unique-receipt-id","actor":"actual-reviewer-id","binding":"FROM_REVIEW_PACKET","revision_id":"FROM_REVIEW_PACKET","epoch":1,"context":"none","evidence":["precise inspected receipt/source/artifact locator"]}
```

The verifier additionally has `verdict` (`pass`, `revise`, `stop`, `inconclusive`) and `checks`, exactly one `{name,result}` per frozen required check; optional per-check `evidence` is allowed. Result is `pass`, `fail` or `unknown`. The critic additionally has `blockers` (list, possibly empty) and `scores`, one entry for every frozen criterion:

```json
{"criterion_id":"fidelity","score":90,"justification":"Specific evidence-grounded reason","evidence":["precise inspected evidence locator"],"gap":"Any remaining gap, or an empty string only at 90 or above"}
```

Scores are **true JSON integers** 0–100; strings, booleans, NaN, missing/duplicate criteria and changed rubrics fail. Mean comparison uses `sum >= 90 * count`, so 89.8 fails and exactly 90 passes. Original scores remain in each revision. Actors must differ from every producer in the lineage and from one another. Imported receipt IDs cannot be reused. The helper accepts one current-epoch scored review pair per revision; invalid attempted imports commit nothing. After a new ownership epoch, `stage.review` can import new genuinely performed, same-output fresh reviews without spending a producer reloop. The old pair is retained in that revision's `review_history`; this operational refresh is bounded to two per producer revision. Same-epoch replacement to shop for favorable scores is rejected. Other coordinator-owned operational retry records and bounds apply outside this helper.

`stage.gate` requires `stage_instance_id` and `decision:"advance"`, with no exception. This requires current hashes/dependencies, matching review bindings/epoch, verifier pass, every required check passing, no critic blocker, no unresolved blocking/major/critical issue, and the numeric threshold. A high average never waives those checks.

### Reserve bounded revisions

`stage.reserve` requires `stage_instance_id`, unique `task_id`, `producer`, and `plan`. Only a reviewed failing revision can reserve the next version. The counter changes before producer dispatch; a missing return does not refund it. The shared plan schema is:

```json
{"reason":"Diagnosed cause","issue_ids":["existing-issue-id"],"expected_changes":"Substantive correction","cheapest_check":"Bounded valid check","closure_criteria":"Measurable successful correction","budget":"Actual remaining allocation reference"}
```

`issue_ids` may be empty when the critic's score gaps themselves specify the correction. At most r0/r1/r2 are permitted in one lineage. Reopening a chat, changing a worker, or renaming a task does not reset it. Use versioned output paths and reserve before editing. The previous output is hash-checked when reserving; editing it first invalidates the return.

### Conditional advancement after actual reloop 2

`stage.gate` with `decision:"conditional_advance"` additionally requires `exception`. It only applies to a still-below-90 version after **three submitted and scored versions**, with all mandatory checks passing and no blocker. It records `conditionally_accepted`; it never changes the scores or closes findings.

`exception` requires: `actor`, `decision_owner` (`coordinator` or `delegated_executor`), `binding`, `epoch`, `revision_ids` (all r0/r1/r2 IDs in order), `reason`, `options_considered` (nonempty list), `accepted_limitations` (nonempty list), `scope_claim_changes`, `resource_implications`, `downstream_effects`, `next_action`, and `minor_disposition`. A coordinator actor equals the current lock owner and cannot be a producer. A delegated actor additionally supplies `delegation:{by,to,scope,evidence}` binding the current coordinator to the nonproducer executor.

`minor_disposition` requires `actor` (the current independent verifier, different from the decision-maker and producers), `context:"none"`, current `binding`/`epoch`, `issue_ids` (every unresolved issue in this stage), `severity:"minor"`, `blocking:false`, `downstream_satisfied:true`, `rationale`, and nonempty `evidence`. The independent reviewer must actually establish those facts. A flag alone is insufficient. An upstream ARS limit at count 0/1 cannot unlock this operation.

### Stop, invalidate, reconcile, reopen and replan

`stage.stop` and `stage.invalidate` require `stage_instance_id` and `reason`. Stopping invalidates descendants; invalidation traverses all descendants while preserving every revision, review and count. A changed current input/output/protocol file makes status report an effective invalidated state and blocks dependent advancement. Use an explicit invalidation transaction to record the observed change canonically; read-only status never writes state.

`project.stop` requires `reason` and prevents new stage reservations/submissions/gates. `project.resume` requires `reason` and `authorization:{source:"user_decision",actor,scope,evidence}` referring to an actual new user decision. It preserves the stop reason and resume history, creates no new resource allowance, and does not reactivate historical jobs/tasks. A stage operation cannot bypass project cancellation or resource exhaustion.

`stage.reconcile` requires `stage_instance_id`, the original `task_id`, exact `previous_epoch`, `disposition` (`not_started`, `stopped`, `completed_return_available`), and nonempty `evidence`. It rebinds a producing reservation to new ownership without changing its ID or counter. It must follow actual worker/controller/job reconciliation; unknown/live ownership is not an allowed disposition. It records assertions and does not contact the backend itself.

`stage.reopen` repairs an explicitly stopped/invalidated stage under the same frozen rubric/protocol. It requires `stage_instance_id`, renewed `inputs`, `task_id`, `producer`, the plan above, and `remedy:{actor,context,previous_binding,verdict,reason,evidence}`. The remedy actor must be an independent nonproducer distinct from the coordinator; `context` is `none`, `previous_binding` is the old stage binding, and `verdict` is `remedy_approved`. Current accepted dependencies are checked and rebound. Optional `dependencies` replaces dependency IDs with accepted compatible replacements after substantive upstream replanning; the same independent remedy must establish compatibility and fulfillment of the original obligations. Previous IDs/bindings are retained in `dependency_history`. If output already existed, reopening reserves the next counted revision and refuses a third. If an original reservation never returned output, its exact task/producer/count are retained and its remedy is recorded. No unseen dispatch or spending authority is created.

Renewed inputs must retain an actual file matching the frozen protocol hash; a reopen cannot drop or silently replace the protocol. A substantive protocol change uses `stage.replan`, whose new hash must bind an actual new protocol input file.

`stage.replan` is for a genuinely substantive authorized protocol/route change, never a cosmetic retry. It takes every `stage.create` field for the new unique instance, plus `source_stage_instance_id` and `amendment`. The new protocol hash must differ. `amendment` requires `actor` (current coordinator), `authority_scope`, `previous_binding`, `reason`, `material_change`, nonempty `evidence`, and `independent_review:{actor,context,verdict,evidence}`. The independent actor is neither coordinator nor old/new producer, context is `none`, and verdict is `substantive_replan`. This judgment requires actual inspection; different hash bytes alone do not prove material change. The operation invalidates the source and descendants and records `predecessor`, `root_lineage`, `successors`, and the amendment. Original failed history and counts remain intact. New phase obligations/claims must not inherit uncorrected defects merely because the new instance starts at r0.

## Issues and verified closure

`issue.open` requires `issue_id`, `stage_instance_id`, `severity` (`minor`,`major`,`critical`), boolean `blocking`, `owner`, `description`, nonempty `affected` descriptors, `reproduction`, and `expected_behavior`. Major/critical issues must be blocking. Opening a blocker against an accepted stage invalidates it and descendants. Issues start `open` and cannot be overwritten under the same ID.

`issue.fix` requires `issue_id` and `fix:{actor,description,outputs,evidence}`. The actor must be the assigned owner. Outputs must exactly match current submitted stage outputs and current hashes. This moves to `awaiting_verification`; it is not closure.

`issue.close` requires `issue_id` and `verification` with `actor`, `context:"none"`, `outputs`, `correction`, `regression`, `original_reproduction`, and `close_reason`. The actor differs from every producer/fixer/owner. Output descriptors must equal the current correction and stage output. `correction` and `regression` are `{result:"pass",evidence:[...]}`; original reproduction is `{result:"reproduced",evidence:[...]}`. All evidence lists and close reason are nonempty. Successful closure becomes `verified_resolved` with a truthful current timestamp.

When a submitted revision changes the corrected output descriptor set, a formerly resolved issue reopens automatically and its prior fix/verification/timestamp are retained in `closure_history`. The current version needs a new `issue.fix` and independent `issue.close` before a blocker clears. This deliberately binds a closure to the full inspected stage output set. `issue.reopen` with `issue_id` and `reason` also records a later-discovered failure of a previously closed correction; a reopened blocker invalidates accepted stage descendants.

This conservative closure path requires reproducible original evidence, correction and regression. When practical reproduction cannot establish full closure, retain the issue and residual uncertainty. There is no generic `closed:true`, severity downgrade, delete, or blocker-deferral bypass. Conditional acceptance retains eligible open minor issues.

## Recovery procedure

1. Read `status`; reconcile actual coordinator/process/controller/job ownership. Read-only inspection never repairs files.
2. Retain the existing matching owner lock when it is still yours. If no owner lock exists and record recovery is needed, use `lock-acquire --for-recovery`. This allocates recovery-only ownership; it cannot dispatch/submit until recovery succeeds.
3. Use `recover` with the current valid-prefix sequence. A missing/stale/malformed snapshot is rebuilt from the journal; existing malformed snapshots are preserved in `.research/recovery/*.snapshot-original.bin` with recorded hashes.
4. For a malformed **final** event line only, explicitly add `--quarantine-tail`. The entire original journal is preserved as `.research/recovery/*.events-original.bin`, with its SHA-256 and valid-prefix byte count in a new recovery event. No bytes are guessed into a successful event. Interior corruption, hash-chain failure, unsupported schema or absent initialization are not auto-repaired.
5. Revalidate and reconcile existing reservations. Historical records never reactivate agents, jobs, controllers, automations or author decisions.

An expired heartbeat alone is insufficient for takeover. The helper deliberately supplies no force-unlock or cross-host fencing. A crash while holding `transaction.lock` needs process reconciliation and explicit operator handling of that marker. Journal recovery does not prove an external job stopped or completion delivery succeeded. Use the delivery helper and actual backend/plugin receipts for their separate scope.

## Verification suite

From the implementation workspace, run:

```powershell
python -m unittest discover -s work/research-orchestrator-tests -v
```

The isolated tests use temporary projects and explicitly synthetic artifacts. They exercise numerical boundaries, malformed scores, stale hashes, placeholder/empty outputs, independent issue closure, persistent reservations, cap exhaustion, conditional exceptions, upstream early stop, recursive invalidation, bounded reopen/substantive replan, ownership contention, epoch reconciliation, snapshots, torn logs, unsupported schemas and CLI behavior. These tests establish record-helper behavior; they do not establish scientific results, real fresh-agent settings, paid compute execution, or live Drive backup.
