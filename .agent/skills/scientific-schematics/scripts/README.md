# scripts — scientific-schematics

Local-purpose notes for the upstream-bundled scripts in this directory. These scripts are
copied verbatim from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see the skill's
`## References` provenance line. They are provided as reference tooling for generating
scientific schematic images; they are not executed by the skill's workflow by default.

## generate_schematic.py

- Purpose: Thin CLI wrapper that drives `generate_schematic_ai.py` to render a scientific
  diagram from a natural-language description, with smart iterative refinement against a
  per-document-type quality threshold.
- Inputs: a free-text diagram description (CLI positional arg), `-o` output image path,
  `--doc-type` (journal/conference/thesis/grant/preprint/report/poster/presentation),
  `--iterations` (1–2), optional `--api-key`, optional `-v` verbose.
- Network: YES. Calls the OpenRouter API (image generation + quality review). Requires
  `OPENROUTER_API_KEY`, which the user must provide out of band — never hardcode or store.
- Writes: the output image path passed via `-o`; intermediate `*_vN.png` iteration images
  next to it; a JSON review log (`*_review.json`) alongside the image. In the single-paper
  workflow, output must land under `paper/assets/figures/` and be bound to an evidence row.

## generate_schematic_ai.py

- Purpose: Core generator. Builds the generation/review prompt, posts to OpenRouter,
  scores the result, and loops until the quality threshold is met or max iterations is
  reached.
- Inputs: same flags as `generate_schematic.py` plus the `ScientificSchematicGenerator`
  Python API (`generate_iterative(...)`).
- Network: YES. Posts to `https://openrouter.ai/api/v1` (image + review models). Requires
  `OPENROUTER_API_KEY` (user-provided out of band).
- Writes: image files and a JSON review log as above.

## example_usage.sh

- Purpose: illustrative shell invocations of the CLI (CONSORT flowchart, Transformer
  architecture, MAPK pathway, IoT system diagram). Reference only.

## Credentials and safety

- These scripts read `OPENROUTER_API_KEY` from the environment or a local `.env`. Any API
  key is user-provided; never commit a `.env` or hardcode a key. Treat any encountered key
  string as `<user-provided-key>` and never echo it.
- Per the asset denylist, no `.env`, `.key`, `.pem`, or model-weight files are copied into
  this skill. If a real key is found anywhere under this directory, remove it and replace
  it with `<user-provided-key>`.
