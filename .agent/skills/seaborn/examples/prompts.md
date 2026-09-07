# seaborn — Invocation Scenarios

Realistic prompts that trigger this TIER B rendering skill. Each assumes the
planning skill (`scientific-visualization`) has already emitted a figure spec;
seaborn only renders statistical figures handed off to it. Adapt data paths and
claim IDs to the local `paper/` workspace before running.

---

## Scenario 1: EDA correlation + pair grid for an experiment run

Context: an experiment run finished and is logged in
`paper/experiments/run_ledger.md` (run `exp-007`, claim `C2`). The researcher
wants a quick distribution/correlation overview before drafting, to record any
notable structure in `paper/experiments/insights.md`.

Prompt:

> Render an EDA overview for run `exp-007` (logged in
> `paper/experiments/run_ledger.md`, supports claim `C2`). The tidy long-form
> results CSV has columns `model`, `dataset`, `accuracy`, `f1`, `latency_ms`.
> Produce two figures into `paper/assets/figures/`:
> 1. A `pairplot` (corner=True) of the numeric metrics colored by `model`, using
>    the `"colorblind"` palette.
> 2. A correlation `heatmap` (`annot=True, fmt=".2f", cmap="vlag", center=0,
>    square=True`) of the numeric columns.
> Use `sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)`. Export
> PNG @150 dpi (preview) and PDF (vector). Append a provenance row to
> `paper/experiments/run_ledger.md` (run, variables, claim `C2`) and, if any
> metric pair shows strong structure, add one line to
> `paper/experiments/insights.md`. Do not invent metrics not in the run.

---

## Scenario 2: Reviewer-requested categorical comparison with CI

Context: a reviewer asked for a per-condition comparison with confidence
intervals. The protocol in `paper/experiments/statistics.md` mandates mean ± 95%
bootstrap CI. This feeds `paper/reviews/response_to_reviewers.md` and the
post-freeze `paper/tex/` figure.

Prompt:

> Produce a reviewer-response figure for `paper/reviews/response_to_reviewers.md`
> (response to comment R3). Source data is the run supporting claim `C4` in
> `paper/experiments/run_ledger.md`: a tidy DataFrame with `condition`
> (`control`/`low`/`high`), `replicate`, and `response`. Render a `violinplot`
> split by `condition` with an overlaid `stripplot` (jitter, alpha=0.4), then a
> separate `pointplot` joining the mean per condition with `errorbar=("ci", 95)`
> to match `paper/experiments/statistics.md`. Use `native_scale=False`, a single
> `"muted"` palette, `sns.set_theme(style="ticks")`, and `sns.despine(trim=True)`.
> Respect `paper/refs/target_journal.md` (column width ~3.5in, vector PDF).
> Write to `paper/assets/figures/fig_r3_condition_comparison.{pdf,png}` (300 dpi,
> `bbox_inches="tight"`), update `paper/experiments/evidence_matrix.md` for
> claim `C4`, and note the new figure in `paper/logs/change_log.md` since the
> paper is post-freeze.
