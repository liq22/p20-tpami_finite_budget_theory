---
name: matplotlib
description: 'Implementation skill for low-level plotting with matplotlib (Python). Use for fine-grained control over plot elements, novel plot types (3D surfaces, custom projections), subplots/mosaics, rcParams styling, or PNG/PDF/SVG export. Do not use for figure planning — defer to scientific-visualization; this is only the rendering engine.'
---

# matplotlib

## Purpose

Render publication-quality figures with matplotlib: full control over the
Figure/Axes hierarchy, plot types (line, scatter, bar, histogram, heatmap,
contour, box, violin, 3D), `rcParams` styling, colormaps, layout, and export.
This is an implementation-only tool skill; it executes rendering, not planning.

## Use When

- A figure needs pixel-level control over ticks, annotations, colormaps, or
  custom projections (e.g. 3D surface, `TwoSlopeNorm`, mosaic layouts).
- You must export to a specific format/resolution (PDF vector, 300 dpi PNG, SVG).
- Bulk restyling of existing figures under a shared `.mplstyle` sheet.
- A plot type is needed that seaborn/plotly do not provide directly.
- A `paper/assets/figures/` artifact must be produced for embedding in
  `paper/tex/` or `paper/draft/`.

This is a TIER B tool skill: prefer `scientific-visualization` as the primary
skill for figure planning (panel layout, journal column widths, captions).
Classical ML plots defer to scikit-learn; deep-learning training curves to
pytorch-lightning; Bayesian model plots to pymc. This skill handles only the
low-level matplotlib rendering those skills may hand off to.

## Required Inputs

- Data arrays (NumPy / pandas) or a path to a results file referenced in
  `paper/experiments/run_ledger.md`.
- Target output path under `paper/assets/figures/` and the desired format/dpi.
- The relevant target-journal figure constraints from
  `paper/refs/target_journal.md` (column width, font, vector vs raster).
- No API keys or credentials are required. If a wrapped workflow ever needs an
  external credential, the user must provide it; never hardcode or store it.

## Workflow

1. Confirm the figure spec from the calling planning skill (panel layout,
   metrics, colormap, journal constraints). Do not invent new science.
2. Prefer the object-oriented interface (`fig, ax = plt.subplots(...)`); avoid
   the pyplot state machine except for quick one-off exploration.
3. Set layout via `constrained_layout=True` (or `tight_layout()`) and a shared
   `rcParams` / `.mplstyle` block so figures stay visually consistent.
4. Choose a perceptually uniform colormap (sequential `viridis`/`plasma`;
   diverging `coolwarm`/`RdBu` with a centered norm; qualitative `tab10`/`Set3`
   for categories). Avoid rainbow maps such as `jet`.
5. Make figures accessible: colorblind-safe colormaps (`viridis`, `cividis`),
   hatching/patterns on bars, sufficient contrast, descriptive labels/legends.
6. Export with explicit `dpi` (300 for print, 150 for web) and
   `bbox_inches='tight'`. Write both PDF (vector) and PNG when a journal
   requires vectors and a preview is needed.
7. Write the figure into `paper/assets/figures/` and record provenance in
   `paper/experiments/run_ledger.md` (source run, metric, claim ID) so it can
   be linked from `paper/experiments/evidence_matrix.md`.
8. Close figures explicitly (`plt.close(fig)`) to avoid memory leaks in batch
   rendering.

## Output Contract

- One or more figure files under `paper/assets/figures/` (PNG/PDF/SVG), named to
  match the figure ID used in `paper/experiments/evidence_matrix.md`.
- Optional `.mplstyle` sheet under `paper/assets/figures/` or a project styles
  dir for reusable restyling.
- An updated provenance entry in `paper/experiments/run_ledger.md` and, where the
  figure supports a claim, a row in `paper/experiments/evidence_matrix.md`.
- A note in `paper/logs/change_log.md` when figures are restyled post-freeze.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only matplotlib`
- `python src/S03_Scripts/validate_project.py`
- Re-open each exported file to confirm it is non-empty and the expected format.
- Confirm no figure is used to support a claim that `paper/experiments/evidence_matrix.md`
  marks `unsupported`, `missing_evidence`, or `refuted`.
- Confirm DPI/size matches `paper/refs/target_journal.md` (e.g. column width).

## Boundaries

- Do not decide figure content, panel choice, or captions on its own — that is
  `scientific-visualization`'s job. This skill only renders what it is given.
- Do not fabricate data; plot only values present in a run referenced by the
  ledger or supplied explicitly by the user.
- Do not write figures anywhere except `paper/assets/figures/` (or a clearly
  named scratch dir); never into `paper/tex/`, `paper/refs/`, or `paper/submission/`.
- Do not embed raster screenshots where the journal requires vector output.
- Do not modify source data files to make a plot look better.

## Stop With

- The figure spec is missing, ambiguous, or contradicts
  `paper/refs/target_journal.md` constraints.
- The requested plot would imply a causal claim from correlational data.
- The data needed for the plot is not in the ledger and the user has not
  supplied it.
- matplotlib/the chosen backend is unavailable or fails to render (e.g. missing
  `ipympl`, GUI backend error in a headless environment) — fall back to the Agg
  backend for file output and report the failure.

## References

- Plot types catalog: `.agent/skills/matplotlib/references/plot_types.md`
- Styling guide: `.agent/skills/matplotlib/references/styling_guide.md`
- API reference: `.agent/skills/matplotlib/references/api_reference.md`
- Common issues: `.agent/skills/matplotlib/references/common_issues.md`
- Helper scripts: `.agent/skills/matplotlib/scripts/` (see `README.md` there)
- Workspace artifacts: `paper/assets/figures/`, `paper/experiments/run_ledger.md`,
  `paper/experiments/evidence_matrix.md`, `paper/refs/target_journal.md`,
  `paper/logs/change_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://matplotlib.org/ , https://matplotlib.org/stable/gallery/index.html
