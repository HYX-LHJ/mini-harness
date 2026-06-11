# harness — master index

Not a business runtime directory. Collaboration rules: root [AGENTS.md](../AGENTS.md).

## Per-round entry (L0)

| File | Purpose |
|------|---------|
| [todo.md](todo.md) | Current weekly task board (only place to check boxes) |
| [PROGRESS.md](PROGRESS.md) | Snapshot: branch, diff, gates, in-progress tasks |
| [DECISIONS.md](DECISIONS.md) | **Active** architecture / boundary constraints |
| [backlog/decisions-archive.md](backlog/decisions-archive.md) | Archived / superseded decisions (read-only) |

## Subdirectories (drill into each `index.md`)

| Directory | Index |
|-----------|-------|
| [plans/](plans/) | [plans/index.md](plans/index.md) — major task plans |
| [docs/](docs/) | [docs/index.md](docs/index.md) — integration, Plan workflow |
| [code_review/](code_review/) | [code_review/index.md](code_review/index.md) — review reports, open-findings |
| [code_simplifier/](code_simplifier/) | [code_simplifier/index.md](code_simplifier/index.md) — pre-commit refinement archive |
| [tests/](tests/) | [tests/index.md](tests/index.md) — pytest |
| [scripts/](scripts/) | [scripts/index.md](scripts/index.md) — gates and maintenance scripts |
| [sql/](sql/) | [sql/index.md](sql/index.md) — DDL (optional) |
| [backlog/](backlog/) | [backlog/index.md](backlog/index.md) — historical weekly todos |

`harness/pre/` and `harness/out/` are **gitignored** — local trial runs only, not in repo.

## Tests and gates

Run from repository root (unit tests only):

```powershell
{{LINT_CMD}}
{{PYTEST_CMD}}
```

Wrap-up: `python harness/scripts/sync_progress.py` (`--skip-gates` / `--dry-run` see [scripts/index.md](scripts/index.md)).

**Every Monday** (first Agent session that day): run the [docs/weekly-review.md](docs/weekly-review.md) weekly review round first (see [AGENTS.md](../AGENTS.md)).

If you `git commit` and/or `git push` this round, run `sync_progress.py` again after push and hand-write PROGRESS human sections (see root [AGENTS.md](../AGENTS.md)).

## Single source of truth (what to read)

| You want to know… | Read first |
|-------------------|------------|
| What tasks the Agent still has | Unchecked items in [todo.md](todo.md) |
| Near-term manual/ops intent | PROGRESS "Next steps" |
| What was done this week | PROGRESS "Completed" (mechanical) |
| Whether code is on remote, tests green | PROGRESS "Latest git" / "Tests" / "lint" |
| Hand off to a new session | PROGRESS "Current state" + "In progress" |
| Why you cannot change it that way | [DECISIONS.md](DECISIONS.md) |
| Known tech debt | [open-findings.md](code_review/open-findings.md) |

## How to write PROGRESS.md

Main Agent **hand-writes** "Current state", "Known issues", "Next steps"; rest via `sync_progress.py`.

- **Current state** (≤5 bullets): what a new session needs in 30 seconds; **not** a changelog.
- **Next steps**: near-term intent; **need not** go in todo; remove when done.
- **git / tests / lint / Completed / In progress**: filled by `sync_progress.py`.
- **Known issues**: open P0/P1/P2 only; if none, write "None".
- **After commit/push**: must refresh again.

## Maintaining DECISIONS.md

- Keep ~15–25 active entries; superseded → [backlog/decisions-archive.md](backlog/decisions-archive.md).
- Add when changing how code is written, API contracts, deploy constraints; normal delivery goes in `plans/` + `todo.md`.
