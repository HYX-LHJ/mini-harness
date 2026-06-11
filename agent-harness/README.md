# agent-harness

Portable Agent Skill for [round-harness](../README.md).

**Languages:** [English](#english) · [中文](#中文)

---

<a id="english"></a>

## English

Scaffold a standard agent collaboration harness in **any repository**, on **Cursor, Codex, Claude Code**, or any tool that loads `SKILL.md` directories.

### Install

See **[docs/installation.md](../docs/installation.md)** for all tools.

```bash
# Skills CLI
npx skills add <your-org>/round-harness@agent-harness -g -y

# Or copy agent-harness/ to:
#   ~/.cursor/skills/     (Cursor)
#   ~/.codex/skills/      (Codex)
#   ~/.claude/skills/     (Claude Code)
#   ~/.agents/skills/     (Universal)
```

### Use

Tell your agent:

> Use agent-harness to create harness in this repository

Or run:

```bash
python path/to/agent-harness/scripts/init_harness.py --root /path/to/repo --project-name my_api
```

### Package layout

```text
agent-harness/
├── SKILL.md              # Agent instructions
├── references/           # Agent reference docs
├── templates/            # Scaffold templates
├── bundled/scripts/      # Copied to harness/scripts/
└── scripts/init_harness.py
```

### Docs

| Doc | Audience |
|-----|----------|
| [SKILL.md](SKILL.md) | Agents |
| [references/installation.md](references/installation.md) | Agents + humans |
| [../docs/installation.md](../docs/installation.md) | Humans (full guide) |
| [../docs/getting-started.md](../docs/getting-started.md) | Humans |

---

<a id="chinese"></a>

## 中文

在**任意仓库**、**多种 Agent 工具**（Cursor、Codex、Claude Code 等）上，一键生成标准 harness 协作工程。

### 安装

完整说明见 **[docs/installation.md](../docs/installation.md)**。

```bash
# Skills CLI
npx skills add <your-org>/round-harness@agent-harness -g -y

# 或复制 agent-harness/ 到：
#   ~/.cursor/skills/     （Cursor）
#   ~/.codex/skills/      （Codex）
#   ~/.claude/skills/     （Claude Code）
#   ~/.agents/skills/     （通用）
```

### 使用

对 Agent 说：

> 用 agent-harness 在当前仓库创建 harness

或手动执行：

```bash
python path/to/agent-harness/scripts/init_harness.py --root /path/to/repo --project-name my_api
```

### 包内结构

```text
agent-harness/
├── SKILL.md              # Agent 主指令
├── references/           # Agent 细则
├── templates/            # 落盘模板
├── bundled/scripts/      # 复制到 harness/scripts/
└── scripts/init_harness.py
```

### 文档

| 文档 | 读者 |
|------|------|
| [SKILL.md](SKILL.md) | Agent |
| [references/installation.md](references/installation.md) | Agent + 人类 |
| [../docs/installation.md](../docs/installation.md) | 人类（完整安装指南） |
| [../docs/getting-started.md](../docs/getting-started.md) | 人类 |
