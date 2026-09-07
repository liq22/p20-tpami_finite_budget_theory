# 可选 ARIS 执行后端

PaperTrace Core 不依赖 ARIS。只有当前任务确实需要外部检索、实验执行、结果分析、图表或 LaTeX 编译能力时，才显式启用固定版本的 ARIS 子模块。

```text
PaperTrace 决定科研问题、主要产物和最终表达
ARIS 仅提供被选中的执行能力
```

## 使用模式

| Profile | 用途 | ARIS |
|---|---|---:|
| `core` | 研究状态、方法、代码、写作和原生工具 | 不初始化；默认 |
| `execution` | 显式增加检索、实验、图表和编译能力 | 初始化 |
| `review` | 在 execution 基础上显式允许独立核验能力 | 初始化 |

```bash
# 默认 Core
python scripts/setup_papertrace.py

# 明确需要外部执行后端
python scripts/setup_papertrace.py --profile execution
```

Execution/Review 需要 Git clone，以固定子模块版本。Core 可在普通目录中使用。

本地 `.papertrace/setup.json` 不存在时按 Core 处理；文件存在但损坏、schema 错误或 profile 无效时明确失败。修复或删除该文件后再显式选择 profile，系统不会静默退回 Core。

## 单入口边界

PaperTrace 仍只暴露：

```text
00-router
grill-me
```

ARIS Skills 不会安装到 `.claude/skills/`、`.codex/skills/` 或 `.agents/skills/`。不要运行上游 installer；它们会绕过 PaperTrace Router。

允许能力由 `profile.yaml` 管理：

- execution：少量文献、实验、图表和编译能力；
- review：仅在用户明确要求时增加 citation/experiment/claim review；
- disabled：上游 research/paper/review-loop 等高层 pipeline。

Router 先选择 PaperTrace primary，再通过 `adapter.py` 解析一个 capability。Backend 名称、Skill 路径和内部状态不进入普通用户回复或论文正文。

## 检查与解析

```bash
python scripts/check_aris_backend.py --profile core
python scripts/check_aris_backend.py --profile execution --require-initialized
python integrations/aris/adapter.py status --profile execution
python integrations/aris/adapter.py resolve analyze-results --profile execution
```

可选依赖只在对应 capability 被选择时检查。例如 `paper-compile` 需要 `latexmk`，`paper-figure` 需要 matplotlib。缺少未使用的工具不会让 Core 安装失败。

## 维护边界

- 固定 Git commit 是依赖版本，不建立额外 hash 或 manifest 系统；
- 升级 pin 前只检查 allowlisted capability 是否存在且主路径仍工作；
- 不维护 speculative fork 状态、兼容性数据库、自动更新器或 fallback backend tree；
- 若长期没有真实 Router→adapter→product 调用，应进一步压缩或移除集成，而不是扩展它。
