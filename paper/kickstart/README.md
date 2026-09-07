# Paper Kickstart

`kickstart/` 是一次性探索区，不是持续同步的项目状态系统。

| File | Use |
|---|---|
| `new_project_intake.yaml` | 可选的一次性事实输入；已有项目可以跳过 |
| `idea_candidates.yaml` | 方向仍开放时保存少量机制不同的候选；零个候选合法 |
| `core_innovation.md` | 一页 provisional 决策卡；不是 novelty 证明或作者批准 |

当前研究状态只写入 `paper/paper.yaml -> research_state`。作者选择只写入 `paper/paper.yaml -> idea_selection`。intake 不与当前状态同步，候选文件也不保存批准状态。

## `@初始化入口`

初始化从真实 failure、矛盾或未解释边界出发：

```text
已观察问题
-> 机制不同的候选（如有）
-> 最强竞争解释
-> 最近邻差异
-> divergent prediction
-> decisive test
-> provisional 决策
```

没有已观察 failure 或区分性证据时：

```text
failure = unknown
provisional front-runner = not selected
current decision = insufficient evidence
next action = 获取能够区分解释的证据
```

只有存在真实机制差异时才生成 2–4 个候选；一个或零个候选均合法。M1–M5 和 P01–P15 只在有助于发现不同 changed object 时作为内部镜头，不要求出现在产品中。

## 候选最小内容

保留一个候选只需说明：

- research object 与 before → after core change；
- mechanism、observable prediction 和 rejection condition；
- closest-neighbour delta 或未决检索问题；
- bounded kill test 与 claim boundary；
- retain、revise、merge、downgrade 或 eliminate 决策。

候选机制重复时合并并停止。Null 或 contradictory evidence 必须改变方向或边界，不通过改写叙事保护原方案。未知内容保持 `unknown` 或 `unverified`。
