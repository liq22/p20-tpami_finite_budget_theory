# Claim–Support Matrix

本表只在形成正式 claim 后使用。它回答：当前理论、实验、分析或原始文献允许论文说到什么程度，以及边界在哪里。

| Claim ID | Claim text | Strength | Hypothesis provenance | Evidence ID | Evidence type | Run/ref/artifact | Strongest counterexample / alternative | Figure/table | Boundary | Status |
|---|---|---|---|---|---|---|---|---|---|---|

## Strength

- `hypothesis`: 尚未验证。
- `weak`: 单一或探索性结果，仍有重要混杂。
- `moderate`: 多次一致结果，但适用范围或独立确认有限。
- `strong`: 关键替代解释已被区分，并有独立结果和明确边界支持。

## Hypothesis provenance

- `unknown`: 尚未核对形成时间；新条目默认使用此值。
- `H0`: 在相关结果之前提出。
- `H1`: 由探索性结果启发。
- `H2`: 已由新的独立结果确认。
- `H3`: 仍是结果后的解释。

不得把 H1、H3 或 unknown 倒写成 H0。

## Status

- `missing`
- `planned`
- `to_verify`
- `supported`
- `partially_supported`
- `refuted`
- `blocked`

## Rules

- 正向支持引用 run 时，该 run 必须是 `completed`。
- 正向支持引用文献时，该文献必须完成全文核验。
- 直接引用结果文件时填写可理解的文件路径或数据来源；不计算文件 hash。
- 记录最强反例或竞争解释，以及对象、工况、数据、协议或外部效度边界。
- 探索性结果可以进入论文，但不得伪装成独立确认。
- 新结果否定主张时修改主张，不保护原叙事。
