---
name: pytorch-lightning
description: Support a selected PaperTrace code or experiment task with a minimal, explicit PyTorch Lightning training loop, configuration, and directly inspected run outputs.
---

# PyTorch Lightning

## Purpose

Use PyTorch Lightning when a selected implementation or experiment benefits from
its structured training loop, callbacks, logging, checkpointing, or distributed
execution.

This is a supporting capability. `code-change` owns implementation defects and
`06-experiment-ops` owns execution of an approved run. The primary Skill defines
the model, data, split, objective, metric, comparison, and claim boundary.
Lightning must not replace those decisions.

## Workflow

1. Confirm the task, model inputs and outputs, labels, sampling unit, data split,
   objective, metric, baseline, and execution environment. Stop when any
   scientific meaning is ambiguous.
2. Inspect the installed `lightning`/PyTorch versions and the current official API
   before using version-sensitive arguments. Do not rely on a repository-wide
   version or strategy rule.
3. Reproduce the relevant current behavior with the smallest direct path before
   refactoring it into Lightning.
4. Implement only the required structure:
   - a `LightningModule` for model behavior and optimization;
   - a `LightningDataModule` only when shared data lifecycle code is useful;
   - callbacks and loggers only when the active run needs them.
5. Keep the data contract explicit. Fit transforms and statistics on training data
   only, preserve group or temporal splits, and ensure each process observes the
   intended samples.
6. Make run-affecting settings explicit: seed, devices, accelerator, precision,
   accumulation, stopping rule, monitored metric, checkpoint policy, and
   distributed strategy. Choose them from the actual model, hardware, and
   comparison rather than parameter-count thresholds.
7. Run one bounded smoke path to catch implementation errors. A smoke run is not
   scientific evidence.
8. When the primary task authorizes execution, run the approved configuration and
   inspect the actual losses, metrics, unit counts, checkpoints, and failure
   messages. Verify that logged metrics use the intended aggregation and split.
9. Save the requested source/configuration and actual result. Keep large
   checkpoints outside the paper repository unless the user explicitly designates
   an artifact location; record the path and loading contract needed to reproduce
   the result.
10. Preserve null, negative, unstable, and contradictory outcomes and update the
    claim or boundary through the primary Skill.
11. Run the closest code test or experiment smoke path once and stop.

## Output Contract

Return the direct product requested by the primary Skill, together with:

- source files and the relevant Lightning module/data-module boundary;
- the exact run configuration that affects scientific interpretation;
- actual output paths, metrics, variability, and unit counts;
- checkpoint selection and metric-aggregation semantics;
- any environment, data, or distributed-execution limitation;
- one direct validation.

A Trainer configuration, logger dashboard, callback list, or run record cannot
replace executable source and actual run outputs.

## Boundaries

- Do not require target-journal, statistics, ablation, reproducibility,
  decision-log, dead-end, insight, or review files before implementing or running
  the requested task.
- Do not hard-code Lightning/PyTorch versions, model-size thresholds, device
  counts, precision policies, batch-size scaling, or DDP/FSDP/DeepSpeed choices.
- Do not migrate a working training loop to Lightning without a concrete
  readability, reuse, execution, or correctness benefit.
- Do not add a DataModule, callback stack, logger stack, distributed strategy, or
  configuration framework merely because Lightning supports it.
- Do not silently fall back to a different device, precision, strategy, data
  loader, checkpoint, or metric after failure.
- Do not report a smoke run, successful process exit, or logger availability as
  scientific evidence.
- Do not commit credentials or large model checkpoints. Load external-service
  credentials from the environment only when the user has selected that service.
- Do not suppress a result or wait for authorization merely because it weakens or
  refutes the current claim.
- Do not create training wrappers, experiment registries, fallback stacks,
  dashboards, or additional logging surfaces around one task.
