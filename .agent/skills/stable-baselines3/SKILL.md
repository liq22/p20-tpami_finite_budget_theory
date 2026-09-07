---
name: stable-baselines3
description: 'Implementation skill: Stable Baselines3 RL recipes (PPO/SAC/DQN/TD3), Gymnasium envs, callbacks, evaluation into paper/experiments/. Use for single-agent RL. Do not use for DL training (pytorch-lightning), classical ML (scikit-learn), plotting (scientific-visualization), or Bayesian modeling (pymc). Prefer planning skill as primary.'
---

# stable-baselines3

## Purpose

Provide implementation guidance and reference material for reinforcement-learning
(RL) experiments with Stable Baselines3 (SB3): algorithm selection (PPO, SAC,
DQN, TD3, DDPG, A2C), custom Gymnasium environments, vectorized environments,
callbacks, hyperparameter schedules, and `evaluate_policy`-based evaluation. In
Auto-01-tiny-research this skill is a TIER B implementation-only supporting
skill: it documents the RL recipes and protocols that produce evidence backing
the paper's RL claims, and maps every result onto the `paper/experiments/`
ledger so downstream skills (`08-markdown-draft`, `09-tex-freeze-formalize`,
`13-reviewer-response`) can cite it. It is a supporting tool; the relevant
planning skill should be preferred as primary when one exists.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` requires an RL training or
  evaluation result (mean episode reward, success rate, sample efficiency) on a
  Gymnasium environment logged in `paper/experiments/run_ledger.md`.
- You need to document a custom Gymnasium environment (observation/action space,
  reward shaping, termination) so a reviewer can reproduce it from
  `paper/experiments/reproducibility.md`.
- A reviewer asks for hyperparameter sweeps, ablations across algorithms, or
  reward-scaling justifications (`paper/reviews/response_to_reviewers.md`,
  `paper/experiments/ablation.md`).
- A model-comparison or ablation table for RL algorithms is needed in
  `paper/assets/tables/` and the formal `paper/tex/` draft.
- You need callback-based evaluation/checkpointing recipes (EvalCallback,
  CheckpointCallback) documented for the methods section.

Do not use this skill for general deep-learning training engineering (defer to
pytorch-lightning), classical ML (scikit-learn), plot rendering
(scientific-visualization), Bayesian modeling (pymc), multi-agent or
massively-parallel RL training (pufferlib/sb3-contrib are out of scope here),
or any non-Python RL stack. It is also not an execution harness: in this repo it
documents and recipes RL analyses; it does not run production training jobs or
ship executable training/inference scripts.

## Required Inputs

- A Gymnasium environment spec (env id, or a fully specified custom env:
  observation space, action space, reward function, termination/truncation
  rules) referenced from `paper/experiments/run_ledger.md`. Do not invent envs.
- The claim ID(s) this RL run must support, from
  `paper/experiments/evidence_matrix.md`, so each metric can be tied back.
- The evaluation metric and protocol mandated by
  `paper/refs/target_journal.md` and `paper/experiments/statistics.md`
  (e.g. mean +/- std reward over N evaluation episodes with fixed seeds).
- The algorithm and a hyperparameter config (learning rate, batch size, buffer
  size, network architecture, schedule) selected via
  `references/algorithms.md`; record every candidate in
  `paper/experiments/ablation.md`.
- A target output path for any persisted result under `paper/experiments/` or
  `paper/assets/tables/`.
- stable-baselines3 >= 2.8 with PyTorch >= 2.3 and Python 3.10+; optional
  Gymnasium extras (mujoco, atari) and TensorBoard. The user is responsible for
  installing these; this skill does not pin or ship a runtime.
- No API keys or credentials are required by SB3 itself. If an environment,
  dataset, or model hub needs a credential (e.g. a private dataset token), the
  user must provide it; never hardcode or store it.

## Workflow

1. Read the target claim and its required metric from
   `paper/experiments/evidence_matrix.md` and `paper/refs/target_journal.md`.
   Do not pick a metric the journal or claim does not sanction.
2. Confirm the environment is logged in `paper/experiments/run_ledger.md`; if it
   is absent or unlogged, stop (see Stop With) rather than substituting an env.
3. Select the algorithm using `references/algorithms.md`: PPO/A2C for
   general-purpose on-policy, SAC/TD3 for continuous off-policy control, DQN for
   discrete off-policy, HER for goal-conditioned tasks. Document the rationale.
4. Specify the custom env via `references/custom_environments.md` if needed
   (inherit `gymnasium.Env`, implement `reset`/`step`, image obs as `np.uint8`
   in `[0,255]`, channel-first). Validate with `check_env()` before training and
   record the result.
5. Set up vectorized environments via `references/vectorized_envs.md`
   (`DummyVecEnv` vs `SubprocVecEnv`) when throughput matters; for off-policy
   with multiple envs set `gradient_steps=-1`. Document the choice.
6. Configure callbacks via `references/callbacks.md` (EvalCallback for best-model
   selection, CheckpointCallback for snapshots) so the run is auditable.
7. Fix and record all seeds (`seed`, `random_state`, env seeds) for
   reproducibility; document learning-rate schedules and `policy_kwargs`.
8. Evaluate with `evaluate_policy(model, env, n_eval_episodes=N,
   deterministic=True)` using the journal-mandated protocol; report mean +/- std
   and, where required, a CI from `paper/experiments/statistics.md`.
9. Persist: append a run row to `paper/experiments/run_ledger.md` (algorithm,
   env, hyperparameters, metric, CI, seeds, data/env ref, claim ID), write an
   ablation/comparison table to `paper/assets/tables/` and mirror it in
   `paper/experiments/ablation.md`, update the claim status in
   `paper/experiments/evidence_matrix.md` (`supported`/`partial`/`refuted`),
   and record versions + seeds in `paper/experiments/reproducibility.md`.
10. Surface non-trivial decisions in `paper/logs/decision_log.md`; record
    negative results (e.g. algorithm failed to learn) honestly in
    `paper/experiments/dead_ends.md` instead of suppressing them.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` with: algorithm, env id/spec,
  vectorization, hyperparameter config, evaluation protocol (N episodes,
  deterministic flag), point metric + CI, seeds, and the data/env + claim IDs.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim the
  run addresses (`supported` / `partial` / `refuted` / `unsupported`).
- An ablation/model-comparison table under `paper/assets/tables/` when more than
  one algorithm or hyperparameter set was compared; mirror it in
  `paper/experiments/ablation.md`.
- A statistical note in `paper/experiments/statistics.md` when CIs or tests over
  evaluation episodes were computed.
- A reproducibility note in `paper/experiments/reproducibility.md` covering SB3,
  PyTorch, Gymnasium, and ale-py/mujoco versions, all seeds, env spec, and the
  exact data/env ref.
- Optional decision/dead-end entries in `paper/logs/decision_log.md` and
  `paper/experiments/dead_ends.md`.
- No executable training/inference scripts and no model weights shipped into the
  repo (this is a paper repo, not an RL runtime); code stays as documented
  recipes in `references/`. The replay buffer is never persisted.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only stable-baselines3`
- `python src/S03_Scripts/validate_project.py`
- Confirm every RL run referenced by `paper/experiments/evidence_matrix.md` has a
  matching row in `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm no metric is reported for a claim the matrix marks `unsupported`,
  `missing_evidence`, or `refuted`.
- Confirm all seeds (algorithm `seed`, env seeds) and SB3/PyTorch/Gymnasium
  versions are recorded in `paper/experiments/reproducibility.md`.
- Confirm the custom env passed `check_env()` (cite the validation result);
  image observations are `np.uint8` in `[0,255]` where applicable.
- Confirm evaluation used the journal-mandated episode count and deterministic
  policy flag from `paper/refs/target_journal.md`.

## Boundaries

- Do not run general deep-learning training engineering here; defer to
  pytorch-lightning. RL with SB3 only.
- Do not fabricate rewards, episode counts, or benchmark numbers; if a result is
  missing, mark the claim `missing_evidence` and stop.
- Do not persist raw trained models, replay buffers, `.zip`/`.pth`/`.ckpt`
  artifacts, or recorded videos into the paper repo; record recipes and metrics,
  not weights or large binaries.
- Do not copy the upstream `scripts/` executable training/inference code into
  this repo; this skill ships `references/` documentation only.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/`, and the designated logs; never into `paper/tex/`,
  `paper/refs/`, or `paper/submission/`.
- Do not treat multi-agent systems, massively parallel RL (pufferlib), or
  experimental algorithms (sb3-contrib: MaskablePPO, RecurrentPPO) as in scope
  beyond a one-line pointer; surface them in `paper/logs/open_questions.md`.

## Stop With

- The environment or data needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The required evaluation metric or protocol is unspecified by
  `paper/refs/target_journal.md` / `paper/experiments/statistics.md` and the user
  has not disambiguated (e.g. number of evaluation episodes, deterministic flag).
- The custom env fails `check_env()` and the user has not authorized proceeding
  with the documented caveat.
- SB3 or a required dependency (PyTorch, Gymnasium, mujoco/ale-py extra) is
  unavailable and the user cannot install it; do not silently fall back to a
  different RL library.
- Training did not converge and the result would contradict the claim's required
  direction; if the user has not authorized reporting a `refuted` finding,
  surface it in `paper/logs/decision_log.md` and wait rather than overstate it.

## References

- Algorithm selection & characteristics: `.agent/skills/stable-baselines3/references/algorithms.md`
- Custom Gymnasium environments: `.agent/skills/stable-baselines3/references/custom_environments.md`
- Vectorized environments & wrappers: `.agent/skills/stable-baselines3/references/vectorized_envs.md`
- Callbacks (EvalCallback, CheckpointCallback, custom): `.agent/skills/stable-baselines3/references/callbacks.md`
- Invocation scenarios: `.agent/skills/stable-baselines3/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/dead_ends.md`, `paper/experiments/insights.md`,
  `paper/assets/tables/`, `paper/refs/target_journal.md`,
  `paper/logs/decision_log.md`, `paper/logs/open_questions.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://stable-baselines3.readthedocs.io/en/master/ ,
  https://gymnasium.farama.org/
