# Create harness — Agent execution checklist

After others install the **mini-harness-en** Skill, the **same Agent conversation** can generate a standard harness in any repo. This document is the Agent step-by-step checklist.

## User phrases that trigger this

- "Create harness", "Initialize harness", "Set up agent workspace"
- "Install mini-harness-en for me", "Set up collaboration directories"

## Agent required steps (in order; do not skip)

### 1. Locate the skill directory

`SKILL_ROOT` = this Skill's install path (`mini-harness-en/` directory), varies by tool:

| Tool | Personal path | Project path |
|------|---------------|--------------|
| Cursor | `~/.cursor/skills/mini-harness-en/` | `<repo>/.cursor/skills/mini-harness-en/` |
| Codex | `$CODEX_HOME/skills/mini-harness-en/` | — |
| Claude Code | `~/.claude/skills/mini-harness-en/` | `<repo>/.claude/skills/mini-harness-en/` |
| Universal | `~/.agents/skills/mini-harness-en/` | `<repo>/.agents/skills/mini-harness-en/` |

Or via Skills CLI: `npx skills add HYX-LHJ/mini-harness@mini-harness-en`

Script path: `<SKILL_ROOT>/scripts/init_harness.py`

See [installation.md](installation.md) for details.

### 2. Confirm target repository

- `REPO_ROOT` = user-specified directory, default current workspace root
- If `harness/index.md` already exists and the user did not request overwrite → ask whether to use `--force`

### 3. Collect parameters (use defaults when inferable)

| Parameter | Default | When to change |
|-----------|---------|----------------|
| `--project-name` | Folder name | User specifies project name |
| `--src-dir` | `src` | Business code is not under `src/` |
| `--dev-branch` / `--test-branch` | `dev` / `test` | Team uses different branches |
| `--lint-cmd` / `--pytest-cmd` | See template | Non-Windows or no venv — adjust paths |

Linux/macOS example:

```bash
--lint-cmd '.venv/bin/python harness/scripts/lint_src.py'
--pytest-cmd '.venv/bin/python -m pytest'
```

### 4. Run scaffold (Agent must run it)

```bash
python <SKILL_ROOT>/scripts/init_harness.py --root <REPO_ROOT> --project-name <NAME>
```

Non-zero exit code → fix scaffold only; do not tell the user it is complete.

### 5. Verify (built into script + Agent visual check)

All of these must exist:

```
AGENTS.md
pytest.ini
harness/index.md
harness/todo.md
harness/PROGRESS.md
harness/DECISIONS.md
harness/docs/plan-mode.md
harness/docs/weekly-review.md
harness/scripts/lint_src.py
harness/scripts/sync_progress.py
harness/scripts/archive_harness_todo.py
harness/code_review/index.md
harness/code_simplifier/index.md
harness/plans/index.md
harness/tests/index.md
```

### 6. Wrap-up message to user

Tell the user:

1. Standard harness generated (directory tree + Playbook + maintenance scripts)
2. Each round: Agent reads `AGENTS.md` + `harness/todo.md` / `PROGRESS.md`
3. Recommended companion Skills: `tdd`, `code-review-expert`, `code-simplifier`
4. If there is `src/` and gates should pass: configure `.venv`, `ruff`, `pyright`, `pytest`
5. First Agent session each Monday must run harness weekly review (see `harness/docs/weekly-review.md`)

### 7. Do not

- **Do not** hand-write a simplified harness instead of running `init_harness.py`
- **Do not** skip `AGENTS.md` or `pytest.ini`
- **Do not** start changing business code before initialization completes

## Generated artifacts

| Artifact | Description |
|----------|-------------|
| Directory tree | `backlog/`, `plans/`, `docs/`, `code_review/`, `code_simplifier/`, `tests/`, `scripts/`, `sql/` |
| `AGENTS.md` | Generic Playbook; project constraints go in `DECISIONS.md` |
| Maintenance scripts | `lint_src`, `sync_progress`, `archive_harness_todo` (bundled with skill) |
| `pytest.ini` | `harness/tests` + excludes `integration` |
| `harness/docs/plan-mode.md` | Plan mode details |
| `harness/docs/weekly-review.md` | Weekly review: Agent active/archive readable surface |

Project-specific content (API docs, DDL, integration tests) is added by the user under `harness/docs/`, `harness/sql/`, `harness/tests/`.
