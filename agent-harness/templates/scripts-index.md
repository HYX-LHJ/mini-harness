# scripts — 维护与门禁

均在**仓库根目录**执行。

## 每回合门禁

| 脚本 | 用途 |
|------|------|
| [lint_src.py](lint_src.py) | ruff + pyright（仅 `{{SRC_DIR}}/`） |
| （pytest） | `pytest.ini` → [../tests/](../tests/)，不含 `integration` 标记用例 |

```powershell
{{LINT_CMD}}
{{PYTEST_CMD}}
```

## PROGRESS / todo

| 脚本 | 用途 |
|------|------|
| [sync_progress.py](sync_progress.py) | 刷新 PROGRESS 机械章节；`--skip-gates`、`--dry-run` |
| [archive_harness_todo.py](archive_harness_todo.py) | 跨周归档 todo → [../backlog/archive.md](../backlog/archive.md) |
