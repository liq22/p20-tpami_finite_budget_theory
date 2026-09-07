# 将研究代码拆成独立子模块

本文讨论把**本论文自己的稳定研究代码**拆成独立 Git 仓库。它与可选的 `external/aris/` 后端不同。

## 什么时候值得拆仓

只有出现实际收益时才拆分：

- 同一代码需要被多篇论文复用；
- 代码需要独立发布、版本管理或权限；
- `src/S01_Package/` 已形成稳定、可测试的包；
- 论文仓与代码仓需要不同维护节奏。

早期 demo、一次性脚本、频繁变化的接口继续留在当前仓库更简单。

```text
先让代码正确、清晰、可测试，再决定是否独立版本化。
```

## 推荐结构

父论文仓：

```text
PaperTrace-project/
  paper/
  src/
    README.md
    <package>/          # Git submodule
  .gitmodules
```

独立代码仓：

```text
<package>/
  pyproject.toml
  src/<package>/
  configs/
  scripts/
  tests/
  README.md
  LICENSE
```

## 拆分前检查

确认：

- 当前代码和相关测试已提交；
- 包的公开入口基本稳定；
- targeted tests 能通过；
- 新仓名称、许可证和 URL 已确定；
- `.gitmodules` URL 不含 token；
- 维护者同意结构变更。

不需要补齐 manifest、hash、receipt 或额外治理文件。

## 操作步骤

### 1. 创建代码仓

```bash
mkdir <package>-repo
cd <package>-repo
git init

# 迁移代码、配置和测试
python -m unittest discover -s tests

git add -- <confirmed-paths>
git commit -m "init reusable research package"
git remote add origin <repository-url>
git push -u origin main
```

### 2. 从父仓移除已迁移代码

```bash
git rm -r -- src/S01_Package/<migrated-part>
git commit -m "move reusable package to independent repository"
```

### 3. 添加子模块

```bash
git submodule add <repository-url> src/<package>
git commit -m "add research package submodule"
```

父仓记录子模块 commit 作为依赖版本，不需要额外 digest。

### 4. 更新入口并验证

更新 import、配置路径、运行脚本和 README。然后只运行受影响的测试：

```bash
python -m unittest discover -s src/<package>/tests -v
python -m unittest discover -s src/S04_Tests -v
```

最终 PR 再运行一次完整 PaperTrace 校验。

### 5. 验证全新克隆

```bash
git clone --recurse-submodules <parent-repository-url> /tmp/papertrace-check
cd /tmp/papertrace-check
python scripts/setup_papertrace.py --profile core --non-interactive
python src/S03_Scripts/validate_project.py
```

## 日常更新

```bash
git -C src/<package> fetch origin
git -C src/<package> checkout <reviewed-commit>
git diff --submodule
git add -- src/<package>
git commit -m "chore: update research package pin"
```

不要自动跟随子仓 `main`。每次 pin 变化都应对应可说明的代码变化和相关测试结果。

## 回滚

```bash
git submodule deinit -f -- src/<package>
git rm -f -- src/<package>
rm -rf .git/modules/src/<package>
git commit -m "remove research package submodule"
```

## 停止条件

停止拆分并先解决实际问题，当：

- 当前代码或测试不稳定；
- 接口仍频繁变化；
- 文件归属不清楚；
- 许可证、权限或 URL 不明确；
- 全新递归克隆不能运行；
- 拆分只增加维护步骤，没有复用或发布收益。
