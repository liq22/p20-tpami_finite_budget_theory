# statistical-analysis — invocation scenarios

Realistic prompts for the `statistical-analysis` skill. Each maps onto the
`paper/` workspace. These are examples, not the only valid invocations.

---

## Scenario 1: Two-group comparison with assumption violations

> I have accuracy scores for a proposed method vs a baseline from the run logged
> in `paper/experiments/run_ledger.md` (run id `R-014`, claim `C-02` in
> `paper/experiments/evidence_matrix.md`). 48 vs 52 samples. Group B looks
> skewed. Run the appropriate two-group comparison, check assumptions first,
> give me Cohen's d with a CI, and write the APA block into
> `paper/experiments/statistics.md`. If parametric assumptions fail, switch to
> the non-parametric alternative and record the decision in
> `paper/logs/decision_log.md`.

Expected flow: select independent t-test → run
`comprehensive_assumption_check` → if Levene significant use Welch's t, if
normality severely violated use Mann-Whitney U → compute Cohen's d (+CI, or
rank-biserial for the non-parametric case) → emit APA results block → update
evidence matrix verdict.

---

## Scenario 2: A-priori power analysis before data collection

> We're planning an ablation with 3 conditions (full model, no-aux-loss, baseline)
> and expect a medium effect (f = 0.25). What sample size per condition do we
> need for 80% power at alpha = 0.05? Record the planned n and the rationale in
> `paper/logs/decision_log.md` so the experiment-ops skill can size the run, and
> note the sensitivity bound in `paper/experiments/reproducibility.md`.

Expected flow: one-way ANOVA power analysis with `FTestAnovaPower` → report
required n per group → flag that post-hoc power will not be reported → also
report the minimum detectable effect at the chosen n as a sensitivity bound.

---

## Scenario 3: Bayesian alternative for an underpowered result

> The frequentist t-test for claim `C-07` came back p = 0.08 with n = 22 per
> group — underpowered. Run a Bayesian independent-samples t-test with weakly
> informative priors, report BF10, the 95% credible interval for the mean
> difference, and the posterior probability that the proposed method is better.
> Confirm convergence (R-hat, ESS) and write the block to
> `paper/experiments/statistics.md`. Then draft the reviewer-response note in
> `paper/reviews/response_to_reviewers.md` explaining why the Bayesian result
> is the more informative framing.

Expected flow: PyMC model → sample → ArviZ convergence diagnostics → report
BF (or Savage-Dickey if no dedicated BF tool), HDI, posterior probability →
update evidence matrix verdict (likely `inconclusive` with quantified evidence
*for* vs *against* the null) → never overclaim a small n result.
