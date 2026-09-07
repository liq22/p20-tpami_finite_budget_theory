---
name: generate-image
description: Generate or edit conceptual, illustrative, and outreach imagery (hero art, poster backdrops, slide visuals) via OpenRouter image models (FLUX.2, Gemini Flash Image). Requires a user-provided OPENROUTER_API_KEY and network. Do not use for data figures, quantitative plots, exact-geometry model diagrams, or paper evidence figures.
---

# Generate Image

## Purpose

Produce non-quantitative visual assets for a single-paper project: title-slide hero
images, poster banners, presentation imagery, and light edits of existing outreach
imagery. The skill renders a prompt (and optional source image) through an OpenRouter
image-capable model and writes one PNG to the workspace. It is the **illustrative**
visual channel — everything it emits is decoration, communication, or outreach, never
evidence. Output that must be bound to a claim lives in `paper/experiments/evidence_matrix.md`,
and that binding is produced by `scientific-visualization` or `scientific-schematics`, not
here.

## Use When

- Building a hero / title-slide image for a talk or group meeting about the paper.
- Producing a poster backdrop or banner artwork (pre-freeze, illustrative).
- Creating conceptual or evocative artwork for outreach, a press kit, or a website.
- Light, non-structural edits to an existing outreach image (regrade, restyle) whose
  source contains **no data**.

Do **not** use this skill for: data figures or quantitative plots (line/bar/scatter/box/
heatmap from experiment numbers — use `scientific-visualization` with matplotlib/seaborn),
exact-geometry model diagrams, methodology flowcharts, neural-network architecture
diagrams, circuits, or pathways (use `scientific-schematics`), or any figure that must
serve as paper evidence bound to a claim/evidence row.

## Required Inputs

- A precise text prompt describing the desired illustrative image (or edit instruction).
  Vague prompts ("a cool image", "lab art") are rejected up front.
- An output destination under `paper/assets/figures/`. Use an `outreach_` / `poster_` /
  `slides_` prefix to mark the asset as illustrative, non-evidence.
- `paper/refs/target_journal.md` — only to confirm the journal does NOT classify the
  artwork as a numbered figure; if it would, stop and switch skills.
- `paper/logs/decision_log.md` — to record model, prompt intent, and that the asset is
  illustrative-only.
- `paper/checklists/` — figure-provenance confirmation that the asset is illustrative and
  not derived from experimental data.

**External credentials:** running the bundled script requires an OpenRouter API key.
`OPENROUTER_API_KEY` must be provided by the user out of band (environment variable or a
`.env` the user owns); **never hardcode, echo, log, or store a key, token, or credential**
in this skill, its scripts, or any workspace file. Treat any encountered key string as
`<user-provided-key>`. Network access to `https://openrouter.ai` is required.

## Workflow

1. **Confirm scope.** Verify the request is illustrative/outreach, not a data figure or a
   diagram bound to evidence. If it touches experiment numbers or a claim/evidence row,
   stop and route to `scientific-visualization` or `scientific-schematics`. Consult
   `paper/refs/target_journal.md` to ensure the journal will not classify the result as a
   numbered figure.
2. **Compose a precise prompt.** State subject, composition, mood, palette, style, and
   explicitly "no text, no labels" unless labels are wanted for outreach clarity. Avoid
   anything that implies exact geometry, real data, or specific individuals.
3. **Choose a model.** Default `google/gemini-3.1-flash-image-preview` (high quality,
   generation + editing). Use `black-forest-labs/flux.2-pro` for fast high-quality work,
   or `flux.2-flex` for low-cost generation-only.
4. **Generate or edit.** Run `scripts/generate_image.py` with the user-supplied key:
   ```bash
   python .agent/skills/generate-image/scripts/generate_image.py "<prompt>" \
     --model black-forest-labs/flux.2-pro \
     --output paper/assets/figures/outreach_title_hero.png
   ```
   For edits, pass `--input <existing non-data image>`.
5. **Land and label.** Save under `paper/assets/figures/` with an illustrative prefix.
   Confirm the file is illustrative-only and not bound to
   `paper/experiments/evidence_matrix.md`.
6. **Record.** Log the choice (model, purpose, illustrative-only status) in
   `paper/logs/decision_log.md` and note any model-output caveat in
   `paper/logs/open_questions.md` (e.g. an artifact that needs human review before public
   use).

## Output Contract

- Exactly one raster image (PNG by default) at the `--output` path under
  `paper/assets/figures/`, named with an illustrative prefix.
- No claim/evidence row is created or modified — this skill does not emit evidence.
- A decision-log entry in `paper/logs/decision_log.md` recording model, intent, and
  illustrative-only status; optionally a note in `paper/logs/insights.md` for reusable
  prompt patterns.
- The asset is excluded from the formal figure list (`paper/tex/`, `paper/submission/`)
  unless a human explicitly promotes it via another skill.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only generate-image`
- `python src/S03_Scripts/validate_project.py`
- Manual: confirm no `OPENROUTER_API_KEY` value appears in any committed file; confirm
  the output image is illustrative and not referenced as evidence in
  `paper/experiments/evidence_matrix.md`.

## Boundaries

- **Illustrative/outreach only.** Never produce data figures, quantitative plots,
  exact-geometry model diagrams, methodology/architecture/pathway/circuit diagrams, or any
  paper evidence figure. Route those to `scientific-visualization` (matplotlib/seaborn) or
  `scientific-schematics`.
- **External service.** Depends on network access to `https://openrouter.ai` and a
  user-provided `OPENROUTER_API_KEY`. The user must supply the credential; this skill must
  not invent, hardcode, or persist secrets.
- **No data edits.** Never pass a data figure as `--input`; editing data imagery here
  would corrupt evidence.
- **Single image per call.** Run multiple times for multiple assets; do not batch into a
  composite that could be mistaken for a numbered figure.
- **Provenance.** Generated imagery is AI-produced; flag this in outreach contexts where
  disclosure is expected and record it in the decision log.

## Stop With

- A request to generate a data figure, plot, or any diagram bound to evidence — re-route
  to `scientific-visualization` or `scientific-schematics`.
- No user-provided `OPENROUTER_API_KEY` and no network — ask the user to supply the
  credential; never fabricate or store one.
- A prompt that implies real experimental data, exact geometry, identifiable individuals,
  or content that would require disclosure the user has not approved.
- An output the journal would classify as a numbered figure — switch skills before freeze.

## References

- Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see NOTICE.md
  and `.agent/references/scientific_agent_skills_source.md`.
- Workspace: `paper/assets/figures/` (illustrative outputs), `paper/refs/target_journal.md`
  (scope check), `paper/experiments/evidence_matrix.md` (the binding this skill must NOT
  produce), `paper/logs/decision_log.md` and `paper/logs/open_questions.md` (records).
- Bundled runner: `scripts/generate_image.py` (see `scripts/README.md` for inputs/outputs/
  network/writes); worked scenarios in `examples/prompts.md`.
