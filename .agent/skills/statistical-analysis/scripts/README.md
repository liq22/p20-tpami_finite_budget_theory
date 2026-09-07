# scripts/ — local README

Bundled helper for the `statistical-analysis` skill. Copied (adapted) from
K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see NOTICE.md and
`../../../../.agent/references/scientific_agent_skills_source.md`.

## assumption_checks.py

- **Purpose:** automated statistical-assumption checking for the analysis
  workflow — outlier detection (IQR + z-score), normality (Shapiro-Wilk +
  Q-Q plots), homogeneity of variance (Levene + box plots), and linearity.
- **Public API:**
  - `comprehensive_assumption_check(data, value_col, group_col=None, alpha=0.05)`
  - `check_normality(data, name, alpha=0.05, plot=True)`
  - `check_normality_per_group(...)`
  - `check_homogeneity_of_variance(...)`
  - `check_linearity(...)`
  - `detect_outliers(...)`
- **Inputs:** an in-memory pandas `DataFrame` (or 1-D array for normality).
  No file path is read. The caller is responsible for sourcing the data, e.g.
  from a run referenced in `paper/experiments/run_ledger.md`.
- **Outputs:** Python `dict` results containing test statistics, p-values,
  interpretation text, and recommendations. When `plot=True`, matplotlib
  figures are created in the active session (caller decides where to save).
- **Network:** none. Pure local computation.
- **File writes:** none directly. Any figure persistence must be done by the
  caller into `paper/assets/figures/`; record provenance in
  `paper/experiments/run_ledger.md`.
- **Credentials:** none required. If the surrounding workflow ever needs an
  external key, the user must provide it; never hardcode or store a key.

## Running

```bash
# from the skill scripts dir, or add it to sys.path
python -c "from assumption_checks import comprehensive_assumption_check; ..."
```

Add `scripts/` to `sys.path` (e.g. `sys.path.insert(0, "scripts")`) before
importing when running from the repo root.
