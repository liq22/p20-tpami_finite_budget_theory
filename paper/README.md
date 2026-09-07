# `paper/` 工作区

`paper/` 服务一篇论文。当前状态、正文和历史记录分开维护；未使用的阶段文件不需要预先创建。

## 唯一职责

| 内容 | 位置 |
|---|---|
| 当前研究问题、主张风险、最大不确定性和下一动作 | `paper/paper.yaml -> research_state` |
| 方向批准 | `paper/paper.yaml -> idea_selection` |
| 当前正文 | `paper.yaml.active_source` 指向的文件 |
| 研究决策历史 | `paper/logs/research_log.md` |
| 论文主张与正文变更历史 | `paper/logs/paper_log.md` |

`new_project_intake.yaml` 只用于首次输入，不与 `paper.yaml` 持续同步。Git 已记录文件修改，不再维护 change log、freeze log 或第二套决策日志。

## 默认工作方式

在 `idea`、`outline` 和 `markdown_draft` 阶段，`paper/draft/main.md` 是 active source。只有形成真实内容后才创建对应记录：

```text
候选方向        paper/kickstart/idea_candidates.yaml
方法规格        paper/method/method_spec.yaml
关键文献        paper/refs/reading_matrix.md
实验运行        paper/experiments/run_ledger.md
claim 支持      paper/experiments/evidence_matrix.md
图表            paper/assets/
正式 TeX        paper/tex/
审稿返修        paper/reviews/
投稿材料        paper/submission/
```

这些路径不存在或为空均表示“当前不需要”，不是缺失进度。不要创建 C1、E1、R1、RUN-1、F1 或空章节来填满模板。

## 研究闭环

```text
问题或失败
→ 最强竞争解释
→ 最小区分动作
→ 真实结果
→ 更新 claim、机制或边界
→ 需要时写入正文
```

方法进入 `ready` 时才要求 failure、最小 intervention、预测、拒绝条件、公平比较和 boundary test 闭合。正向 evidence 只能引用 completed run 或核验过的原文。负结果必须保留。

## Markdown 与 TeX

Markdown 正文稳定并经作者确认后，创建 `paper/tex/`，将 `active_source` 切换为 `tex`，并设置 `freeze.frozen=true`。转换后不再独立维护第二份正式正文。

## Review 与投稿

Review 是显式任务。只保留会改变结论或修订顺序的 P0/P1；连续视角不再产生新问题时停止扩展。Review 和 submission 文件由相应 Skill 在真实任务发生时生成，不保留空白评分表或通用 checklist。

## 验证

```bash
python src/S03_Scripts/validate_project.py
```

Validator 检查 active source、现有 scientific records 及必要的跨文件引用；它不要求完整生命周期骨架。
