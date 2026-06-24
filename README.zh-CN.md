# mini-harness

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/HYX-LHJ/mini-harness/actions/workflows/validate-scaffold.yml/badge.svg)](https://github.com/HYX-LHJ/mini-harness/actions/workflows/validate-scaffold.yml)

**[English README](README.md)**

---

## 一句话

**可移植的 Agent 工作流插件** — 安装插件即可获得 **using-harness skill**（superpowers 式 Playbook，见 `skills/using-harness/SKILL.md`）；在仓库执行 `install` 一次性生成 `harness/` 状态目录。支持 **Cursor · Codex · Claude Code**。

---

## 本仓库是什么

这是 **插件源码仓库**，不是已激活 harness 的项目。只改 `mini-harness/`；在你自己的项目（或临时目录）执行 `install` 才会生成 `harness/`、`tests/`。**不要**把这些 install 产物提交回本仓库。

```text
mini-harness/   # 权威插件源码（skills、安装器、模板）
docs/           # 用户文档
.github/        # CI
```

---

## 快速开始

### 1. 安装插件（一键）

| 宿主 | 操作 |
|------|------|
| **Claude Code** | `/plugin marketplace add HYX-LHJ/mini-harness` → `/plugin install mini-harness@mini-harness` |
| **Cursor** | Dashboard → Plugins → 导入 `https://github.com/HYX-LHJ/mini-harness` → 安装 **mini-harness** |
| **Codex** | `codex plugin marketplace add github.com/HYX-LHJ/mini-harness` → `codex plugin install mini-harness` |

详见 [docs/zh-CN/installation.md](docs/zh-CN/installation.md)

### 2. 在目标仓库激活 harness

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**可选 — 本地插件开发**（不经市场导入）：

第一次试用？见 [mini-harness/TRIAL.md](mini-harness/TRIAL.md)（约 5 分钟）。

---

## 为什么需要它

| 没有 harness | 有 harness |
|-------------|-----------|
| 每开新对话从零开始 | `PROGRESS.md` + `todo.md` **无缝接手** |
| 改完就提交 | **pytest / ruff / mypy 门禁** + subagent 审查 |
| Plan、审查只在聊天里 | **落盘到 git** |
| 每人一套 Prompt | 统一 **using-harness skill**（`SKILL.md`） |

---

## 你会得到什么

| 产物 | 作用 |
|------|------|
| `skills/using-harness/SKILL.md` | 每回合 Playbook（插件内；`install` 后位于 `harness/skills/`） |
| `harness/todo.md` | 当前任务与验收标准（AC） |
| `harness/PROGRESS.md` | 进度快照 |
| `harness/skills/` | 内置 Skill（tdd、code-review、acceptance 等） |
| `harness/scripts/` | `mini_harness.py`（install / update / doctor） |
| `tests/` | 全部测试文件（仓库根目录） |

<details>
<summary>生成后的目录结构</summary>

```text
your-repo/
├── tests/
└── harness/
    ├── todo.md、PROGRESS.md、DECISIONS.md
    ├── skills/、rules/、scripts/
    ├── plans/、acceptance/、code_review/、backlog/
    └── ...
```

</details>

---

## 文档

| 中文 | English |
|------|---------|
| [docs/zh-CN/](docs/zh-CN/) | [docs/en/](docs/en/) |
| [快速入门](docs/zh-CN/getting-started.md) | [Getting started](docs/en/getting-started.md) |
| [安装指南](docs/zh-CN/installation.md) | [Installation](docs/en/installation.md) |
| [架构说明](docs/zh-CN/architecture.md) | [Architecture](docs/en/architecture.md) |
| [协作流程](docs/zh-CN/workflow.md) | [Workflow](docs/en/workflow.md) |

插件维护文档：[mini-harness/README.md](mini-harness/README.md) · [using-harness](mini-harness/skills/using-harness/SKILL.md)

---

## 协作流程概览

```mermaid
flowchart LR
    A["用户输入"] --> B["读 harness 状态"]
    B --> C{"重大任务?"}
    C -->|是| D["Plan + 确认 AC"]
    C -->|否| E["登记 todo + AC"]
    D --> E
    E --> F["AC 已确认?"]
    F -->|否| G["等待用户"]
    F -->|是| H["Subagent 写测试"]
    H --> I["实现 + 本地门禁"]
    I --> J["Subagent 验收 ∥ 审查"]
    J --> K["归档 + PROGRESS"]
    K --> L{"用户要求提交?"}
    L -->|是| M["精炼 → 审查 → Git"]
    L -->|否| N["回合结束"]
    M --> N
```

详见 [docs/zh-CN/workflow.md](docs/zh-CN/workflow.md)

---

## 要求

Python 3.10+ · 支持 Skill / 插件的 Agent 工具 · 可选：`ruff`、`pytest`、`mypy`

[CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) · [CHANGELOG.md](CHANGELOG.md) · [MIT License](LICENSE)
