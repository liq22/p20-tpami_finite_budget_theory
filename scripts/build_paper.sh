#!/usr/bin/env bash
# Derived reading PDF; Markdown and editable SVG remain the source artifacts.
set -euo pipefail
cd "$(dirname "$0")/.."
output="${1:-build/p20}"
mkdir -p "$output"
python experiments/p19/plot_motivation.py
for figure in motivation method_overview; do
  cairosvg "paper/assets/figures/$figure.svg" -o "paper/assets/figures/$figure.pdf"
  cairosvg "paper/assets/figures/$figure.svg" --output-width 2400 -o "$output/$figure.png"
done
out_abs="$(cd "$output" && pwd)"
cd paper/draft
sed -E 's@(\.\./assets/figures/[[:alnum:]_]+)\.svg@\1.pdf@g' main.md |
  pandoc --from=markdown --standalone --citeproc --bibliography=../refs/references.bib \
    --pdf-engine=xelatex -V papersize=a4 -V geometry:margin=22mm -V fontsize=10pt \
    -V colorlinks=true -V mainfont='DejaVu Serif' \
    -V header-includes='\usepackage[section]{placeins}' -o "$out_abs/manuscript.pdf"
