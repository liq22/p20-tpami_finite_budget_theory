---
name: dask
description: Support a selected PaperTrace data, experiment, or analysis task with out-of-core or parallel computation when the actual workload exceeds a simpler in-memory path.
---

# Dask

## Purpose

Use Dask when a selected task must process data larger than available memory,
combine many files, or execute a parallel computation graph that cannot be handled
reliably by a simpler pandas, NumPy, or Polars implementation.

This is a supporting capability. The primary Skill defines the scientific
question, data semantics, comparison, metric, and requested product. Dask changes
only how the same computation is executed.

## Workflow

1. Confirm the input paths, schema, units, independent unit, required computation,
   expected output, and available memory or workers. Stop when any scientific
   meaning is ambiguous.
2. Establish the computation on a representative bounded subset or another
   directly checkable reference when feasible. The distributed result must preserve
   the same rows, filters, grouping, and metric definition.
3. Select the smallest fitting Dask collection:
   - DataFrame for partitioned tabular operations;
   - Array for chunked numerical arrays;
   - Bag for semi-structured records;
   - delayed or futures for an irregular task graph.
4. Read data lazily through Dask rather than loading the full dataset first.
   Choose partitions, chunks, and scheduler from the measured workload and
   environment; do not apply universal sizes or worker rules.
5. Keep the graph simple. Project and filter early, avoid repeated `compute()`,
   persist only intermediates that are reused, and make scheduler or cluster
   changes explicit.
6. Execute the required computation and inspect actual output shape, units,
   missingness, key counts, and one invariant or reference result that can reveal
   changed semantics.
7. Produce the requested source, notebook, table, array, or summary. Record a
   completed run only when a real experiment record is in use, and keep only the
   environment and execution details needed to reproduce the result.
8. Surface memory failures, worker loss, partition skew, serialization errors, and
   disagreements with the reference result directly. Do not return a partial
   calculation as complete evidence.
9. Run the closest bounded script, test, or smoke path and inspect the output once.

## Output Contract

Return the direct product requested by the primary Skill, together with:

- data source and computation actually executed;
- Dask collection, partition/chunk, and scheduler choices that affect the result;
- actual output path, dimensions, units, and relevant runtime or resource limits;
- comparison with the reference computation or checked invariant;
- any unresolved execution or semantic limitation;
- one direct validation.

A dashboard link, graph description, run row, or reproducibility note is supporting
information and cannot replace the computed result.

## Boundaries

- Do not require target-journal, statistics, ablation, reproducibility,
  decision-log, dead-end, or insight files before processing user-supplied data.
- Do not choose or change the metric, grouping, split, filter, independent unit, or
  scientific task.
- Do not use Dask when the data fits a simpler reliable in-memory path.
- Do not hard-code library versions, partition sizes, worker counts, or scheduler
  choices without a project-specific reason.
- Do not silently fall back to pandas, NumPy, another scheduler, sampled data, or a
  different computation after failure.
- Do not treat dashboard availability, successful task completion, or a large
  worker count as evidence that the scientific result is correct.
- Do not create cluster infrastructure, generic execution wrappers, fallback
  stacks, extra logs, or status reports.
- Do not suppress a null, negative, unstable, or contradictory result because it
  weakens the current claim.
