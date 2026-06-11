# Getting Started

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
npx skills add HYX-LHJ/round-harness@agent-harness-en -g -y

# Or clone
git clone https://github.com/HYX-LHJ/round-harness.git
# Then copy agent-harness-en/ to ~/.cursor/skills/, ~/.claude/skills/, ~/.codex/skills/, or ~/.agents/skills/
```

| Tool | Personal path |
|------|---------------|
| Cursor | `~/.cursor/skills/agent-harness-en/` |
| Codex | `~/.codex/skills/agent-harness-en/` |
| Claude Code | `~/.claude/skills/agent-harness-en/` |
| Universal | `~/.agents/skills/agent-harness-en/` |

Restart your agent tool after install (required for Codex).

### Step 2 — Initialize harness

**Via agent (recommended):**

> Use agent-harness-en to create harness in this repository

**Manually:**

```bash
python /path/to/agent-harness-en/scripts/init_harness.py --root . --project-name my_api

# Linux / macOS
python /path/to/agent-harness-en/scripts/init_harness.py \
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

Install to the **same skill path** as `agent-harness-en`.

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
