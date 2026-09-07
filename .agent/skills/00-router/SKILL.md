---
name: 00-router
description: Route a non-trivial PaperTrace request to one internal skill that changes the requested manuscript, code, experiment, figure, submission file, or research decision directly.
---

# 00 Router

## Purpose

Turn a broad request into one substantive product change. Routing is internal and
must not become the user's deliverable.

## User-facing initialization alias

`@初始化入口`, “初始化 Idea 阶段”, and “生成核心创新文档” route to
`scientific-brainstorming`. The primary product is
`paper/kickstart/core_innovation.md`, with only the minimum necessary updates to
the intake and candidate workspace.

This is a natural-language alias handled by `00-router`, not a third exposed host
Skill. It never approves the paper direction or converts a provisional candidate
into `paper/paper.yaml` authority.

## Anti-defensive writing alias

“避免防御性写作”, “去掉防御性写法”, `anti-defensive writing`, and requests
to remove repeated caveats, disclaimers, imagined-reviewer rebuttals, or stacked
hedges route to `10-language-polish` as the primary and
`anti-defensive-writing` as its one supporting Skill.

Use this route only for scientifically stable prose. If removing a qualification
would change evidence strength or the claim boundary, use `05-claim-evidence`;
if the section's scientific logic is incomplete, use `08-markdown-draft`.

## Workflow

1. Identify the actual product and the scientific, evidential, or behavioral
   defect to solve. For research tasks, state the failure/unresolved contradiction
   and the decision the action must change.
2. Select one primary skill; use at most one supporting skill.
3. Read only the inputs needed for that change. Read `paper/paper.yaml` only when
   stage, active source, claim state, or a consequential author confirmation
   matters.
4. Modify the requested product in the same turn unless `plan_only` is explicit.
5. Validate once with the closest direct check:
   - idea initialization: problem kernel, non-duplicate candidates, front-runner,
     closest-prior-art delta, falsifier, kill test, and boundary;
   - research question/method: failure, competing explanation, prediction,
     decisive comparison, and boundary;
   - literature: verify only sources used by the synthesis;
   - writing: reread target and adjacent context;
   - code: targeted test or smoke path;
   - experiment: inspect independent unit, outputs, metrics, uncertainty, and
     expected signature;
   - statistics: check estimand, unit, estimate, uncertainty, and interpretation;
   - figure/table: open the asset and check data/message;
   - TeX: compile once.
6. Report the substantive result and stop.

Generic “review”, “continue”, or “optimize” means improve the named product. It
does not imply a full audit, formatting pass, repository scan, statistics battery,
or Python validation.

## Output Contract

Return:

```text
Changed: <substantive product change>
Result: <direct outcome or scientific decision>
Validation: <one relevant check>
Remaining: <one material issue, only when present>
```

Do not expose route packets, YAML traces, status matrices, file hashes, or process
reports.

## Boundaries

- A plan, checklist, ledger, manifest, review report, or formatting-only diff is
  not completion for a product task.
- Audit skills require explicit audit intent.
- Do not run Python to evaluate ordinary prose or Markdown form.
- Do not calculate hashes or create receipts.
- Do not add validators, wrappers, factories, registries, tests, or defenses for
  hypothetical cases without a real/common/high-impact failure.
- Do not silently repair ambiguous scientific semantics; fail clearly and stop.
- Optional ARIS capabilities remain behind PaperTrace and are resolved one at a
  time only when they directly help produce the requested product.
