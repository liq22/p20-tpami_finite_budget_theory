# Experiment Run Ledger

只记录真正执行过或已明确批准的运行。主要产物是实验结果；本表仅保留理解和复现实验所需的信息。

| Run ID | Date | Code version | Config | Data/version | Seed | Budget/hardware | Primary metric | Result | Status | Output path | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Status

- `planned`
- `running`
- `completed`
- `failed`
- `timeout`
- `cancelled`
- `invalid`
- `to_verify`

## Rules

- 进程正常退出不自动等于实验完成；使用真实结果状态。
- `failed`、`invalid`、`planned` 和 `to_verify` 不得支持正向结论。
- 协议、代码行为、数据、配置或 seed 实质变化时创建新 run。
- `completed` 记录代码版本、配置、数据版本、seed、指标、结果和输出路径；不需要 hash 或 receipt。
- 负结果、null、unstable 和 contradictory outcome 若影响判断，必须保留。
