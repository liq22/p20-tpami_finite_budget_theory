# Goal G6 — Analysis, figures and synchronization

Scientific question: Can the final scientific decision be reproduced from immutable run artifacts without model inference, hidden filtering or expected-value plotting?

Hypothesis: A separate analysis/plot layer can regenerate every table and figure from committed compact data plus native result paths.

Estimand: No new estimand. G6 visualizes and audits the estimands frozen in E2–E5.

## Inputs

```text
native PHMFactory result directories
response table and unit index
E2–E5 raw unit-level CSV/JSON artifacts
analysis lock and failure records
```

## Fixed conditions

- Plotting never imports the model, trainer, data reader or response collector.
- Analysis reads frozen CSV/JSON/NPZ artifacts only.
- No missing/failed run is dropped without a visible status.
- Figures contain no expected, simulated replacement or hand-entered result values.

## Changed variable

Only the visual encoding and aggregation explicitly defined by the estimand.

## Execution

1. Add a direct Benchmark analysis entry, for example:

```text
scripts/p20/analyze_real_falsification.py
scripts/p20/plot_real_falsification.py
```

Do not add a plotting factory, registry or dashboard.

2. Produce only panels supported by actual data:

```text
primary paired unit effect with uncertainty
matched-objective comparison at the frozen primary k,Q
prespecified k,Q sensitivity
structured-support contrast
intervention-law sensitivity
cost/effect table or frontier
```

If a required experiment is blocked, replace the panel with nothing, not an expected curve.

3. Export:

```text
editable SVG with real text and independent objects
PDF
high-resolution PNG preview
figure_data.csv for every figure
README with exact regeneration command
```

4. Inspect every final-size figure for labels, units, uncertainty, sample-size meaning and collisions. The scientific message must be one decision, not a decorative dashboard.

5. Run the relevant Benchmark checks:

```bash
python -m pytest test/test_p20_*.py -q
python -m scripts.validate_configs
python -m scripts.validate_docs
phmfactory preflight \
  --config configs/experiments/p20/<dataset>_response_objectives.yaml \
  --local-config configs/local/p20_machine.yaml
git diff --check
```

Run broader repository checks required by the actual changed paths. Do not suppress a failing test.

## Validation

- Recomputed summaries exactly match the committed compact tables.
- Plot source has no inference/data-loading imports.
- SVG contains text/shape objects, no embedded whole-panel bitmap or base64.
- Caption states independent unit, `N`, estimator, interval and claim boundary.
- Negative/null results are visually as prominent as positive results.

## Required artifacts

```text
reports/p20/figures/*.svg
reports/p20/figures/*.pdf
reports/p20/figures/*.png
reports/p20/figures/*_data.csv
reports/p20/figures/README.md
reports/p20/FINAL_DECISION.md
reports/p20/EXECUTION_COMMANDS.md
reports/p20/FAILURE_INDEX.md
```

`FINAL_DECISION.md` must state one of `SUPPORT`, `NARROW`, `REJECT`, or `BLOCKED`, and point to the exact unit-level evidence.

## Acceptance criteria

All configured runs and figures are reproducible from the recorded commands. No Results prose is written in the paper repository during this local execution stage.

## Failure handling

If analysis reveals a schema, unit or estimand mismatch, invalidate the affected result and record the failure. Do not patch the plot or aggregate around it. Continue any independent valid analysis.

## Sync

1. Inspect the complete Benchmark diff and exclude raw datasets, personal paths, caches and large checkpoints.
2. Commit only validated code, configs, tests, compact real artifacts, figure data/source and failures.
3. Push the topic branch and open a focused PR to Benchmark `dev`.
4. Record the Benchmark commit and PR in `FINAL_DECISION.md`.
5. Merge only after the Benchmark's required checks pass. Do not update `main`.
6. Stop. The subsequent paper-update prompt will consume the accepted Benchmark evidence and revise claims/Results.
