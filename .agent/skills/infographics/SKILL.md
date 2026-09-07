---
name: infographics
description: Generate communication-grade infographics (timelines, comparisons, process lists, statistical callouts) via OpenRouter image models with AI quality review against a document-type threshold. Requires a user-provided OPENROUTER_API_KEY and network. Do not use for data plots, exact-geometry schematics, or paper evidence figures.
---

# Infographics

## Purpose

Produce polished, visually compelling **communication** infographics for a
single-paper project: outreach graphics, slide tiles, poster banners, social
media assets, and explanatory visual summaries of concepts already established
in the manuscript. The skill renders a natural-language content brief into an
infographic through an OpenRouter image model (e.g. Nano Banana Pro / Gemini 3
Pro Image), then has a review model score each generation against a
document-type threshold (marketing 8.5, report 8.0, presentation 7.5, social
7.0, draft 6.5) and iterates only while quality is below threshold. Output is
decorative or explanatory communication — never experiment evidence.

**Critical principle:** an infographic from this skill is a communication asset,
not a numbered evidence figure. Every emitted file lands in
`paper/assets/figures/` under an `infographic_` / `outreach_` / `slides_`
prefix, is named to match its first callout (or use), and is recorded in
`paper/logs/decision_log.md` as illustrative, non-evidence. Quantitative
figures bound to a claim/evidence row belong to `scientific-visualization` or
`scientific-schematics`.

## Use When

- Summarising already-written paper content into a visual for a talk, group
  meeting, poster, or social-media outreach post (e.g. "5 contributions of the
  paper", "method at a glance").
- Producing a timeline of project milestones, paper timeline, or field history
  for a presentation (`--type timeline`).
- Building a side-by-side comparison graphic for outreach (option A vs option B,
  before/after, our-method vs baseline) that uses **concepts**, not experiment
  numbers (`--type comparison`).
- Communicating a process or workflow as a numbered-step graphic
  (`--type process`).
- Rendering statistical **callouts** sourced from the manuscript's own reported
  headline numbers (not raw experiment data) for a press kit or title slide
  (`--type statistical`, optional `--research` for cited external context).

Do **not** use this skill for: data-driven plots (line/bar/scatter/box/heatmap
from experiment numbers — use `scientific-visualization`), exact-geometry model
diagrams, methodology flowcharts, neural-network architecture diagrams,
biological pathways, circuits, or CONSORT/PRISMA diagrams (use
`scientific-schematics`), any figure that must serve as numbered paper evidence
bound to a claim/evidence row, or generating arbitrary non-infographic imagery
(use `generate-image`).

## Required Inputs

- A precise content brief: subject, the specific points/items/timeline events
  to show, intended audience, and the infographic type (`--type`), style
  (`--style`), and palette (`--palette`) if relevant. Vague prompts
  ("an infographic about my paper") are rejected up front.
- An output destination under `paper/assets/figures/` using an `infographic_` /
  `outreach_` / `slides_` prefix to mark it as illustrative, non-evidence.
- `paper/refs/target_journal.md` — only to confirm the journal will NOT classify
  the graphic as a numbered figure; if it would, stop and switch skills.
- `paper/logs/decision_log.md` — to record model, brief intent, threshold used,
  final quality score, and that the asset is illustrative-only.
- `paper/checklists/` — figure-provenance confirmation that the asset is
  illustrative and not derived from experimental data.

**External credentials:** running the bundled script requires an OpenRouter API
key. `OPENROUTER_API_KEY` must be provided by the user out of band (environment
variable or a `.env` the user owns); **never hardcode, echo, log, or store a
key, token, or credential** in this skill, its scripts, or any workspace file.
Treat any encountered key string as `<user-provided-key>`. Network access to
`https://openrouter.ai` is required (and, with `--research`, to Perplexity
Sonar Pro via OpenRouter).

## Workflow

1. **Confirm scope.** Verify the request is a communication/outreach infographic,
   not a data figure or a diagram bound to evidence. If it touches experiment
   numbers or a claim/evidence row, stop and route to `scientific-visualization`
   or `scientific-schematics`. Consult `paper/refs/target_journal.md` to ensure
   the journal will not classify the result as a numbered figure.
2. **Compose the brief.** State the subject, the explicit items/events/points,
   the audience, and the visual style. Be specific about content (concrete
   items, not "things") and prefer the document type that matches the use
   (`marketing` for outreach, `presentation` for slides, `draft` for working).
   Record the brief in `paper/logs/decision_log.md`.
3. **Choose type, style, palette.** Pick `--type` (statistical, timeline,
   process, comparison, list, geographic, hierarchical, anatomical, resume,
   social), `--style` (corporate, healthcare, technology, nature, education,
   marketing, finance, nonprofit), and `--palette` (wong / ibm / tol for
   colorblind-safe output). See `references/infographic_types.md`,
   `references/design_principles.md`, `references/color_palettes.md`.
4. **Generate and review.** Run
   `python .agent/skills/infographics/scripts/generate_infographic_ai.py`
   with the brief, output path, type/style/palette, document type, and max
   iterations. The model generates the image, a review model scores it against
   the document-type threshold, and the script regenerates only while below
   threshold (early-stop on success). Optionally pass `--research` to pull cited
   external context via Perplexity Sonar Pro — but for paper-sourced numbers,
   cite the manuscript instead.
5. **Place and name.** Write the final PNG to `paper/assets/figures/` with the
   chosen prefix. Keep the sibling `*_review.json` (quality scores, critiques,
   early-stop reason) under `paper/assets/figures/` or `paper/logs/` for
   provenance.
6. **Record provenance.** Append to `paper/logs/decision_log.md`: model, brief,
   type/style/palette, document type, threshold, final score, early-stop flag,
   output path, and an explicit "illustrative, non-evidence" tag. If the asset
   is meant for a talk/poster, note that in `paper/checklists/` figure
   provenance. Log surprises in `paper/logs/insights.md` and dead-ends in
   `paper/logs/dead_ends.md`.

## Output Contract

- One final PNG under `paper/assets/figures/` named with an `infographic_` /
  `outreach_` / `slides_` prefix and a slug matching its first callout/use.
- A `*_review.json` capturing iterations, scores per criterion (visual
  hierarchy, typography, data viz, color/accessibility, overall impact), the
  final score, and the early-stop reason.
- A `*_research.json` **only** when `--research` was used.
- A `paper/logs/decision_log.md` entry marking the asset illustrative and
  non-evidence, with model, threshold, and score.
- No claim/evidence binding. If a downstream stage needs this content as
  evidence, it must be regenerated through `scientific-visualization` or
  `scientific-schematics`.

## Validation

- Run `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only infographics`.
- Run `python src/S03_Scripts/validate_project.py`.
- Confirm the emitted PNG exists, opens, and is named with the required prefix.
- Confirm `*_review.json` reports `final_score >= quality_threshold` (else it
  should have hit `max_iterations` and that must be logged).
- Confirm no secret pattern appears in any output (re-scan with the validator).
- Confirm `paper/logs/decision_log.md` carries the illustrative, non-evidence
  tag and the chosen model/score.

## Boundaries

- **External/network tier.** This skill calls OpenRouter image and text models
  over HTTPS, and (with `--research`) Perplexity Sonar Pro via OpenRouter. It
  therefore **requires network access and a user-provided `OPENROUTER_API_KEY`**.
  The user must supply the credential out of band (env var or a `.env` the user
  owns); **never invent, hardcode, echo, log, or store** a key, token, or
  credential anywhere in this skill, its scripts, outputs, or workspace files.
  Treat any encountered key string as `<user-provided-key>` and scrub it.
- **No evidence.** Infographics from this skill are communication assets. They
  must not be used as numbered paper figures or bound to a claim/evidence row in
  `paper/experiments/evidence_matrix.md`; route those to
  `scientific-visualization` or `scientific-schematics`.
- **No fabricated facts.** Do not invent statistics, percentages, or citations.
  For paper-sourced numbers, cite the manuscript; with `--research`, the cited
  facts come from Perplexity Sonar Pro and must be checked before outreach use.
- **Out-of-scope visuals.** Do not produce data plots, exact-geometry diagrams,
  methodology/architecture/pathway/circuit schematics, or arbitrary non-
  infographic imagery (use the appropriate sibling skill).
- **Cost and iteration cap.** Honour `--iterations`; do not loop unbounded. Stop
  when the threshold is met or the cap is reached.

## Stop With

- A final PNG and `*_review.json` whose `final_score` meets the document-type
  threshold (early-stop), or the iteration cap is reached and that is logged.
- The asset placed under `paper/assets/figures/` with the required prefix and a
  `paper/logs/decision_log.md` entry tagged illustrative, non-evidence.
- A clean validator run (no errors) for both
  `validate_agent_skills.py --strict --only infographics` and
  `validate_project.py`.
- If the request was actually a data figure, schematic, or evidence asset, stop
  immediately and route to the correct skill instead of generating here.

## References

- Bundled: `references/infographic_types.md` (extended templates for all types),
  `references/design_principles.md` (hierarchy, layout, typography),
  `references/color_palettes.md` (full palette specs incl. colorblind-safe),
  `scripts/generate_infographic_ai.py` and `scripts/generate_infographic.py`
  with `scripts/README.md` (purpose/inputs/outputs/network/writes).
- Workspace: `paper/assets/figures/` (output), `paper/refs/target_journal.md`
  (figure-classification check), `paper/logs/decision_log.md`,
  `paper/logs/insights.md`, `paper/logs/dead_ends.md`, `paper/checklists/`
  (figure provenance), `paper/experiments/evidence_matrix.md` (the skill does
  NOT write here — routing target only).
- Provenance: Ported (adapted) from `K-Dense-AI/scientific-agent-skills`
  v2.53.0 (MIT); see `NOTICE.md` and
  `.agent/references/scientific_agent_skills_source.md`.
