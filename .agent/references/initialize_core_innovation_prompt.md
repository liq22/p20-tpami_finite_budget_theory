# @初始化入口 — PaperTrace 核心创新初始化 Prompt

将下面指令交给在 PaperTrace 仓库中工作的 Agent。它由 `00-router`
路由到 `scientific-brainstorming`，不新增 host Skill。

```text
@初始化入口

直接把当前研究材料收敛为一页核心创新决策卡。不要只给计划，也不要要求先填满模板。

目标文件：
- paper/kickstart/core_innovation.md
- paper/kickstart/idea_candidates.yaml
- paper/kickstart/new_project_intake.yaml（仅在需要记录已知初始事实时更新）

执行规则：

1. 先找真实的 observed problem、failure、未决矛盾或未解释边界。
   若当前材料不支持任何一项，写 `unknown`，不选择 front-runner，
   将“获得能够区分解释的证据”作为下一动作。

2. 最多保留四个机制不同的候选。只有存在真实差异时才生成 2–4 个；
   一个或零个也可以。候选的 before → after 或机制开始重复时，立即合并并停止。

3. 每个候选只写：
   research object、before → after、mechanism、observable prediction、
   rejection condition、closest-neighbour delta 或待核验问题、
   bounded kill test、claim boundary。

4. M1–M5、P01–P15 只可作为内部可选搜索镜头。不得为了覆盖模式生成候选，
   不要求把模式 ID 写入结果，也不得把模式标签当作新颖性证据。

5. 仅在证据足够时选择一个 provisional front-runner。只为它保留：
   一个 favored mechanism、一个 strongest competing explanation、
   一个 divergent prediction、一个 main confound 和一个 decisive test。
   provisional 不等于作者批准；唯一批准状态在
   paper/paper.yaml -> idea_selection。

6. 只核验当前决策所需的最强近邻。无法检查原文时标记 `unverified`，
   不得声称“首次”“尚无研究”“显著创新”或“完全统一”。

7. decisive test 必须能够区分 favored mechanism 与 strongest competitor，
   明确 independent unit、matched baseline、mechanism on/off、main confound、
   task metric、mechanism metric、rejection signature 和 boundary。

8. positive、null、contradictory、boundary-only 结果必须改变当前决策。
   null 或 contradictory 结果应使方向 revise、downgrade 或 eliminate，
   不得通过改写保护原故事。

直接更新一页 paper/kickstart/core_innovation.md，包含：
- observed problem or unresolved contradiction
- current claim at risk
- evidence already observed
- before → after core change
- provisional front-runner（证据不足时为 not selected）
- favored mechanism
- strongest competing explanation
- closest verified prior and irreducible delta
- divergent prediction
- decisive test
- scope or boundary
- current decision
- most informative next action
- stop or rejection condition

最终只报告：
Changed: 实际修改的文件。
Decision: 当前保留、修改、降级、淘汰或证据不足。
Decisive next action: 一个最能改变研究判断的动作。
Remaining uncertainty: 最多一个。
```
