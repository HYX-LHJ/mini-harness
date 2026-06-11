# scripts — maintenance and gates

Run from **repository root**.

## Per-round gates

| Script | Purpose |
|--------|---------|
| [lint_src.py](lint_src.py) | ruff + pyright (only `{{SRC_DIR}}/` ) |
| (pytest) | `pytest.ini` → [../tests/](../tests/), excludes `integration` marker |

```powershell
{{LINT_CMD}}
{{PYTEST_CMD}}
```

## PROGRESS / todo

| Script | Purpose |
|--------|---------|
| [sync_progress.py](sync_progress.py) | Refresh PROGRESS mechanical sections; `--skip-gates`, `--dry-run` |
| [archive_harness_todo.py](archive_harness_todo.py) | Cross-week todo archive → [../backlog/archive.md](../backlog/archive.md) (Agent invokes during weekly review round) |
