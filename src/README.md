# Research code

`src/` 存放本论文的研究代码、配置、运行入口、校验器和测试。论文正文、文献笔记和投稿材料放在 `paper/`。

```text
src/
  S01_Package/   可复用的研究实现
  S02_Configs/   会随实验变化的配置
  S03_Scripts/   运行、校验和辅助入口
  S04_Tests/     单元、语义和负向测试
  MODULE_MAP.md  中央模块的简明说明
```

## 用户要求改代码时

进入真实实现路径：

```text
复现问题或建立最小 baseline
-> 修改源码
-> 增加或更新 targeted test
-> 运行最小验证
-> 汇报行为变化
```

主要产物是：

```text
source code + relevant tests
```

以下内容不能替代实现：

```text
MODULE_MAP.md
代码 review 报告
实现计划
状态文件
```

`MODULE_MAP.md` 只在公开接口、科学职责或重要假设发生变化时同步更新。

## 只想理解代码时

使用 `code-module-xray`，一次解释一个 subsystem 或至多三个紧密耦合模块。重点回答：

```text
它解决什么问题？
谁调用它？
输入和输出是什么？
数据与控制如何流动？
哪些条件必须保持成立？
哪些参数改变科学行为？
怎样测试关键行为？
它对应论文中的哪条方法或实验？
```

不要为了显得完整而制作全仓调用图，也不要逐行复述代码。

## 编码原则

- 名称和结构表达基本含义；注释只解释非显而易见的选择。
- Docstring 使用编程和工程语言，不写 PaperTrace 的 route、gate、ledger、manifest 或 blocker 术语。
- 研究参数与工程参数分开；会随实验变化的设置进入配置。
- 一个已知语义 bug 应转化为一个 focused regression test。
- 不为了获得通过而删除失败测试、改变数据划分或修改指标定义。
- 未验证的行为标为 `UNKNOWN`，并指出最小验证方法。

## 最小实现路径

1. 明确要改变的行为和验收条件。
2. 在 `S01_Package/` 中实现可复用逻辑。
3. 在 `S02_Configs/` 中放置可版本化参数。
4. 在 `S03_Scripts/` 中提供一个有界入口。
5. 在 `S04_Tests/` 中保护关键行为和失败条件。
6. 运行 targeted test；只有共享接口变化时才更新 `MODULE_MAP.md`。

## 两种“子模块”不要混淆

### 可选 ARIS 后端

```text
external/aris/
```

它是 PaperTrace 的可选执行能力来源，由 `scripts/setup_papertrace.py` 管理。它不是本论文的研究代码。

### 将本论文代码拆成独立仓库

当研究实现已经稳定、需要跨论文复用或独立发布时，才考虑把本项目代码拆成单独 Git 仓库。具体步骤见 [`submodule_sop.md`](./submodule_sop.md)。

不要仅为了“看起来更工程化”而提前拆仓。
