# Agent Skill Evals

PaperTrace 将“规则文件有效”和“Agent 真实行为正确”明确分开。

## 1. Definition validation

`skill_trigger_cases.yaml` 与 `product_surface_cases.yaml` 定义路由和产物期望：

```bash
python .agent/scripts/validate_skill_evals.py
```

该命令只检查 YAML/JSON 结构、case ID、expected primary、禁止路由和产物字段。它不调用 Claude、Codex、ARIS 或其他模型，也不能证明真实任务已经修改主要产物。

## 2. Explicit host results

在相同模型、工具策略和仓库状态下独立运行 case 后，可保存 JSONL 并评分：

```bash
python .agent/scripts/validate_skill_evals.py --results path/to/results.jsonl
```

`selected_primary`、`product_changed` 和用户摘要是行为记录，不是独立证据。最终仍需检查实际目标文件、实验输出、图表或投稿文件，以及与该改动最近的直接验证。

## 3. Targeted semantic tests

单元测试只保护可执行语义，例如：

- wrapper 只暴露批准的 host entry；
- active source 与 paper stage 一致；
- planned/failed run 不能支持正向 evidence；
- 未核验文献不能支持确定性 claim；
- ready method 需要 failure、预测、拒绝条件、公平比较和边界；
- ARIS 保持可选且不成为第二 Router。

不要使用 Python 统计普通 Markdown 中的术语、标题、hedge 或“AI 味”，也不要把关键词存在性称为产品行为验证。

## Skill-local evals

个别 Skill 可以在 `.agent/skills/<name>/evals/` 保存小型触发与输出用例。只有存在真实、稳定且可观察的失败时才增加 case；不按 Skill 数量追求覆盖率。

CI 运行 definition validation 和针对性单元测试，不执行付费模型或网络行为测试。
