# Post-bootstrap configuration

Agent steps for creating harness: [create-harness.md](create-harness.md).

After `init_harness.py` generates the skeleton, adjust the following per project and record in root `AGENTS.md`.

## Paths

| Variable | Default | Notes |
|----------|---------|-------|
| Business code dir | `src/` | Changing business code requires tdd + code-review |
| Unit test dir | `harness/tests/` | Should match `pytest.ini` |
| Harness root | `harness/` | Renaming not recommended |

## Gate commands

Template default (Windows venv):

```powershell
.\.venv\Scripts\python.exe harness/scripts/lint_src.py
.\.venv\Scripts\python.exe -m pytest
```

On Linux/macOS use `.venv/bin/python`. Without `lint_src.py` temporarily:

```bash
ruff check src/
pyright src/
pytest
```

## Git branches

| Role | Default |
|------|---------|
| Development | `dev` |
| Integration/staging | `test` |
| Do not commit directly | `main` / `master` |

Workflow: commit/push on `dev` → merge to `test` → push → return to `dev`.

## Default do-not-commit

- Local paths, secrets, `.env` values
- Trial artifacts: `harness/out/`, `harness/pre/`
- Unrequested integration scratch code (list specifics in project DECISIONS or AGENTS)

## Bundled scripts (written by `init_harness.py`)

| Script | Purpose |
|--------|---------|
| `sync_progress.py` | Refresh PROGRESS mechanical sections |
| `archive_harness_todo.py` | Cross-week todo archive |
| `lint_src.py` | ruff + pyright wrapper (default checks `src/`) |

## Install this Skill (multi-tool)

Copy entire `agent-harness-en/` (including `SKILL.md`) to the matching path, or use Skills CLI:

```bash
npx skills add HYX-LHJ/mini-harness@agent-harness-en -g -y
```

| Tool | Personal path | Project path |
|------|---------------|--------------|
| **Cursor** | `~/.cursor/skills/agent-harness-en/` | `<repo>/.cursor/skills/agent-harness-en/` |
| **Codex** | `$CODEX_HOME/skills/agent-harness-en/` | — |
| **Claude Code** | `~/.claude/skills/agent-harness-en/` | `<repo>/.claude/skills/agent-harness-en/` |
| **Universal** | `~/.agents/skills/agent-harness-en/` | `<repo>/.agents/skills/agent-harness-en/` |

- Cursor: **do not** put in `~/.cursor/skills-cursor/`
- Codex: **restart** after install
- Full docs: [installation.md](installation.md) · [docs/installation.md](../../../docs/installation.md)
