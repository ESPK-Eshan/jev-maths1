# Offline delivery verification helper

Use after preparing the full permitted inventory and after obtaining actual transfer/plugin evidence. This helper does not enumerate remote projects, scrub secrets, create ZIPs, upload, inspect service accounts, authenticate receipts, alter the project ledger or execute restored jobs. Apply [archive-drive-delivery.md](archive-drive-delivery.md) for those agent/tool obligations and [record-cli.md](record-cli.md) for canonical transitions. A valid local record is not independent proof of a remote action.

## Archive content and safe restoration

```text
python <skill-dir>/scripts/research_delivery.py archive-verify <project.zip> --manifest <inventory.json>
python <skill-dir>/scripts/research_delivery.py archive-verify <project.zip> --manifest <inventory.json> --extract-to <new-directory> --max-bytes <authorized-expanded-byte-limit>
```

The default expansion limit is 10 GiB; set an explicit fitting limit for larger authorized packages. The extraction parent must exist and the destination must be new. Check available disk first. ZIP64 is supported by Python's zipfile library; this helper does not require large fixtures to exercise inventory logic. It rejects traversal, encrypted/special/symlink entries, duplicates, case/Unicode normalization collisions, Windows device names/streams and ambiguous path components. If a legitimate source uses such names, prepare and validate a reversible path map before creating a portable archive; do not silently drop or rename entries during restoration.

Inventory schema (replace example values with actual paths, sizes and SHA-256 values):

```json
{
  "schema_version": 1,
  "files": [{"path": "results/measurements.csv", "bytes": 1432, "sha256": "actual-sha256-required"}],
  "exclusions": [{"path": ".env", "reason": "Credential file excluded; credentials are provisioned separately."}]
}
```

The hash marker above is explanatory and deliberately invalid. `files` must cover every file in the ZIP, exactly once; declared sizes and full contents are verified. The coordinator separately verifies that this inventory covers every permitted source-project file, including failures, checkpoints and logs. Secret auditing and disclosed license/access exclusions are mandatory upstream obligations; a matching manifest cannot prove that omitted source files were justified. Interrupted extraction may leave a partial new directory; retain its failure evidence, never treat it as a successful restore or overwrite it silently.

Exit 0 means local contents match; exit 2 means invalid/unreadable content or unsafe extraction. Extracted scientific records still undergo independent review and the replay rules in state-recovery.md.

## Ordered closing records

```text
python <skill-dir>/scripts/research_delivery.py delivery-verify <delivery-directory> --index <delivery-index.json> --ack <terminal-local-ack.json>
```

All referenced paths are relative to the supplied delivery directory and must resolve to actual local files. For a cloud backup, materialize the permitted base/supplements and actual service receipts first; no remote URI is treated as a local file.

Index fields:

```json
{
  "schema_version": 1,
  "project_id": "project-identity",
  "run_id": "run-identity",
  "delivery_version": 1,
  "base": {"path": "project.zip", "sha256": "actual-base-hash"},
  "segments": [{"path": "closing-001.json", "sha256": "actual-segment-hash", "sequence": 1, "previous_sha256": "actual-base-hash"}]
}
```

Each segment is a JSON object with `schema_version:1`, the same three identity fields, consecutive integer `sequence` starting at 1, `base_sha256`, `previous_sha256`, timezone-aware `created_at` and `state`. Intermediate state is `recording` or `limitation`; the last completed chain uses `acceptance-ready`. The first predecessor is the base hash; later predecessors are the preceding segment hashes. Store actual post-cutoff ledger/OKF events and log inventory/references in those records or bound attachments. The last segment has `stage22_reviews`, an array of `{path, sha256}` references to actual stage verifier and critic reports; native gates enforce their substance and independence.

The terminal local acknowledgment has the same schema/identity fields plus:

- `status: "delivered"`, `stage22_status: "accepted"`;
- `base_sha256`, `last_segment_sha256`;
- timezone-aware `verified_at`, recorded only after all content checks actually finish;
- `content_verifications`: one record per base/segment hash with `artifact_sha256`, `method` (`checksum` or `full-content-readback`), `evidence: {path, sha256}` and its actual timezone-aware `verified_at`.

The terminal timestamp cannot precede a content verification, and a segment's verification cannot precede its creation. Each evidence file must contain the actual tool/service receipt or raw readback evidence, including observed destination IDs, relevant checksum/digest calculation, coverage and limitations. Do not write a claim of success as a substitute. The helper checks local hashes/ordering, while the independent verifier inspects the actual service evidence. Metadata-only checks cannot satisfy this contract.

Result `recorded-delivery-supported` (exit 0) means the supplied local chain is consistent; it explicitly leaves `remote_independently_attested:false`. Missing or mismatched records return `delivery-pending` (exit 3) with reasons and the number of valid segments. No acknowledgment, job, folder or upload is fabricated or replayed. Restore can reconstruct the valid earlier boundary; a later actual successful reconciliation receives its own truthful timestamp, never an invented historical acknowledgment.
