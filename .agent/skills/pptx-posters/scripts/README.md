# pptx-posters / scripts

Two-part AI schematic generator used to produce the poster visuals (hero, intro,
methods flowchart, results chart, conclusions cards) that the `pptx-posters` skill
assembles into an HTML poster for later PDF/PPTX export.

## Purpose
Provide the runnable backing for the `pptx-posters` skill's visual-element stage. The
scripts describe a scientific diagram in natural language, render it through an
OpenRouter image-capable model, and optionally AI-review quality before writing a PNG.
They exist here because poster visuals are deliberately large, simple, and AI-generated
(60-70% of the poster area), not data figures.

## Files
- `generate_schematic.py` — thin CLI wrapper. Validates inputs, locates the AI runner,
  enforces max 2 refinement iterations, and passes the API key via the environment (never
  on the command line) to avoid exposure in process listings.
- `generate_schematic_ai.py` — the actual generator. Calls
  `https://openrouter.ai/api/v1` (chat-completions, image-capable model) and decodes the
  returned image into a PNG; runs an optional AI quality-review step.

## Inputs
- `prompt` (positional, required) — natural-language description of the desired diagram.
- `-o / --output` (required) — destination PNG path. For poster visuals write under
  `paper/assets/figures/` with an `outreach_` / `poster_` prefix to mark the asset as
  illustrative, non-evidence.
- `--doc-type` — quality-threshold context; use `poster` for this skill. Other values:
  `journal`, `conference`, `thesis`, `grant`, `preprint`, `report`, `presentation`,
  `default`.
- `--iterations` — max refinement iterations (hard-capped at 2).
- `--api-key` — OpenRouter key. **Must be provided by the user**; if omitted the script
  reads `OPENROUTER_API_KEY` from the environment or a `.env` in cwd / script dir.
- `-v / --verbose` — verbose output.

## Outputs / Writes
- One PNG image at the `--output` path. Nothing else is written.

## Network
- Calls `https://openrouter.ai/api/v1/chat/completions` over HTTPS (image generation
  and, optionally, an AI quality review). Requires outbound network and a valid
  user-provided `OPENROUTER_API_KEY`. No other network calls.

## Credential handling
- Never hardcode, echo, or log a key. The wrapper passes the key via the process
  environment only; the AI runner reads it from `OPENROUTER_API_KEY`.
- Treat any key string encountered as `<user-provided-key>`. Do not commit `.env`.

## Scope (IMPORTANT)
These scripts produce **illustrative poster visuals ONLY** — hero banners, simplified
flowcharts, icon rows, summary cards, conceptual artwork. They must NOT be used for data
figures, quantitative plots, exact-geometry model diagrams, or any paper evidence figure.
Poster prompts must enforce strict simplicity (3-4 elements, <=10 words, 50%+ white space,
giant fonts 80pt+). Route paper data figures via `scientific-visualization`
(matplotlib/seaborn) and technical/structural diagrams via `scientific-schematics`.
