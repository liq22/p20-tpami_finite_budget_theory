# scripts/ — statistical-power

Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT).
Both scripts are stdlib + scientific-Python only. They are read-and-compute helpers;
they do not touch the network and do not delete or overwrite workspace files.

## power.py

- **Purpose:** unified closed-form power / sample-size interface over
  `statsmodels` and `scipy`. One entry point each for the four quantities
  people actually want.
- **Public API:** `sample_size(test, ...)`, `power(test, ...)`,
  `mde(test, ...)`, `power_curve(test, ...)`.
- **Supported `test=` values:** `t_ind`, `t_paired`/`t_one`, `anova`,
  `two_proportions`, `one_proportion`, `correlation`, `chi2`, `linear_regression`.
- **Inputs:** effect size (d / f / h / w / r / f²), α, target power, allocation
  `ratio`, `k_groups` (ANOVA), `dof` (chi²), `df_num`/`k_total` (regression).
- **Outputs:** returns numbers / arrays to the caller; **writes only when**
  `power_curve(save=<path>)` is passed, in which case it saves one PNG figure
  via `matplotlib.figure.savefig` to the path the caller chooses (typically
  `paper/assets/figures/`). Running `python power.py` with no args runs an
  internal smoke test that only prints to stdout.
- **Network:** none.
- **Dependencies:** `statsmodels>=0.14.6`, `scipy>=1.11`, `numpy`, `matplotlib`.
  (Use `statsmodels>=0.14.6` with `scipy>=1.11` to avoid `_lazywhere` import
  errors on SciPy 1.16+.)

## simulate_power.py

- **Purpose:** Monte Carlo power harness for designs with no closed-form
  formula (logistic/Poisson regression, mixed-effects models, cluster-randomized
  trials, survival, mediation, interactions).
- **Public API:** `simulate_power(gen_and_test, n, n_sims=2000, alpha=0.05, seed=0)`
  returns a `PowerEstimate(power, n_sims, n, ci_low, ci_high)`; `find_sample_size(...)`
  searches for the n that hits target power. Ships four worked examples
  (two-group difference, logistic regression, cluster-randomized with ICC,
  linear mixed model).
- **Inputs:** a caller-supplied `gen_and_test(n, rng)` that builds a dataset
  under the assumed effect and returns True if the planned test is significant;
  plus n, n_sims, alpha, seed.
- **Outputs:** returns a `PowerEstimate` to the caller (with a Wilson-score
  Monte Carlo CI). **Writes nothing** unless the caller wraps it. Running the
  module directly executes the four examples and prints to stdout only.
- **Network:** none.
- **Dependencies:** `numpy`, `scipy`, `statsmodels`; the survival example also
  uses `lifelines` (optional).

## Reproducibility

Record the library versions, `seed`, `n_sims`, and the exact command/script in
`paper/experiments/run_ledger.md` and `paper/experiments/reproducibility.md` so
any reported power figure can be regenerated.
