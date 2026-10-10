# Compute planning, placement and execution

Read at resource feasibility, immediately after experiment design, and before any remote/pilot/development/confirmation job. The native `compute_scheduler` uses the saved role settings. It owns the authorized queue/leases and lifecycle; the coordinator owns science/gates, codex-autoresearch owns trial choice/commit/rollback, and the fresh confirmation executor owns frozen evaluation. One assignment mutates a given compute queue; read-only profiling may be delegated.

## Deliver requirements before full implementation

Keep separate immutable stage-11 instances: `initial-feasibility` supplies stage 9; `protocol-bound-recommendation` consumes completed stage 9 and precedes full stage 10. Each gets its own hashes/reviews. Refinement never overwrites initial feasibility, creates a dependency cycle or resets stage-9 reloops. Later pilot measurements and substantive protocol/recovery changes produce linked requirement versions and affected invalidation.

Immediately after planning, provide a readable recommendation plus `.research/compute/requirements.json`, including in plan-only mode. Label a provisional review-pending report honestly and deliver it promptly; full implementation/intensive dispatch still requires accepted prerequisites. Use analytic footprints, verified relevant workloads and affordable existing smoke measurements, with unsupported quantities `unknown`.

For preparation, pilot, development, confirmation, analysis and archive, specify:

- Minimum and recommended CPU cores, RAM/shared memory, temporary/persistent disk, GPU count and usable VRAM or explicit CPU-only execution; precision, batch, sequence/image size, model/data size and dependencies.
- Transfer/checkpoint retention, job concurrency, elapsed-time and CPU/GPU-hour ranges; basis, uncertainty and capacity fit. Include setup/failures and protected confirmation/review/closeout costs.
- Selected actual host/placement and source ownership; dated verified provider rate/currency where checked, otherwise monetary cost pending; why added hardware is worth its overhead.

Quantization, PEFT or a smaller model is an option only if it preserves the question or receives a protocol amendment. OOM/undersized hardware cannot silently change the scientific method.

## Host and authority preflight

Record existing host/provider/account/region, authorized access reference, actual OS/shell, GPU model/count/usable VRAM, CPU/RAM/shared memory, disk, software/runtime, data/model rights and upload boundary, rates/billing granularity, money/time/GPU-hour limits, spot tolerance, max machines/jobs, durable checkpoint/export destination, idle/drain/retention policy and whether provisioning/resizing is authorized. Check current provider prices/quotas/lifecycle semantics before use. An estimated budget without enforcement is not a hard billing cap.

Prefer a suitable already-authorized remote project host for implementation/execution, retaining its environment, working directory and ownership. Otherwise inspect actual local/existing-cloud resources and use them if they fit. An LLM account is not a GPU host. Rent only needed phases; CPU-heavy work can require CPU rental. If insufficient, set task `needs-input` with readiness reason `user-rental-needed` and give a portable rental brief: hardware/VRAM/CPU/RAM/disk, OS/runtime, time/resource hours, region/data constraints, access, persistence/recovery, affordable rate if known and exact next prerequisite. The user's intention to rent does not purchase/provision authority. Continue affordable eligible preparation, then validate provided access and proceed without repeated permission.

Record one authoritative writable Git source and a source-to-execution map. A local codex-autoresearch controller needs a real accessible local filesystem `--repo`, never an SSH/remote-only path. Its exclusive writer owns source/commits/rollback; the adapter exports immutable candidate snapshots to a nonauthoritative remote execution copy. A remote authoritative controller needs its own validated remote runtime; a Linux rental does not fix an unsafe local Windows controller.

## Choose the smallest useful backend

Use Orchestra SkyPilot and Ray Train when the workload/provider fit and gains justify setup, data movement and operations. Load their actual installed skills before selection. SkyPilot is infrastructure/job/lifecycle orchestration; Ray Train is suitable training execution; Ray Data/Core is useful preprocessing/task execution. They can be used independently or together. Keep a simpler supported existing-host plan when it meets the need. Do not force distributed training onto a small single-GPU pilot, Ray Train onto inference-only work, or add Ray Tune as a competing optimizer.

Before paid GPU time prepare the frozen protocol, executable baseline, dependency/container definition, small correctness tests, pinned permitted model/data inputs, footprints and job manifest. Build eligible CPU transforms/tokenization/index inputs on local or cheaper authorized CPU resources. In a DAG, overlap CPU preparation for the next eligible job and CPU analysis for completed immutable results with GPU execution. Never cross unmet scientific gates or train/evaluation/confirmation access boundaries for utilization.

## Admission and resource tuning

Each job declares ID/dependencies, candidate/protocol/environment/input hashes, owner/output path, GPU IDs/count and peak VRAM plus headroom, CPU/threads, RAM/shared memory, disk/I/O, priority, timeout, preemptibility and lease. Atomically reserve measured usage plus outstanding and unknown-charge liabilities before dispatch, preserving confirmation/review/final-build/log/archive/transfer allocations. Nested retries share a bounded allowance; timeout does not release the reservation before reconciliation.

Reserve CPU/RAM/I/O for GPU feeding and avoid starving larger ready jobs. Dedicated GPU allocation is the default. Fractional scheduling does not enforce VRAM limits: share only after representative measured throughput, memory and measurement validity checks. Latency/time/memory/energy comparisons use the frozen isolated or controlled-contention conditions, warmup, synchronization, repeated measurements and matched accounting; incompatible co-location is blocked.

Measure load, warmup/compilation, CPU prep, data wait, transfers, compute, checkpointing and analysis before tuning. Bound aggregate DataLoader workers/threads/prefetch/shared memory. Pinned-memory/async transfer gains require correct dependencies and lifetimes; nonblocking flags do not prove overlap. Validate numerical behavior, weighting/order, seeds/restart and protocol fit before adopting batching, packing, precision, kernels, compile or model-worker reuse. Separate mutable state/adapters/logs/confirmation. Keep a tuning change only when measured useful end-to-end throughput/cost gain repays its remaining overhead and guards still pass; protocol-changing tuning needs amendment.

Capture available GPU utilization/peak VRAM, CPU/RAM, disk/network, queue/data wait, useful units per time, failures/completions, rental duration and costs with declared sampling. Missing telemetry stays unknown. Prefer light provider/NVML metrics; coordinate DCGM/profiler ownership to avoid perturbing benchmarks. High activity is not efficiency. Cost per valid experiment includes setup, failures, storage/transfer/export; reserved GPU-hours sum devices over reserved time. No useful eligible work can trigger authorized idle shutdown.

## Frozen remote evaluation adapter

Remote autoresearch is unavailable until the selected project-local adapter is implemented and validated. Record exact path/invocation, backend/client, credential-reference boundary, immutable version/hash, metric/receipt format, candidate binding, reuse rule, timeout/cancellation/reconciliation and raw-log durability in the protocol, outside mutable scope. Do not scaffold every provider or claim the record helper executes jobs.

The installed `finish` commits the candidate and synchronously invokes frozen `verify`. That command calls the adapter: snapshot/bind the committed candidate; submit or reconcile one uniquely identified job; verify complete raw outputs and receipt hashes; return the defined finite numeric last stdout line or explicit metric-key JSON expected by the controller. Success exits zero even for a poor measured result. Guards and Git-visible cleanliness remain intact.

Reuse requires a matching accepted receipt for candidate/data/environment/protocol/adapter hashes. The scheduler must not pre-run evaluation then let `finish` bill it again. On disconnect, timeout or rollback persist job/candidate identity, attempt supported cancellation, retain unknown running/charge ownership, reject late results for later trials and prevent replacement overlap until reconciled. Adapter validation uses a cheap permitted fixture to exercise duplicate dispatch, interrupted/unknown outcome, stale result, malformed metric, timeout and log preservation before paid use.

## Durable jobs and shutdown

Persist job/provider-instance IDs, remote path, leases/process owner, hashes, status/exit, raw outputs, checkpoints, telemetry/cost and side-effect IDs before/reconciled after calls. Lost SSH or native interruption does not prove job failure. Query the existing durable job before retry. Checkpoints preserve the supported model/optimizer/scheduler/RNG/sampler state; label restart fidelity and reject partial/duplicate/missing shards.

At completion, a long dependency wait or a limit: stop admission, checkpoint/drain owned work within the fixed allowance, incrementally/finally synchronize and seal logs, export required evidence, verify durable hashes, perform authorized stop/termination, then verify provider state and continuing storage/IP charges. SkyPilot autostop/autodown follows actual job/SSH-idle semantics, not GPU utilization; protect transfers/checkpoints as work. Provider-side handling must honor the bounded preservation-versus-termination policy when Codex disconnects.

Export failures retain evidence under authorized durable storage and explicit pending status; neither indefinite rental nor destruction of the sole copy is an implied fallback. A verified local archive and required durable copy can allow GPU shutdown before local Drive upload. Return resource plan/DAG, capability preflight, measured tuning/cost limits, job/export receipts and final ownership/charge state for independent stage inspection. See [logs](logs-analysis.md) and [archive delivery](archive-drive-delivery.md).
