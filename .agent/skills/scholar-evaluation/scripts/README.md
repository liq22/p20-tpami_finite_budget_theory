# scholar-evaluation / scripts

Conservative copy of the upstream scholar-evaluation scripts. Only the lightweight,
dependency-free helper is ported; the heavy AI image-generation scripts are
intentionally excluded (see "Not ported" below).

## calculate_scores.py

- **Purpose:** Compute aggregate ScholarEval scores from per-dimension 1–5 ratings.
  Supports default weights, a user-supplied `--weights` JSON, threshold/band
  analysis, and a plain-text score report. Used by the Workflow "Aggregate scores"
  step.
- **Inputs:** A JSON file of dimension scores via `--scores` (e.g.
  `paper/reviews/scholar_eval_scores.json`); optionally a `--weights` JSON; or run
  `--interactive` to enter scores on the terminal.
- **Outputs:** A plain-text report (default `--output report.txt`, or stdout) with
  weighted aggregate, quality band, and per-dimension breakdown. No file outside
  the path passed to `--output` is written.
- **Network:** None. Stdlib only (`json`, `argparse`, `sys`, `pathlib`,
  `typing`). Runs fully offline.
- **Writes:** Only the file path given to `--output`; nothing under `paper/`
  unless the caller points `--output` there.
- **Default weights:** `problem_formulation 0.15, literature_review 0.15,
  methodology 0.20, data_collection 0.10, analysis 0.15, results 0.10,
  writing 0.10, citations 0.05` (total 1.00).
- **Example:**
  ```bash
  python .agent/skills/scholar-evaluation/scripts/calculate_scores.py \
      --scores paper/reviews/scholar_eval_scores.json \
      --output paper/reviews/scholar_eval_report.txt
  ```

## Not ported (intentionally)

- `generate_schematic.py`, `generate_schematic_ai.py` — AI image-generation
  scripts that depend on external image-generation APIs (Nano Banana / Gemini) and
  a `OPENROUTER_API_KEY`-style pipeline. Schematic generation is owned by the
  separate `scientific-schematics` skill, so they are not carried here. This keeps
  the review/scoring skill dependency-free and offline-capable.

## Provenance

Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see
`NOTICE.md` and `.agent/references/scientific_agent_skills_source.md`.
