# peer-review/scripts — local notes

This directory holds optional helper scripts copied from the upstream
`peer-review` skill. The peer-review skill does **not** require any script to
produce a review — the bundled `references/*.md` rubrics and the workspace
`paper/` artifacts are sufficient. Scripts here are convenience tooling only.

## generate_schematic.py

- **Purpose:** Generate a publication-quality scientific diagram (e.g. a CONSORT
  participant-flow diagram, an evaluation-criteria decision tree) from a natural
  language description. Useful for illustrating the review workflow itself or
  the methodology-assessment framework in `paper/reviews/ai_review.md`.
- **Inputs:** a quoted description string and `-o <output.png>`; optional
  `--doc-type {journal,presentation,poster}` sets the quality threshold.
- **Outputs:** a PNG image written to the path given by `-o` (default writes
  into a local `figures/` directory). Nothing is written into `paper/` unless
  the caller passes an explicit `paper/assets/figures/...` path.
- **Network:** Yes — it shells out to an external image-generation service
  (Nano Banana / Gemini family). Runs offline only if a cached image exists.
- **Writes:** only the output image path. No workspace files are mutated.
- **Key handling:** this lightweight script does not read any API key directly.
  The sibling `generate_schematic_ai.py` from upstream required
  `OPENROUTER_API_KEY`; that script was **deliberately not copied** because it
  is a schematic-generation tool tied to the `scientific-schematics` skill, not
  review-core, and it performs authenticated network calls. If LLM-assisted
  schematic generation is needed, use the `scientific-schematics` skill and
  provide any key out of band — never hardcode or store it.

Source: K-Dense-AI/scientific-agent-skills v2.53.0 (MIT). Adapted (comments
only); see NOTICE.md.
