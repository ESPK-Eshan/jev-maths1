# Installed integration routing

Read the selected route only. Resolve the current installed skill entrypoint, load it and relevant referenced files before dispatch. Record actual path, version/commit, entrypoint and used reference/script hashes in the project capability manifest. A named skill in a prompt is not proof it was read. Installed instructions, available tools and configured/verified execution are separate capability levels. On resume, a changed loaded contract invalidates affected workflow assumptions and receipts even if output hashes match.

## Local anchors and ownership

Observed installation anchors on 10 October 2026:

| Anchor | Observed path/version |
| --- | --- |
| `SKILLS_ROOT` | `C:/Users/eshan/.agents/skills/`; Orchestra commit `773a52944ba4747a18bd4ae9ade53fff041adcbc`, K-Dense commit `92ace75ac21efe19a620434e0ca4e356081fe807`. |
| `ARS_ROOT` | `C:/Users/eshan/.codex/plugins/cache/ars-codex/ars-codex/3.23.0/skills/academic-research-suite/`; router/adapter 3.23.0, installation commit `52228e8280dd1770e18ecfc3b1fdf16b13b58104`. |
| codex-autoresearch | `SKILLS_ROOT/codex-autoresearch/`; commit `0f54c571707487f59486ba7c50d405edfc746c19`. |
| Standalone tools | `C:/Users/eshan/.codex/research-tools/AutoResearchClaw/` (0.5.0) and `paper-orchestra/`; installed receipt records `configured: false`. |
| Installation receipt | `C:/Users/eshan/.codex/research-tools/installation-manifest.json`. |

These are discovery anchors, not portable remote paths or attestations of credentials. Re-resolve on another host. One native coordinator owns the hybrid pipeline; one experiment controller per active experiment repository. Standalone frameworks use isolated job directories and return inspectable artifacts. No framework owns the canonical research state instead.

## Primary scientific routes

| Need | Load first and exact selected route |
| --- | --- |
| Scoping, research question, literature, source checking, synthesis | `ARS_ROOT/SKILL.md`, then `ars/deep-research/WORKFLOW.md`; resolve `socratic`, `full`, `lit-review`, `systematic-review` or other applicable mode explicitly. Use its `research_question_agent.md`, `research_architect_agent.md`, `source_verification_agent.md`, `synthesis_agent.md`, `devils_advocate_agent.md` as applicable. |
| Creative mechanisms and alternatives | Orchestra `brainstorming-research-ideas/SKILL.md`, `creative-thinking-for-research/SKILL.md`. K-Dense `hypothesis-generation`, `experimental-design`, `scientific-critical-thinking` complement specific scientific needs. |
| Implementation/evaluation | Smallest relevant Orchestra skill set after task resolution: e.g. RAG `llamaindex`/`langchain`, `sentence-transformers`, vector search, `dspy`; LLM `peft`, `trl-fine-tuning`, `unsloth`, `lm-evaluation-harness`, `vllm`; diffusion `stable-diffusion`, `ml-training-recipes`. Directory names are local entrypoints; read YAML skill names before invocation. |
| Execution/statistics checks | Applicable ARS `ars/experiment-agent/WORKFLOW.md` and complementary K-Dense `experimental-design`, `statistical-analysis`. The native controller/protocol still owns actual execution. |
| ML/systems writing and packaging | Orchestra `ml-paper-writing`, `systems-paper-writing`, `academic-plotting`; complement with K-Dense `scientific-writing`, `scientific-visualization`, `venue-templates` where useful. Current selected journal/institution format overrides generic conference defaults. |
| Review/citations/integrity | ARS `ars/academic-paper-reviewer/WORKFLOW.md` with `codex/agents/paper-reviewer-panel.md`; `ars/academic-paper/agents/citation_compliance_agent.md`; selected `ars/academic-pipeline` integrity/claim verification contracts. Read exact filenames from the current router, not recalled aliases. |
| Compute backend | Orchestra `skypilot/SKILL.md`, `ray-data/SKILL.md`, `ray-train/SKILL.md` only where useful under [compute execution](compute-execution.md). |

ARS leads academic scoping, literature, source verification, synthesis and integrity/review contracts; Orchestra leads creative ideation, AI implementation/evaluation, ML/systems writing and packaging. K-Dense is complementary, not the automatic replacement. Missing ARS/optional entrypoints trigger an explicit available route choice and limitation; no pretend invocation. Screening uses `ars/sr-screener/WORKFLOW.md` only for an actual requested screening task, not automatically for every literature review. Do not launch a second full ARS pipeline merely to reuse one check.

The ARS Codex router maps vendored `SKILL.md` references to workflow `WORKFLOW.md`, `${CLAUDE_PLUGIN_ROOT}`/root references to `ARS_ROOT/ars/`, and Claude `sonnet`/`opus` hints to role descriptions, not model selections. `codex/model-runtime-policy.md` preserves explicit user/runtime settings. The optional fixed planner and hook pack do not execute the user's arbitrary role/effort profile and remain opt-in; they are not prerequisites for native delegation. Existing settled routes continue on resume instead of routing again.

## Select manuscript mode before its dependencies

| Route | Concrete obligations |
| --- | --- |
| Orchestra draft + named ARS checks | Native stages 16–19 own drafting. Obey prerequisites of the selected checks; report a draft/check result, never claim ARS `academic-paper full` ran. |
| ARS `academic-paper full` | Load `ars/academic-paper/WORKFLOW.md`; actual Paper Configuration Record confirmation precedes Phase 1; actual outline approval precedes Phase 3. Reuse matching exact recorded decisions. Native stages 16–17 map to the owning draft route. |
| ARS standalone/pipeline `revision` | Native 19 consumes immutable `revision-roadmap/1.0` plus explicit `author-adjudication/1.0` and exact registered surfaces. Use installed anchorize → current patch → deterministic apply → finalizer/evidence replay. |
| ARS pipeline revision/re-review | Stage 4 proceeds to mandatory applicable Stage 3-prime; allowed Stage 4-prime precedes Stage 4.5 final integrity. Native verifier/critic remain additional gates. |

In `academic-paper full`, physically separate four model calls: writer 4a paper-blind precommitment; writer 4b visible drafting; evaluator 6a paper-blind precommitment (can inspect the permitted writer 4a artifact, never draft 4b); evaluator 6b visible evaluation. Read exact prompt/input/lint contracts and `shared/contracts/writer/full.json`, `shared/contracts/evaluator/full.json`. One agent presenting four headings is not separation. Preserve acronym/lint reports and exact upstream unusable-phase outcomes; native numeric criticism does not substitute for them.

Revision uses `ars/scripts/ars_anchorize_draft.py`, `ars/shared/contracts/patch/revision_patch.schema.json` (current patch 1.1), `ars/scripts/ars_apply_revision_patch.py` (current report 1.3), `ars/academic-paper/references/revision_patch_protocol.md`, and the finalizer selected there. Registered claim movement requires the exact authorized replacement, and declined overlap requires exact collateral authority. Unregistered claim drift found by E6 requires actual `restore`, `authorize_with_reason`, or `pause` with its required raw session-event byte binding; an ordinary native revision matrix or generic “continue” cannot invent `author-adjudication/1.0`.

Prepare concrete PCR/outline/roadmap/patch/replacement text before an essential unresolved author question. Persist the exact pending checkpoint; proceed with independent permitted work. Reuse applicable author decisions and the user's explicit authority. Do not infer human reading, institution approval or assent to unknown later text. If an installed requirement blocks, name/link its exact file and quote the applicable rule. A declared authorized bounded drafting route can deliver an honest draft; it cannot relabel failed full-mode obligations as passed.

## Exact current re-review

Read `ars/academic-paper-reviewer/references/re_review_mode_protocol.md`. Current `shared/contracts/re_review/input_manifest.schema.json` is 1.1: bind original pre-revision and revised manuscripts, immutable roadmap, explicit author sidecar, replayed `revision-evidence-bundle/1.0`, exact ordered patch/apply-report pairs and applicable response/decision letters, original findings and frozen reviewer cards. Mandatory missing/hash-mismatched material yields `manifest_incomplete`/`manifest_hash_mismatch`; no silent mixed 1.0/1.1 or legacy fallback. Preserve legitimate optional-absence policies from the current schema.

Run three sequential physically fenced gates: revision-blind criteria commitment → persuasion-blind manuscript/evidence verdict (persist before revealing letter) → response-letter claim matching. Preserve specified post-2B ordering, dissent, new-issue attribution and deferral/reapplication contracts. Invoke `ars/scripts/check_re_review_synthesis.py` with the current manifest/precommitment/verdict/traceability/roadmap and exact `--author-adjudication`, `--revision-evidence-bundle`, `--revision-evidence-root` plus manifest-required ordered flags before surfacing a decision; rerun after an allowed deferral update. Carry frozen traceability/new issues into final integrity.

Share one declared manuscript edit allocation across native reloops and nested ARS revision limits. Native maximum is two reloops; selected ARS tighter limits also apply (inspected pipeline Stage 4 plus at most one Stage 4-prime). If the tighter cap expires at native count 0/1, stop with `upstream_edit_limit` and an unaccepted partial draft; unused revisions do not count as exhausted-two eligibility for conditional advancement. Preserve actual scores/dispositions. ARS categorical/Schema-6 judgments and optional ARA 1–5 ratings are not converted into the separate native 0–100 critic sidecar. Invalid string/boolean scores fail numeric validation.

ARS passport append/report/show and exact decision persistence are in [state recovery](state-recovery.md). Pre-review integrity and post-revision/final integrity remain required by the chosen route. Optional external-model review, hooks or bibliography services need selected provider/content authority; installation alone activates none.

## codex-autoresearch and Windows

Resolve `SKILLS_ROOT/codex-autoresearch/scripts/autoresearch.py`; read its `references/workflow.md` before starting/changing/resuming. It owns metric measurement, commits, rollback and events. Scope, finite numeric metric/target, verify, fixed guards and per-trial resources are frozen. Successful foreground initialization precedes its matching native Goal; an already-complete initialization needs none. Only verified target success completes the campaign Goal. Scope/new-target/limit/plateau controls follow the installed workflow and [experiment campaigns](experiment-campaigns.md).

Initial support is foreground only. The inspected core calls `os.kill(pid, 0)` for liveness, unsafe on Windows; this is source-based compatibility evidence, not a tested live-PID probe. Disable detached launch and affected live-PID status/resume/archive paths until a narrow fix and process-ownership tests pass. Inspect stored mode safely before following generic status instructions; an existing Windows background run must not enter foreground controls. Do not use background-only CLI `stop` as a foreground strategy change or forge Goal completion. The detached contract has model but no effort field; never invent one. Remote adapter support is project-local validated work, not installed capability.

Orchestra `0-autoresearch-skill/SKILL.md` contributes scientific loop ideas only; do not run its separate Claude/OpenClaw continuity/Git mechanism. Foreground campaigns serialize in the coordinator's actual Goal namespace; no invented account-wide limit or extra-chat bypass.

## Optional packages and connectors

- **ARA:** `compiler/SKILL.md` (`ara-compiler` 1.0.0) can produce a separately scoped compatible ARA after inspected input coverage and actual Level-1 validation. `rigor-reviewer/SKILL.md` (`ara-rigor-reviewer` 3.0.0) requires that passed ARA and reads `PAPER.md`, `logic/claims.md`, `experiments.md`, `problem.md`, `concepts.md`, solution architecture/algorithm/constraints/heuristics, related work, exploration tree and evidence. It reads supplied local files only: no code execution, URLs or external acquisition. OKF alone is ineligible. `research-manager/SKILL.md` (`ara-research-manager` 1.0.0) is only a post-task epilogue after requested delivery; never an in-flight stage-21 recorder or canonical facts owner. Later permitted epilogue files use a supplement without recursive epilogue.
- **AutoResearchClaw:** use `researchclaw/pipeline/stages.py` as the exact 23-stage vocabulary. Optional actual framework jobs need isolated run directories, explicit real experiment mode, provider/config/resource contract and raw receipts. The inspected ACP session does not supply native per-role model/effort or independent reviewers; omitted mode may simulate. Validate checkpoints; no simulated/placeholder evidence promoted to measurements.
- **PaperOrchestra:** optional after evidence/figures freeze, at `paper_writing_cli.py` and `methods/paper_writer.py`. Native role settings do not configure direct APIs/effort. Each invocation uses a fresh output directory because reuse can delete prior draft/PDF artifacts. Do not enable arbitrary generated plotting execution. Imported drafts receive the same claim/citation/build/render checks. External TeX remains a separately checked capability.
- **Discovery:** alphaXiv discovery/content/raw-PDF and Consensus search/fetch tools were discoverable; use current live schemas/limits, returned IDs, and original passages. Fetch Consensus results before citing; generated summaries and publisher status need individual checks. See [literature contracts](literature-gap-hypotheses.md). Shared quotas cannot be evaded by worker fan-out.
- **Drive:** read `google-drive:google-drive` base file workflow and live upload/metadata/raw-fetch declarations; [delivery](archive-drive-delivery.md) owns actual capability checks. No upload capability is proven by discovery.
- **Artifacts:** load `pdf:pdf` for reading/render inspection and `documents:documents` for requested editable DOCX/thesis. Resolve bundled runtime/helpers and operation contracts at use time. User/journal/institution requirements prevail. A preview tab is not a successful build/render inspection. Slides/spreadsheets only when requested.
- **Hugging Face/tracking:** papers/Dataset Viewer/`hf-cli` are optional discovery or pinned permitted acquisition; previews do not replace complete inputs/revisions/hashes. Jobs/training/publishing need a selected authority/backend. One useful local/offline MLflow/TensorBoard/Trackio tracker can aid inspection; API uploads need the provider/data contract. Tracker receipts cannot rewrite controller outcomes or leak sealed confirmation.

Aider, OpenHands, Agon and AI-Scientist-v2 are not installed dependencies. Missing optional capabilities remain explicit; do not auto-install global packages or silently change provider. [Execution trust](execution-trust.md) governs all imported instructions and executable content.
