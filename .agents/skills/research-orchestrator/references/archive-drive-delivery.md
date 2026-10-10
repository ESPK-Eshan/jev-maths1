# Complete archive and Google Drive delivery

Read at remote-project closeout or restore. The user's standing instruction authorizes a private ZIP completion backup via the connected Google Drive plugin. Record/reuse that authority and any per-project restrictions; it does not authorize public sharing or submission. Plan-only/incomplete work does not create a premature folder. An accepted negative/inconclusive project can reach this same closeout. Use [delivery CLI](delivery-cli.md) for the implemented offline inventory/chain validator and supported schemas; it neither authenticates remote receipts nor executes/restores jobs.

## Own one delivery transaction

The coordinator owns identity `project_id/run_id/delivery_version`; compute owns snapshot/transfer/lifecycle, artifact author packages, documentation steward updates mappings and a fresh verifier checks delivery. First attempt creates one new folder; retries reconcile/reuse that actual folder ID. A later completed run/material archive revision gets a new identity. Use a supplied verified parent, otherwise the current Drive account root absent a conflicting rule. Name the folder with slug, completion date and run ID; retain returned ID immediately.

Keep delivery states distinct: `research_complete`, `archive_ready`, `local_transfer_verified`, `drive_upload_pending`, `drive_content_verified`, `completion_delivered`. Science alone cannot complete a pending backup. Stage 21 prepares inventory/retention; stage 22 finishes all deliverables/builds/render checks and documentation before freeze.

## Freeze and prove the inventory

Quiesce all writers or take an actually consistent snapshot. Inventory every project-owned file in declared roots, including code/config/notebooks, present data/weights/checkpoints, raw/processed/failed results, logs, pending and accepted receipts, `.research`, role/protocol snapshots, environments, Git history/uncommitted work, manuscript/bibliography, editable and rendered figures/tables, requested thesis and OKF. A useful Git bundle supplements working files; it does not replace uncommitted content. Never traverse unrelated home/account paths or external symlink targets.

For every included/excluded path record relative path, bytes, SHA-256, role, disposition and reason; exclusions also record authorized retention/retrieval and restoration impact. Preserve executable permission/link semantics and destination path mapping. Include total inventory/archive sizes, snapshot/contract identities, cutoff and reconstruction instructions. Large files/caches cannot disappear silently. Restricted inputs or sanitized history make completeness limited, not “all files”.

Inspect current files, logs, notebook output, config, nested archives and Git history/bundles for secret-bearing content. Export audited sanitized copies or explicitly excluded restricted originals with retained evidence under authorized policy; never rewrite research history merely for backup or upload known secrets. Record unresolved inspection limits. Preserve scientific failures regardless of favorable-result status.

Create standard ZIP/ZIP64 outside the source snapshot to avoid self-inclusion. Verify archive entries against inventory and safely extracted full-content hashes; ZIP integrity testing alone is insufficient. Put archive checksums in a separate delivery manifest. If limits require partitions, use independently valid numbered ZIPs and a complete reconstruction map, not arbitrary byte splits. A changed source after freeze invalidates its archive/readiness; append-only operational sidecars do not permit silent scientific edits.

## Transfer and plugin capability

Read the current `google-drive:google-drive` base skill and inspect live tool schemas. Default to authenticated download from exact remote path into an explicit local project-backup directory; verify remote/local bytes and hashes. Use a materializable runtime file reference only when supported. Record transfer receipts and absolute source/destination paths. A remote-only path, SSH URL or base64 is not an accepted local upload automatically.

The inspected tools are `google_drive_create_folder`, `google_drive_upload_file`, `google_drive_get_file_metadata`, folder listing and raw `fetch`; tool discovery is not a tested upload credential. Validate the actual accepted `file_uri` representation using a small real project manifest before bulk ZIP transfer. Resolve current staging/Drive quota and connector size limits where available, and respect drain time/cost. Report missing materialization or size support honestly; do not silently switch to direct API/rclone.

Create folder with `name` and optional `parent_folder`; upload with actual returned `parent_folder_id`, accepted `file_uri`, file name and `application/zip`. Keep binary ZIPs unconverted. Read metadata with `fileId`/supported `fields`: compare ID/name/MIME/parent/size/checksum and cross-check folder listing. Preserve inherited sharing and return only links observed in completed connector results/readback.

Content verification prefers server SHA-256 against the local archive. If only MD5 is returned, compare independently computed local MD5 and state the method. Otherwise use supported raw `fetch` (`download_raw_file: true`, `include_base64: false` where exposed), materialize its authenticated top-level reference and compare full hashes. Metadata/name/size alone cannot satisfy `drive_content_verified`. Stored ZIPs do not inherit native Docs' export-size rule. Do not assume resumable upload controls or idempotency keys absent from the live plugin.

Unknown-outcome create/upload must reconcile saved IDs and destination contents before retry. Matching names alone are insufficient. If intended identity/content cannot be established, stop that transaction unresolved instead of making another speculative folder/file. Save actual IDs/hashes in append-only receipts. Failures preserve local verified archive and authorized durable remote evidence under bounded policy; report exact access/quota/representation prerequisite and pending delivery.

## Close without recursive self-inclusion

1. Freeze and verify the scientific/base snapshot with explicit event/log cutoff. It may still show stage 22 reviewing.
2. Create, transfer, upload and verify the base archive. Append all construction/delivery/lifecycle records outside it.
3. Obtain stage-22 verifier/critic receipts over the scientific package and inspected delivery evidence. Record coordinator `acceptance-ready` or limitation under the still-reviewing stage. Neither means final acceptance.
4. Seal ordered operational supplements containing post-cutoff records, stage-22 reviews, acceptance-ready/limitation, ledger and OKF delivery-map changes and lifecycle state. Each names base identity/hash, sequence/predecessor, included paths/hashes, cutoff and related receipts. Upload to the same reconciled folder and content-verify. The delivery index lists the exact base and ordered segments.
5. After the last declared supplement actually passes verification, write final stage-22 acceptance and `completion_delivered` in a disclosed **terminal local acknowledgment**. It identifies the verified closing segment and true timestamp. No uploaded record claims its own future upload succeeded. Keep the terminal receipt locally and identify its path/hash/local-only status in the final delivery information; its not-yet-existing acknowledgment is not recursively packaged.

Use bounded deterministic closing-supplement validation, not an infinite critic-on-upload-receipt loop. Retrying delivery appends a new segment and reconciles IDs. An unchanged scientific base need not be rebuilt for lifecycle logs; a substantive artifact/integrity change reopens affected gates. Optional post-task provenance later uses a versioned supplement and does not relabel prior evidence or trigger recursive epilogues.

## Restore and report

Before extraction follow [execution trust](execution-trust.md): traversal/collision/symlink checks, isolated destination and reversible cross-platform path map. Validate base inventory and every available supplement's project/run/delivery, ordering/predecessor, hash, cutoff and referenced receipts. Reconstruct only validated record transitions; never execute historical jobs or reenable automations. Preserve originals and use installed ledger recovery interfaces.

An older base is not the final state until supplements are reconciled. Missing/mismatched segments or absent terminal acknowledgment leave completion unknown/pending. Bounded read-only destination reconciliation may establish a new timestamped verification; it cannot fabricate historical acceptance/time or create duplicate science/folders/uploads. `acceptance-ready` alone remains unaccepted. See [state recovery](state-recovery.md).

Final receipt/report names inventory completeness/exclusions, remote/local/archive hashes and locations, observed Drive folder/file IDs/links, content-check method, ordered segments/cutoffs, terminal local receipt, upload status, infrastructure state and remaining charges. Report completed research with delivery pending until the full closing contract succeeds.
