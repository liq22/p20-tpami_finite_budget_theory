# experimental-design scripts

Reproducible, seeded helpers that turn a design choice into a ready-to-use
allocation schedule or design-of-experiments (DOE) matrix. Both modules are
**pure computation**: they `import` numpy / pandas / pyDOE3, take arguments, and
return a `pandas.DataFrame`. They never touch the network and never write files —
the caller decides where to persist output (e.g. `df.to_csv(...)` into a chosen
workspace path).

## `randomization.py` — allocation schedules

- **Purpose:** produce reproducible random-assignment tables (simple, permuted
  block, stratified block, cluster, factorial run-order) so an experiment's
  allocation is auditable and can be archived / re-generated from a seed.
- **Public API:** `simple_randomization`, `block_randomization`,
  `stratified_block_randomization`, `cluster_randomization`,
  `assign_factorial_runs`, `arm_balance`.
- **Inputs:** unit count or unit list, arm names, optional allocation `ratio`,
  integer `seed`.
- **Outputs:** a `pandas.DataFrame` with one row per unit/cluster and an `arm`
  (and `stratum`/`block` where relevant) column.
- **Dependencies:** `numpy`, `pandas`. (Stdlib-only would be possible; numpy is
  used for the RNG.)
- **Network:** none. **Writes:** none (returns a DataFrame).

## `doe_designs.py` — DOE matrices in real factor units

- **Purpose:** wrap `pyDOE3` so designs come back decoded into real-world factor
  levels (temperature in °C, concentration in mM) with named columns and a
  randomized `run_order`, instead of raw coded ±1 matrices.
- **Public API:** `full_factorial`, `two_level_factorial`,
  `fractional_factorial`, `plackett_burman`, `central_composite`,
  `box_behnken`, `latin_hypercube`.
- **Inputs:** a `factors` dict mapping factor name → `(low, high)` (continuous,
  two-level) or a level list (categorical); integer `seed`; design-specific
  options (e.g. `generator` for fractional, `center`/`alpha`/`face` for CCD).
- **Outputs:** a `pandas.DataFrame` in real units with a `run_order` column.
- **Dependencies:** `numpy`, `pandas`, `pyDOE3`. Install with
  `uv pip install "numpy>=1.26" "pandas>=2.0" pyDOE3` (pyDOE3 is the maintained
  successor to pyDOE/pyDOE2 and supplies factorial, fractional, Plackett-Burman,
  central-composite, Box-Behnken, and Latin-hypercube generators).
- **Network:** none. **Writes:** none (returns a DataFrame).

## Reproducibility note

Every function takes an integer `seed`. Persist the seed together with the
emitted schedule (e.g. in `paper/experiments/reproducibility.md` and
`paper/experiments/run_ledger.md`) so the exact layout can be regenerated for an
audit or trial registration.
