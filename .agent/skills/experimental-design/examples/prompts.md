# experimental-design — invocation scenarios

Realistic pre-data design invocations for the single-paper workflow. Each
scenario shows the inputs read from `paper/` and the artifacts written back. The
scripts referenced (`scripts/randomization.py`, `scripts/doe_designs.py`) are
pure local computation (numpy/pandas/pyDOE3): they return `pandas.DataFrame`s,
touch no network, and write no files — the caller persists output (e.g.
`df.to_csv(...)` into a chosen workspace path).

## Scenario 1: Blocked, stratified randomization for a two-arm preclinical trial

Context: a drug-vs-vehicle study is being planned. The experimental unit is the
mouse (treatment is injected per mouse), but samples are processed across two
sites and three batches, both known nuisance factors. The team needs a
reproducible allocation schedule that stays balanced across arms throughout
enrollment and across the site stratum, recorded so the analysis is
confirmatory and the layout is auditable.

Prompt:
> Read the framing in `paper/logs/decision_log.md` and confirm the experimental
> unit is the mouse with arms `["drug", "vehicle"]`. Use
> `scripts/randomization.py` (`stratified_block_randomization`) to produce a
> seeded allocation with site as the stratum (e.g. `{"siteA": 30, "siteB": 30}`,
> ratio `(1, 1)`, `seed=42`) and a second pass that additionally tags each unit
> with its processing batch so batch never aligns with arm. Sanity-check counts
> with `arm_balance`. Persist the schedule to
> `paper/assets/tables/allocation_schedule.csv` (caller-side `to_csv`) with a
> `run_order`/processing-order column, and record the design, replicate level
> (mouse, not cells), blocking/stratification structure, planned analysis, and
> seed in `paper/experiments/run_ledger.md`; record the exact function call,
> arguments, seed, and numpy/pandas versions in
> `paper/experiments/reproducibility.md`. Hand the chosen design to the
> **statistical-power** skill for sizing — do not compute n here. Flag any
> nuisance factor that cannot be blocked or randomized across into
> `paper/logs/open_questions.md` rather than leaving it confounded.

Inputs: `paper/logs/decision_log.md`, `scripts/randomization.py`,
`references/randomization_and_blocking.md`.

Outputs: `paper/assets/tables/allocation_schedule.csv`, a design row in
`paper/experiments/run_ledger.md`, a reproduction recipe in
`paper/experiments/reproducibility.md`, a planned-analysis note in
`paper/experiments/statistics.md`, open questions in
`paper/logs/open_questions.md`.

## Scenario 2: Fractional-factorial screening of seven process factors

Context: a wet-lab process has seven candidate factors (temperature,
concentration, pH, catalyst loading, stir speed, residence time, feed ratio) and
the team wants to find the few that actually matter, cheaply, before committing
to a full optimization. A two-level full factorial (2^7 = 128 runs) is
unaffordable; a resolution-III Plackett-Burman or a resolution-IV fractional
factorial is wanted, with run order randomized to defeat drift.

Prompt:
> Read the candidate factors and their `(low, high)` ranges from
> `paper/logs/open_questions.md` / `paper/logs/insights.md`. Use
> `scripts/doe_designs.py` (`plackett_burman`, or `fractional_factorial` with a
> stated generator) to produce a seeded screening design in real factor units
> with a randomized `run_order` (`seed=42`). Record the alias/resolution
> structure explicitly — for `fractional_factorial` state the generator and
> which main effects are aliased with which interactions — and write it into
> `paper/experiments/statistics.md` so no factor is later dismissed as inert
> without checking the aliasing. Persist the run table to
> `paper/assets/tables/screening_runs.csv` (caller-side `to_csv`). Log the
> design choice, replicate level, and resolution in
> `paper/experiments/run_ledger.md`; log the call, arguments, seed, and
> pyDOE3/numpy/pandas versions in `paper/experiments/reproducibility.md`. Note
> that this screening design cannot detect curvature, so if an interior optimum
> is later plausible the team must follow with a response-surface design
> (`central_composite`/`box_behnken`) — record that as a forward note in
> `paper/logs/decision_log.md`.

Inputs: `paper/logs/open_questions.md`, `paper/logs/insights.md`,
`scripts/doe_designs.py`, `references/factorial_and_doe.md`.

Outputs: `paper/assets/tables/screening_runs.csv`, an alias/resolution block in
`paper/experiments/statistics.md`, a design row in
`paper/experiments/run_ledger.md`, a reproduction recipe in
`paper/experiments/reproducibility.md`, a forward note in
`paper/logs/decision_log.md`.

## Scenario 3: Cluster-randomized layout with the cluster as the unit

Context: an intervention is delivered at the clinic level, so individual
patients cannot be randomized independently. The cluster (clinic) is the
experimental unit; analyzing patients as independent would pseudoreplicate. The
team needs the cluster-level randomization and a record that fixes the replicate
level before any data are collected.

Prompt:
> Confirm in `paper/logs/decision_log.md` that the intervention is delivered at
> the clinic level, so the clinic — not the patient — is the experimental unit.
> Use `scripts/randomization.py` (`cluster_randomization`) to assign the listed
> clinics to `["intervention", "control"]` with a fixed `seed`. Persist the
> cluster allocation to `paper/assets/tables/cluster_allocation.csv`
> (caller-side `to_csv`). State explicitly in `paper/experiments/run_ledger.md`
> that the replicate is the clinic and that patients-within-clinic are nested
> (not independent), so the planned analysis must use a cluster-level or
> mixed-model analysis matched to the design. Hand off to **statistical-power**
> for cluster-level sizing once a pilot ICC and cluster size are available; if
> either is missing, record the gap in `paper/logs/open_questions.md` and do not
> proceed to sizing. Record the call, arguments, and seed in
> `paper/experiments/reproducibility.md`.

Inputs: `paper/logs/decision_log.md`, `scripts/randomization.py`,
`references/design_types.md`.

Outputs: `paper/assets/tables/cluster_allocation.csv`, a replicate-level row in
`paper/experiments/run_ledger.md`, a reproduction recipe in
`paper/experiments/reproducibility.md`, a planned-analysis note in
`paper/experiments/statistics.md`, open questions in
`paper/logs/open_questions.md`.
