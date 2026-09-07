# Invocation scenarios

Realistic prompts for the `scientific-visualization` skill. Each assumes the
single-paper workspace under `paper/` already has recorded runs and a target
journal defined.

## Scenario 1: Build the main results figure for a target journal

> We are submitting to Nature. Build the main results figure (Figure 2) from
> run `R07` in `paper/experiments/run_ledger.md`: a two-panel composite with
> panel A = mean response over dose (log-x) with 95% CI bands across three
> treatment arms, and panel B = a box+strip comparison of the endpoint at the
> top dose. Use the Okabe-Ito palette, single-column width (89 mm), sans-serif
> fonts ≥7 pt at final size, and export both PDF and PNG at 300 DPI into
> `paper/assets/figures/`. Add panel labels a/b (Nature uses lowercase),
> specify error bars and sample size in the caption draft, and bind the figure
> to its evidence row in `paper/experiments/evidence_matrix.md`. Record the
> run id and palette choice in `paper/logs/decision_log.md`.

## Scenario 2: Retrofit a draft figure to pass accessibility and journal checks

> The draft `paper/assets/figures/fig3_ablation.png` uses a red-green palette
> and is a 150 DPI JPEG. Rebuild it as a vector PDF at ≥600 DPI line-art, swap
> to a colorblind-safe diverging colormap (`RdBu_r`, centered at 0), verify it
> reads in grayscale, confirm width against `paper/refs/target_journal.md`,
> and re-export into `paper/assets/figures/`. Update the caption and the
> `paper/experiments/evidence_matrix.md` binding, and log the change in
> `paper/logs/change_log.md` since the manuscript is already frozen.
