# Canonical state, ownership and recovery

Read at initialization, compaction, resume, status, invalidation and backup restore. Use the implemented [record CLI](record-cli.md) for helper commands and supported schemas; it validates records and hashes, not scientific truth, OS isolation or provider execution.

## State ownership and records

The coordinator owns `.research/` outside every active experiment's mutable scope. Workers write assigned report directories. The experiment index references codex-autoresearch's authoritative history; never edit or replace that history with a second registry. If actual paths differ, bind the resolved locations in the contract.

| Record | Authority/content |
| --- | --- |
| `contract.json`, `protocol.json` | Scope, exact input/fixed constraints, effective profile, decisions, budgets, route, evidence boundaries and amendments. |
| `state.json`, `events.jsonl` | Current projection and append-only coordinator transitions. |
| `sources.jsonl`, `experiments.jsonl`, `claims.csv`, `artifacts.json` | Source access/proposition checks; engine/raw receipts; claim bindings; artifact inputs/scripts/hashes. |
| `issues.jsonl`, `verification/`, `criticism/` | Findings, independent checks and version-bound closure, criterion vectors and all reloops. |
| `agents/`, `compute/`, `recovery/`, `reproduction/` | Assignments/returns, requirements/jobs/leases, all recovery candidates, bounded clean replay evidence. |
| `logs/`, `delivery/`, `originality/`, `framework-jobs/` | Full available logs, backup transactions, manuscript report review and isolated optional jobs. |

Common records bind schema/version, ID/time, parent and input IDs/hashes, producer/settings, command/tool receipt, environment, output paths/hashes, evidence kind, validation, uncertainty, resources and amendments. Stage executions additionally bind `stage_instance_id`, numbered stage, phase, campaign/candidate and protocol version. Pilot/development receipts cannot satisfy confirmation dependencies.

Keep route applicability, task execution, scientific outcome/evidence kind, gate, author/readiness, ownership and delivery as separate state axes. Distinguish `placeholder_or_invented`, `synthetic_fixture`, `executed_simulation`, and `observed_real_system`. A valid negative result may pass a stage; a successful upload or zero process exit cannot establish scientific acceptance. OKF is the navigable projection, not another source of mutable facts.

## Exclusive transitions

Acquire the project lock atomically on a filesystem with supported semantics before canonical mutation or dispatch. Each operation checks owner/run, ownership epoch and expected committed event sequence under the lock. Persist intended side-effect/task/revision IDs and reservations before dispatch. Apply state through checked event commit/replay and atomic replacement. Reject/quarantine stale epoch, wrong input, duplicate and late returns. Never manufacture an event from a partial JSONL tail; preserve it and recover only from the last verified committed boundary using explicit supported repair.

The helper's cooperative lock coordinates compliant local writers; it is not remote fencing or a security boundary. Timestamp/heartbeat expiry cannot prove an old process/controller/job stopped. Before takeover establish old ownership cessation or backend fencing, reconcile repository/controller locks and jobs, then acquire an exclusive new epoch. If a previous controller can still dispatch and cannot be fenced, mutating takeover is unavailable; read-only status can name the last valid snapshot.

The project lock does not replace controller repository locking or the coordinator's current-thread Goal boundary. Reserve revision IDs/resources under the same exclusive transition before dispatch. Outstanding/unknown job and charge liabilities remain reserved until reconciled; two resumes cannot spend the same allocation.

## Gates, invalidation and schemas

Ready work needs current applicable dependencies, authority, ownership, input hashes and allocation. Reviewing requires inspectable outputs tied to the reserved task/revision. Normal acceptance needs current independent verifier/critic, the frozen rubric mean at least 90 and all applicable integrity/no-blocker checks. See [verification](verification.md) and [journal criticism](journal-stage-critique.md) for actual substantive gate contracts and two-reloop rules.

Changed source, protocol, model/data identity, relevant loaded skill/script/reference contract or output invalidates affected receipts and descendants. Keep old receipts, their failed outcomes and counters; traverse dependencies with cycle detection. Resume starts at the earliest required invalidated/incomplete stage, not the furthest conversational claim. Meaningful amendments may reopen dependencies; renaming a stage/file or replacing a worker never resets its lineage.

Unsupported record/profile schemas stop mutation, preserve bytes and report the migration prerequisite. Explicit migration must retain IDs, exact user decisions, failed history, reloop counters and input/output bindings, and emit before/after hashes with new-schema validation. Do not auto-reset on a version mismatch. Status may truthfully inspect supported known fields without inventing missing state.

## ARS passport and user decisions

When an ARS passport exists, the calling coordinator owns its path/hash and the adjacent run ledger. Resolve `ARS_ROOT` via [integrations](integrations.md), read `ars/academic-pipeline/agents/pipeline_orchestrator_agent.md`, then use its exact helper contract:

```text
python <ARS_ROOT>/ars/scripts/run_ledger.py append --passport-path <passport> --entry-file <run-local-entry.json>
python <ARS_ROOT>/ars/scripts/run_ledger.py report --passport-path <passport> --claims <run-local-claims.json>
python <ARS_ROOT>/ars/scripts/run_ledger.py show --passport-path <passport>
```

Create entry JSON with a file-writing tool in run-local storage outside the plugin/repository; never interpolate user text into shell code. Record initial instructions, opened/closed checkpoint questions and exact user words including partial answers, required stdout/exit-only step receipts with actual `input_paths`, counters/retries and needed transient file paths. Let the installed script hash files; refused append stays refused. Never manually edit or directly read the ledger; use `show`/`report`.

After every subagent return, compaction/resume and stage close, run `report --claims`; at close enumerate required stdout/exit-only steps as `expected_steps`. Reuse `step_outcomes` only for unchanged input files. A summary/paraphrase alone does not supply exact authority or a passed step. If retries cannot be established, follow the installed missing-receipt rule rather than restart an unknown allowance. Display report output verbatim with `--render en` or `--render zh-TW` when applicable. Reuse backed choices; ask only for essential unsupported decisions. Keep the whole ledger local, outside worker/cross-model payloads; pass only the needed decision. The default-off inquiry ledger and hooks are separate opt-ins.

## Resume and continued execution

Read current contract/profile, route, accepted receipts, open issues, capability manifest, engine/Git state, exact framework directory and process/job ownership. Validate current hashes/contracts and reconcile existing side effects before launching. Active foreground orchestration proceeds through eligible stages until contracted completion or an essential boundary; a plan, worker return, trained model or draft alone does not finish a full project.

A skill is not a daemon. A durable remote job can survive without automatic analysis. Before returning for a dependency persist project path, protocol/profile/stage hashes, candidate/engine and job IDs, remaining allocations/exposure, relevant OKF roots, next event/action and a natural-language resume instruction. Only an explicitly requested, actually created supported heartbeat/automation supplies a wakeup: retain its real ID/schedule/scope/budgets, obey the same lock/stop state, stay quiet on unchanged state, and reconcile the same job once. Otherwise continuation requires an active session or manual resume.

Cancellation/budget stop prevents new scientific or paid dispatch, including automatic native Goal continuations. Only authorized bounded preservation/reconciliation/shutdown remains. Do not change an unmet Goal into completion, create replacement Goals or bypass an essential native control; follow [experiment campaigns](experiment-campaigns.md).

## Restore base plus operational closure

Follow [archive and Drive delivery](archive-drive-delivery.md). A complete delivered state is the frozen base, ordered hash-bound supplements and the disclosed terminal local acknowledgment. Validate all identities, predecessor/sequence bindings, hashes and cutoffs before isolated extraction and record-only replay. The older base can legitimately precede stage-22 reviews and acceptance; reconcile supplements before declaring scientific work unfinished.

Never replay historical tool calls, queued jobs, user decisions or automation settings as actions. Missing/truncated/unverified segments or terminal acknowledgment leave completion unknown/pending. Use bounded read-only destination/job reconciliation; do not create another run/folder/upload or guessed historical acceptance. `acceptance-ready` is still reviewing. A later successful restoration check may append its own truthful timestamped verification/acceptance only after all conditions are independently established. Active resume then separately checks current authority/resources and obtains a new ownership epoch; historical locks are not ownership.
