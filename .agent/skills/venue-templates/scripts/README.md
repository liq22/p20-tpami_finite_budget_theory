# venue-templates — helper scripts

These three scripts are local, dependency-light Python helpers ported from the upstream
K-Dense-AI/scientific-agent-skills (MIT) venue-templates skill. They operate entirely on
the bundled `assets/` and `references/` of this skill — no network access, no API calls,
no credentials.

## query_template.py

- Purpose: search and retrieve venue-specific LaTeX templates by venue name, document
  type, or keyword, and print a venue's formatting requirements.
- Inputs: CLI flags (`--venue`, `--type`, `--keyword`, `--list-all`, `--requirements`).
- Outputs: stdout listing of matching template files under `../assets/journals/`,
  `../assets/grants/`, `../assets/posters/` and requirement summaries.
- Network: none.
- Writes: none (read-only).

## customize_template.py

- Purpose: copy a bundled template and substitute placeholder fields (title, authors,
  affiliations, email) with values from CLI flags or interactive prompts.
- Inputs: `--template` (path to a bundled `.tex`), `--title/--authors/--affiliations/--email`,
  `--output`, or `--interactive`.
- Outputs: a customized `.tex` at the `--output` path.
- Network: none.
- Writes: only the file given via `--output`.

## validate_format.py

- Purpose: check a compiled PDF or `.tex` against a venue's formatting requirements
  (page count, margins, fonts, citation style presence).
- Inputs: `--file` (PDF/TeX), `--venue`, `--check` / `--check-all`, optional `--report`.
- Outputs: stdout compliance report, optional report file via `--report`.
- Network: none.
- Writes: only the report file when `--report` is given.

## Deliberately NOT ported

`generate_schematic.py` and `generate_schematic_ai.py` from upstream are intentionally
excluded: they perform AI image generation over the network (OpenRouter) and belong to the
visualization / figure-design skill family, not venue formatting. If schematic generation
is needed, use the figure/table-design or scientific-visualization skills instead.
