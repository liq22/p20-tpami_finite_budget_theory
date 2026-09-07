---
name: xlsx
description: Create, edit, or analyze a spreadsheet when the workbook or table is the requested deliverable, prioritizing correct data, formulas, comparisons, and decisions before styling.
---

# XLSX

## Purpose

Produce a correct, usable workbook or tabular export. The data model, formulas,
and decision-relevant table are the product.

## Workflow

1. Define the rows, columns, units, keys, formulas, and decision the workbook must
   support.
2. Import or enter the actual data without silently changing types or missing
   values.
3. Build only the formulas, summaries, or charts needed for the requested use.
4. Check a few representative formulas and totals against direct calculations.
5. Apply minimal formatting for readable headers, units, number formats, widths,
   and frozen panes.
6. Open or recalculate the workbook once and inspect formula errors and the
   affected sheets.
7. Stop when the workbook is correct and usable.

## Output Contract

Produce the requested `.xlsx`, `.csv`, or `.tsv` with correct data and formulas.
Include a short note for assumptions or unresolved missing data when material.

## Boundaries

- Do not begin with colors, borders, dashboards, conditional formatting, or print
  layout before the data and formulas are correct.
- Do not create charts, helper sheets, scenarios, or summary tabs without a user
  or scientific decision they support.
- Do not run repository-wide validation for spreadsheet work.
- Use Python or spreadsheet tools to create or test the actual workbook, not to
  generate audit reports or exhaustive edge-case matrices.
- Do not add defensive handling for file types or formula states not present in
  the task.
- Stop when representative formulas recalculate correctly and the workbook opens.
