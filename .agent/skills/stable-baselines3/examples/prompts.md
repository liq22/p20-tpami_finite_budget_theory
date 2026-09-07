# stable-baselines3 — invocation scenarios

Realistic prompts for invoking the stable-baselines3 implementation skill inside
the Auto-01-tiny-research workspace. Each scenario shows the kind of request
that should trigger this skill, the artifacts it reads, and the workspace
outputs it must produce. Remember: in this repo the skill documents and recipes
RL analyses — it does not ship executable training scripts or model weights.

## Scenario 1: PPO baseline on a Gymnasium env for a sample-efficiency claim

> The paper claims our PPO agent reaches the CartPole-v1 reward threshold in
> fewer steps than the baseline reported in `paper/experiments/run_ledger.md`
> (run `R-011`). The target journal (`paper/refs/target_journal.md`) wants mean
> +/- std reward over 20 evaluation episodes with a deterministic policy and a
> 95% CI. Document the PPO recipe (MlpPolicy, learning rate, n_steps, batch
> size, seed), evaluate, and update claim `C-05` in
> `paper/experiments/evidence_matrix.md`.

This triggers stable-baselines3 because the request is single-agent RL with a
standard on-policy algorithm (PPO) on a Gymnasium environment — exactly the
recipe this skill documents. The skill reads the env ref and claim requirements,
selects PPO via `references/algorithms.md`, documents the hyperparameter config
and seed, specifies EvalCallback-based best-model selection
(`references/callbacks.md`) and the evaluation protocol from
`references/algorithms.md`, then writes a run row to
`paper/experiments/run_ledger.md`, updates `C-05` in
`paper/experiments/evidence_matrix.md`, and records SB3/PyTorch/Gymnasium
versions + seed in `paper/experiments/reproducibility.md`. Do NOT use
pytorch-lightning or a custom training loop here; do NOT persist a `.zip` model
or replay buffer into the repo — record the recipe and metrics only.

## Scenario 2: SAC vs TD3 ablation on a continuous-control custom env

> I need an ablation table comparing SAC and TD3 on our custom continuous-control
> environment (spec in `paper/experiments/run_ledger.md`, run `R-014`), to go
> into `paper/assets/tables/ablation_rl.tex` and `paper/experiments/ablation.md`.
> Use the same observation/action space, reward scaling, and evaluation protocol
> so the comparison is fair. Mark any variant that does not significantly beat
> the SAC baseline as `partial` in the evidence matrix.

This triggers stable-baselines3: multi-algorithm comparison on a continuous
action space with off-policy algorithms and a fixed evaluation protocol. The
skill pulls the selection guide from `references/algorithms.md` (SAC vs TD3
tradeoffs), documents the custom env from
`references/custom_environments.md` (and confirms `check_env()` passed),
specifies vectorized envs + `gradient_steps=-1` per
`references/vectorized_envs.md`, runs the same N-episode deterministic
evaluation, applies any multiple-comparison correction noted in
`paper/experiments/statistics.md`, and emits both the LaTeX table into
`paper/assets/tables/` and a mirrored markdown table in
`paper/experiments/ablation.md`. Each variant gets its own run row in
`paper/experiments/run_ledger.md`; the evidence matrix is updated per variant.
Honest negative results go to `paper/experiments/dead_ends.md` rather than being
dropped, and any open question about multi-agent extensions goes to
`paper/logs/open_questions.md` (out of scope here — defer to pufferlib).

## Scenario 3: Custom Gymnasium environment for a goal-conditioned task with HER

> We are introducing a new goal-conditioned manipulation env in the methods
> section. Document the env spec (observation/action spaces, reward, termination)
> and a SAC + HerReplayBuffer recipe so reviewers can reproduce it from
> `paper/experiments/reproducibility.md`. Record the env-check result and the
> goal-selection strategy.

This triggers stable-baselines3 for the custom-env authoring and the HER recipe:
the skill follows `references/custom_environments.md` (inherit `gymnasium.Env`,
`reset`/`step` signatures, image-obs dtype rules, `check_env()`), documents the
SAC + `HerReplayBuffer` configuration (`MultiInputPolicy`,
`n_sampled_goal`, `goal_selection_strategy`) per `references/algorithms.md`, and
records env spec + check result + versions + seeds in
`paper/experiments/reproducibility.md`, with a run row in
`paper/experiments/run_ledger.md`. It does NOT render any env visualization
itself — scientific-visualization owns figure rendering into
`paper/assets/figures/`; this skill only produces the spec and the analytic
justification. If `check_env()` fails, stop and surface it in
`paper/logs/decision_log.md` rather than proceeding silently.
