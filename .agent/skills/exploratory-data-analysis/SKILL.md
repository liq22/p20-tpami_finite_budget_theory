---
name: exploratory-data-analysis
description: Support a selected PaperTrace task with a bounded, decision-relevant characterization of actual data before confirmatory analysis or modeling.
---

# Exploratory Data Analysis

## Purpose

Use exploratory data analysis to determine what an actual dataset contains,
whether its structure and quality match the intended scientific design, and which
single issue most affects the next analysis or experiment decision.

This is a supporting capability. The primary Skill defines the question,
independent unit, intended comparison, and requested product. EDA characterizes
the data; it does not establish a causal, mechanistic, or confirmatory claim.

## Workflow

1. Confirm the data path, format, expected schema or metadata, scientific unit,
   grouping or temporal structure, and the decision the characterization must
   inform. User-supplied data does not need a pre-existing ledger entry.
2. Select the reader from the actual format and project environment. Do not rely
   on an extension alone when the container, encoding, or domain convention is
   ambiguous.
3. Inspect only decision-relevant structure and quality, such as:
   - unit and observation counts;
   - dimensions, dtypes, labels, units, and metadata;
   - missing, invalid, duplicate, non-finite, or impossible values;
   - group, class, batch, temporal, and operating-condition coverage;
   - consistency between stated and observed sampling or acquisition metadata.
4. Distinguish observed facts from suspected artifacts and hypotheses. Do not
   automatically impute, discard outliers, normalize, repair metadata, or change
   labels.
5. Compute descriptive summaries or exploratory plots only when they can reveal a
   quality problem, confound, imbalance, leakage risk, or boundary relevant to the
   selected task. State any sampling, chunking, or approximation.
6. Compare the observed data with the expected design. Identify the strongest
   blocker or the most informative next analysis rather than generating a generic
   catalogue of recommendations.
7. Produce the requested notebook, script, concise report, table, or exploratory
   figure. Save only artifacts needed by the current task; create no fixed report
   package.
8. If the characterization changes the scientific judgment, update the current
   claim or boundary through the primary Skill. Record a run only when a real run
   record is in use.
9. Re-run the closest bounded analysis and inspect the output once.

## Output Contract

Return the requested characterization with:

- data source, format reader, and any sampling or chunking;
- actual unit counts, structure, metadata, and relevant descriptive summaries;
- concrete quality issues and their effect on the planned analysis;
- clear separation of observed facts, suspected artifacts, and hypotheses;
- one recommended next action only when it can change the decision;
- one direct validation.

A comprehensive Markdown report is not required. The product should be as small as
the decision permits.

## Boundaries

- Do not require target-journal, reading-matrix, statistics, reproducibility,
  evidence-matrix, decision-log, open-question, insight, or change-log files before
  inspecting user-supplied data.
- Do not generate a universal report, format encyclopedia, preprocessing checklist,
  or generic list of future analyses.
- Do not use broad exception handling to convert unreadable, corrupt, unsupported,
  or partially parsed data into a successful report.
- Do not apply fixed missingness, outlier, imbalance, or quality thresholds across
  domains.
- Do not silently clean, impute, resample, normalize, truncate, or relabel data.
- Do not run confirmatory hypothesis tests, fit predictive models, or infer
  causation or mechanism.
- Do not invoke an external narrative service or transmit data unless the user
  explicitly requests it and the data boundary permits it.
- Do not calculate custom hashes, create integrity reports, or treat a readable
  file as proof of valid scientific provenance.
- Do not create report generators, reader registries, fallback parser chains, or
  multiple logging surfaces.
