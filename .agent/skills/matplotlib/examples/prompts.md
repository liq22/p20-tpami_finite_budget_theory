# matplotlib — invocation scenarios

Realistic prompts for invoking the matplotlib tool skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill and the workspace artifacts it produces or reads.

## Scenario 1: Custom multi-panel ablation figure

> I need a publication-quality multi-panel figure for the ablation table in
> `paper/experiments/ablation.md`. It should show, side by side: (a) a bar chart
> of the metric across the four ablation variants, (b) a line plot of the
> training-curve per variant from `paper/experiments/run_ledger.md`, and (c) a
> heatmap of the per-class confusion deltas. Fine-grained control over tick
> labels, colormap (use a perceptually uniform sequential map), and panel
> annotations is required. Export to both PDF and PNG at 300 dpi into
> `paper/assets/figures/`.

This triggers matplotlib because the request demands pixel-level control over
panels, custom annotations, and dual PDF/PNG export. The skill uses the
object-oriented API with `plt.subplot_mosaic`, sets a publication `rcParams`
block, and writes the figures into `paper/assets/figures/` (recorded in the
run ledger as figure provenance). Do NOT use seaborn or plotly here — the
multi-panel layout and annotation requirements exceed their high-level
defaults; prefer `scientific-visualization` as the primary planning skill for
journal-fit styling and hand off the low-level rendering to this skill.

## Scenario 2: Novel 3D surface plot not covered by seaborn

> One of our reviewers asked for a 3D response surface over the two
> hyperparameters in `paper/experiments/statistics.md`. This is a novel plot
> type for us: a 3D surface with projected contours on the floor and a custom
> diverging colormap centered at the baseline metric. Save as
> `paper/assets/figures/response_surface.pdf` and embed it in the
> post-freeze TeX at `paper/tex/`.

This triggers matplotlib because seaborn has no first-class 3D surface API and
the diverging colormap centered at a specific value needs `TwoSlopeNorm` plus
explicit `Axes3D` control. The skill produces the figure via
`fig.add_subplot(projection='3d')`, `ax.plot_surface(...)`, and `ax.contour`,
saves the PDF into `paper/assets/figures/`, and notes the embedding target in
`paper/tex/`. For the overall figure-design plan (which panel, which journal
column width, caption) defer to `scientific-visualization`; this skill owns
only the low-level rendering and export.

## Scenario 3: Restyling all draft figures after a journal switch

> We just switched target journal (see `paper/refs/target_journal.md`) and the
> new one requires a specific font, single-column width of 3.5 inches, and
> vector-only output. Re-render every figure currently in
> `paper/assets/figures/*.png` as PDF using a shared `rcParams` style sheet so
> they are visually consistent.

This triggers matplotlib: the task is bulk restyling and re-export of existing
figures under a shared style sheet, which is exactly the
`style_configurator.py` + `rcParams` workflow. The skill generates one
`.mplstyle` file and re-exports all figures as PDF into `paper/assets/figures/`,
logging the change in `paper/logs/change_log.md`. Use `scientific-visualization`
as the primary skill for deciding which journal conventions apply; this skill
only executes the mechanical restyle.
