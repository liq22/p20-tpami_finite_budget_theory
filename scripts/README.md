# PaperTrace scripts

普通用户通常只需要一个命令：

```bash
python scripts/setup_papertrace.py
```

## `setup_papertrace.py`

用途：

- 创建隔离的 `.venv`；
- 安装 PaperTrace 校验依赖；
- 选择 Core、Research Execution 或 Advanced Review；
- 按需初始化固定版本的 `external/aris`；
- 保存机器本地设置到被忽略的 `.papertrace/setup.json`；
- 检查项目结构和可选后端。

常用命令：

```bash
# 交互式，推荐新用户
python scripts/setup_papertrace.py

# 无交互，启用执行后端
python scripts/setup_papertrace.py --profile execution --non-interactive

# 只使用 PaperTrace Core
python scripts/setup_papertrace.py --profile core --non-interactive

# 不修改环境，只检查上次选择的模式
python scripts/setup_papertrace.py --check-only

# 重新创建虚拟环境
python scripts/setup_papertrace.py --profile core --recreate-venv
```

## `check_aris_backend.py`

用途：检查可选 ARIS 后端是否满足 PaperTrace 的边界：

- `.gitmodules` URL 与 profile 一致；
- `external/aris` 是 mode `160000` 的真实 gitlink；
- gitlink commit 与固定 pin 一致；
- Core 模式允许未初始化子模块；
- Execution/Review 模式要求正确 checkout；
- allowlist skill 存在；
- ARIS skill 没有直接暴露为 Claude/Codex 命令。

常用命令：

```bash
python scripts/check_aris_backend.py --profile core
python scripts/check_aris_backend.py --profile execution --require-initialized
```

## 边界

不要在 `scripts/` 中建立第二套研究流水线。这里的脚本只负责：

```text
安装
兼容性检查
用户明确要求的有限维护操作
```

研究任务仍由 `00-router` 选择主要产物和内部能力。ARIS 的安装器不能从这里被间接调用，也不能把 ARIS skills 写入宿主 skill 目录。
