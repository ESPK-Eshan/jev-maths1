# OKF knowledge bundle and selective handoffs

Read when producing project documentation or dispatch/resume packets. Use local `knowledge/` files throughout the project; no Google Cloud account, Gemini, BigQuery or reference agent is required.

## Format and research profile

Pin [Google Cloud OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md) at commit `ad30107c31c06aec8a7d5636e0d1058118604e6f` plus the project research-profile version. A concept is UTF-8 Markdown with YAML frontmatter and a nonempty string `type`; unknown types/extensions remain tolerated/preserved. `index.md` and `log.md` are reserved navigation/history, not concepts. Root index can declare `okf_version`. Parse with a real safe YAML parser; a text scanner cannot claim full YAML compatibility.

Metadata families include `sources` entries with `resource` (and optional IDs for body references), `generated`, `verified`, lifecycle `status` (`draft`, `stable`, `deprecated`) and offset-qualified `stale_after` when applicable. Use real actor/check/time information; machine confirmation is not human review. A stable label does not prove a factual claim.

Our stricter research profile additionally binds run/stage-instance, evidence IDs/input hashes, protocol version, access class and claim state as applicable. Required scientific readiness means meaningful content, resolvable critical raw/source links, accurate computation/artifact mappings and fresh receipts. Separate that judgment from basic OKF conformance: a format-compatible file can remain scientifically unready. Preserve unsupported/unknown fields; do not call every project-specific failure a Google format violation.

## Create only useful concepts

Start with a small root index and accepted-change `log.md`. Add concepts when actual evidence exists: charter, search boundary/nearest work, current gap, hypothesis/rivals/falsifier, method, pilot and separate confirmation protocol, approved metric, pilot and separate confirmation findings, strategy decisions, issues, figure/claim maps and scoped reusable lessons. Include versioned resource plan/DAG/job ownership/utilization/checkpoint/export/lifecycle concepts for remote work, and delivery/reproduction maps at closeout. Do not generate an empty directory vocabulary.

Keep raw data, full logs, PDFs, receipts and manuscript source in authoritative project locations and reference them. `.research` and controller receipts own facts; knowledge documents are navigation plus authored interpretation. Documentation steward proposes updates from accepted outputs, coordinator merges, independent verifier checks changed knowledge against evidence. Pending findings can be clearly draft. Update navigation/history at meaningful boundaries; preserve failed history and distinguish pilot from confirmation.

## Load and hand off selectively

Begin with root index/current stage summary, then only relevant concepts and necessary dependencies/raw sources. A numerical or source-support check opens the required originals, not just a compressed summary. Record partial/full access. Never load the entire bundle, all skills or all logs by default. Apply confirmation/restricted access to link text and indexes as well as files.

Dispatch packet: bounded question; role/model/settings; stage/phase/protocol; accepted concept IDs/hashes; essential raw locators; current facts and contrary evidence; relevant issues; permitted writes/resources/deadline; output/pass contract; specific next decision. Aim at roughly 1,500–2,500 summary tokens when practical, marking estimated counts unless measured with a tokenizer. Essential evidence is not removed to meet that target. Exclude unrelated history and peer reviewer verdicts. [Agent contracts](agent-contracts.md) govern actual fresh contexts.

Cache by task contract, source/concept hashes, protocol and freshness. Changed evidence/method/metric/claim invalidates affected concepts/handoffs/checks; retain historical verification but clearly supersede it. Traverse dependency links with cycle detection and ensure current links resolve to the intended candidate. Track actual input/output usage and repeated loads if available; no invented token-saving percentage.

## Attested Computation is conditional

Use `type: Attested Computation` only with its pinned interface: `runtime`; typed named `parameters` where applicable; `computation` source path or the body `# Computation` fence; `executor.resource`; `executor.receipt` declaring returned fields; and `attester.resource` for a deterministic no-LLM checker. Bind executable/config/data hashes, allowed parameter values, actual receipt and displayed numbers. If executor/attester interfaces are absent, use an ordinary metric/evidence concept with explicit unverified status. A link does not authorize execution or replace immutable controller state. Semantic scientific review remains separate.

## Resume and delivery

Continuation packet names project path, contract/profile, stage instance, selected candidate, engine/job ownership, relevant knowledge roots, open issues/limits and next permitted action. It supplements exact durable user/ARS decisions; it cannot recreate missing authority. At export include knowledge and reproduction maps. Delivery concept references inventory/exclusions, actual verified transfer/Drive IDs/observed links, operational segment order and terminal-local-receipt limitation. An unknown upload or stopped-machine state cannot become success through documentation. Restore follows [state recovery](state-recovery.md), without historical job/automation reactivation.

ARA is a different optional format. This bundle cannot establish ARA Level 1 or qualify for `ara-rigor-reviewer`; see [integrations](integrations.md).
