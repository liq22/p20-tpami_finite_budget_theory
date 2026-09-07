# matplotlib scripts (ported)

Reference helper scripts for the matplotlib tool skill. These are optional
convenience utilities; the skill is fully usable by writing inline code against
the object-oriented matplotlib API.

## plot_template.py

- **Purpose:** Template demonstrating several plot types (line, scatter, bar,
  histogram, heatmap, contour, box, violin, 3D) with a publication-style
  `rcParams` block. Use as a starting point for new figure code.
- **Inputs:** CLI flags `--plot-type`, `--style`, `--output`. Generates its own
  synthetic sample data via NumPy; takes no data files.
- **Outputs:** A single figure file at the path given by `--output`
  (default `plot.png`), written via `plt.savefig(..., dpi=300, bbox_inches='tight')`.
- **Network:** None. No HTTP, sockets, or remote calls.
- **Writes:** Only the `--output` figure path in the current working directory.
  Does not touch `paper/` or any repo-tracked path; copy or move the produced
  figure into `paper/assets/figures/` yourself.
- **Run:** `uv run python .agent/skills/matplotlib/scripts/plot_template.py --plot-type all --output fig.png`

## style_configurator.py

- **Purpose:** Interactive utility to pick a preset matplotlib style (publication,
  presentation, dark) or build a custom `rcParams` style sheet.
- **Inputs:** Interactive stdin prompts (style choice, font size, dpi, colormap,
  etc.). No data files.
- **Outputs:** A custom matplotlib `.mplstyle` sheet file (path prompted at
  runtime) plus an optional `preview.png`.
- **Network:** None.
- **Writes:** The `.mplstyle` file path you enter and a `preview.png` in the
  current working directory. Does not write into `paper/`.
- **Run:** `uv run python .agent/skills/matplotlib/scripts/style_configurator.py`

## Provenance

Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see
NOTICE.md and `.agent/references/scientific_agent_skills_source.md`.
