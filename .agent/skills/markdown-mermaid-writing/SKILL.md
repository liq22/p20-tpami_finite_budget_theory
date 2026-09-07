---
name: markdown-mermaid-writing
description: Write scientific documents as markdown with embedded Mermaid diagrams (workflow, sequence, timeline, schema, relationship). Do not use for scatter plots of real data, raster figures, or polished images — those belong to scientific-visualization / matplotlib / figure-table-design.
---

# Markdown and Mermaid Writing

## Purpose

Make markdown with embedded Mermaid diagrams the default and canonical documentation format for the single-paper workflow. The bet: a relationship expressed as a Mermaid diagram inside a `.md` file is more valuable than any image — it is text, so it diffs cleanly in git, requires no build step, renders natively on GitHub/GitLab/VS Code, uses fewer tokens than a prose description of the same relationship, and can always be converted to a polished image later while the text remains the source of truth. This skill defines the documentation layer that wraps every other skill's output: when any skill produces an artifact that describes flow, structure, or relationships, it should land here as markdown + Mermaid.

This is a core capability skill. Its standards apply wherever a paper artifact is committed: `paper/draft/` (pre-freeze markdown), `paper/tex/` (post-freeze, where Mermaid is rendered to an image asset and the `.md` source stays committed), `paper/experiments/`, `paper/logs/`, `paper/reviews/`, and `paper/submission/`.

## Use When

- Creating any paper artifact that is structural or relational: experimental workflow, decision logic, data pipeline, service interactions, state machine, project timeline.
- A skill asks you to "add a diagram", "visualize the relationship", or "show the flow" — Mermaid in markdown first, always, before any raster image.
- Drafting `paper/draft/` sections, methods explanations, or `paper/logs/decision_log.md` entries that benefit from a structural figure.
- Producing `paper/reviews/response_to_reviewers.md` with a workflow that clarifies a revision.
- Writing any document committed to the repo (READMEs, ADRs in `paper/logs/`, status reports, templates) that will be version-controlled.
- Another skill needs a brief that a downstream figure tool (scientific-visualization, matplotlib) will later render to PNG.

Do NOT start with matplotlib, seaborn, or AI image generation for structural or relational diagrams. Those are Phase 2 / Phase 3 — used only when Mermaid cannot express what is needed (e.g., scatter plots of real data, photorealistic images).

## Required Inputs

- A clear relationship or structure to express: a workflow, a sequence, a hierarchy, a timeline, a schema, a state machine, or proportions.
- A destination artifact under `paper/` (e.g., a draft section, a methods note, a decision log entry) so the diagram is placed inline with related text — not in a separate "Figures" section.
- The paper's target style context from `paper/refs/target_journal.md` (citation style, figure conventions) so diagrams and captions stay consistent with the manuscript.

**Optional downstream conversion** (rendering a Mermaid source to a publication PNG via an external renderer) is *not* required: the user must provide any renderer API key out of band; never hardcode or store a key, token, or credential in this skill, its scripts, or any workspace file. Treat any encountered key string as `<user-provided-key>` and never echo it.

## Workflow

1. **Identify the document type.** Before writing from scratch, check `templates/` (`research_paper.md`, `decision_record.md`, `status_report.md`, `project_documentation.md`, `how_to_guide.md`, `issue.md`, `pull_request.md`, `kanban.md`, `presentation.md`). Map the paper artifact onto the closest template: a methods section → `research_paper.md`; an architecture decision in `paper/logs/decision_log.md` → `decision_record.md`; a revision-progress note in `paper/reviews/` → `status_report.md`.
2. **Read the markdown style guide.** Before writing any `.md` file, read `references/markdown_style_guide.md`. Internalize: one H1 per document; cite every external claim with a footnote `[^N]`; bold sparingly (max 2–3 per paragraph, never full sentences); tables over prose for comparisons and structured data; diagrams over walls of text for anything that describes flow, structure, or relationships; horizontal rule after every `</details>`.
3. **Pick the diagram type and read its guide.** Before any Mermaid block, read `references/mermaid_style_guide.md`, then open the specific type file under `references/diagrams/`. Match the type to the relationship, do not default to flowcharts: experimental workflow/decision logic → `flowchart.md`; service interactions/messaging → `sequence.md`; data model/schema → `er.md`; state machine/lifecycle → `state.md`; project timeline → `gantt.md`; proportions → `pie.md`; concept hierarchy → `mindmap.md`; chronological events → `timeline.md`; two-axis comparison/prioritization → `quadrant.md`; multi-dimensional comparison → `radar.md` (use `radar-beta`).
4. **Apply the mandatory diagram rules.** Every supported diagram gets `accTitle` (3–8 words) and `accDescr` (one or two sentences). No `%%{init}` directives (breaks GitHub dark mode). No inline `style` — use `classDef` only. One emoji per node max, at the start of the label. `snake_case` node IDs that match the label. For `radar-beta` (no accessibility support), place a descriptive italic paragraph above the code block.
5. **Write the document.** Start from the template; apply the markdown style guide; place diagrams inline with related text. Map outputs onto the workspace: methods/structural figures drafted in `paper/draft/`; experiment pipelines recorded in `paper/experiments/run_ledger.md` and `reproducibility.md`; decisions into `paper/logs/decision_log.md`; insights into `paper/logs/insights.md`.
6. **Commit as text.** The `.md` file with embedded Mermaid is what gets committed as the source of truth. If a publication PNG is later produced for `paper/assets/figures/` or `paper/tex/`, it is supplementary — the markdown stays committed so the relationship remains diffable and parseable.

## Output Contract

- A markdown artifact with embedded, accessible, `classDef`-styled Mermaid diagrams placed inline with the related prose — committed under the appropriate `paper/` location (`paper/draft/` pre-freeze, `paper/logs/`, `paper/experiments/`, `paper/reviews/`).
- Every diagram carries `accTitle` + `accDescr` (or, for unsupported types like `radar-beta`, a descriptive italic paragraph directly above the code block).
- No `%%{init}` directives and no inline `style` anywhere in committed Mermaid.
- Every external claim cited with a `[^N]` footnote carrying a full URL.
- One H1 per document; emoji on H2 headings only; horizontal rules after every `</details>`.
- When a diagram feeds a post-freeze `paper/tex/` figure, the rendered PNG lands in `paper/assets/figures/` and the change is recorded in `paper/logs/change_log.md`, while the Mermaid source stays committed as the source of truth.
- A note in `paper/logs/decision_log.md` when a diagram type choice is non-obvious (e.g., choosing a sequence over a flowchart for a messaging protocol).

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only markdown-mermaid-writing`
- `python src/S03_Scripts/validate_project.py`
- Every committed Mermaid block carries `accTitle` + `accDescr` (or a descriptive italic paragraph for unsupported types); no block uses `%%{init}` or inline `style`.
- Every `[^N]` footnote in any committed `paper/` markdown resolves to a full URL or a `references.bib` key.
- Diagram type matches the relationship being expressed (no flowchart-as-default-for-everything); spot-check against the type-selection table in `references/mermaid_style_guide.md`.

## Boundaries

- Do not produce raster figures, scatter plots of real data, or photorealistic images — hand those to scientific-visualization / matplotlib / figure-table-design; this skill owns text-based structural diagrams only.
- Do not invent scientific content; diagrams express relationships already established by other skills (claim-evidence, experiment-ops, scientific-writing) — never fabricate a workflow that the underlying evidence does not support.
- Do not draft the manuscript's full flowing prose — this skill produces structural diagrams and the markdown that frames them; prose IMRAD expansion belongs to scientific-writing.
- Do not use `%%{init}` directives or inline `style` in any committed Mermaid — they break GitHub dark mode and theme neutrality.
- Do not hardcode, echo, or persist any API key, token, or credential; any renderer key is user-provided out of band and never written to the workspace.
- Do not overwrite a frozen `paper/tex/` figure without recording the change in `paper/logs/change_log.md` and keeping the Mermaid source committed.

## Stop With

- No clear relationship or structure to express — a diagram without a purpose is noise; ask what the reader needs to understand first.
- The relationship is genuinely quantitative (real data points, distributions, regressions) — that is a chart for scientific-visualization / matplotlib, not a Mermaid diagram.
- The target venue explicitly forbids embedded diagrams in supplementary markdown, or requires a figure format Mermaid cannot render to — stop and route to figure-table-design.
- A diagram type cannot express the needed relationship after consulting `references/diagrams/` — escalate to a raster figure via scientific-visualization and record the decision in `paper/logs/decision_log.md`.
- Asked to overwrite a frozen `paper/tex/` figure or already-submitted artifact without explicit confirmation.

## References

- Markdown style guide: `references/markdown_style_guide.md`
- Mermaid style guide and type-selection table: `references/mermaid_style_guide.md`
- Diagram type guides (24 types): `references/diagrams/` (`flowchart.md`, `sequence.md`, `er.md`, `state.md`, `gantt.md`, `pie.md`, `c4.md`, `mindmap.md`, `timeline.md`, `class.md`, `user_journey.md`, `quadrant.md`, `requirement.md`, `sankey.md`, `xy_chart.md`, `block.md`, `kanban.md`, `architecture.md`, `radar.md`, `treemap.md`, `packet.md`, `git_graph.md`, `zenuml.md`, `complex_examples.md`)
- Document templates (9 types): `templates/` (`research_paper.md`, `decision_record.md`, `status_report.md`, `project_documentation.md`, `how_to_guide.md`, `issue.md`, `pull_request.md`, `kanban.md`, `presentation.md`)
- Worked example: `assets/examples/example-research-report.md`
- Invocation scenarios: `examples/prompts.md`
- Workspace artifacts: `paper/draft/`, `paper/tex/`, `paper/assets/figures/`, `paper/experiments/run_ledger.md`, `paper/experiments/reproducibility.md`, `paper/reviews/response_to_reviewers.md`, `paper/logs/decision_log.md`, `paper/logs/change_log.md`, `paper/logs/insights.md`, `paper/refs/target_journal.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see NOTICE.md and `.agent/references/scientific_agent_skills_source.md`.
