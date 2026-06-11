# 安装指南

### 支持的工具

`agent-harness-zh` 是**可移植的 Agent Skill**，不绑定单一 IDE。任何能加载 `SKILL.md` 目录的环境均可使用：

| 工具 | 个人（全局） | 项目（仓库共享） | 说明 |
|------|-------------|-----------------|------|
| **[Cursor](https://cursor.com/)** | `~/.cursor/skills/agent-harness-zh/` | `<repo>/.cursor/skills/agent-harness-zh/` | **勿**放入 `~/.cursor/skills-cursor/`（内置目录） |
| **[Codex](https://github.com/openai/codex)** | `$CODEX_HOME/skills/agent-harness-zh/` | — | 默认 `$CODEX_HOME` 为 `~/.codex`；安装后**重启 Codex** |
| **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** | `~/.claude/skills/agent-harness-zh/` | `<repo>/.claude/skills/agent-harness-zh/` | 从 **git 仓库根** 的 `.claude/skills/` 加载 |
| **通用 / 跨 Agent** | `~/.agents/skills/agent-harness-zh/` | `<repo>/.agents/skills/agent-harness-zh/` | 多工具共用的 Skill 目录约定 |
| **Skills CLI** | 见下文 | 见下文 | 开放生态安装器 — [skills.sh](https://skills.sh/) |

> **通用规则：** 将完整的 `agent-harness-zh/` 文件夹（须含 `SKILL.md`）复制到你所用工具的 Skill 目录；若工具无标准路径，可手动将该目录加入 Agent 上下文。

### 方式一 — Skills CLI（推荐，通用安装）

需要 [Node.js](https://nodejs.org/)（`npx`）：

```bash
# 列出本仓库中的 Skill
npx skills add HYX-LHJ/round-harness --list

# 全局（用户级）
npx skills add HYX-LHJ/round-harness --skill agent-harness-zh -g -y

# 项目级（可提交到仓库）
npx skills add HYX-LHJ/round-harness --skill agent-harness-zh -y

# 指定 Cursor + Claude Code + Codex
npx skills add HYX-LHJ/round-harness --skill agent-harness-zh -a cursor -a claude-code -a codex -g -y
```

浏览 Skill：[skills.sh](https://skills.sh/)。完整指南：[skills-cli.md](skills-cli.md)

### 方式二 — Git 克隆 + 复制

```bash
git clone https://github.com/HYX-LHJ/round-harness.git
```

将 `round-harness/agent-harness-zh/` 复制到上表对应路径。

**Windows（PowerShell）— Cursor 个人：**

```powershell
Copy-Item -Recurse round-harness\agent-harness-zh $env:USERPROFILE\.cursor\skills\agent-harness-zh
```

**macOS / Linux — Claude Code 个人：**

```bash
cp -r round-harness/agent-harness-zh ~/.claude/skills/agent-harness-zh
```

**macOS / Linux — Codex：**

```bash
cp -r round-harness/agent-harness-zh "${CODEX_HOME:-$HOME/.codex}/skills/agent-harness-zh"
```

### 方式三 — 符号链接（开发者）

```bash
# 示例：通用跨 Agent 路径
ln -s "$(pwd)/round-harness/agent-harness-zh" ~/.agents/skills/agent-harness-zh
```

### 方式四 — 内嵌到项目仓库

将 Skill 提交到项目中，团队共享：

```text
your-repo/
├── .cursor/skills/agent-harness-zh/    # Cursor
├── .claude/skills/agent-harness-zh/    # Claude Code
└── .agents/skills/agent-harness-zh/    # 通用
```

按团队实际使用的工具，**任选其一**即可。

### 验证安装

1. 重启 Agent 工具（或重新加载 Skill）
2. 询问 Agent：「列出可用 Skill」或「是否有 agent-harness-zh？」
3. 在目标仓库中说：**「用 agent-harness-zh 在当前仓库创建 harness」**

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

配套 Skill 安装到与 `agent-harness-zh` **相同的工具路径**。
