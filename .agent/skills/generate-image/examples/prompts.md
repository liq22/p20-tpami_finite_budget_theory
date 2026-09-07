# generate-image — example invocations

Realistic single-paper scenarios for conceptual, illustrative, and outreach visuals only.
These are NOT for data figures, quantitative plots, or paper evidence figures — route
those via `scientific-visualization` (matplotlib/seaborn).

## Scenario 1: Title-slide hero image for a group meeting talk

The draft's narrative concerns cellular heterogeneity in a tumor microenvironment, and
the author wants a non-quantitative, evocative hero image for a talk slide.

Inputs the user provides out of band:
- `OPENROUTER_API_KEY` exported in the shell or set in a `.env` (never committed).

Run:
```bash
python .agent/skills/generate-image/scripts/generate_image.py \
  "Abstract conceptual illustration of diverse cells within a tumor microenvironment, \
   glowing immunotherapy agents approaching, modern scientific art style, soft palette, \
   no text, no labels" \
  --model "black-forest-labs/flux.2-pro" \
  --output paper/assets/figures/outreach_title_hero.png
```

Notes:
- Output goes under `paper/assets/figures/` but with an `outreach_` prefix to signal it is
  a non-evidence, illustrative asset (not bound to `paper/experiments/evidence_matrix.md`).
- If a claim/evidence row would ever be needed, stop and switch to `scientific-schematics`
  or `scientific-visualization` — this skill does not produce evidence.

## Scenario 2: Poster hero backdrop for a conference poster

Before the LaTeX poster is frozen, the author wants a photorealistic lab backdrop to use
as the poster's hero banner.

```bash
python .agent/skills/generate-image/scripts/generate_image.py \
  "Photorealistic modern laboratory bench with pipettes, microplates, and a softly blurred \
   microscope in the background, warm even lighting, depth of field, no people, no text" \
  --model "google/gemini-3.1-flash-image-preview" \
  --output paper/assets/figures/poster_hero_backdrop.png
```

After generation:
- Record the choice (model, purpose, that it is illustrative-only) in
  `paper/logs/decision_log.md`.
- Confirm in `paper/checklists/` (figure-provenance) that this asset is illustrative and
  not derived from experimental data.

## Scenario 3: Light edit of an existing outreach image

The author has an outreach PNG whose color palette clashes with the slide template and
wants a regrade (not a redraw of any data — the source contains no data).

```bash
python .agent/skills/generate-image/scripts/generate_image.py \
  "Shift the overall color grade to a cool blue-teal palette, keep composition and \
   subjects unchanged, do not add or remove any text or labels" \
  --input paper/assets/figures/outreach_title_hero.png \
  --model "google/gemini-3.1-flash-image-preview" \
  --output paper/assets/figures/outreach_title_hero_v2.png
```

Notes:
- Only ever feed this skill non-data imagery as `--input`. Editing a data figure here
  would corrupt evidence — for data figures use `scientific-visualization` and regenerate
  from source numbers.
