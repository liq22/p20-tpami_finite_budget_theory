# liteparse — helper scripts

A single lightweight, local-only Python helper ported from the upstream
K-Dense-AI/scientific-agent-skills (MIT) `liteparse` skill. All scripts operate
entirely on local files and perform **no network access, no cloud API calls, and
no credential handling**. Heavy ML training/inference code is intentionally not
shipped — this skill is an implementation support tool only.

## Layout

```
scripts/
  batch_parse_dir.py   # batch-parse a directory of docs into text/json via LiteParse
```

## Per-script notes

### batch_parse_dir.py
- Purpose: parse every supported document in an input directory into a uniform
  `text` or `json` output directory, using the LiteParse Python API.
- Inputs: `INPUT_DIR`, `OUTPUT_DIR`, plus optional `--format json|text`,
  `--no-ocr`, `--recursive`, `--extension .pdf` (CLI args).
- Outputs: one parsed file per source document written under `OUTPUT_DIR`.
- Network: **none**. Local parsing only; LiteParse is fully local (bundled
  Tesseract OCR).
- Writes: only the declared `OUTPUT_DIR`. Source files are read-only and never
  modified.
- Requires: `liteparse==2.0.0` (`uv pip install "liteparse==2.0.0"`); optional
  LibreOffice for Office inputs and ImageMagick for image inputs.
