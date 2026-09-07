---
name: seaborn
description: 'Implementation skill for statistical plotting with seaborn. Use for tidy-DataFrame distributions, categorical comparisons, pair/joint grids, regression plots, and correlation heatmaps with semantic mapping. Do not use for figure planning or styling (defer to scientific-visualization), interactive plots, or low-level pixel control (matplotlib).'
---

# seaborn

## Purpose

Render publication-quality statistical graphics with seaborn: dataset-oriented
plotting of tidy pandas DataFrames, automatic semantic mapping (`hue`/`size`/
`style`), built-in statistical estimation and error bars, multi-panel grids
(`FacetGrid`/`PairGrid`/`JointGrid`), regression visualization, and matrix
heatmaps. This is a TIER B implementation-only tool skill: it renders
statistical figures, it does not plan them.

## Use When

- A statistical figure needs distribution, categorical, relational, regression,
  or correlation views and seaborn's defaults and `hue` semantics materially
  reduce the rendering code.
- An EDA pass must summarize `paper/experiments/` results into a pair grid,
  faceted distribution, or correlation heatmap for `paper/experiments/insights.md`.
- A reviewer-requested comparison plot (`paper/reviews/response_to_reviewers.md`)
  needs box/violin/point estimates with confidence intervals across groups.
- A figure must be embedded in `paper/draft/` (pre-freeze) or `paper/tex/`
  (post-freeze) and benefits from seaborn's statistical defaults.

This is a TIER B tool skill: prefer `scientific-visualization` as the primary
skill for figure planning (panel layout, journal column widths, captions,
restyling). Plotting tools defer to scientific-visualization; classical-ML
diagnostic curves defer to scikit-learn; deep-learning training curves to
pytorch-lightning; Bayesian model plots to pymc. seaborn handles only the
statistical rendering those skills may hand off to it; matplotlib remains the
escape hatch for plot types seaborn lacks (3D, custom projections).

## Required Inputs

- A tidy long-form pandas DataFrame, or a path to a results file already logged
  in `paper/experiments/run_ledger.md`. Wide-form arrays are accepted only for
  matrices (heatmaps) and simple series; do not fabricate data.
- The figure spec from the calling planning skill: variables, semantics
  (`hue`/`size`/`style`), plot family, and the claim ID from
  `paper/experiments/evidence_matrix.md` it must support.
- Target-journal constraints from `paper/refs/target_journal.md` (column width,
  font, vector vs raster) and the output path under `paper/assets/figures/`.
- seaborn >= 0.13 with matplotlib/pandas/NumPy; optional scipy/statsmodels for
  some regression/clustering examples. The user is responsible for installing
  these; this skill does not pin or ship a runtime.
- No API keys or credentials are required. If a wrapped workflow ever needs an
  external credential (e.g. a private dataset token), the user must provide it;
  never hardcode or store it.

## Workflow

1. Read the figure spec and target claim from the planning skill and
   `paper/experiments/evidence_matrix.md`. Do not invent new science or metrics.
2. Load only data referenced by `paper/experiments/run_ledger.md`; if it is
   absent or unlogged, stop (see Stop With) rather than substituting.
3. Prefer long-form DataFrames and keyword arguments (`data=`, `x=`, `y=`,
   `hue=`). Avoid positional args and unnamed arrays, which drop axis labels.
4. Pick the family by question: distributions (`histplot`/`kdeplot`/`ecdfplot`/
   `displot`), relational (`scatterplot`/`lineplot`/`relplot`), categorical
   (`boxplot`/`violinplot`/`boxenplot`/`stripplot`/`swarmplot`/`barplot`/
   `pointplot`/`catplot`), regression (`regplot`/`lmplot`/`residplot`), matrix
   (`heatmap`/`clustermap`). Use `references/function_reference.md` for the
   0.13 API (e.g. `errorbar=` replaces `ci=`; `native_scale=` for numeric cats).
5. Use figure-level functions (`relplot`/`displot`/`catplot`/`lmplot`) for
   faceting (small multiples); use axes-level functions inside matplotlib
   subplots for custom multi-panel layouts.
6. Set a single theme (`sns.set_theme(style=, context=, palette=)`) and a
   colorblind-safe palette (`"colorblind"`, `"viridis"`, `"mako"`, diverging
   `"vlag"` centered at 0 for correlations) consistent with journal constraints.
7. Control statistical estimation explicitly: choose `estimator=` and
   `errorbar=` (`('ci', 95)`, `'sd'`, `('pi', 90)`) to match the protocol in
   `paper/experiments/statistics.md`; never let the default CI imply a stronger
   inference than the analysis supports.
8. Export with explicit `dpi` (300 print / 150 web) and `bbox_inches='tight'`;
   write both PDF (vector) and PNG when the journal requires vectors and a
   preview is needed. Close figures (`plt.close(fig)`) to avoid leaks.
9. Write the figure into `paper/assets/figures/` and append provenance to
   `paper/experiments/run_ledger.md` (source run, variables, claim ID) so it can
   be linked from `paper/experiments/evidence_matrix.md`; note post-freeze
   restyles in `paper/logs/change_log.md`.

## Output Contract

- One or more figure files under `paper/assets/figures/` (PNG/PDF/SVG), named
  to match the figure ID used in `paper/experiments/evidence_matrix.md`.
- A provenance row in `paper/experiments/run_ledger.md` (data ref, plot family,
  semantics, claim ID) and, where the figure supports a claim, a status update
  in `paper/experiments/evidence_matrix.md`.
- An optional insight entry in `paper/experiments/insights.md` when an EDA plot
  reveals structure worth recording, and a `paper/logs/change_log.md` note when
  figures are restyled after freeze.
- No executable scripts shipped into the repo; code stays as documented recipes
  in `references/`. This is a paper repo, not a plotting runtime.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only seaborn`
- `python src/S03_Scripts/validate_project.py`
- Re-open each exported file to confirm it is non-empty and the expected format.
- Confirm no figure supports a claim that `paper/experiments/evidence_matrix.md`
  marks `unsupported`, `missing_evidence`, or `refuted`.
- Confirm DPI/size and palette match `paper/refs/target_journal.md` (column
  width, colorblind-safety, vector vs raster).
- Confirm `errorbar=`/`estimator=` match the protocol recorded in
  `paper/experiments/statistics.md` (no stronger CI than the analysis supports).

## Boundaries

- Do not decide figure content, panel choice, or captions on its own — that is
  `scientific-visualization`'s job. This skill only renders what it is given.
- Do not fabricate data; plot only values present in a run referenced by the
  ledger or supplied explicitly by the user.
- Do not write figures anywhere except `paper/assets/figures/` (or a clearly
  named scratch dir); never into `paper/tex/`, `paper/refs/`, or
  `paper/submission/`.
- Do not embed raster screenshots where the journal requires vector output, and
  do not use rainbow colormaps (`jet`) or default CIs that overstate inference.
- Do not run heavy ML training/inference; classical-ML diagnostic plots defer
  to scikit-learn, training curves to pytorch-lightning, Bayesian plots to pymc.
- Do not copy executable training/inference scripts; ship `references/` docs only.

## Stop With

- The figure spec is missing, ambiguous, or contradicts
  `paper/refs/target_journal.md` constraints.
- The data needed for the plot is not in `paper/experiments/run_ledger.md` and
  the user has not supplied it.
- The requested plot would imply a causal claim from correlational data, or a
  stronger CI/inference than `paper/experiments/statistics.md` sanctions.
- seaborn or a required dependency (matplotlib/pandas) is unavailable and the
  user cannot install it; do not silently fall back to a different library.
- The result would contradict the claim's required direction and the user has
  not authorized reporting a `refuted` finding — surface it in
  `paper/logs/decision_log.md` and wait.

## References

- Function reference (0.13 API): `.agent/skills/seaborn/references/function_reference.md`
- Objects interface (`seaborn.objects`): `.agent/skills/seaborn/references/objects_interface.md`
- Common use cases and code patterns: `.agent/skills/seaborn/references/examples.md`
- Invocation scenarios: `.agent/skills/seaborn/examples/prompts.md`
- Companion rendering skill: `.agent/skills/matplotlib/SKILL.md`
  (escape hatch for plot types seaborn lacks)
- Workspace artifacts: `paper/assets/figures/`,
  `paper/experiments/run_ledger.md`, `paper/experiments/evidence_matrix.md`,
  `paper/experiments/statistics.md`, `paper/experiments/insights.md`,
  `paper/refs/target_journal.md`, `paper/logs/change_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://seaborn.pydata.org/ ,
  https://seaborn.pydata.org/tutorial.html
