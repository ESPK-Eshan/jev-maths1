# Faithful architecture diagrams and figure package

Read when a method, experimental protocol or system needs a diagram, and before artifact review/export. Use Orchestra [academic plotting](C:/Users/eshan/.agents/skills/academic-plotting/SKILL.md), relevant architecture/domain skills and complementary [scientific visualization](C:/Users/eshan/.agents/skills/scientific-visualization/SKILL.md). Resolve actual local tools through [integrations](integrations.md); optional external image APIs are not automatically authorized.

## Figure assignment

Start with a question/claim-linked figure plan and verified implementation/protocol module specification. Select only explanatory views: method overview, novel module detail, training/inference flow, agent interaction, experiment/split plan or computational execution. The research orchestrator itself is not automatically the method studied in the paper. Decorative complexity is not scientific evidence.

For every architecture figure, record figure/claim IDs; intended takeaway; components and actual interfaces; data/control/feedback arrows with legend; inputs/outputs; learned/frozen portions; training/inference boundary; novel/inherited blocks; verified dimensions/tensor shapes where relevant; code/config/protocol links and versions; panel labels/symbols and manuscript terminology. Label proposed/conceptual/unimplemented components explicitly. Do not invent an interface or dimension to make the graphic look complete.

Group complexity into readable layers, inset the contribution when useful and remove decoration that does not explain the question. Distinguish visual hierarchy from causal claims. Arrow direction, labels and module dependencies must correspond to actual code/protocol. Equations, diagrams and prose use consistent names. A neat diagram cannot prove implementation correctness, model validity or a theorem.

## Build and deliver

Produce an editable deterministic master where appropriate, such as TikZ, Graphviz or SVG, its actual build script/tool version, journal-compatible exports, vector PDF with appropriate fonts when supported, final-size previews, caption, alt description where supported and a provenance manifest. The manifest binds master/export/build hashes, inspected implementation/protocol/evidence IDs, authoring tool, output formats, target placement/size and review receipts.

SVG is a useful editable master, not an assertion that every journal accepts it for submission. Verify actual selected-journal rules. [IEEE graphics formats](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/) and [resolution/size guidance](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/) are authoritative starting points; supported raster resolution depends on line art/image type and final size. Do not hard-code one DPI requirement for every figure or treat file extensions as compliance.

Measured displays follow [writing-artifact manifests](writing-artifacts.md): raw/aggregate hashes, scripts, transformations/exclusions, independent n, units and uncertainty. Tables distinguish project measurements from author-reported literature facts and missing values. Generated artwork is optional conceptual illustration and cannot supply empirical observations, synthetic-looking benchmark samples presented as collected evidence, numerical curves or proof.

## Final-size review contract

Inspect every main figure at intended single/double-column placement and inside the actual compiled paper. Check readable text/math, accessible colors and grayscale distinction, arrows/legend consistency, margins/cropping, panel labels, symbols, axes/units, uncertainty definitions, caption/data/implementation agreement and citations. Captions state takeaway/setup/caveats without adding unsupported claims. Supplement moves preserve claim and reproduction links.

The stage verifier checks provenance, faithfulness, rendering and reproduction; the critic assesses whether the view explains a meaningful scientific point. Output concrete mismatch/readability findings with affected source/export hashes and closure checks. After correction regenerate affected exports and recheck current manuscript placement. Metadata-only validation or inspection of a large standalone image cannot satisfy final-size review. Missing build/render capability yields a truthful source-only or pending-render artifact, not a verified figure package.
