# latex-posters — example invocations

Realistic prompts for driving the `latex-posters` skill. Each scenario assumes
the user has a working local LaTeX toolchain (`pdflatex`/`xelatex`/`lualatex`
with `beamerposter`/`tikzposter`/`baposter` installed) and that the project's
claims and figures already live under `paper/experiments/` and
`paper/assets/figures/`.

## Scenario 1: A0 portrait conference poster from a finished draft

> The paper at `paper/draft/01_main.md` is accepted at the ML4H symposium, which
> requires an A0 portrait poster. Build a `tikzposter`-based poster that leads
> with the headline accuracy number from `paper/experiments/statistics.md`, uses
> the architecture figure at `paper/assets/figures/architecture.pdf` and the
> results bar chart at `paper/assets/figures/results_bars.pdf`, and ends with a
> QR code to the code release. Keep total text under 600 words, no section over
> 80 words, and run the overflow/font-embedding QA before delivering.

Expected handling: confirm A0 portrait (841×1189mm); start from
`assets/tikzposter_template.tex`; distill to Title / Problem / Methods /
Results / Conclusions; place figures at `width=0.85\linewidth`; compile with
`pdflatex`; run `grep -i overfull poster.log`, `pdfinfo poster.pdf`,
`pdffonts poster.pdf`, and `scripts/review_poster.sh`; deliver
`paper/submission/poster/poster.pdf` + `.tex` and log the class/size in
`paper/logs/decision_log.md`.

## Scenario 2: baposter multi-column thesis-defense poster with AI schematics

> For my PhD defense I need a 36×48" landscape poster using `baposter` with
> three columns. The pipeline overview in `paper/assets/figures/pipeline.pdf` is
> too dense for a poster — generate a simplified 3-box "DATA → MODEL →
> PREDICTION" poster schematic instead (I have an OpenRouter API key in my
> environment), and pair it with the existing ablation table from
> `paper/experiments/ablation.md`. Target ≤ 500 words; embed all fonts.

Expected handling: confirm 36×48" landscape; start from
`assets/baposter_template.tex`; for the simplified schematic, prompt the
upstream AI schematic generator (user-provided OpenRouter key, read from the
environment — never hardcoded) with strict poster constraints (≤ 3 elements,
≥ 50% white space, ≥ 80pt labels); write the new schematic to
`paper/submission/poster/figures/`; compile, then enforce zero `Overfull`
warnings and `emb=yes` on every font before delivery. If no API key is
available, fall back to simplifying the existing `pipeline.pdf` panel rather
than generating a new one, and record the choice in `paper/logs/decision_log.md`.
