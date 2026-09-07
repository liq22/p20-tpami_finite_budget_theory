# External optional backends

`external/` 存放可选、固定版本的外部能力后端。

当前包含：

```text
external/aris/
```

它是 ARIS 的 Git 子模块，不是 PaperTrace 的第二套用户入口。

- 使用 PaperTrace Core 时，可以不初始化该目录；
- 使用 Research Execution 或 Advanced Review 时，由
  `python scripts/setup_papertrace.py` 自动初始化；
- 不要直接运行 ARIS installer；
- 不要手工编辑子模块内部文件并混入 PaperTrace 提交；
- 更新版本时只更新 gitlink pin，并运行兼容性测试。

查看具体集成规则：`integrations/aris/README.md`。
