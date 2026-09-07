# PaperTrace 快速使用

## 1. 初始化

```bash
python scripts/setup_papertrace.py --non-interactive
```

默认 Core 不下载 ARIS，足以处理研究状态、方法设计、代码修改、实验设计、统计分析、图表规划和论文写作。只有当前任务确实需要额外外部能力时，才显式使用 `--profile execution`。

## 2. 从当前问题开始

### 已有项目

```text
读取 paper/paper.yaml 和当前任务直接相关的文件。
找出最影响当前 claim 的一个问题，直接修改主要产物，并执行一次最近验证。
未知项保持 TODO/unknown；不要补齐未使用的流程文件。
```

已有代码、结果或草稿时，不需要重新填写 intake。

### 方向尚未收敛

```text
@初始化入口
从已知研究对象、环境、观测、任务、真实 failure 或未决矛盾出发，
生成机制确实不同的候选，核验最强近邻，并形成一页核心创新决策卡。
```

规则：

- 没有已观察 failure、矛盾或未解释边界时，保持 `unknown`，不选择 provisional front-runner；
- 只有存在真实机制差异时才生成 2–4 个候选；一个或零个候选均合法；
- 下一候选开始重复已有机制时立即停止；
- M1–M5 和 P01–P15 只是可选搜索镜头，不是必填标签或新颖性证据；
- 作者选择只记录在 `paper/paper.yaml -> idea_selection`。

## 3. 直接推进任务

| 目标 | 请求示例 |
|---|---|
| 修复代码 | `复现并修复 sampling-rate metadata 传播错误；修改源码和最近的 regression test，不增加 fallback 或无关重构。` |
| 设计实验 | `设计区分机制解释与 capacity-only 解释的最小公平实验，明确 independent unit、指标、可能结果和决策。` |
| 执行实验 | `执行已确定的 matched comparison，返回真实输出、指标、不确定性和更新后的 claim。` |
| 修改正文 | `依据已验证结果重写目标段落，保持数字、引用和结论边界。` |
| 避免防御性写作 | `删除空 caveat、免责声明和叠加 hedge，保留真实不确定性、null result、数字和引用。` |
| 生成图表 | `基于指定结果生成实际图表和自包含 caption。` |
| 准备投稿 | `核验目标期刊当前官方要求并生成可上传文件；不执行正式投稿。` |

## 4. 按需记录

默认只维护 `paper/paper.yaml` 和当前 active source。候选、方法、文献、实验、图表、TeX、review 与 submission 记录在真实任务需要时创建；不要用空 claim、run、reference、figure 或 checklist 表示进度。

## 5. 最近验证

- 论文：重读目标及相邻逻辑，核对改变的数字和引用；
- 文献：核验承担结论的原文和最强近邻；
- 方法：检查 failure、竞争解释、假设、预测、拒绝条件和边界；
- 代码：运行最近的针对性测试或 smoke path；
- 实验/统计：检查 independent unit、协议、公平性、指标、不确定性和解释；
- 图表：打开资产，核对数据、单位、标签和 caption；
- TeX：编译一次；
- 投稿文件：确认文件存在、可打开并符合官方要求。

完整仓库检查只在最终 PR 阶段运行一次。
