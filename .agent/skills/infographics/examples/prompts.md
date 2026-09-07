# Infographics — example invocations

Realistic scenarios for the single-paper workspace. Each assumes the user has
exported `OPENROUTER_API_KEY` out of band and that network access to
`https://openrouter.ai` is available. Outputs are illustrative / non-evidence
assets placed under `paper/assets/figures/`.

## Scenario 1: outreach "5 contributions" list infographic for a group meeting

Context: the manuscript's intro lists five contributions; the author wants a
clean list graphic for a title slide and the lab's social channel. This is
communication, not evidence.

Brief:
```
python .agent/skills/infographics/scripts/generate_infographic_ai.py \
  "5 contributions of our work: (1) a latency-optimal sampler for latent
   diffusion, (2) a 2.3x wall-clock speedup at matched FID, (3) no quality
   drop on ImageNet-1k, (4) drops in cleanly to any LD pipeline, (5) open
   source, MIT licensed" \
  -o paper/assets/figures/infographic_contributions.png \
  --type list --style technology --doc-type presentation --iterations 3
```
After it runs:
- Confirm `paper/assets/figures/infographic_contributions.png` exists and the
  sibling `*_review.json` shows `final_score >= 7.5`.
- Append to `paper/logs/decision_log.md`: model, threshold 7.5, final score,
  early-stop flag, output path, and the tag "illustrative, non-evidence, for
  group meeting / outreach".
- Note in `paper/checklists/` figure provenance that this is not a numbered
  figure and is not derived from experimental data.

## Scenario 2: timeline of the method's lineage for a poster banner

Context: a poster needs a horizontal timeline showing the field lineage that
motivates the method (DDIM, PLMS, DPM-Solver, this work). No experiment numbers,
pure communication.

Brief:
```
python .agent/skills/infographics/scripts/generate_infographic_ai.py \
  "Timeline of diffusion samplers: 2020 DDIM, 2022 PLMS, 2022 DPM-Solver,
   2023 DPM-Solver++, 2025 OurWork (latency-optimal). Mark each node with a
   short one-line label and an icon." \
  -o paper/assets/figures/infographic_sampler_timeline.png \
  --type timeline --style corporate --doc-type report --iterations 3
```
After it runs:
- Confirm the PNG and `*_review.json` (target `final_score >= 8.0` for
  `report`).
- Record model, threshold, and score in `paper/logs/decision_log.md`, tagged
  illustrative / non-evidence / poster-banner.
- If a node label is wrong or a date is off, regenerate with a more specific
  prompt rather than hand-editing the PNG.

## Scenario 3: comparison graphic for a press kit (concepts, not numbers)

Context: the press kit wants a side-by-side "standard sampler vs our sampler"
graphic that communicates *qualitative* trade-offs (more steps vs fewer steps,
tunable vs fixed) without binding to specific experiment numbers (those live in
`paper/experiments/` and must come from `scientific-visualization`).

Brief:
```
python .agent/skills/infographics/scripts/generate_infographic_ai.py \
  "Side-by-side comparison: Standard sampler vs Our latency-optimal sampler.
   Rows: steps-per-image (many vs few), schedule (fixed vs tunable),
   quality (matched vs matched), drop-in (no vs yes). Use check/cross marks
   and a clean two-column layout." \
  -o paper/assets/figures/infographic_sampler_comparison.png \
  --type comparison --style technology --palette wong --doc-type marketing --iterations 3
```
After it runs:
- Target `final_score >= 8.5` for `marketing`; if not met, log it as a dead-end
  in `paper/logs/dead_ends.md` and either bump `--iterations` or simplify the
  brief.
- Record provenance in `paper/logs/decision_log.md` (illustrative, non-evidence,
  press-kit, model, palette, score).
- Re-verify no secret leaked into the review JSON.
