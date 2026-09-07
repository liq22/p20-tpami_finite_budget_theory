# scripts/ — local note on schematic generators

The upstream `scientific-agent-skills` skill ships two figure-generation scripts:

- `generate_schematic.py` — wraps the Nano Banana 2 / Gemini image model to produce a
  schematic from a natural-language description.
- `generate_schematic_ai.py` — heavier LLM-driven variant with iterative review.

These were **intentionally NOT copied** into this port. Both depend on external
image-LLM APIs (Google Gemini / Nano Banana), require `GOOGLE_API_KEY` /
`GEMINI_API_KEY` out of band, write binary PNG/JPEG outputs, and are not lightweight
enough for the single-paper workflow's offline-first contract. Keeping them would also
violate the "scripts/ only if lightweight" copy rule.

| aspect        | value                                                          |
|---------------|----------------------------------------------------------------|
| purpose       | generate publication-quality schematics from a text prompt     |
| inputs        | natural-language diagram description; `--doc-type` flag        |
| outputs       | PNG/JPEG image written under `paper/assets/figures/`           |
| network       | YES — calls Google Gemini / Nano Banana image API              |
| writes        | `paper/assets/figures/*.png`, local temp files                 |
| secrets       | requires `GOOGLE_API_KEY` / `GEMINI_API_KEY` (user-provided)   |

If a schematic is actually needed in this repo, generate it out of band with the
upstream tool and commit only the resulting figure under
`paper/assets/figures/` — do not run the API-calling script from inside the skill.

For figure *design* (what to draw, callouts, layout) without rendering, use the
`15-figure-table-design` stage skill and `scientific-visualization` instead; those are
offline and produce SVG/Python specs rather than rendered raster images.
