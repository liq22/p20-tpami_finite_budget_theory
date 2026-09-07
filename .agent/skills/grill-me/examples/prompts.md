# Grill Me Examples

## Scenario 1 — Research question and novelty pressure test

User:

```text
/grill-me this research plan before I approve the research question. Ask one question at a time, recommend your answer, and do not write files or start literature search.
```

Expected behavior:

- select `grill-me` directly because the user explicitly invoked it;
- inspect only the bounded project facts needed for the current decision;
- ask one high-impact upstream question using the required recommendation/trade-off format;
- wait for `accept`, `change: ...`, `unknown`, `skip`, `summary`, `stop`, or a free-form answer;
- finish only after convergence or an explicit stop;
- change no files and approve no human gate.

## Scenario 2 — Experiment protocol pressure test

User:

```text
严厉盘问这个 benchmark 协议，先找出会让 TPAMI reviewer 否定结论的根本决策。一次只问一个问题，并给出你推荐的答案。不要运行实验。
```

Expected behavior:

- select `grill-me`, not `06-experiment-ops` or `07-experiment-audit`;
- begin with the highest-dependency unresolved decision, such as task definition, primary estimand, baseline fairness, leakage boundary, or success criterion;
- give one recommendation and the strongest viable alternative;
- do not register a run, edit the protocol, or claim the protocol is approved.

## Scenario 3 — No subject supplied

User:

```text
/grill-me
```

Expected behavior:

- ask only what idea, plan, design, or decision should be pressure-tested;
- do not invent a topic;
- do not dump a questionnaire or provide a generic planning framework.

## Scenario 4 — Contradiction and convergence

Conversation state:

```text
The user first accepted “no external APIs” and later requires a paid hosted judge.
```

Expected behavior:

- name the contradiction plainly;
- reopen the affected dependency;
- ask one question about which constraint governs;
- after all blocking branches are resolved, produce the structured Decision brief;
- ask only the final `approve` or corrections question;
- treat approval as confirmation of the brief, not permission to implement.

## Scenario 5 — Do not use for completed-work audit

User:

```text
Audit the completed experiments for leakage, baseline fairness, statistical power, artifact provenance, and claim support. Return a read-only report.
```

Expected behavior:

- do not select `grill-me` because there is no explicit grill-style request and the task concerns completed evidence;
- route to `07-experiment-audit` or a declared global read-only audit;
- produce location-bound findings rather than an interactive decision interview.

## Scenario 6 — Do not use for ordinary peer review

User:

```text
Review the full manuscript as a journal reviewer and return P0/P1/P2 comments without editing the paper.
```

Expected behavior:

- do not select `grill-me`;
- select `peer-review` with `scientific-critical-thinking` where appropriate;
- preserve the reviewer fact-base and manuscript read-only boundary.
