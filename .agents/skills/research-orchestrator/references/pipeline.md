# Scientific route and stage contracts

Read at intake, route changes, or when selecting the next stage. [Integrations](integrations.md) resolves the installed ARS/Orchestra contracts; [state and recovery](state-recovery.md) owns mutations, receipt validity, and continuation. Stage numbers retain the inspected [AutoResearchClaw vocabulary](C:/Users/eshan/.codex/research-tools/AutoResearchClaw/researchclaw/pipeline/stages.py); its numeric execution sequence and controller are not imported.

## Normalize the scientific input

Preserve the user's exact input and distinguish fixed anchors from preferences. Mixed inputs may contain several anchors. Imported projects enter through provenance checks without overwriting existing evidence.

| Input | Required normalization before substantial execution |
|---|---|
| Idea | Answerable question, intended benefit, operational task, plausible alternatives; novelty remains to be tested. |
| Hypothesis | Variables, population/tasks, mechanism, predicted contrast, rivals and falsifier; the user's assertion is not supporting evidence. |
| Area | Bounded dated scoping scan, materially different feasible questions, reasoned selection within the delegated scope. |
| Named model/family | Actual identity/version or architecture scope, available access/license/capabilities and hardware implications; a question around that anchor. Do not assume weights/API access or silently substitute an easier model. |

For broad inputs, compare significance, nearest-work overlap, testability, data/baseline access and the cheapest informative study. Record rejected directions and the planning allocation. Exploratory scoping does not replace the later literature search or retrospectively establish a prospective review protocol. A narrow testable hypothesis need not be expanded into needless brainstorming.

The charter contains original input, selected question and rationale, fixed anchors, provisional paper route, evidence that could defeat it, pilot concept, compute-estimate status, effective role/profile and autonomy decision, deliverable inventory, bounded resources, stop conditions and next prerequisite. Reuse standing decisions; resolve only missing operating authority, essential scientific ambiguity and required author decisions. Deriving datasets, metrics, methods and outlines is the skill's work. Public affordable planning can proceed while unrelated resource prerequisites are pending. Full-project mode continues through all applicable authorized gates; the charter alone is not its endpoint.

## Stage-instance contract

Each instance declares stage number/name, phase, stable lineage/revision ID, task, input/output hashes, required predecessor instances, selected skill contracts, producer and independent verifier/critic, frozen rubric, authority/allocation, expected outputs, gate and next action. Every executed instance needs current separate [verifier](verification.md) and [critic](journal-stage-critique.md) receipts. A skipped instance needs an explicit `not_applicable` rationale, any replacement obligation, verification and critic disposition; it receives no fabricated score or execution receipt.

| # | Exact stage | Task, output and substantive exit criterion |
|---|---|---|
| 1 | TOPIC_INIT | ARS topic route: charter, normalized input, anchors, model identity/access where relevant, profile/autonomy/resources/deliverables. Essential ambiguity resolved or explicitly blocking. |
| 2 | PROBLEM_DECOMPOSE | Orchestra ideation: bounded questions, claim types, alternatives and task boundaries; answerable rather than a collection of trends. |
| 3 | SEARCH_STRATEGY | ARS research: dated source/query/coverage plan, alternate terminology, citation chains, inclusion/exclusion and access limits. |
| 4 | LITERATURE_COLLECT | Deduplicated work/family manifest, publication/version identity and source access/locators; distinguish original text, abstracts and generated summaries. |
| 5 | LITERATURE_SCREEN | Relevance decisions and reasons, strongest competitors and contrary work. Ordinary selection does not activate ARS `sr-screener`; use that workflow only on explicit request under its contract. |
| 6 | KNOWLEDGE_EXTRACT | Source-located comparable tasks, assumptions, data, method, metrics, baselines, resources, findings and limits; unavailable fields remain unavailable. |
| 7 | SYNTHESIS | ARS synthesis/devil's advocate plus Orchestra framing: contradictions, bounded gap, nearest-method delta and separate novelty counter-search. Disconfirmed gaps are removed or reframed. |
| 8 | HYPOTHESIS_GEN | Literature-bound predictions, rivals, falsifiers, useful effect/precision target, minimal decisive pilot, exploratory status and justified paper route. |
| 9 | EXPERIMENT_DESIGN | ARS experiment workflow first, Orchestra evaluation, complementary design/statistics: frozen protocol, measurement validity, units, contrasts, splits, guards, failure/exclusion/multiplicity/stopping rules and confirmation plan. Triggers immediate protocol-bound compute recommendation. |
| 10 | CODE_GENERATION | Selected Orchestra implementation: minimal baseline/method, dependency recipe, correct evaluator, relevant checks and smoke receipts. Both current feasibility and protocol-bound resource recommendation already pass. |
| 11 | RESOURCE_PLANNING | Separate initial-feasibility and protocol-bound-recommendation instances: bounded allocation, uncertainty, per-phase hardware/time/cost, host fit, placement/rental prerequisite and confirmation/closeout reserve. See [compute execution](compute-execution.md). |
| 12 | EXPERIMENT_RUN | Separate pilot and confirmation instances: actual execution, raw outcomes/failures, hashes, protocol, resource/cost/log receipts. A pilot closes before its analysis/decision; confirmation uses a frozen candidate and untouched evidence. |
| 13 | ITERATIVE_REFINE | Optional bounded development with codex-autoresearch, retained/discarded trials, guards, strategy/plateau decisions and exclusive controller ownership. |
| 14 | RESULT_ANALYSIS | Phase-specific reproducible aggregates, contrasts, uncertainty, robustness, cost and failure analysis; distinguish supported, negative and inconclusive findings. |
| 15 | RESEARCH_DECISION | Evidence/budget-backed proceed, refine, pivot, narrow or stop; assess recovery/fresh-evidence obligations. No forced acceptance at exhausted pivot limits. |
| 16 | PAPER_OUTLINE | Evidence-to-section/claim map, contribution and paper type, venue fit, artifact plan and contracted thesis adaptation. |
| 17 | PAPER_DRAFT | Complete evidence-bound draft, deterministic measured tables/plots, justified conceptual figures, references and supplements. |
| 18 | PEER_REVIEW | Fresh scientific/citation review; selected ARS panel first, complementary peer review. Pre-review integrity must precede an applicable ARS manuscript review. |
| 19 | PAPER_REVISION | Issue-to-change/evidence matrix; selected ARS route additionally requires exact author/patch/evidence carriers and re-review. Method changes reopen experiments. |
| 20 | QUALITY_GATE | Current execution, scientific, citation, integrity, artifact, format and bounded reproduction checks for every selected deliverable and declared status; stage 23 has already passed for verified export. |
| 21 | KNOWLEDGE_ARCHIVE | Findings, failed routes, provenance, effective profile, environment/reproduction, next questions and complete inventory. Required evidence is retained. Optional ARA research-manager runs only after task completion. |
| 22 | EXPORT_PUBLISH | Versioned requested sources/editable formats, actual builds/renders and declared draft status; remote completion includes verified archive/transfer/Drive delivery. No implicit public release or submission. |
| 23 | CITATION_VERIFY | ARS citation/source verification first: real identities, matching versions, proposition support and locators, coverage and applicable official venue rules. |

## Actual dependency routes

Empirical route:

`1–8 → 11(initial-feasibility) → 9(protocol) → 11(protocol-bound-recommendation) → 10 → 12(pilot) → 14(pilot-analysis) → 15(pilot-decision) → optional 13(development) → candidate freeze → 12(confirmation) → 14(final-analysis) → 15(final-decision) → 16 → 17 → pre-review integrity → 18 → 19 → applicable ARS re-review/bounded re-revision → post-revision integrity + 23 → 20(reproduction included) → 21 → 22`.

The initial stage 11 enables design; its separate immutable refinement binds the completed protocol and enables full implementation. Refinement cannot overwrite feasibility, form a cycle, or reset stage 9's lineage. Deliver its readable recommendation immediately after planning, including plan-only mode. Intensive work waits for actual authorized capacity; eligible affordable preparation continues.

A valid negative/harmful/inconclusive pilot enters stages 14–15 directly, before unrun development or confirmation. [Recovery](negative-result-recovery.md) may yield a discriminating follow-up, scoped route amendment or faithful report. Invalid measurement returns to engineering/evaluation. Closed development or a prespecified checkpoint can likewise enter phase-specific analysis/decision using only permitted development evidence. A promising pilot permits bounded development or justified direct freeze/confirmation. Neither route substitutes pilot receipts for final-analysis/final-decision or confirmation receipts. Record unrun downstream instances as pending, stopped, or verified not applicable; never accepted by implication.

Review/synthesis route: `1–3 → 11 → 9(review protocol) → 4–7(substantive collection/screening/extraction/synthesis) → 8(analytic propositions) → 14–23 as applicable`. Stages 10–13 apply only to real extraction/analysis code or a justified empirical component. Separate exploratory scoping from the review corpus; protocol/amendments precede claimed prospective work. Retrospective imports cannot become preregistered by adding a timestamp. Preserve source verification, family deduplication, selection/coverage and bias limitations. No GPU/Goal is needed merely to fill numbered stages.

Theory route: stages 1–8 establish nearest results, assumptions, conjectures and proof obligations; 11 budgets review; 9 fixes theorem/assumption/verification plan. Stages 10–13 apply only to actual computational checks. Stage 14 requires complete inspectable derivations and independent proof scrutiny; examples are not proof. Missing expertise/obligations lead to a conjecture/analysis draft rather than certification.

Plan, pilot, artifacts, manuscript, review and resume modes activate the requested subgraph after imported-evidence verification. Declare entry assumptions, missing upstream checks and own completion status. Manuscript-only work does not certify novelty or experiments; pilot-only work does not certify confirmation or complete a full-project request.

## Scientific decisions and author boundaries

Choose the provisional paper type before experiments and reassess from evidence. Method papers need a material distinction, fair strong baselines and informative ablations; comparative work needs useful new evaluation insight; mechanism claims need appropriate rival/intervention tests; systems work needs real workloads and quality/cost measurement; replication/negative studies need faithful setup and useful precision. Non-significance is not equivalence. Review and theory satisfy their alternative obligations above. A thesis adds coherent explanation, not invented contributions.

Select the manuscript route before dependent work: Orchestra drafting with named ARS checks, ARS `academic-paper full`, or applicable ARS revision/pipeline. [Writing artifacts](writing-artifacts.md) and [integrations](integrations.md) define exact PCR/outline/author-adjudication and re-review carriers. Reuse applicable actual author decisions; prepare concrete reviewable material before requesting missing decisions. General autonomy does not supply unknown future claim replacements or human review. A tighter ARS cap reached at native reloop 0/1 means `stopped` with `upstream_edit_limit` and an unaccepted partial draft, not two-reloop conditional advancement.

Any material change invalidates affected descendants and returns to the earliest affected obligation. Preserve hypotheses, failures, costs and lineages. Route amendments must be scientific changes with their own evidence, never cosmetic resets. Stage quality assesses truthful inference even when the hypothesis loses.
