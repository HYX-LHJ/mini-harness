# Getting Started

This guide walks you through activating mini-harness in your project.

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| An agent tool | Cursor, Codex, or Claude Code |
| Python 3.10+ | For `mini_harness.py` and session hooks |
| Git repo | Recommended for target project |

For Python gates in the target repo (after `python-code-style` setup):

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\pip install ruff pytest mypy
# Unix:    .venv/bin/pip install ruff pytest mypy
```

### Step 1 — Get the plugin

Clone or vendor the `mini-harness/` directory into your environment:

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
```

**Optional — host plugin** (session-start reminders only):

| Host | Local test |
|------|------------|
| Cursor | Copy/symlink `mini-harness/` → `~/.cursor/plugins/local/mini-harness` |
| Claude Code | `claude --plugin-dir /path/to/mini-harness` |
| Codex | Install from marketplace; trust hooks; new session |

See [installation.md](installation.md) for details.

### Step 2 — Activate harness in your repo

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**Via agent (recommended):**

> Initialize mini-harness in this repository — run install and doctor.

The installer creates `AGENTS.md`, `harness/`, `tests/`, syncs built-in skills to `harness/skills/`, and writes `harness/scripts/mini_harness.py`.

| Flag | Description |
|------|-------------|
| `--root` | Target repo root (default: cwd) |

Existing `AGENTS.md` is **not overwritten** unless the repo has none.

### Step 3 — Built-in skills (no separate install)

After activation, skills live in `harness/skills/`:

| Skill | When |
|-------|------|
| `tdd` + `python-testing-patterns` | Before runtime code (subagent) |
| `acceptance-verification` | After implementation (subagent) |
| `code-review-expert` | After implementation (subagent) |
| `code-simplifier` | Before commit (subagent) |
| `brainstorming` | During Plan mode |
| `python-code-style` | Once at init (Python toolchain) |

Always reference repo paths, e.g. `harness/skills/tdd/SKILL.md` — not global `~/.agents/skills/`.

### Step 4 — Customize

- Project constraints → `harness/DECISIONS.md`
- Collaboration docs → `harness/docs/`
- Coding rules → `harness/rules/` or `DECISIONS.md`

### Verify

`doctor` returns `ok: true` with no warnings, and these exist:

```text
AGENTS.md
harness/index.md, harness/todo.md, harness/PROGRESS.md
harness/scripts/mini_harness.py
harness/skills/mini-harness/SKILL.md
tests/
```

Ask your agent: *"Read AGENTS.md and harness/PROGRESS.md, then summarize current state."*

### FAQ

**Existing `harness/`?** The installer preserves project-owned files; managed templates are updated idempotently. Run `doctor` to check drift.

**No Python project?** Skip `python-code-style`; harness still works for docs-only repos.

**Agent skipped todo / AC?** Remind it to follow `AGENTS.md` hard constraints — register todo and confirm AC before implementation.

### Next steps

- [architecture.md](architecture.md) — directory design
- [workflow.md](workflow.md) — rounds and commits
- [installation.md](installation.md) — full multi-host guide
- [TRIAL.md](../../mini-harness/TRIAL.md) — 5-minute trial
