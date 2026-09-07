# statistical-power — invocation scenarios

Realistic a priori power-analysis invocations for the single-paper workflow. Each
scenario shows the inputs read from `paper/` and the artifacts written back. The
scripts referenced (`scripts/power.py`, `scripts/simulate_power.py`) write only
to caller-chosen paths and touch no network.

## Scenario 1: A priori sample size for a two-group primary endpoint (closed-form)

Context: the study compares a treatment to control on a continuous outcome. The
team has agreed a Cohen's d = 0.50 as the smallest effect of clinical interest.
The power analysis must support the Methods section and the pre-registration
before any participant is enrolled.

Prompt:
> Read `paper/experiments/run_ledger.md` to confirm the planned analysis is a
> two-sample t-test, then use `scripts/power.py` to compute the required n per
> group for Cohen's d = 0.50, α = 0.05 (two-sided), power = 0.80, and again at
> power = 0.90. Then run a sensitivity analysis across d = 0.40–0.60 and save
> the power curve to `paper/assets/figures/power_curve_primary.png` with a
> caption and first callout. Apply a 20% attrition adjustment to report the
> enrolled n. Write the full justification (test, effect-size basis with its
> citation from `paper/refs/references.bib`, α, power, computed n per group and
> total, enrolled n after dropout, library versions) into
> `paper/experiments/statistics.md`, the figure caption into
> `paper/experiments/evidence_matrix.md`, and a sample-size justification
> paragraph into `paper/draft/methods.md`. Log the effect-size choice and the
> power target in `paper/logs/decision_log.md`.

Inputs: `paper/experiments/run_ledger.md`, `paper/refs/references.bib`,
`scripts/power.py`, `references/closed_form_recipes.md`,
`references/effect_sizes.md`.

Outputs: a power block in `paper/experiments/statistics.md`,
`paper/assets/figures/power_curve_primary.png`, a row in
`paper/experiments/evidence_matrix.md`, a paragraph in `paper/draft/methods.md`,
a decision in `paper/logs/decision_log.md`.

## Scenario 2: Simulation-based power for a cluster-randomized design

Context: clinics (not patients) are randomized, so a closed-form t-test would
pseudoreplicate. There is a pilot ICC and cluster size; the planned analysis is
a linear mixed model. There is no closed-form formula.

Prompt:
> Confirm in `paper/experiments/run_ledger.md` that the planned analysis is a
> linear mixed model with a random clinic intercept, and read the pilot ICC and
> cluster size from `paper/experiments/statistics.md`. Use
> `scripts/simulate_power.py` to write a `gen_and_test(n, rng)` that simulates
> the cluster-randomized data under the agreed effect and fits the exact mixed
> model, then estimate power at n = 10, 14, 18 clusters per arm with 5,000 sims
> each and a fixed seed. Report the power and its Monte Carlo 95% CI at each n
> into `paper/experiments/statistics.md`, and search with `find_sample_size`
> for the smallest n per arm reaching 0.80 power. Record the data-generating
> assumptions (baseline, residual SD, ICC, cluster size, seed, n_sims, library
> versions) and the reproduction command in
> `paper/experiments/reproducibility.md`. Save the power-vs-clusters figure to
> `paper/assets/figures/` with a caption. Flag any unresolved assumption into
> `paper/logs/open_questions.md` — do not invent the ICC or effect size.

Inputs: `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
`scripts/simulate_power.py`, `references/simulation_based_power.md`,
`references/effect_sizes.md`.

Outputs: simulation power table + MDE in `paper/experiments/statistics.md`,
reproducibility record in `paper/experiments/reproducibility.md`, figure in
`paper/assets/figures/`, open assumptions in `paper/logs/open_questions.md`.

## Scenario 3: Minimum detectable effect (MDE) at a fixed sample budget

Context: the funder caps enrolment at 30 participants per group. The question is
not "how many do we need" but "what can we actually detect" — to be honest about
the study's limits in the Methods and the limitations section.

Prompt:
> Read the fixed n = 30/group and α = 0.05 (two-sided) from
> `paper/experiments/run_ledger.md`, and use `scripts/power.py` `mde(...)` to
> report the minimum detectable Cohen's d at power = 0.80. Then produce a
> sensitivity curve of detectable d across n = 20–40/group and save it to
> `paper/assets/figures/mde_sensitivity.png` with a caption and first callout.
> Do NOT compute observed/post-hoc power. Write the MDE and its interpretation
> into `paper/experiments/statistics.md`, a sentence acknowledging the
> detectable-effect limit into `paper/draft/discussion.md` (limitations), and
> the design-effect / power choice into `paper/logs/decision_log.md`.

Inputs: `paper/experiments/run_ledger.md`, `scripts/power.py`,
`references/closed_form_recipes.md`, `references/effect_sizes.md`.

Outputs: MDE block in `paper/experiments/statistics.md`,
`paper/assets/figures/mde_sensitivity.png`, a limitations sentence in
`paper/draft/discussion.md`, a decision in `paper/logs/decision_log.md`.
