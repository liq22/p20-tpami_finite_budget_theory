# generate-image / scripts

`generate_image.py` — thin client over the OpenRouter chat-completions endpoint that
generates or edits a single conceptual/illustrative image and writes it to disk as a PNG.

## Purpose
Provide the runnable backing for the `generate-image` skill. It calls an OpenRouter
image-capable model (default `google/gemini-3.1-flash-image-preview`, also
`black-forest-labs/flux.2-pro` / `flux.2-flex`) and decodes the returned base64 data URL
into a PNG/JPEG file in the workspace.

## Inputs
- `prompt` (positional, required) — text description or edit instruction.
- `--model / -m` — OpenRouter model id (default above).
- `--output / -o` — destination path (default `generated_image.png`). For paper outreach
  assets write under `paper/assets/figures/` or a non-evidence outreach folder.
- `--input / -i` — source image path to edit (PNG/JPEG/GIF/WebP). Enables edit mode.
- `--api-key` — OpenRouter key. **Must be provided by the user**; if omitted the script
  reads `OPENROUTER_API_KEY` from a `.env` in cwd or any parent dir.

## Outputs / Writes
- One image file at the `--output` path. Nothing else is written.

## Network
- Calls `https://openrouter.ai/api/v1/chat/completions` over HTTPS. Requires outbound
  network and a valid user-provided `OPENROUTER_API_KEY`. No other network calls.

## Credential handling
- Never hardcode or echo a key. Treat any key string encountered as `<user-provided-key>`.
- Do not commit `.env`. The repo's `.gitignore` should already exclude it.

## Scope (IMPORTANT)
This skill is for **conceptual / illustrative / outreach visuals ONLY** — hero images,
title-slide art, poster backdrops, presentation imagery. Do **not** use it for data
figures, quantitative plots, exact-geometry model diagrams, or any paper evidence figure.
Route paper figures via `scientific-visualization` -> `matplotlib` / `seaborn`; route
technical/structural diagrams via `scientific-schematics`.
