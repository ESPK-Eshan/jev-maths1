# Independent stage criticism and scored gate

Read when assigning a stage, reviewing its output, revising it or making a post-reloop decision. The designated `journal_stage_critic` gives demanding evidence-based AI journal criticism, separate from the stage verifier and producer. This is model-assisted review, not human credentials, an editorial decision or acceptance odds.

## Freeze assignment before scoring

For each executed stage instance, freeze purpose/phase, input/output contract, at least five distinct applicable criterion definitions with evidence expectations, rubric version/hash and threshold before its initial output is judged. Default to seven equal-weight criteria:

1. Correctness and evidence fidelity.
2. Scientific importance and relevance to the bounded contribution.
3. Methodological/evaluation rigor.
4. Coverage of alternatives and limitations.
5. Reproducibility and operational completeness.
6. Communication and artifact quality.
7. Efficiency and practical feasibility.

Tailor criterion meaning to stage purpose: intake needs an actionable charter, execution needs actual valid runs, export needs usable verified artifacts/restoration. Do not demand final results at intake or treat aesthetics as validity. Replace inapplicable criteria before review with distinct relevant criteria; never award N/A 100 or drop a weak criterion after scoring.

The critic and verifier get separate fresh scoped packets with original task, immutable artifacts/hashes, applicable primary evidence and skill contracts, venue rules when established, resource/inspection limits and explicit supported settings. Use `fork_turns="none"` for fresh/blinded roles; native defaults inherit history. Parallelize only within actual slots/resources, otherwise review sequentially without sharing initial verdicts. A contaminated reused producer cannot stand in for either reviewer. Follow [swarm capacity](swarm-execution.md).

ARS source/devil's-advocate/experiment/integrity/reviewer contracts lead academic review; Orchestra domain/writing/rigor skills inform ML substance and complementary critical-thinking fills gaps. Do not launch an entire ARS panel at every stage. If invoking its manuscript review even at an intermediate stage, satisfy the mandatory pre-review integrity prerequisite first.

## Critique receipt

Record stage/phase/instance/revision, role/model/effort, inspected input/output/rubric hashes and source locators, performed/missing checks, supported merits, complete criterion scores and reasoned gaps, and issue records. Each issue needs ID/category/severity, exact objection and evidence, likely scientific or presentation consequence, cheapest discriminating check, proposed fix, owner and closure criterion. Mark uncertain objections or inaccessible evidence. Novelty, validity, literature, fair baselines, inference, reproducibility, artifacts, prose and venue fit apply in proportion to stage purpose.

Each score is an integer 0–100 with justification and evidence locator. Reject booleans, numeric strings, missing/nonfinite/out-of-range values and duplicate/missing criteria. Anchors: 0–59 severe inadequacy; 60–79 substantial deficiencies; 80–89 generally sound but material gaps; 90–99 strong evidence/completeness in scope with at most minor limits; 100 exceptional completeness in scope, never infallibility. Do not raise a score for pipeline convenience.

The native sidecar is independent of ARS live categorical/Schema-6 judgments and their `NOT_CALIBRATED` provenance. Never inject its scores/weights/mean into ARS carriers or convert ARS categories into numbers. Optional ARA 1–5 ratings remain their own report. No rating is a calibrated journal-acceptance probability.

## Normal gate and exact boundary

Compute the equal-weight unrounded mean `sum(scores) / count(scores)`. At least five distinct valid applicable criteria are mandatory. Compare the actual mean: exactly 90 meets the numerical boundary; a mean below 90 rounded for display to 90.00 does not. The verifier independently recomputes and checks rubric/hash/issue consistency; the [record helper](record-cli.md) validates recorded structure, not the substantive truth of judgments.

Ordinary `advance` requires mean ≥90, current passing independent verifier/critic receipts bound to actual hashes, required ARS integrity/author/execution prerequisites and no stage-blocking findings. A high average cannot waive fabricated citations, nonexecution, leakage, malformed metrics, missing required artifacts, unverified backup, false approval or other critical validity/integrity faults.

## At most two producer reloops

Iteration 0 is the original output and assessment. Reloop 1 is the first changed producer output and fresh receipts; reloop 2 is the second. At most three scored producer versions exist in a lineage. Before exhaustion, below 90 returns to the same stage with expected substantive improvements if feasible; budget, invalid premise or required evidence can stop earlier. The cap is “up to two,” not an instruction to waste rounds.

Reserve/persist the next revision number and stable revision/task ID before dispatch under coordinator ownership. Each revision packet contains issue IDs, original evidence, prioritized expected changes, owner, cheapest valid check, output/hash changes, allocated resources and measurable closure criteria. Critic rescores against the frozen rubric with reasons for changes; verifier checks the actual correction and relevant regression/source/artifact evidence. Cosmetic rewriting cannot count as repairing a substantive flaw.

Resume, compaction, retries, worker replacement or renamed files/stages preserve counter/rubric/history. Repairing malformed review syntax on the same producer hash/revision is a bounded operational retry; changed producer content requires the proper reloop. No hidden retries or arbitrary new lineage. A genuine authorized scientific replan links original history, changes real obligations and invalidates affected dependents. Experiment trials and project pivots retain their separate bounds; two critic reloops are not a two-trial limit.

Selected ARS inner edits and native revisions share the declared stage lineage/allocation; upstream tighter caps still apply. In the inspected pipeline, Stage 4 plus at most one Stage 4-prime replaces standalone revision allowances. If that upstream limit stops editing at native count 0 or 1, record `stopped`, reason `upstream_edit_limit`, and preserve an honest unaccepted partial draft. Unused revisions cannot be counted as exhausted. This case is ineligible for `conditional_advance`; normal advance remains possible if actual prerequisites already pass.

## Decision after reloop 2

If still below threshold or blocked after two reloops, stop automatic same-lineage edits. The main orchestrator or an explicitly delegated bounded decision executor assesses impact, remaining authority/resources, alternatives and downstream dependencies; coordinator remains sole state writer. Producer cannot approve its own unresolved faults or impersonate the critic/verifier. Routine permitted choices do not automatically become user questions.

| Remaining demonstrated impact | Permitted next action |
|---|---|
| Minor/nonblocking | `conditional_advance` only with independent support for nonblocking status, current mandatory gates, preserved actual below-90 scores and open/deferred issues, accepted limitations and reasoned exception receipt. |
| Major/addressable | Meaningful authorized strategy change, stronger baseline, claim narrowing, alternative tool or substantive replan; reopen earliest affected obligations. Do not rename the same defect to buy a third edit. |
| Critical validity/execution/citation/integrity/confirmation/backup/author fault | Block dependent claims/stages; feasible authorized repair/replan or honest stop/report. Never waive the mandatory obligation. |
| Insufficient evidence/resources or defeated premise | Stop expensive work; narrower defensible report or explicit unavailable/inconclusive state. Ask only when next action genuinely needs external information/authority. |

Exception/decision receipt includes original scores/rubric/current hashes, actual two revision IDs, findings and verification states, severity rationale, options, chosen action, scope/claim/resource changes, accepted limits, downstream effects and next permitted action. Preserve dissent; labels or majority votes cannot erase faults. Conditional advance is neither a numerical pass nor issue closure and does not confer author approval. Export carries the actual limitation. New spending/provider/upload, materially external scope or essential author information still follows the project contract.

Material changes require critic reinspection/new or amended hash-bound critique; nonmaterial edits need a scoped impact confirmation. Final independent scientific reviewer/applicable ARS panel remains a manuscript-wide synthesis; accumulated stage scores do not replace it.
