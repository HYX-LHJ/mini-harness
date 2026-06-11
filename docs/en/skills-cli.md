# Skills CLI

### Prerequisites

- [Node.js](https://nodejs.org/) 18+ (`npx` available)
- Network access to GitHub

### Discover skills in this repo

```bash
npx skills add HYX-LHJ/mini-harness --list
```

Expected output includes **`agent-harness-en`** (declared in [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json)).

### Install

```bash
# Global — all projects on this machine
npx skills add HYX-LHJ/mini-harness --skill agent-harness-en -g -y

# Project — committed with your team repo
npx skills add HYX-LHJ/mini-harness --skill agent-harness-en -y

# Shorthand (same as --skill agent-harness-en)
npx skills add HYX-LHJ/mini-harness@agent-harness-en -g -y
```

### Target specific agents

```bash
# Cursor + Claude Code + Codex only
npx skills add HYX-LHJ/mini-harness \
  --skill agent-harness-en \
  -a cursor -a claude-code -a codex \
  -g -y
```

| Agent | `--agent` flag | Global install path |
|-------|----------------|---------------------|
| Cursor | `cursor` | `~/.cursor/skills/agent-harness-en/` |
| Claude Code | `claude-code` | `~/.claude/skills/agent-harness-en/` |
| Codex | `codex` | `~/.codex/skills/agent-harness-en/` |
| Universal | `amp`, `opencode`, … | `~/.agents/skills/agent-harness-en/` |

Full agent list: [vercel-labs/skills README](https://github.com/vercel-labs/skills#supported-agents).

### Try without installing

```bash
npx skills use HYX-LHJ/mini-harness@agent-harness-en --agent claude-code
```

### Manage installed skills

```bash
npx skills list              # what's installed
npx skills update agent-harness-en -y
npx skills remove agent-harness-en -y
npx skills find harness      # search skills.sh ecosystem
```

### Pin in your project

Copy [`.skills.json.example`](../.skills.json.example) to your project as `.skills.json`:

```json
{
  "skills": [
    {
      "name": "agent-harness-en",
      "remote": "HYX-LHJ/mini-harness",
      "skill": "agent-harness-en"
    }
  ]
}
```

### CI-friendly install

```bash
npx skills add HYX-LHJ/mini-harness \
  --skill agent-harness-en \
  -g -a cursor -y
```

### After install

1. Restart agent tool if needed (Codex requires restart)
2. In target repo: *"Use agent-harness-en to create harness in this repository"*
