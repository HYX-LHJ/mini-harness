# Getting Started / 快速入门

**Languages:** [English](#english) · [中文](#中文)

---

<a id="english"></a>

## English

This guide walks you through installing round-harness and enabling agent collaboration in your project.

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| An agent tool | Cursor, Codex, Claude Code, or any SKILL.md loader |
| Python 3.10+ | For `init_harness.py` and harness scripts |
| Git repo | Recommended for target project |

For gates in the target repo:

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\pip install ruff pyright pytest
# Unix:    .venv/bin/pip install ruff pyright pytest
```

### Step 1 — Install the skill

See **[installation.md](installation.md)** for all tools. Quick options:

```bash
# Skills CLI (universal)
npx skills add HYX-LHJ/round-harness@agent-harness -g -y

# Or clone
git clone https://github.com/HYX-LHJ/round-harness.git
# Then copy agent-harness/ to ~/.cursor/skills/, ~/.claude/skills/, ~/.codex/skills/, or ~/.agents/skills/
```

| Tool | Personal path |
|------|---------------|
| Cursor | `~/.cursor/skills/agent-harness/` |
| Codex | `~/.codex/skills/agent-harness/` |
| Claude Code | `~/.claude/skills/agent-harness/` |
| Universal | `~/.agents/skills/agent-harness/` |

Restart your agent tool after install (required for Codex).

### Step 2 — Initialize harness

**Via agent (recommended):**

> Use agent-harness to create harness in this repository

**Manually:**

```bash
python /path/to/agent-harness/scripts/init_harness.py --root . --project-name my_api

# Linux / macOS
python /path/to/agent-harness/scripts/init_harness.py \
  --root . --project-name my_api \
  --lint-cmd '.venv/bin/python harness/scripts/lint_src.py' \
  --pytest-cmd '.venv/bin/python -m pytest'
```

| Flag | Default | Description |
|------|---------|-------------|
| `--root` | cwd | Target repo root |
| `--project-name` | folder name | Written to `AGENTS.md` |
| `--src-dir` | `src` | Business code directory |
| `--force` | — | Overwrite existing files |
| `--dry-run` | — | Print only, no writes |

### Step 3 — Companion skills (recommended)

| Skill | When |
|-------|------|
| `tdd` | Before changing `src/` |
| `code-review-expert` | After `src/` changes |
| `code-simplifier` | Before commit with `src/` changes |

Install to the **same skill path** as `agent-harness`.

### Step 4 — Customize

- Project constraints → `harness/DECISIONS.md`
- API / deployment docs → `harness/docs/`
- DDL → `harness/sql/`

### Verify

Exit code 0 and these files exist:

```text
AGENTS.md, pytest.ini, harness/index.md, harness/todo.md,
harness/PROGRESS.md, harness/scripts/lint_src.py
```

Ask your agent: *"Read harness/index.md and summarize current state."*

### FAQ

**Existing `harness/`?** Without `--force`, existing files are skipped. Backup then use `--force` to overwrite.

**No `src/`?** Gates may fail; use `--skip-gates` with `sync_progress.py` or adjust `lint_src.py`.

**Agent didn't run init?** Run the script manually; ensure skill is in the correct path for your tool.

### Next steps

- [architecture.md](architecture.md) — directory design
- [workflow.md](workflow.md) — rounds and commits
- [installation.md](installation.md) — full multi-tool guide

---

<a id="chinese"></a>

## 中文

本文介绍如何安装 round-harness，并在你的项目中启用 Agent 协作工程。

### 前置条件

| 依赖 | 说明 |
|------|------|
| Agent 工具 | Cursor、Codex、Claude Code 或任何支持 SKILL.md 的环境 |
| Python 3.10+ | 运行 `init_harness.py` 与维护脚本 |
| Git 仓库 | 目标项目建议已 `git init` |

目标项目跑通门禁：

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\pip install ruff pyright pytest
# Unix:    .venv/bin/pip install ruff pyright pytest
```

### 第一步 — 安装 Skill

完整说明见 **[installation.md](installation.md)**。快速方式：

```bash
# Skills CLI（通用）
npx skills add HYX-LHJ/round-harness@agent-harness -g -y

# 或克隆
git clone https://github.com/HYX-LHJ/round-harness.git
# 将 agent-harness/ 复制到 ~/.cursor/skills/、~/.claude/skills/、~/.codex/skills/ 或 ~/.agents/skills/
```

| 工具 | 个人路径 |
|------|----------|
| Cursor | `~/.cursor/skills/agent-harness/` |
| Codex | `~/.codex/skills/agent-harness/` |
| Claude Code | `~/.claude/skills/agent-harness/` |
| 通用 | `~/.agents/skills/agent-harness/` |

安装后重启 Agent 工具（Codex 必须重启）。

### 第二步 — 初始化 harness

**通过 Agent（推荐）：**

> 用 agent-harness 在当前仓库创建 harness

**手动执行：**

```bash
python /path/to/agent-harness/scripts/init_harness.py --root . --project-name my_api

# Linux / macOS
python /path/to/agent-harness/scripts/init_harness.py \
  --root . --project-name my_api \
  --lint-cmd '.venv/bin/python harness/scripts/lint_src.py' \
  --pytest-cmd '.venv/bin/python -m pytest'
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--root` | 当前目录 | 目标仓库根 |
| `--project-name` | 文件夹名 | 写入 `AGENTS.md` |
| `--src-dir` | `src` | 业务代码目录 |
| `--force` | — | 覆盖已有文件 |
| `--dry-run` | — | 仅打印，不写文件 |

### 第三步 — 配套 Skill（建议）

| Skill | 时机 |
|-------|------|
| `tdd` | 改 `src/` 前 |
| `code-review-expert` | 改过 `src/` 后 |
| `code-simplifier` | 提交前（含 `src/` 变更） |

安装到与 `agent-harness` **相同的路径**。

### 第四步 — 定制

- 项目约束 → `harness/DECISIONS.md`
- API / 部署文档 → `harness/docs/`
- DDL → `harness/sql/`

### 验证

退出码为 0，且以下文件存在：

```text
AGENTS.md、pytest.ini、harness/index.md、harness/todo.md、
harness/PROGRESS.md、harness/scripts/lint_src.py
```

对 Agent 说：「读 harness/index.md，总结当前状态」。

### 常见问题

**已有 `harness/`？** 不加 `--force` 会跳过已有文件；备份后使用 `--force` 覆盖。

**没有 `src/`？** 门禁可能失败；对 `sync_progress.py` 使用 `--skip-gates` 或调整 `lint_src.py`。

**Agent 未执行 init？** 手动运行脚本；确认 Skill 安装在对应工具的正确路径。

### 下一步

- [architecture.md](architecture.md) — 目录设计
- [workflow.md](workflow.md) — 回合与提交
- [installation.md](installation.md) — 多工具安装完整指南
