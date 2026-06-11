# Installation

### Supported tools

`mini-harness-en` is a **portable Agent Skill** — not tied to a single IDE. It works anywhere that loads a `SKILL.md` directory:

| Tool | Personal (global) | Project (repo-shared) | Notes |
|------|-------------------|----------------------|-------|
| **[Cursor](https://cursor.com/)** | `~/.cursor/skills/mini-harness-en/` | `<repo>/.cursor/skills/mini-harness-en/` | Do **not** use `~/.cursor/skills-cursor/` (built-in skills) |
| **[Codex](https://github.com/openai/codex)** | `$CODEX_HOME/skills/mini-harness-en/` | — | Default `$CODEX_HOME` is `~/.codex`; **restart Codex** after install |
| **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** | `~/.claude/skills/mini-harness-en/` | `<repo>/.claude/skills/mini-harness-en/` | Claude Code resolves `.claude/skills/` at the **git repo root** |
| **Universal / cross-agent** | `~/.agents/skills/mini-harness-en/` | `<repo>/.agents/skills/mini-harness-en/` | Shared convention across multiple agent tools |
| **Skills CLI** | see below | see below | Open ecosystem installer — [skills.sh](https://skills.sh/) |

> **Generic rule:** copy the entire `mini-harness-en/` folder (must include `SKILL.md`) into your tool's skill directory. If your tool has no standard path, point it at this folder or add `SKILL.md` to your agent's context manually.

### Method 1 — Skills CLI (recommended for universal install)

Requires [Node.js](https://nodejs.org/) (`npx`):

```bash
# List skills in this repo
npx skills add HYX-LHJ/mini-harness --list

# Global (user-level)
npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -g -y

# Project-level (committed with the repo)
npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -y

# Target Cursor + Claude Code + Codex
npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -a cursor -a claude-code -a codex -g -y
```

Browse skills at [skills.sh](https://skills.sh/). Full guide: [skills-cli.md](skills-cli.md).

### Method 2 — Git clone + copy

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
```

Then copy `mini-harness/mini-harness-en/` to the path for your tool (see table above).

**Windows (PowerShell) — Cursor personal:**

```powershell
Copy-Item -Recurse mini-harness\mini-harness-en $env:USERPROFILE\.cursor\skills\mini-harness-en
```

**macOS / Linux — Claude Code personal:**

```bash
cp -r mini-harness/mini-harness-en ~/.claude/skills/mini-harness-en
```

**macOS / Linux — Codex:**

```bash
cp -r mini-harness/mini-harness-en "${CODEX_HOME:-$HOME/.codex}/skills/mini-harness-en"
```

### Method 3 — Symlink (developers)

```bash
# Example: universal cross-agent path
ln -s "$(pwd)/mini-harness/mini-harness-en" ~/.agents/skills/mini-harness-en
```

### Method 4 — Vendor into your repo

Commit the skill inside your project so the whole team shares it:

```text
your-repo/
├── .cursor/skills/mini-harness-en/    # Cursor
├── .claude/skills/mini-harness-en/    # Claude Code
└── .agents/skills/mini-harness-en/    # Universal
```

You only need **one** of these paths depending on which tools your team uses.

### Verify installation

1. Restart your agent tool (or reload skills).
2. Ask the agent: *"List available skills"* or *"Do you have mini-harness-en?"*
3. In a target repo, say: **"Use mini-harness-en to create harness in this repository"**

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

Install companion skills to the **same tool-specific path** as `mini-harness-en`.
