# 项目画像

> 由 mini-harness 脚手架生成于 `harness/profile/`。填写后删除本提示。本文件为**项目自有**，插件 `update` 不会覆盖。

Agent **每回合必读**。只写当前可执行的协作规则，不写长篇决策背景（背景进 `DECISIONS.md` 按主题归档）。

## 技术栈与布局

- 语言 / 框架：（填写）
- 业务代码目录：（如 `src/`、`app/`）
- 测试目录：`tests/`（仓库根）

## 本地门禁

权威配置在仓库根 **`pyproject.toml`**；可选在 `harness/.mini-harness.json` 的 `commands.gate` 登记命令列表。  
此处只写**本项目常用的一键门禁**（与配置一致即可，勿重复维护两套）：

```text
gate:
  - （例）pytest -q
  - （例）ruff check .
```

## 协作例外

- （例）仅改 `docs/` 时可跳过 TDD subagent

## 禁止事项

- （例）不得提交 `.env`、密钥文件
- （例）不得跳过 AC 核对直接写运行时代码

## 与 DECISIONS 的关系

- **重大取舍**（为何选 A 而非 B）→ 写入 `harness/DECISIONS.md` 对应主题
- **提炼后的可执行规则** → 写在本文件
- 确认后追加 `harness/profile/evolution.jsonl` 一行（`status`: `applied` | `rejected`）
