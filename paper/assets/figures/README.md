# Motivation figure

## Message and mapping

The figure exposes a confounded routing comparison. Panel a is plain union-OMP;
panel b is context-restricted support search; panel c is the same-information
union emulator. The response, k, Q, development information and descriptor map
to Section 3 notation. The selector and zero-padding map to the finite-query
emulation proposition. The numerical footer reads the executed synthetic summary,
not a constructed curve. Main-text Section 1 explains the ambiguity; Sections
3–5 provide the formulation, mechanism and comparison.

## Regenerate

From the repository root:

```bash
python experiments/p19/plot_motivation.py
cairosvg paper/assets/figures/motivation.svg -o paper/assets/figures/motivation.pdf
mkdir -p build
cairosvg paper/assets/figures/motivation.svg --output-width 3000 -o build/motivation.png
bash scripts/build_paper.sh build/p20
```

Dependencies: Python 3, CairoSVG, Pandoc, XeLaTeX and DejaVu fonts. Install locally
with the platform package manager; no font files are included. To regenerate the
source experiment, run `python experiments/p19/toy.py --output results/paired_control`
and explicitly pass its `toy_summary.json` to `plot_motivation.py --summary`.
Do not replace the recorded summary with hypothetical output.

SVG source uses independent text, rectangles, lines and an arrowhead path. It has
no raster images or base64 data. The SVG is the committed editable asset; PDF and
high-resolution PNG are reproducible exports. The design follows the requested
nature-figure emphasis on a single scientific ambiguity and evidence mapping;
its full external automatic audit suite is not claimed to have run.
