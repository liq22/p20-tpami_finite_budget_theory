# xlsx — invocation scenarios

Realistic prompts for invoking the xlsx core skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill and the workspace artifacts it produces or reads.

## Scenario 1: Build the ablation matrix workbook from the run ledger

> Turn `paper/experiments/ablation.md` into a publication supplementary Excel
> file. Pull the raw metric columns from the runs listed in
> `paper/experiments/run_ledger.md`, put each ablation variant on its own row,
> and compute the deltas vs. baseline as LIVE Excel formulas (not hardcoded
> numbers). Format with a professional font, blue for the input cells (the raw
> metrics) and black for the computed delta/growth cells, percentages at 0.0%,
> negatives in parentheses. Save it under `paper/submission/` as
> `ablation_matrix.xlsx` so it can go to the journal as supplementary
> material, and make sure there are zero formula errors.

This triggers xlsx because the deliverable is the workbook itself, the deltas
must be live formulas (not Python-computed literals frozen into cells), and it
needs formatting plus journal-bound export. The skill uses openpyxl to author
the workbook with assumption cells for the raw metrics and `=(B5-$B$2)/$B$2`
-style delta formulas, applies the blue/black number-format conventions from
`paper/refs/target_journal.md`, then runs
`python .agent/skills/xlsx/scripts/recalc.py paper/submission/ablation_matrix.xlsx`
to force LibreOffice to recalculate and confirm `total_errors: 0` before
delivery. Do NOT use this skill for the figure version of the ablation (that is
matplotlib/scientific-visualization); this owns only the tabular workbook and
its provenance row in `paper/experiments/evidence_matrix.md`.

## Scenario 2: Reviewer-requested results table with documented assumptions

> Reviewer 2 asked for a per-dataset breakdown of precision/recall/F1 with the
> exact evaluation protocol. I have the raw per-fold results in a `.csv` from
> run `R-117` in `paper/experiments/run_ledger.md`. Produce an Excel table that
> averages the folds with `=AVERAGE(...)` formulas, marks every hardcoded input
> cell with a source comment ("Source: run R-117, fold k, ..."), and highlights
> the one assumption cell we tuned (the decision threshold) in yellow. Wire it
> into the reviewer response at `paper/reviews/response_to_reviewers.md` and
> log the addition in `paper/logs/change_log.md`.

This triggers xlsx: the deliverable is a formatted workbook with formulas,
source-annotated hardcodes, and an industry-standard yellow highlight on the
key assumption. The skill loads the raw `.csv` via pandas, writes the
per-fold block with openpyxl, adds `=AVERAGE(...)`/`=STDEV(...)` formula cells
in black, annotates each literal input cell with its run/fold provenance
comment, fills the threshold assumption cell yellow, then recalc-checks for
zero errors and writes the workbook under `paper/assets/tables/` (linked from
the reviewer response). Do NOT use a plain `.md` table here — the reviewer
explicitly wants an Excel file, and the live fold averages must recompute if a
fold is corrected.

## Scenario 3: Post-freeze restyle of a supplementary workbook after a journal switch

> We switched target journal (see `paper/refs/target_journal.md`). The new one
> wants currency in EUR not USD, units spelled out in every header, and
> one-decimal percentages. Re-format the existing
> `paper/submission/cost_table.xlsx` WITHOUT changing any formula or value,
> matching the existing template's layout exactly, and re-run recalc so the
> cached values still match.

This triggers xlsx: it is an in-place edit of an existing workbook where
existing template conventions override defaults, formulas must be preserved
exactly (never open with `data_only=True` and save), and recalc must re-confirm
zero errors after the cosmetic edit. The skill loads the workbook with
openpyxl, restyles only number formats / headers per the new journal spec,
leaves all formula strings untouched, runs recalc, and logs the post-freeze
change in `paper/logs/change_log.md`. Use this skill rather than re-exporting
from a `.csv` because preserving the live formulas and template layout is the
whole point of the request.
