---
name: transformers
description: Support a selected PaperTrace code or experiment task with explicit Hugging Face model, tokenizer or processor, inference, generation, or Trainer behavior and directly inspected outputs.
---

# Transformers

## Purpose

Use Hugging Face Transformers when the selected task requires a pretrained
checkpoint, tokenizer or processor, pipeline inference, controlled generation, or
Trainer-based fine-tuning.

This is a supporting capability. The primary Skill owns the task, data semantics,
comparison, metric, experiment design, and claim boundary. Transformers provides
the smallest correct model-loading, preprocessing, inference, or fine-tuning
implementation.

## Workflow

1. Confirm the task, input/output schema, labels, split, independent unit,
   baseline, metric, and requested artifact. Stop rather than infer missing
   scientific semantics.
2. Identify the exact model and tokenizer/processor source. Record the model ID,
   revision when reproducibility requires it, license or access conditions, and
   any custom code boundary.
3. Inspect the installed package and current official model/API documentation
   before using version-sensitive classes or arguments. Do not assume a fixed
   repository-wide Transformers or PyTorch version.
4. Use the smallest fitting interface:
   - a pipeline for bounded standard inference when its defaults are explicit and
     acceptable;
   - explicit model plus tokenizer/processor when preprocessing, batching,
     outputs, devices, or generation need control;
   - Trainer only when the task actually requires fine-tuning.
5. Make preprocessing semantics explicit: special tokens, truncation, padding,
   sequence/window construction, label alignment, sampling, and train-only fitted
   transforms. Check that no target or evaluation information enters the input.
6. For generation, fix and report the decoding configuration that affects the
   comparison. Do not compare methods under different prompt, context, stopping,
   or sampling budgets without declaring the difference.
7. Use `trust_remote_code` only when the selected model requires reviewed custom
   code and the user accepts that execution boundary. Never substitute an
   ungated or different model silently when access fails.
8. Run the bounded inference or the approved fine-tuning configuration through
   the primary execution path. Inspect actual outputs, shapes, labels, decoded
   samples, metrics, unit counts, and failure messages.
9. Save the requested source/configuration and result. Keep downloaded weights and
   caches outside the paper repository; record the model identity and loading
   contract needed to reproduce the run.
10. Preserve null, negative, unstable, and contradictory outcomes. Update the
    scientific claim or boundary through the primary Skill rather than selecting
    a more favorable checkpoint or decoding setup after the fact.
11. Run one closest test, sample inference, or experiment smoke path and stop.

## Output Contract

Return the direct product requested by the primary Skill, together with:

- model and tokenizer/processor identity and relevant access/license boundary;
- preprocessing, prompt/context, generation, or training configuration that
  affects meaning;
- actual output path, dimensions, representative checked outputs, and metrics;
- comparison fairness and any unresolved model/data limitation;
- one direct validation.

A model-card citation, configuration summary, run row, or generated narrative
cannot replace executable source and actual outputs.

## Boundaries

- Do not require target-journal, statistics, ablation, reproducibility,
  decision-log, dead-end, insight, or review files before using user-supplied data
  or models.
- Do not hard-code package versions, checkpoint choices, decoding settings,
  metric suites, confidence intervals, or training budgets as universal rules.
- Do not silently change model revision, tokenizer, truncation, prompt, context
  length, precision, device placement, dataset, split, or evaluation metric.
- Do not use a larger or gated model merely because it is available, and do not
  treat model scale as evidence of a stronger baseline.
- Do not use an LLM-as-judge or generated score unless the primary experiment
  defines its rubric, independence, uncertainty, and failure boundary.
- Do not paste access tokens into source, notebooks, logs, or committed
  configuration. Use the environment or the user's approved credential store.
- Do not commit downloaded model weights or caches to the paper repository.
- Do not suppress or delay a result because it weakens or refutes the claim.
- Do not create a generic model hub, prompt registry, training framework,
  fallback model chain, or extra record system.
