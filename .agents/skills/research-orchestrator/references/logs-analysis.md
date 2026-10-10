# Available log retention and analysis

Read before executing processes/campaigns, at stage close/resume, and before export. Retain all available successful, failed, timed-out, cancelled, discarded, rolled-back and superseded project evidence. Summaries/indexes support navigation; they never replace original logs.

## Capture and bind

Capture process stdout/stderr from launch into full project log files outside editable method scope and rollback paths, separately from truncated tool responses. Bind project/run/stage-instance/task/trial/revision IDs, command or structured arguments with secrets removed, working directory, environment/package/config/code hashes, seeds, actual timestamps/timezone/duration/exit, remote IDs and output hashes. Unknown fields stay unknown; do not reconstruct invocation time or commands by guessing.

Retain exposed tool requests/returns, search/source-version locators, assignment/settings/visible returns, verifier and criterion-vector/critic reports, fixes and all reloops, issue closure, strategy decisions, metrics/guards, build/render/citation receipts, telemetry/cost/checkpoints, transfer/ZIP/Drive records. Distinguish requested versus observed model settings. No claim extends to hidden reasoning, inaccessible provider internals or a complete native transcript without a real export surface.

Use append-only events and versioned stream segments rather than overwritten `latest.log`. The research profile's `logs/index.jsonl` contains log ID, producer, stage/task/trial bindings, relative path, type, access class, audience, capture interval, sealed hash, bytes, capture status and related receipt links. This is the project's log profile, not a universal upstream schema. Open streams have no final hash; flush before sealing. Record ordering/offsets when available, explicitly empty streams, truncation, dropped telemetry and inaccessible/partial capture.

## Live durability and controller behavior

The inspected codex-autoresearch verify path buffers output with `communicate()` and writes its controller log afterward. That is not live durable capture. Before a campaign, configure/validate a frozen logging wrapper or selected remote adapter outside mutable scope when durability is needed; bind its hash in the protocol. It captures/synchronizes stdout/stderr without changing metric stdout protocol, guards, exit status, Git cleanliness or controller ownership. Do not add/change it mid-trial. If unavailable, retain eventual controller logs and explicitly report the live/durable gap before deciding paid preemption risk is acceptable.

For remote work incrementally synchronize logs/checkpoints using actual supported acknowledgments; record unsynchronized intervals and loss exposure. Before shutdown/archive flush and seal, reconcile remote/local hashes and inventory logs. Budget storage and transfer. At capacity exhaustion stop new admission or expand within existing authority; never silently prune failed trials or keep billable instances indefinitely. Compression/deduplication requires verified restoration and complete indexed identity.

Each executor owns assigned capture; documentation steward maintains coverage/index; coordinator reconciles at stage close/resume. Independent verifier checks substantive/valid-empty streams, IDs/hashes and failure retention. Invalid measurements remain searchable and are excluded by documented rules, not deletion. Analysis indexes group dispositions/failure types, duration, observed cost/utilization, reloops and strategies, linking originals without inventing causal explanations.

## Scoped access and sensitive records

Classes are `development`, `confirmation-sealed`, and `restricted`, with permitted audience. Apply access to full streams, indexes, summaries, failure analyses, OKF and backups. Optimizer views expose only allowed coverage while holdout identity/metrics/error analysis remain sealed. Retention does not grant every agent access; record actual enforced isolation and any unavailable boundary.

Use credential references, redact tokens/passwords/signed URLs/unnecessary personal data at capture when possible, preserving scientific context. If a sensitive original already exists, preserve it only in an authorized restricted location and export an audited sanitized copy. Redaction manifest records affected fields/disposition/coverage, never secret values. Inspect history/bundles/notebooks/nested logs before ordinary Drive export. Licensing or confidentiality restrictions do not authorize deleting unfavorable outcomes; report restricted or missing coverage.

## Cutoff and delivery closure

Follow [archive delivery](archive-drive-delivery.md) exactly: frozen base with declared cutoff; ordered hash-bound sealed operational supplements into the same delivery folder; terminal local acknowledgment after the last supplement verifies. Supplements include stage-22 reviews, still-reviewing acceptance-ready/limitation, ledger and OKF/lifecycle changes. They do not claim their own future upload. Final acceptance lives only in the disclosed terminal receipt after closing verification. Restore needs the whole declared chain; absent closure is unknown/pending, never a guessed historical success.
