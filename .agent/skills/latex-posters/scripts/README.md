# latex-posters/scripts

## Bundled (local, no network)

### `review_poster.sh`

Local PDF quality-check helper for a compiled poster PDF.

- **Purpose**: prints page size (via `pdfinfo`), embedded-font status (via
  `pdffonts`), page count, and file size, plus a reminder of the manual checks
  (100%-zoom edge inspection, reduced-scale print test, contrast, proofreading).
- **Inputs**: a single poster PDF path, e.g.
  `bash review_poster.sh paper/submission/poster/poster.pdf`.
- **Outputs**: stdout report only; writes nothing to disk.
- **Network**: none. Uses only local Poppler tools (`pdfinfo`, `pdffonts`) and
  coreutils. The user must install Poppler if not present.
- **Writes to**: nothing (read-only diagnostic).

## Not bundled (external, opt-in)

The upstream skill ships two AI schematic generators — `generate_schematic.py`
and `generate_schematic_ai.py` — that call external image and LLM APIs (Nano
Banana 2 / OpenRouter / Gemini) to produce poster figures. They are **not
copied** into this repo because:

- They require network access and a **user-provided** API key
  (e.g. `OPENROUTER_API_KEY`) at call time. Never hardcode or store the key.
- The recommended path for this repo is to reuse already-validated figures from
  `paper/assets/figures/` rather than generating new ones.

If the user explicitly opts into AI schematic generation:

1. The user obtains the scripts from upstream
   `K-Dense-AI/scientific-agent-skills` (see
   `.agent/references/scientific_agent_skills_source.md` for the pinned ref).
2. The user provides the required API credential in their environment; this
   skill reads it at call time only and never persists it.
3. Any generated figure is written under `paper/submission/poster/figures/`,
   then must pass the same overflow/readability QA as any other poster figure.

No secret material belongs in this directory.
