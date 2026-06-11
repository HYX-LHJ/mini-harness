# Skills CLI / Skills CLI 指南

**Languages:** [English](#english) · [中文](#中文)

[Skills CLI](https://github.com/vercel-labs/skills) (`npx skills`) installs `agent-harness` to **Cursor, Codex, Claude Code**, and [60+ agents](https://github.com/vercel-labs/skills#supported-agents) in one command.

---

<a id="english"></a>

## English

### Prerequisites

- [Node.js](https://nodejs.org/) 18+ (`npx` available)
- Network access to GitHub

### Discover skills in this repo

```bash
npx skills add HYX-LHJ/round-harness --list
```

Expected output includes **`agent-harness`** (declared in [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json)).

### Install

```bash
# Global — all projects on this machine
npx skills add HYX-LHJ/round-harness --skill agent-harness -g -y

# Project — committed with your team repo
npx skills add HYX-LHJ/round-harness --skill agent-harness -y

# Shorthand (same as --skill agent-harness)
npx skills add HYX-LHJ/round-harness@agent-harness -g -y
```

### Target specific agents

```bash
# Cursor + Claude Code + Codex only
npx skills add HYX-LHJ/round-harness \
  --skill agent-harness \
  -a cursor -a claude-code -a codex \
  -g -y
```

| Agent | `--agent` flag | Global install path |
|-------|----------------|---------------------|
| Cursor | `cursor` | `~/.cursor/skills/agent-harness/` |
| Claude Code | `claude-code` | `~/.claude/skills/agent-harness/` |
| Codex | `codex` | `~/.codex/skills/agent-harness/` |
| Universal | `amp`, `opencode`, … | `~/.agents/skills/agent-harness/` |

Full agent list: [vercel-labs/skills README](https://github.com/vercel-labs/skills#supported-agents).

### Try without installing

```bash
npx skills use HYX-LHJ/round-harness@agent-harness --agent claude-code
```

### Manage installed skills

```bash
npx skills list              # what's installed
npx skills update agent-harness -y
npx skills remove agent-harness -y
npx skills find harness      # search skills.sh ecosystem
```

### Pin in your project

Copy [`.skills.json.example`](../.skills.json.example) to your project as `.skills.json`:

```json
{
  "skills": [
    {
      "name": "agent-harness",
      "remote": "HYX-LHJ/round-harness",
      "skill": "agent-harness"
    }
  ]
}
```

### CI-friendly install

```bash
npx skills add HYX-LHJ/round-harness \
  --skill agent-harness \
  -g -a cursor -y
```

### After install

1. Restart agent tool if needed (Codex requires restart)
2. In target repo: *"Use agent-harness to create harness in this repository"*

---

<a id="chinese"></a>

## 中文

### 前置条件

- [Node.js](https://nodejs.org/) 18+（可用 `npx`）
- 可访问 GitHub

### 发现本仓库中的 Skill

```bash
npx skills add HYX-LHJ/round-harness --list
```

应能看到 **`agent-harness`**（由 [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) 声明）。

### 安装

```bash
# 全局 — 本机所有项目可用
npx skills add HYX-LHJ/round-harness --skill agent-harness -g -y

# 项目级 — 可提交到团队仓库
npx skills add HYX-LHJ/round-harness --skill agent-harness -y

# 简写（等同 --skill agent-harness）
npx skills add HYX-LHJ/round-harness@agent-harness -g -y
```

### 指定 Agent 工具

```bash
# 仅安装到 Cursor + Claude Code + Codex
npx skills add HYX-LHJ/round-harness \
  --skill agent-harness \
  -a cursor -a claude-code -a codex \
  -g -y
```

| 工具 | `--agent` 参数 | 全局安装路径 |
|------|----------------|-------------|
| Cursor | `cursor` | `~/.cursor/skills/agent-harness/` |
| Claude Code | `claude-code` | `~/.claude/skills/agent-harness/` |
| Codex | `codex` | `~/.codex/skills/agent-harness/` |
| 通用 | `amp`、`opencode` 等 | `~/.agents/skills/agent-harness/` |

完整列表：[vercel-labs/skills README](https://github.com/vercel-labs/skills#supported-agents)

### 不安装直接试用

```bash
npx skills use HYX-LHJ/round-harness@agent-harness --agent claude-code
```

### 管理已安装 Skill

```bash
npx skills list              # 查看已安装
npx skills update agent-harness -y
npx skills remove agent-harness -y
npx skills find harness      # 在 skills.sh 生态搜索
```

### 在项目中锁定版本

将 [`.skills.json.example`](../.skills.json.example) 复制为 `.skills.json`：

```json
{
  "skills": [
    {
      "name": "agent-harness",
      "remote": "HYX-LHJ/round-harness",
      "skill": "agent-harness"
    }
  ]
}
```

### CI 中安装

```bash
npx skills add HYX-LHJ/round-harness \
  --skill agent-harness \
  -g -a cursor -y
```

### 安装后

1. 按需重启 Agent 工具（Codex 须重启）
2. 在目标仓库说：「用 agent-harness 在当前仓库创建 harness」
