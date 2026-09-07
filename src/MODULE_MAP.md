# Scientific Code Module Map

This file explains active research code as a scientific and engineering system.
It is not a file inventory, API dump, or requirement to document every utility.
Map one target subsystem or at most three tightly coupled modules per bounded
comprehension task.

Use `.agent/references/research_prompt_pack.md#P7--Code-module-X-ray` through the
internal `code-module-xray` skill. Use `code-change` instead when implementation,
repair, refactoring, or optimization is requested.

## Fast map

| Module ID | Path | Scientific role | What / Why | Inputs | Outputs | How / key invariant | Config | Tests / diagnostics | Paper link | Status / unknowns |
|---|---|---|---|---|---|---|---|---|---|---|
| MOD-001 | `src/S01_Package/` | TODO: active research implementation | TODO | TODO | TODO | TODO | TODO | TODO | TODO | template |
| MOD-002 | `src/S02_Configs/` | Versioned scientific and execution choices | Separates varying assumptions from implementation | YAML/config values | Runtime configuration | Defaults and units remain explicit | TODO | config validation | relevant experiment | template |
| MOD-003 | `src/S03_Scripts/` | Bounded command-line entry points and utilities | Runs one named task with visible inputs and outputs | CLI/config/data | results, logs, exported files | Exit behavior and errors are explicit | TODO | smoke and integration tests | relevant method/experiment | template |
| MOD-004 | `src/S04_Tests/` | Protect scientific and software behavior | Turns known failures into executable regression cases | code/config/fixtures | test results | A reproduced bug receives a targeted test | test config | unit and negative fixtures | reproducibility | template |

Replace template rows with actual active modules. Do not map generated wrappers,
vendored dependencies, caches, build products, or dead code unless they affect a
paper conclusion or runtime behavior.

## Expanded module card

Use this block only for a scientifically central or difficult module.

```yaml
module_id: MOD-...
path: src/...
entry_points: []
scientific_role: <one sentence>

five_w_one_h:
  what: <object/transformation>
  why: <research or engineering need>
  who: <caller and downstream consumer>
  where: <pipeline/subsystem>
  when: <stage/condition>
  how: <algorithm/control and data flow>

inputs:
  - name: <...>
    type_shape_unit: <...>
    semantics: <...>
outputs:
  - name: <...>
    type_shape_unit: <...>
    semantics: <...>

invariants: []
assumptions: []
side_effects: []
dependencies: []
configuration:
  scientific_knobs: []
  engineering_knobs: []
design_choice:
  chosen: <...>
  strongest_alternative: <...>
  reason: <...>
failure_signatures: []
tests_and_diagnostics: []
paper_links:
  claims: []
  equations: []
  experiments: []
  figures_tables: []
unknowns: []
```

The YAML labels above are internal map fields. Production-code comments and
docstrings should use normal programming terms such as inputs, outputs,
preconditions, errors, complexity, and configuration.

## Representative path trace

For each mapped subsystem, trace one path:

```text
external input
-> validation / normalization
-> core scientific transformation
-> metric or decision
-> returned value / saved result / figure
```

At every arrow record the responsible module, object semantics, required
condition, and expected failure behavior. This is usually more useful than a
complete call graph.

## Product boundary

- A request to understand code may update this map.
- A request to implement, fix, refactor, or optimize code must change source code
  and relevant tests; updating this map alone is not completion.
- Internal PaperTrace terms such as route, gate, ledger, manifest, receipt,
  claim promotion, or blocker do not belong in production comments or docstrings.

## Stop rule

- Do not refactor while explaining.
- Do not infer runtime behavior solely from names or comments.
- Mark uncertain intent or unexecuted branches as `UNKNOWN`.
- Stop after the selected subsystem is understandable enough to modify or test.
- A map that does not change a researcher's ability to reason about the code is
  documentation overhead and should be deleted or simplified.