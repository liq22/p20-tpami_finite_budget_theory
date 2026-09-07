# Lean Context Cards

Use this file only to bound reading. Route selection is defined in
`skills/ROUTING_MATRIX.md`; execution policy is defined in `../AGENTS.md`.

| User job | Read first | Add only when needed |
|---|---|---|
| generate research candidates | observed failure or unresolved contradiction; scope; strongest known alternative | candidate workspace; closest-prior sources |
| formalize one candidate | selected candidate; observed evidence; competing explanation | equations, code, or protocol that distinguishes mechanisms |
| choose or revise direction | candidate; current result; closest verified prior | claim tree and boundary evidence |
| update research state | `paper/paper.yaml` and decision-changing facts | research log entry when the decision changed |
| design or simplify method | failure; competing explanation; current method behavior | assumptions, matched baseline, boundary test |
| position literature | target question or paragraph; load-bearing sources | equivalent terms and neighboring fields |
| implement or fix code | target source; config; nearest test | callers and data contracts needed to reproduce the defect |
| explain code | bounded subsystem | direct callers, configuration, and failure path |
| design experiment | claim; competing explanations; available protocol/data | independent unit, fairness controls, outcome decisions |
| execute experiment | approved protocol; code/config/data | prior result needed for a matched comparison |
| analyze data | actual data; protocol; estimand | model diagnostics required by the selected analysis |
| independently audit experiment | method; run configuration; actual results | source code only where it determines validity |
| generate figure or table | source data/result; reader question | manuscript paragraph and venue constraints |
| draft or restructure manuscript | target section; necessary evidence | adjacent section and changed citations |
| polish stable prose | target text | adjacent sentences only when meaning depends on them |
| review manuscript | manuscript; decisive sources/results | method or code only for a conclusion-changing concern |
| prepare submission | final source; official venue requirements | declarations and author metadata |
| improve PaperTrace | one reproduced repository behavior defect | affected rule, implementation, and nearest test |

Do not expand context because a file exists. Add a source only when it can change
the requested product or decision.
