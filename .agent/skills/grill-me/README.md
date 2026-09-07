# Grill Me v2 in PaperTrace

`grill-me` is an explicit-only, stateless pressure-test for a research idea, experiment protocol, benchmark, paper architecture, venue decision, or other consequential design. It asks one decision question at a time, recommends a position with a material trade-off, reopens contradictions, and ends with a structured Decision brief.

## Invoke

Claude Code:

```text
/grill-me <idea, plan, design, or decision>
```

The generated Claude wrapper sets `disable-model-invocation: true`, so the command is never selected automatically.

Codex and other Agent Skills-compatible hosts:

```text
Use the grill-me skill to pressure-test <subject>. Ask one question at a time and do not implement.
```

The canonical skill still requires explicit grill, challenge, red-team, interrogation, or pressure-test wording.

## Reply protocol

During the interview, reply with one of:

```text
accept
change: <your alternative>
unknown
skip
summary
stop
```

A free-form answer is also valid. `approve` at the end confirms only the Decision brief; it does not authorize implementation.

## Boundaries

- read-only and stateless;
- no `paper/`, code, config, log, checklist, or manifest writes;
- no experiments, network calls, paid tools, Git actions, freeze, or submission;
- no human-gate approval;
- no automatic handoff or implementation after convergence.

## Evaluation assets

```text
evals/evals.json          output-quality assertions
evals/eval_queries.json   positive and negative trigger queries
examples/prompts.md        PaperTrace routing examples
wrappers/claude.yaml       Claude explicit-invocation host override
```

Validate with:

```bash
python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only grill-me
python .agent/scripts/validate_skill_evals.py
python .agent/scripts/validate_agent_skill_wrappers.py
```

## Provenance

The minimal interaction pattern is adapted from `mattpocock/skills` at commit `391a2701dd948f94f56a39f7533f8eea9a859c87` under the MIT license. The v2 working contract and eval assets were supplied in a user-provided archive with SHA-256 `dc5ab73a6983b8a6103f80cc9fa3bf285b18a5de437a97abddf9f047d5794eda` and rewritten into PaperTrace's nine-section skill contract and scientific safety boundaries.
