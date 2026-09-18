#!/usr/bin/env bash
# Derived reading PDF only. Markdown remains the editable manuscript authority.
set -euo pipefail
cd "$(dirname "$0")/.."
output="${1:-build/p20}"
mkdir -p "$output"
python experiments/p19/plot_motivation.py
cairosvg paper/assets/figures/motivation.svg -o paper/assets/figures/motivation.pdf
cairosvg paper/assets/figures/motivation.svg --output-width 3000 -o "$output/motivation.png"
out_abs="$(cd "$output" && pwd)"
cd paper/draft
# Use the vector PDF only during TeX conversion; GitHub/Markdown keeps the SVG.
sed 's@../assets/figures/motivation.svg@../assets/figures/motivation.pdf@g' main.md |
  pandoc --from=markdown --standalone --citeproc --bibliography=../refs/references.bib \
    --pdf-engine=xelatex -V papersize=a4 -V geometry:margin=22mm -V fontsize=10pt \
    -V colorlinks=true -V mainfont='DejaVu Serif' -o "$out_abs/manuscript.pdf"
