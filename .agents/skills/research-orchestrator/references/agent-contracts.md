# Native roles and dispatch contracts

Read for profile setup, any worker launch, and review independence. See [swarm execution](swarm-execution.md) for scheduling and [integrations](integrations.md) for selected skill entrypoints.

## Resolve the effective profile

Global user profiles belong outside the installed skill at `C:/Users/eshan/.codex/research-tools/research-orchestrator/profiles/`. Merge explicit project overrides into an immutable effective-profile snapshot and hash in the project contract. The shipped asset is a template, not a completed user choice. Null/unset role settings block that role's launch unless the user explicitly authorized inheritance. Independent planning can continue. Record amendments before changing settings; never silently substitute a model or effort.

Validate combinations against the current native runtime. The coordinator is the actual parent chat model; a profile cannot change it. For a designated worker, pass supported `model` and `reasoning_effort` spawn arguments. Full-history forks cannot carry overrides in the inspected runtime. Fresh/blinded roles use `fork_turns="none"`, a separate new agent ID, and a scoped packet; merely saying “forget history” does not erase it. Record requested settings, launch arguments, and observed settings if exposed; otherwise observed settings remain `unknown`. A request is not provider attestation.

## Responsibilities and outputs

| Role key | Scoped output and boundary |
| --- | --- |
| `literature_scout` | Dated queries, source identity/version/access, primary passages and nearest work. |
| `novelty_skeptic` | Counter-search, overlap, rivals and evidence that defeats or narrows the gap. |
| `research_designer` | Hypotheses, predictions/falsifiers, route, baseline and frozen protocol. |
| `implementation_engineer` | Executable baseline/method, correctness checks, environment and commands in assigned write scope. |
| `experiment_optimizer` | One coherent development trial through the exclusive codex-autoresearch controller. |
| `confirmation_executor` | Frozen confirmation execution in a fresh context, without tuning or leaking holdout analysis to the optimizer. |
| `compute_scheduler` | Requirements, placement, queue/leases, backend receipts, telemetry, reconciliation and authorized drain/shutdown. |
| `analysis_agent` | Traceable aggregates, uncertainty, robustness and bounded interpretation. |
| `artifact_author` | Deterministic tables/figures, editable sources, rendered previews and archive inventory. |
| `manuscript_author` | Evidence-bound draft, claim map and selected paper/thesis format. |
| `stage_verifier` | Independent inspection of real execution/evidence; separate verdict with blockers and relevant checks. Does not repair the producer's work. |
| `journal_stage_critic` | Independent journal-oriented criticism, frozen criterion vector, source-linked faults and remedies. |
| `scientific_reviewer` | Fresh contribution/design/inference review under the selected ARS review contract. |
| `citation_auditor` | Bibliographic identity, proposition support, exact source locators and unresolved citations. |
| `documentation_steward` | OKF proposals and compact handoffs bound to canonical evidence. |

Roles are responsibilities, not permanently resident agents. The coordinator alone merges accepted reports, owns canonical transitions and closes issues with independently checked evidence. One designated writer owns an active experiment scope; only one compute assignment may mutate a given infrastructure queue. Other assignments may inspect immutable, permitted snapshots.

## Required task packet and return

Before launch persist run/swarm/task/stage-instance IDs, phase and protocol version, ownership epoch, bounded question, effective profile hash, requested settings, actually loaded skill paths/hashes, input concept/evidence hashes, allowed writes, forbidden edits, resource reservation and deadline, required output schema, acceptance criteria, verifier assignment, retry bounds and escalation condition. Do not supply another reviewer's verdict or desired conclusion. Use [knowledge handoffs](knowledge-bundle.md) for selective loading.

The return binds the same IDs/epoch/inputs to output paths and hashes, commands/tool receipts, coverage and failures, limitations/contrary evidence, actual resource use and next dependency. Reject stale or duplicate returns before integration. A completed native task is not an accepted scientific stage.

## Establish repeatable fresh capacity

At project preflight, inspect actual capacity and run a bounded nonpaid lifecycle fixture using the configured settings: create a scoped fresh worker, receive its artifact, finish it, then create additional fresh producer/verifier/critic contexts as needed to establish repeatability. Record observed agent IDs, concurrency, launch acceptance, reuse restrictions and coverage. The historical two successive fresh-worker probe established only that completed workers permitted further creation in that observed state.

The inspected runtime permits four simultaneous agents including the coordinator, hence at most three workers. No reset/release API was exposed; interrupt/followup is not context erasure or proof of slot release. If a necessary fresh context cannot be created, mark the dispatch `unavailable` before empirical work and preserve a review-ready plan. Do not claim full execution or replace required reviewers with contaminated sessions. Reusing a worker is eligible only for compatible nonblind tasks with unchanged model/effort and permitted prior evidence access.

Separate fresh verifier and critic receipts are required for every executed stage instance; applicable specialist/ARS reviews remain additional. Freshness reduces anchoring, not correlated model error; it is neither independent replication nor an enforced security sandbox. Read-only/write scopes and sealed confirmation require actual filesystem/backend controls when isolation is claimed. Record what the runtime really enforces.
