# scientific-schematics — invocation scenarios

Realistic invocation scenarios for the single-paper workflow. Each scenario names the
`paper/` artifacts read, the schematic produced, and the artifacts written back. This skill
produces conceptual/structural schematics only — it never plots numeric experiment results
(that is scientific-visualization) and never drafts prose.

## Scenario 1: Model-architecture diagram for a methods section (pre-freeze)

Context: stage `08-markdown-draft` is in progress. The methods section needs a figure
showing the encoder–decoder Transformer architecture with cross-attention, layer
dimensions, and the residual/norm blocks. `paper/refs/target_journal.md` records a NeurIPS-
style double-column format (vector required, 300+ DPI). `paper/experiments/evidence_matrix.md`
has an open claim row C3 "our architecture supports cross-modal alignment" that this figure
must support. The user has supplied an OpenRouter key out of band.

Prompt:
> Read `paper/refs/target_journal.md` (set `conference` threshold 8.0, double-column width,
> vector primary) and `paper/experiments/evidence_matrix.md` row C3. Compose a precise
> diagram brief for a Transformer encoder–decoder architecture: left encoder stack (input
> embedding, positional encoding, multi-head self-attention, add & norm, feed-forward, add
> & norm) and right decoder stack (output embedding, positional encoding, masked
> self-attention, add & norm, cross-attention from the encoder, add & norm, feed-forward,
> add & norm, linear & softmax), with a dashed cross-attention connection from encoder to
> decoder, layer dimensions labelled in each box, light-blue encoder and light-red decoder,
> colorblind-safe Okabe-Ito accents. Generate via `scripts/generate_schematic.py`, iterate
> up to 2 times against the 8.0 threshold, export vector `fig2_architecture.pdf` plus a PNG
> preview into `paper/assets/figures/`. Run the accessibility pass (grayscale + colorblind
> simulator). Record the caption (key message, all abbreviations defined, claim C3
  supported), the first callout, the generation prompt, and the per-iteration review log;
  bind the figure to evidence row C3; log the threshold/style choice in
  `paper/logs/decision_log.md`.

Inputs: `paper/refs/target_journal.md`, `paper/experiments/evidence_matrix.md`,
`paper/draft/` (callout site), `references/best_practices.md`, `references/QUICK_REFERENCE.md`,
`scripts/generate_schematic.py`, a user-provided `OPENROUTER_API_KEY` (out of band).

Outputs: `paper/assets/figures/fig2_architecture.pdf` + `fig2_architecture.png`, a
`fig2_architecture_review.json` next to them, a new caption + callout + binding row in
`paper/experiments/evidence_matrix.md`, a dated entry in `paper/logs/decision_log.md`. No
prose, no statistics, no experiment run is produced.

## Scenario 2: CONSORT participant-flow diagram bound to the experiment ledger

Context: stage `06-experiment-ops` is settled and `09-tex-freeze-formalize` has not yet
frozen figures. The RCT ran 500 screened / 150 excluded / 350 randomized into two arms of
175, with follow-up losses, recorded in `paper/experiments/run_ledger.md` run R7 and
summarized in `paper/experiments/statistics.md`. The methods section needs a CONSORT flow
diagram. The journal (`paper/refs/target_journal.md`) is a clinical journal requiring
`journal` threshold 8.5.

Prompt:
> Read `paper/refs/target_journal.md` (set `journal` threshold 8.5) and pull the exact
> CONSORT counts from `paper/experiments/run_ledger.md` run R7 and
> `paper/experiments/statistics.md` — do not invent or round any number. Compose the brief:
> "Assessed for eligibility (n=500)" at top; "Excluded (n=150)" with reasons age<18 (n=80),
> declined (n=50), other (n=20); "Randomized (n=350)" splits into "Treatment (n=175)" and
> "Control (n=175)"; each arm shows "Lost to follow-up" (n=15 and n=10); ends with "Analyzed
> (n=160)" and "(n=165)"; blue process boxes, orange exclusion box, green analysis boxes,
> Okabe-Ito colorblind-safe. Generate via `scripts/generate_schematic.py`, iterate up to 2
> against 8.5, export vector `fig1_consort.pdf` + PNG into `paper/assets/figures/`. Run the
> accessibility pass. Bind the figure to its evidence row, cite run R7 as the provenance for
> every count, and record the caption with all abbreviations defined; log the threshold and
> the choice to cite R7 rather than recompute in `paper/logs/decision_log.md`. If any count
> cannot be sourced from R7 or statistics.md, stop and open a question in
> `paper/logs/open_questions.md` rather than guessing.

Inputs: `paper/refs/target_journal.md`, `paper/experiments/run_ledger.md`,
`paper/experiments/statistics.md`, `paper/experiments/evidence_matrix.md`,
`references/best_practices.md`, `scripts/generate_schematic.py`, a user-provided
`OPENROUTER_API_KEY` (out of band).

Outputs: `paper/assets/figures/fig1_consort.pdf` + `fig1_consort.png` +
`fig1_consort_review.json`, a caption + callout + binding row citing run R7 in
`paper/experiments/evidence_matrix.md`, a dated entry in `paper/logs/decision_log.md`, and
if any count was unsourceable a new question in `paper/logs/open_questions.md`. No prose and
no new experiment is produced.
