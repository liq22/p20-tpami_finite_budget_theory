# xlsx scripts

Local copies of helper scripts for the `xlsx` skill. Only the xlsx-relevant
subset of the upstream `scientific-agent-skills/xlsx/scripts/` tree is shipped
here; the upstream `office/` validators (docx/pptx/redlining) and the large
`.xsd` OOXML schema bundle were intentionally NOT copied (out of scope for a
single-paper research workspace, and the schemas are ~1 MB of files not needed
at runtime).

## recalc.py

- **Purpose:** Recalculate every formula in an `.xlsx` workbook using
  LibreOffice, then scan all cells for Excel errors (`#REF!`, `#DIV/0!`,
  `#VALUE!`, `#NAME?`, `#N/A`) and emit a JSON error report. openpyxl writes
  formulas as strings without cached values, so this is mandatory whenever a
  deliverable workbook contains formulas.
- **Inputs:** one `.xlsx` file path and an optional timeout in seconds.
- **Outputs:** recalculated workbook written back in place (same path); a JSON
  blob on stdout with `status`, `total_errors`, `total_formulas`, and an
  `error_summary` mapping each error code to its locations.
- **Network:** none. Fully offline.
- **Writes:** the input `.xlsx` file (in place), and on first run a LibreOffice
  macro file under `~/.config/libreoffice/4/user/basic/Standard/Module1.xba`
  (Linux) or `~/Library/Application Support/LibreOffice/4/user/basic/Standard/`
  (macOS). If Unix domain sockets are restricted, it may compile a one-time gcc
  shim into `~/.cache/xlsx-skill/lo-shim/`.
- **System deps:** `soffice` (LibreOffice 7.x+) on PATH; `gcc` only when Unix
  sockets are blocked; optional `gtimeout` on macOS for the timeout flag.
- **Python deps:** `openpyxl` (and `pandas` for analysis workflows). Install
  with `uv pip install openpyxl pandas` (optionally `python-calamine` for faster
  reads, `defusedxml` to harden against XML expansion on untrusted files).

Usage:

```bash
python .agent/skills/xlsx/scripts/recalc.py <excel_file> [timeout_seconds]
```

## office/soffice.py

- **Purpose:** Internal helper imported by `recalc.py`. Configures the
  LibreOffice (`soffice`) headless environment — including the sandboxed-socket
  gcc shim — and returns the environment dict used to launch `soffice`.
- **Inputs:** none (called as a module).
- **Outputs:** none directly; exposes `get_soffice_env()`.
- **Network:** none.
- **Writes:** may write the gcc shim to `~/.cache/xlsx-skill/lo-shim/` on first
  run in a restricted environment.

Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
(MIT); see NOTICE.md and
`.agent/references/scientific_agent_skills_source.md`.
