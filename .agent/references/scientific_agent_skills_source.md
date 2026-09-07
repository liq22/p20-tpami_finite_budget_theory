# `scientific-agent-skills` 来源说明

本文件仅记录移植到 `.agent/skills/` 的第三方能力来源。它不是运行时注册表、路由表或完整性系统。

## 上游

- Repository: `K-Dense-AI/scientific-agent-skills`
- Upstream license: MIT
- Pinned release: `v2.53.0`
- Resolved commit: `9c9bd2e92af12311ecd0c1a643e0931643f9ea04`
- Port date: 2026-07-02

固定版本用于说明代码来源，不建立额外 digest、receipt 或同步清单。

## 本地改造边界

PaperTrace 只保留与当前科研产品直接相关的能力，并按本地规则改写：

- frontmatter 使用本地 `name` 与明确的任务描述；
- routeable Skill 至少包含 `Purpose`、`Workflow`、`Output Contract` 和 `Boundaries`；
- 输出映射到当前论文、代码、实验或图表，而不是上游高层 pipeline；
- 外部 API、网络和凭据能力保持显式、按需，不保存密钥；
- bundled assets 仅在真实本地用途中保留；
- 每个本地 Skill 的许可证文件继续决定其再分发条件。

当前路由以 `.agent/skills/ROUTING_MATRIX.md` 为准，Skill 清单以 `.agent/skills/INDEX.md` 为准。不要维护第二份生成式端口清单。

## 更新方法

升级某项能力时，只检查该 Skill 的真实用途、上游许可证和最近行为：

1. 核验上游变更；
2. 修改受影响的本地 Skill 或资源；
3. 必要时更新本文件和 `NOTICE.md`；
4. 仅在 host-visible wrapper 的 canonical 内容变化时重新同步 wrapper；
5. 运行受影响的最近测试，并在最终 PR 阶段运行一次现有质量门。

不要批量同步整个上游树，不要自动追踪 `main`，也不要为来源说明生成 registry、manifest 或迁移层。
