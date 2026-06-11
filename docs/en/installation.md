# Installation

### Supported tools

`agent-harness-en` is a **portable Agent Skill** — not tied to a single IDE. It works anywhere that loads a `SKILL.md` directory:

| Tool | Personal (global) | Project (repo-shared) | Notes |
|------|-------------------|----------------------|-------|
| **[Cursor](https://cursor.com/)** | `~/.cursor/skills/agent-harness-en/` | `<repo>/.cursor/skills/agent-harness-en/` | Do **not** use `~/.cursor/skills-cursor/` (built-in skills) |
| **[Codex](https://github.com/openai/codex)** | `$CODEX_HOME/skills/agent-harness-en/` | — | Default `$CODEX_HOME` is `~/.codex`; **restart Codex** after install |
| **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** | `~/.claude/skills/agent-harness-en/` | `<repo>/.claude/skills/agent-harness-en/` | Claude Code resolves `.claude/skills/` at the **git repo root** |
| **Universal / cross-agent** | `~/.agents/skills/agent-harness-en/` | `<repo>/.agents/skills/agent-harness-en/` | Shared convention across multiple agent tools |
| **Skills CLI** | see below | see below | Open ecosystem installer — [skills.sh](https://skills.sh/) |

> **Generic rule:** copy the entire `agent-harness-en/` folder (must include `SKILL.md`) into your tool's skill directory. If your tool has no standard path, point it at this folder or add `SKILL.md` to your agent's context manually.

### Method 1 — Skills CLI (recommended for universal install)

Requires [Node.js](https://nodejs.org/) (`npx`):

```bash
# List skills in this repo
npx skills add HYX-LHJ/round-harness --list

# Global (user-level)
npx skills add HYX-LHJ/round-harness --skill agent-harness-en -g -y

# Project-level (committed with the repo)
npx skills add HYX-LHJ/round-harness --skill agent-harness-en -y

# Target Cursor + Claude Code + Codex
npx skills add HYX-LHJ/round-harness --skill agent-harness-en -a cursor -a claude-code -a codex -g -y
```

Browse skills at [skills.sh](https://skills.sh/). Full guide: [skills-cli.md](skills-cli.md).

### Method 2 — Git clone + copy

```bash
git clone https://github.com/HYX-LHJ/round-harness.git
```

Then copy `round-harness/agent-harness-en/` to the path for your tool (see table above).

**Windows (PowerShell) — Cursor personal:**

```powershell
Copy-Item -Recurse round-harness\agent-harness-en $env:USERPROFILE\.cursor\skills\agent-harness-en
```

**macOS / Linux — Claude Code personal:**

```bash
cp -r round-harness/agent-harness-en ~/.claude/skills/agent-harness-en
```

**macOS / Linux — Codex:**

```bash
cp -r round-harness/agent-harness-en "${CODEX_HOME:-$HOME/.codex}/skills/agent-harness-en"
```

### Method 3 — Symlink (developers)

```bash
# Example: universal cross-agent path
ln -s "$(pwd)/round-harness/agent-harness-en" ~/.agents/skills/agent-harness-en
```

### Method 4 — Vendor into your repo

Commit the skill inside your project so the whole team shares it:

```text
your-repo/
├── .cursor/skills/agent-harness-en/    # Cursor
├── .claude/skills/agent-harness-en/    # Claude Code
└── .agents/skills/agent-harness-en/    # Universal
```

You only need **one** of these paths depending on which tools your team uses.

### Verify installation

1. Restart your agent tool (or reload skills).
2. Ask the agent: *"List available skills"* or *"Do you have agent-harness-en?"*
3. In a target repo, say: **"Use agent-harness-en to create harness in this repository"**

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

Install companion skills to the **same tool-specific path** as `agent-harness-en`.
