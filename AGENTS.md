# Agent Entry

PaperTrace exposes two host entrypoints:

- `00-router`: default route-and-execute front door;
- `grill-me`: explicit read-only decision pressure test.

All other skills are internal modules under `.agent/skills/`.

## Highest authority

PaperTrace exists to reduce the scientific uncertainty that blocks the next
reliable research decision. It does not exist to complete a fixed SOP.

Before a substantial action, answer:

```text
Q1. What current claim is most at risk?
Q2. What is the largest unresolved uncertainty threatening it?
Q3. What is the smallest action whose possible outcomes could change the claim or next decision?
```

If no plausible outcome changes the research judgment, do not perform the action.

Use this adaptive loop:

```text
current claim
-> largest uncertainty
-> competing explanations
-> smallest discriminating action
-> predeclared outcome meanings
-> real evidence
-> updated claim, mechanism, boundary, or novelty
-> stop or iterate
```

Do not continue merely because a workflow has a next stage. Use
`.agent/references/research_first_paper_loop.md` as the detailed contract and load
only the relevant section.

## Direct product execution

The primary task is the scientific or engineering product requested by the user:
research decision, manuscript reasoning, code behavior, experiment result,
analysis, figure/table, or submission material.

```text
understand the decision and target product
-> inspect only necessary inputs
-> change the primary product directly
-> run the smallest check that tests the change
-> update the scientific decision
-> stop
```

A task is not complete when only a plan, report, matrix, manifest, ledger,
checklist, route trace, validation output, or documentation file changed unless
that item was explicitly requested.

## Adaptive research state

Maintain only what chooses the next action:

```text
Central question
Current claim
Supporting evidence
Strongest competing explanation
Largest unresolved uncertainty
Current novelty risk
Most informative next action
Stopping condition
```

Unknowns remain `TODO`, `unknown`, `unsupported`, or `post-hoc interpretation`.
Do not fill them for template completeness.

## Scientific priority

Use this order when choices compete:

1. correct research question and problem boundary;
2. correct data, labels, metadata, split, transforms, objective, and metric;
3. implementation matches the claimed mathematical problem;
4. experiment distinguishes the intended explanations;
5. result is credible, interpretable, and reproducible;
6. novelty survives closest-prior-art falsification;
7. method or theory can be simplified or improved;
8. code is clear enough for researchers to modify;
9. targeted tests protect scientific semantics;
10. general engineering hardening.

Novelty should emerge from a real failure, contradiction, mechanism, constraint,
invariant, boundary, task, or evaluation protocol—not from module count.

## Priority by task type

- Research question: claim at risk -> uncertainty -> competing explanations ->
  decisive test -> claim tree.
- Literature: search the strongest prior art against novelty, including equivalent
  terms and neighboring fields; verify exact overlap and the remaining meaningful
  distinction.
- Theory: seek counterexamples first -> minimum assumptions -> observable
  prediction -> experiment.
- Method: failure -> competing mechanism -> minimal intervention -> testable
  signature -> boundary.
- Code: reproduce behavior -> change source -> targeted test -> stop.
- Experiment: define claim, unit, fairness, possible outcomes, decision rule -> run
  only when an outcome could change the research judgment.
- Statistics: estimand -> independent unit -> simplest valid model -> uncertainty
  -> claim boundary.
- Manuscript: evidence -> argument -> paragraph clarity -> minimal wording and
  formatting.
- Figure/table: correct data and message -> honest encoding -> minimal styling.
- Review: discover new independent P0/P1 science; stop when additional lenses add
  no new major issue.

Do not refine colors, spacing, headings, prose rhythm, table layout, or report
format while the underlying content remains incomplete or incorrect.

## Scientific fail-fast

For dataset, label, metadata, sampling rate, window, stride, split, transform,
task, objective, metric, model, checkpoint, or protocol inconsistencies:

```text
detect semantic inconsistency
-> clear error
-> stop
```

Do not guess, silently repair, infer user intent, select a replacement task, or
fall back to a different scientific problem. Operational recovery is allowed only
when experiment semantics remain unchanged.

## Hypothesis provenance

For every major hypothesis distinguish:

```text
H0: proposed before the relevant result
H1: inspired by exploratory evidence
H2: independently confirmed
H3: still a post-hoc interpretation
```

Do not rewrite H1 or H3 as H0. Facts, inferences, exploratory findings, and
confirmatory evidence remain distinct in analysis and manuscript prose.

## Abstraction threshold

Before adding a validator, wrapper, fallback, cache, factory, registry, schema,
test, CI rule, or metadata field, ask:

1. Does it solve a real observed/current problem?
2. Could the scientific conclusion be wrong without it?
3. Is there a simpler direct implementation?

If the first two answers are no, do not add it. If the third is yes, use the
simpler option. Abstract only after at least two real current use cases exist and
only when the abstraction does not hide the data flow or mathematical objective.

## Python boundary

Use Python for numerical computation, signal/data processing, simulation,
training, inference, statistics, plotting, necessary file generation, and tests of
scientific semantics.

Do not write or run Python merely to count headings, scan wording, score prose,
check ordinary Markdown, wrap an existing shell/Git/CLI operation, generate status
reports, prove completion, silently repair scientific inputs, or enumerate
hypothetical edge cases.

## Integrity boundary

PaperTrace is a research workspace, not a security or forensic system.

- Do not proactively create custom hashes, tree digests, hash chains, receipts,
  ledgers, integrity proofs, or manifest checks.
- An upstream official checksum may be used only for a real download, after actual
  corruption, or when the user explicitly requests content verification.
- Git commit pins identify dependency versions; do not wrap them in a second
  digest system.
- Reproducibility uses understandable information: code version, config, data
  version, command, seed, environment, metric, result path, and date.

## Corner-case discipline

Handle only:

1. a failure already observed;
2. a realistic common user error;
3. a case required by the active protocol;
4. an error that could change a scientific conclusion, corrupt data, expose
   credentials, incur cost, publish externally, or destroy remote work;
5. a cheap local check that does not expand the architecture.

Otherwise fail clearly or record one concrete TODO. Do not let hypothetical edge
conditions drive the main design.

## Minimal validation

Default validation is one direct check:

| Change | Default check |
|---|---|
| manuscript paragraph/section | reread target and adjacent context; verify changed citations/numbers |
| literature/novelty conclusion | verify the load-bearing original sources and closest prior art |
| method/theory | check failure, competing explanation, counterexample, assumptions, prediction, comparison, boundary |
| code | run the closest targeted test or smoke test |
| experiment | inspect actual output, independent unit, fairness, metrics, uncertainty, and outcome decision |
| figure/table | open the asset; check data, labels, units, caption, readability |
| LaTeX | compile once |
| submission files | confirm required files exist and open |
| agent/validator rule | run only the affected validator/test |

Run the full repository test suite once at final PR review, not after every small
change. Never repeat validation without an intervening product change.

## Routing and context

1. Read `paper/paper.yaml` only when the task depends on paper state.
2. Select one context card and one primary skill.
3. Use at most one supporting skill.
4. Read only the files needed for the direct product change.
5. Execute in the same turn unless `plan_only` is explicit.

Audit skills are explicit-only. Generic requests such as “review”, “optimize”, or
“continue” should improve the named product, not start a governance audit.

## Review stop rule

Review is not a fixed number of personas. Select the lenses required by the paper.
Track only new independent P0/P1 issues. When consecutive independent lenses add no
new P0/P1 issue, stop expanding review and enter revision convergence.

## Lightweight logs

Use `paper/logs/research_log.md` and `paper/logs/paper_log.md` only for information
that changes a scientific or manuscript decision. Do not duplicate Git history or
create an audit trail.

## Language boundary

Use domain-native language in manuscripts, code comments, captions,
documentation, and normal user summaries. Internal routing, IDs, state labels,
ledgers, approval fields, or backend details must not leak into product prose
unless they are the subject of the task.

## Safety boundary

Routine local reads, narrow reversible edits, local tests, and diff inspection do
not require a safety detour. Ask only when a concrete action involves credentials,
private-data egress, paid remote compute, destructive remote writes, publication,
or submission.

## Optional ARIS backend

`external/aris` is an optional execution backend, not a second router. Resolve one
allowlisted capability through `integrations/aris/adapter.py`; never run ARIS
installer scripts or expose ARIS skills directly to the host. Core PaperTrace work
must remain usable without the submodule.

## User-facing completion

Report only:

1. the current claim or decision affected;
2. what substantive product changed;
3. the evidence or direct result;
4. the updated claim, boundary, or next decision;
5. one material remaining uncertainty, if any.

Do not expose route packets, YAML traces, validation matrices, or process reports
unless explicitly requested.

## Final PR validation

At final PR review, run the repository's lean CI once:

```bash
python src/S03_Scripts/validate_project.py
python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills
python .agent/scripts/validate_skill_evals.py
python -m unittest discover -s src/S04_Tests
```
