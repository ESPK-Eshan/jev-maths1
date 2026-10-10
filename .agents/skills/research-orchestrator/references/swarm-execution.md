# Adaptive native swarm execution

Read when independent work benefits from delegation. Follow [agent contracts](agent-contracts.md), [state recovery](state-recovery.md) and [compute execution](compute-execution.md).

## Allocate useful work

The standing swarm instruction permits useful native delegation within the project contract. Start with the smallest useful allocation; expand for distinct coverage or critical-path gains measured against coordination/review cost. The ceiling of 100 is worker assignments per declared swarm, including descendants and reviews, not 100 concurrent agents or a target. Only the coordinator allocates task IDs and slots. Record any later swarm and its remaining budget; no hidden unbounded child fan-out.

Active workers are bounded by the minimum of profile ceiling, currently free native slots, workload capacity and reserved project resources. On the inspected four-slot runtime this allows at most three workers beside the coordinator. Discover changes and amend the profile before raising limits. Reserve room/budget for fresh stage reviews. A queued assignment, a reused session and a newly spawned agent are different counts.

Good partitions include literature facets/source-family extraction, novelty counter-search, rival critiques, isolated baseline implementations, prespecified evaluation shards, plots from frozen aggregates, and blind review perspectives. Keep dependent scientific choices and trials serial. Do not manufacture consensus by repeating the same query or counting preprint/published versions as independent studies. Connector quotas apply to the whole request, across all workers.

## Manifest before dispatch

Persist objective and decomposition rationale; task dependency DAG; IDs and owner epoch; role/profile/settings; input hashes; output ownership; priority; reserved time/resources; review assignment; deadline/retry count; lease/heartbeat when exposed; native agent ID when returned; and expected merge decision. Task states are:

`queued → dispatched → running → returned → verifying → accepted`

Other outcomes are `revise`, `failed`, `cancelled`, and `unavailable`. These are execution states, not scientific outcome/quality. Preserve the actual state and partial artifacts when an assignment stalls.

Before each dispatch reserve against measured usage plus all outstanding and unknown-outcome liabilities. Confirmation, independent review, final builds, log storage and delivery have protected allocations. Queue, job, review and merge deadlines plus nested operational retry budgets survive resume. A timeout neither accepts a result nor refunds its allocation.

## Concurrent writes and campaigns

Concurrent writers need distinct directories/worktrees and immutable shared inputs; prompt restrictions alone do not isolate them. Only the active experiment writer changes its controller-approved scope. Scouts and reviewers use permissible immutable snapshots. Confirmation inputs/results/log indexes remain sealed until the frozen evaluation closes.

Foreground codex-autoresearch campaigns owned by this coordinator serialize within its actual native Goal namespace, even for separate repositories. Each requires its matching Goal; a conflicting unfinished Goal cannot be bypassed by starting extra chats. The tools establish a current-thread Goal constraint, not a claimed account-wide constraint. Windows background controllers remain unavailable under the inspected compatibility restriction. Ordinary authorized static/pilot jobs may run concurrently when their isolated resource/protocol contracts permit it.

Ray/SkyPilot jobs remain subordinate infrastructure, not extra scientific controllers or a workaround for native agent capacity. Model/data/task parallelism obeys the approved measurement denominator and resource limits.

## Merge and recover

Workers return bounded OKF packets with raw evidence/command receipts and hashes. Reconcile overlap, contradictory evidence, duplicate source families, missing tasks and dissent before accepting the integrated output. Fresh independent stage verifier/critic inspect that integrated artifact; per-worker checks and majority votes do not replace the gate.

Use supported completion events or bounded waits, with meaningful progress updates at least every 60 seconds during active work. Resume reconciles task ID, input hash, owner epoch, actual worker/process state and returned artifacts before any retry. Stale returns are quarantined. Followup cannot change a worker's model or erase its memory. Wait for capacity only when a real lifecycle event can release it; otherwise record the unavailable dispatch.

On cancellation or a project limit, stop new scientific/paid dispatch, attempt supported interruption and verify owned external-process status. Continue only authorized bounded preservation/reconciliation/shutdown. An interrupted agent may leave a process or paid remote job running. An unmet native Goal cannot override the durable project stop state.
