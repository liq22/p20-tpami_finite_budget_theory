# PaperTrace

PaperTrace 是面向单篇科研论文的轻量工作区。它从当前最重要的科学或实现问题出发，选择一次能够改变判断的最小动作，并直接产出代码、实验结果、图表、正文或投稿文件。

```text
问题或失败
→ 最小区分动作
→ 真实产物与结果
→ 更新主张、机制或边界
```

## 开始使用

需要 Python 3.10+。默认安装 Core，不下载可选 ARIS 后端：

```bash
python scripts/setup_papertrace.py --non-interactive
```

已有代码、实验或草稿时，直接告诉 Agent：

```text
读取 paper/paper.yaml 和当前任务所需文件，找出最重要的一个科学或实现问题，
直接修改主要产物并运行一次最相关验证；不要只输出计划、状态报告或审查材料。
```

研究方向尚未收敛时使用：

```text
@初始化入口
读取当前仓库和已有材料，从真实问题、失败或未决矛盾出发，生成少量机制不同且可证伪的候选；
核验最强近邻，选择一个暂定方向，并直接更新核心创新材料。未知项保留 TODO/unknown。
```

不需要预先填写完整论文、实验、图表、TeX 或投稿模板。

## 常用请求

| 目标 | 直接请求 |
|---|---|
| 收敛研究问题 | `根据当前失败、证据和最强竞争解释，修订中心问题与最小 claim tree。` |
| 设计方法 | `提出区分两个机制的最小 intervention、预测、拒绝条件和 boundary test。` |
| 修改代码 | `复现并修复这个语义错误，修改源码和最近的 regression test。` |
| 运行实验 | `执行 matched comparison，返回真实指标、不确定性和 claim decision。` |
| 分析结果 | `先确认 estimand 和 independent unit，再给出最简单有效的分析。` |
| 生成图表 | `基于真实结果生成可编辑图表和自包含 caption。` |
| 修改论文 | `按当前证据重写目标段落，保留数字、引用和结论边界。` |
| 避免防御性写作 | `去掉重复 caveat、免责声明和叠加 hedge，保留真实不确定性与局限。` |
| 审稿返修 | `先完成必要实验、分析或正文修改，再写 point-by-point response。` |
| 准备投稿 | `按目标期刊官方要求生成可上传文件，不执行正式投稿。` |

## 工作区

| 路径 | 职责 |
|---|---|
| `paper/paper.yaml` | 当前研究问题、主张风险、最大不确定性、下一动作和 active source |
| `paper/draft/main.md` | Markdown 阶段的当前正文入口 |
| `paper/logs/research_log.md` | 改变研究判断的历史记录 |
| `paper/logs/paper_log.md` | 改变论文主张或正文的历史记录 |
| `.agent/skills/00-router/SKILL.md` | 默认路由入口 |

方法、文献、实验、图表、TeX、review 和 submission 文件只在任务实际需要时创建。详细说明见 [`paper/README.md`](paper/README.md)。

## 执行边界

- 科学语义不一致时明确失败，不猜测数据、标签、split、task、objective、metric 或 claim 含义。
- 主要产物优先；记录、manifest、checklist 和报告不能替代源码、结果、图表或正文。
- null、negative、unstable 和 contradictory result 必须如实改变判断。
- 不主动增加 hash、receipt、ledger、tree digest 或完整性证明。
- Python 用于计算、代码、实验、统计、绘图、文件生成和针对性测试，不用于普通 Markdown 或文风评分。
- 一次任务使用一个 primary Skill、至多一个 supporting Skill，并运行一次最相关验证。

完整规则见 [`AGENTS.md`](AGENTS.md)，操作示例见 [`QUICKSTART_NEW_PROJECT.md`](QUICKSTART_NEW_PROJECT.md)。

## 可选执行后端

只有明确需要额外检索、实验、图表或编译能力时才启用固定版本的 ARIS：

```bash
python scripts/setup_papertrace.py --profile execution
```

ARIS 始终位于 PaperTrace Router 之后，不新增用户入口。详见 [`integrations/aris/README.md`](integrations/aris/README.md)。

## 最终检查

```bash
python scripts/check_aris_backend.py --profile core
python src/S03_Scripts/validate_project.py
python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills
python .agent/scripts/validate_agent_skill_wrappers.py
python .agent/scripts/validate_skill_evals.py
python -m unittest discover -s src/S04_Tests -v
```

`validate_skill_evals.py` 在未提供 `--results` 时只校验 case definitions，不执行 Claude、Codex 或其他模型。
