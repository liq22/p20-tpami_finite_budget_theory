---
name: polars
description: Support a selected PaperTrace task with explicit, schema-aware Polars transformations, lazy execution when useful, and directly validated tabular outputs.
---

# Polars

## Purpose

Use Polars when a selected code, experiment, or analysis task needs efficient
tabular loading, filtering, joins, reshaping, aggregation, window operations, or
migration from an existing pandas pipeline.

This is a supporting capability. The primary Skill owns the scientific question,
data semantics, estimand, comparison, and requested product. Polars supplies the
smallest correct transformation and result.

## Workflow

1. Confirm the actual input, expected schema, key columns, units, independent unit,
   row meaning, requested transformation, and output. Stop rather than infer a
   missing schema or scientific definition.
2. Reproduce the current transformation or a small reference result before
   changing libraries or execution strategy.
3. Use eager execution for small direct operations and a lazy query for nontrivial
   scans or pipelines where projection, predicate pushdown, streaming, or query
   optimization has a measured benefit.
4. Select and filter early. Prefer native expressions and explicit type conversion;
   use Python element-wise functions only when no clear expression exists and the
   cost is acceptable.
5. For joins, verify key types, uniqueness/cardinality assumptions, null behavior,
   and before/after row counts. Fail on an unexplained empty, duplicated, or
   expanded result.
6. Keep transformations readable and directly tied to the requested product. Do
   not build a generic ETL framework for a single pipeline.
7. Save the requested source, notebook, Parquet/CSV table, or in-memory result at
   the path required by the task. Add a completed run or evidence update only when
   a real record is already part of that workflow.
8. Compare the output with the reference computation or explicit invariants,
   including rows, columns, dtypes, units, grouping, and aggregate values.
9. Preserve null, negative, unstable, and contradictory downstream results; data
   preparation must not be changed after the fact to recover a preferred claim.
10. Run the closest transformation, unit test, or smoke path and inspect its output
    once.

## Output Contract

Return the direct product requested by the primary Skill, together with:

- input and output schemas;
- transformation and lazy/eager choice;
- join, grouping, null, and type decisions that affect meaning;
- actual output path, shape, and checked values;
- any unresolved data-quality or semantic limitation;
- one direct validation.

A migration note, run row, or schema summary is supporting material and cannot
replace executable transformation code or the resulting table.

## Boundaries

- Do not require target-journal, statistics, ablation, reproducibility,
  decision-log, change-log, dead-end, or insight files before processing
  user-supplied data.
- Do not hard-code a Polars version or optional extras unless the current project
  depends on them.
- Do not silently change key types, null handling, sort order, grouping, row
  cardinality, units, or category encodings.
- Do not silently fall back to pandas, eager loading, sampling, or another data
  source when the requested pipeline fails.
- Do not choose an analysis, metric, model, or scientific conclusion.
- Do not require every transformation to produce a ledger entry or multiple
  supporting documents.
- Do not create generic ETL wrappers, schema registries, migration frameworks,
  dashboards, or extra logs.
- Do not hide a result because it weakens or refutes the current claim.
