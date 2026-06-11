# Installation / 安装指南

**Languages:** [English](#english) · [中文](#中文)

---

<a id="english"></a>

## English

### Supported tools

`agent-harness` is a **portable Agent Skill** — not tied to a single IDE. It works anywhere that loads a `SKILL.md` directory:

| Tool | Personal (global) | Project (repo-shared) | Notes |
|------|-------------------|----------------------|-------|
| **[Cursor](https://cursor.com/)** | `~/.cursor/skills/agent-harness/` | `<repo>/.cursor/skills/agent-harness/` | Do **not** use `~/.cursor/skills-cursor/` (built-in skills) |
| **[Codex](https://github.com/openai/codex)** | `$CODEX_HOME/skills/agent-harness/` | — | Default `$CODEX_HOME` is `~/.codex`; **restart Codex** after install |
| **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** | `~/.claude/skills/agent-harness/` | `<repo>/.claude/skills/agent-harness/` | Claude Code resolves `.claude/skills/` at the **git repo root** |
| **Universal / cross-agent** | `~/.agents/skills/agent-harness/` | `<repo>/.agents/skills/agent-harness/` | Shared convention across multiple agent tools |
| **Skills CLI** | see below | see below | Open ecosystem installer — [skills.sh](https://skills.sh/) |

> **Generic rule:** copy the entire `agent-harness/` folder (must include `SKILL.md`) into your tool's skill directory. If your tool has no standard path, point it at this folder or add `SKILL.md` to your agent's context manually.

### Method 1 — Skills CLI (recommended for universal install)

Requires [Node.js](https://nodejs.org/) (`npx`):

```bash
# List skills in this repo
npx skills add <your-org>/round-harness --list

# Global (user-level)
npx skills add <your-org>/round-harness --skill agent-harness -g -y

# Project-level (committed with the repo)
npx skills add <your-org>/round-harness --skill agent-harness -y

# Target Cursor + Claude Code + Codex
npx skills add <your-org>/round-harness --skill agent-harness -a cursor -a claude-code -a codex -g -y
```

Browse skills at [skills.sh](https://skills.sh/). Full guide: [skills-cli.md](skills-cli.md).

### Method 2 — Git clone + copy

```bash
git clone https://github.com/<your-org>/round-harness.git
```

Then copy `round-harness/agent-harness/` to the path for your tool (see table above).

**Windows (PowerShell) — Cursor personal:**

```powershell
Copy-Item -Recurse round-harness\agent-harness $env:USERPROFILE\.cursor\skills\agent-harness
```

**macOS / Linux — Claude Code personal:**

```bash
cp -r round-harness/agent-harness ~/.claude/skills/agent-harness
```

**macOS / Linux — Codex:**

```bash
cp -r round-harness/agent-harness "${CODEX_HOME:-$HOME/.codex}/skills/agent-harness"
```

### Method 3 — Symlink (developers)

```bash
# Example: universal cross-agent path
ln -s "$(pwd)/round-harness/agent-harness" ~/.agents/skills/agent-harness
```

### Method 4 — Vendor into your repo

Commit the skill inside your project so the whole team shares it:

```text
your-repo/
├── .cursor/skills/agent-harness/    # Cursor
├── .claude/skills/agent-harness/    # Claude Code
└── .agents/skills/agent-harness/    # Universal
```

You only need **one** of these paths depending on which tools your team uses.

### Verify installation

1. Restart your agent tool (or reload skills).
2. Ask the agent: *"List available skills"* or *"Do you have agent-harness?"*
3. In a target repo, say: **"Use agent-harness to create harness in this repository"**

### Tool-specific notes

<a id="cursor"></a>

#### Cursor

- Personal skills: `~/.cursor/skills/`
- Project skills: `.cursor/skills/` (can be committed)
- Subagent workflows use Cursor **Task** tool

<a id="codex"></a>

#### Codex

- Skills live under `$CODEX_HOME/skills/` (default `~/.codex/skills/`)
- Install from GitHub: use Codex's `skill-installer` or copy manually
- Restart Codex after adding skills

<a id="claude-code"></a>

#### Claude Code

- Personal: `~/.claude/skills/`
- Project: `.claude/skills/` at **git repository root**
- Subagent behavior may differ from Cursor; harness **file layout and `AGENTS.md` playbook remain the same**

<a id="universal--cross-agent"></a>

#### Universal `~/.agents/skills/`

A cross-tool convention: many agents that support the open skill format will scan this directory. Prefer this when you use **multiple tools** on the same machine.

### Companion skills (optional)

| Skill | Purpose |
|-------|---------|
| `tdd` | Write tests before changing `src/` |
| `code-review-expert` | Subagent code review |
| `code-simplifier` | Pre-commit simplification |

Install companion skills to the **same tool-specific path** as `agent-harness`.

---

<a id="chinese"></a>

## 中文

### 支持的工具

`agent-harness` 是**可移植的 Agent Skill**，不绑定单一 IDE。任何能加载 `SKILL.md` 目录的环境均可使用：

| 工具 | 个人（全局） | 项目（仓库共享） | 说明 |
|------|-------------|-----------------|------|
| **[Cursor](https://cursor.com/)** | `~/.cursor/skills/agent-harness/` | `<repo>/.cursor/skills/agent-harness/` | **勿**放入 `~/.cursor/skills-cursor/`（内置目录） |
| **[Codex](https://github.com/openai/codex)** | `$CODEX_HOME/skills/agent-harness/` | — | 默认 `$CODEX_HOME` 为 `~/.codex`；安装后**重启 Codex** |
| **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** | `~/.claude/skills/agent-harness/` | `<repo>/.claude/skills/agent-harness/` | 从 **git 仓库根** 的 `.claude/skills/` 加载 |
| **通用 / 跨 Agent** | `~/.agents/skills/agent-harness/` | `<repo>/.agents/skills/agent-harness/` | 多工具共用的 Skill 目录约定 |
| **Skills CLI** | 见下文 | 见下文 | 开放生态安装器 — [skills.sh](https://skills.sh/) |

> **通用规则：** 将完整的 `agent-harness/` 文件夹（须含 `SKILL.md`）复制到你所用工具的 Skill 目录；若工具无标准路径，可手动将该目录加入 Agent 上下文。

### 方式一 — Skills CLI（推荐，通用安装）

需要 [Node.js](https://nodejs.org/)（`npx`）：

```bash
# 列出本仓库中的 Skill
npx skills add <your-org>/round-harness --list

# 全局（用户级）
npx skills add <your-org>/round-harness --skill agent-harness -g -y

# 项目级（可提交到仓库）
npx skills add <your-org>/round-harness --skill agent-harness -y

# 指定 Cursor + Claude Code + Codex
npx skills add <your-org>/round-harness --skill agent-harness -a cursor -a claude-code -a codex -g -y
```

浏览 Skill：[skills.sh](https://skills.sh/)。完整指南：[skills-cli.md](skills-cli.md)

### 方式二 — Git 克隆 + 复制

```bash
git clone https://github.com/<your-org>/round-harness.git
```

将 `round-harness/agent-harness/` 复制到上表对应路径。

**Windows（PowerShell）— Cursor 个人：**

```powershell
Copy-Item -Recurse round-harness\agent-harness $env:USERPROFILE\.cursor\skills\agent-harness
```

**macOS / Linux — Claude Code 个人：**

```bash
cp -r round-harness/agent-harness ~/.claude/skills/agent-harness
```

**macOS / Linux — Codex：**

```bash
cp -r round-harness/agent-harness "${CODEX_HOME:-$HOME/.codex}/skills/agent-harness"
```

### 方式三 — 符号链接（开发者）

```bash
# 示例：通用跨 Agent 路径
ln -s "$(pwd)/round-harness/agent-harness" ~/.agents/skills/agent-harness
```

### 方式四 — 内嵌到项目仓库

将 Skill 提交到项目中，团队共享：

```text
your-repo/
├── .cursor/skills/agent-harness/    # Cursor
├── .claude/skills/agent-harness/    # Claude Code
└── .agents/skills/agent-harness/    # 通用
```

按团队实际使用的工具，**任选其一**即可。

### 验证安装

1. 重启 Agent 工具（或重新加载 Skill）
2. 询问 Agent：「列出可用 Skill」或「是否有 agent-harness？」
3. 在目标仓库中说：**「用 agent-harness 在当前仓库创建 harness」**

### 各工具说明

#### Cursor

- 个人 Skill：`~/.cursor/skills/`
- 项目 Skill：`.cursor/skills/`（可提交 git）
- Subagent 通过 Cursor **Task** 工具派遣

#### Codex

- Skill 目录：`$CODEX_HOME/skills/`（默认 `~/.codex/skills/`）
- 可从 GitHub 安装：使用 Codex 的 `skill-installer` 或手动复制
- 新增 Skill 后需重启 Codex

#### Claude Code

- 个人：`~/.claude/skills/`
- 项目：**git 仓库根** 下的 `.claude/skills/`
- Subagent 机制可能与 Cursor 不同；harness **目录结构与 `AGENTS.md` Playbook 保持一致**

#### 通用路径 `~/.agents/skills/`

跨工具约定：支持开放 Skill 格式的 Agent 通常会扫描此目录。同一台机器使用**多种工具**时优先选此路径。

### 配套 Skill（可选）

| Skill | 作用 |
|-------|------|
| `tdd` | 改 `src/` 前先写测试 |
| `code-review-expert` | Subagent 代码审查 |
| `code-simplifier` | 提交前精炼代码 |

配套 Skill 安装到与 `agent-harness` **相同的工具路径**。
