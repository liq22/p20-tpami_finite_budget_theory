# Invocation Scenarios

Realistic prompts for the markdown-mermaid-writing skill in the single-paper workflow.

## Scenario 1: Diagram the experimental pipeline for the methods section

> The reviewer said our methods are hard to follow. Read `paper/experiments/run_ledger.md` and `paper/experiments/reproducibility.md`, and add a structural diagram of the data pipeline (raw data → preprocessing → train/eval split → model → metrics) to the methods draft in `paper/draft/`. Use Mermaid in markdown — flowchart unless a better type fits — with `accTitle`/`accDescr`, `classDef` only, no `%%{init}`. Place it inline with the prose. Do not generate a PNG; the markdown is the source of truth and a raster figure can be produced later by figure-table-design.

Expected output: a methods-section markdown block in `paper/draft/` containing one accessible Mermaid flowchart whose stages match the run ledger, plus a one-line note in `paper/logs/decision_log.md` if the type choice was non-obvious.

## Scenario 2: Clarify a reviewer-revision flow in the response letter

> In `paper/reviews/response_to_reviewers.md` I need to show how we re-ran the ablation after the reviewer's comment 2.3 and how it feeds the new ablation table. Draft a short Mermaid sequence (reviewer comment → rerun → new statistics → updated `paper/experiments/ablation.md` → response) inline in the response-to-reviewers markdown. Keep it minimal, one emoji per node max, snake_case IDs.

Expected output: a compact Mermaid sequence diagram embedded in `paper/reviews/response_to_reviewers.md`, inline next to the response paragraph for comment 2.3, with `accTitle`/`accDescr` and the change cross-referenced in `paper/logs/change_log.md`.

## Scenario 3: Concept map of the literature landscape

> Before we freeze the research question, build a mindmap of the field from `paper/refs/reading_matrix.md` — the three or four major themes, their seminal papers, and where our gap sits. Put it in `paper/logs/insights.md` as Mermaid so it diffs cleanly. Pick the type from `references/diagrams/` that actually fits a concept hierarchy.

Expected output: a Mermaid mindmap in `paper/logs/insights.md` whose top branches are the themes from the reading matrix, with a descriptive italic note if the chosen type lacks `accTitle`/`accDescr`, and any surfaced gap recorded in `paper/logs/open_questions.md`.
