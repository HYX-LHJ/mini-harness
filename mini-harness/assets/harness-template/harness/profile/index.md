# 项目画像（Profile）

本目录为**项目自有**，mini-harness `install`/`update` **不会覆盖**此处内容。

| 文件 | 用途 |
|------|------|
| [PROJECT.md](PROJECT.md) | Agent 每回合必读：可执行的布局、门禁引用、例外与禁止事项 |
| [evolution.jsonl](evolution.jsonl) | 进化审计日志（只追加） |

| 与之区分 | 路径 |
|----------|------|
| 重大决策（背景 / 结论 / 影响，按主题） | [../DECISIONS.md](../DECISIONS.md) |
| 工具链配置 | 仓库根 `pyproject.toml` |

任务归档或周回顾：**重大取舍** → `DECISIONS.md` 对应主题；**可执行规则** → `PROJECT.md`。须经用户确认后写入，并追加 `evolution.jsonl`。
