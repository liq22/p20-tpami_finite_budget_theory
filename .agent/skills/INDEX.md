# Skills Index

Only `00-router` and explicit `grill-me` are host-visible. The Router selects one
internal primary; libraries, document tools, and lookup backends support that
primary and do not compete with it.

## Routeable primary Skills

| Product | Primary Skills |
|---|---|
| research state and direction | `01-project-brief`, `scientific-brainstorming`, `hypothesis-generation`, `02-research-question`, `05-claim-evidence` |
| literature positioning | `03-literature-deep-research`, `literature-review`, `04-journal-fit` |
| method and critical reasoning | `method-design`, `scientific-critical-thinking` |
| code | `code-change`, `code-module-xray` |
| experiment and statistics | `experimental-design`, `06-experiment-ops`, `statistical-analysis`, `statistical-power` |
| explicit independent review | `07-experiment-audit`, `peer-review`, `11-reference-audit` |
| manuscript and TeX | `08-markdown-draft`, `10-language-polish`, `09-tex-freeze-formalize` |
| figures/tables | `15-figure-table-design` |
| revision/submission | `13-reviewer-response`, `12-submission-pack` |
| consequential preflight | `14-agent-safety` |
| PaperTrace maintenance | `repository-self-evolution` |

Primary behavior is specified in `ROUTING_MATRIX.md` and covered by the case
definitions under `.agent/evals/`.

## Supporting knowledge and tools

These activate only after a primary product is selected:

- writing/source support: `scientific-writing`, `anti-defensive-writing`,
  `citation-management`, `venue-templates`, lookup/search Skills;
- numerical/ML libraries: scikit-learn, PyMC, statsmodels, PyTorch Lightning,
  Transformers, Torch Geometric, UMAP, NetworkX, Dask, Polars, and specialized
  forecasting/RL tools;
- visual backends: scientific visualization/schematics, matplotlib, seaborn,
  Mermaid, slides, image/infographic tools;
- file products: PDF, DOCX, XLSX, PPTX;
- optional external capabilities: allowlisted ARIS Skills resolved through
  `integrations/aris/adapter.py`.

`anti-defensive-writing` is loaded only by `10-language-polish` when the user
explicitly asks to remove defensive framing from stable prose. It does not create
a third host entry or replace claim/evidence correction.

Supporting tools require readable operational guidance, but they are not part of
the universal research workflow and are not copied into a task unless needed.

## Boundaries

- Audit and review are explicit-only.
- A tool record, manifest, matrix, or report does not replace the requested
  product.
- ARIS is opt-in, hidden behind the Router, and its high-level pipelines remain
  disabled.
- Project-specific repositories may keep a smaller Skill subset and local
  overrides; PaperTrace must not synchronize their scientific facts.
