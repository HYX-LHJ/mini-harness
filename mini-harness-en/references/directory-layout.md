# Harness directory layout

Not a business runtime directory — sits alongside `src/`. Collaboration rules follow project-root `AGENTS.md`.

## Standard tree

```
harness/
├── index.md                 # Master index (L0 entry)
├── todo.md                  # Current weekly task board (only place to check boxes)
├── PROGRESS.md              # Snapshot: branch, diff, gates, in-progress tasks
├── DECISIONS.md             # Active architecture / boundary constraints
├── backlog/
│   ├── index.md
│   ├── archive.md           # Historical weekly todos
│   └── decisions-archive.md # Superseded decisions
├── plans/
│   ├── index.md
│   └── YYYY-MM-DD-topic.md
├── docs/
│   ├── index.md
│   ├── plan-mode.md         # Plan workflow details
│   └── weekly-review.md     # Monday Agent weekly review
├── code_review/
│   ├── index.md
│   ├── open-findings.md
│   ├── open-findings-closed.md   # Closed findings (archive)
│   ├── archive-index.md          # Historical review index (archive)
│   └── YYYY-MM-DD_topic.md
├── code_simplifier/
│   ├── index.md
│   └── YYYY-MM-DD_topic.md
├── tests/                   # Or match pytest.ini target
│   └── index.md
├── scripts/
│   ├── index.md
│   ├── lint_src.py          # Project-specific
│   ├── sync_progress.py     # Refresh PROGRESS mechanical sections
│   └── archive_harness_todo.py  # Cross-week todo archive
└── sql/                     # Optional: DDL
    └── index.md
```

## Naming conventions

| Type | Format | Example |
|------|--------|---------|
| Plan | `YYYY-MM-DD-topic.md` | `2026-01-15-user-auth.md` |
| Code review | `YYYY-MM-DD_topic-summary.md` | `2026-01-20-user-auth-review.md` |
| Code simplifier | Same as review | `2026-01-20-user-auth.md` |

Date first for easy sorting.

## index.md rules

Each subdirectory has one `index.md`: one-line purpose + table pointing to files in that directory (new → old). `harness/index.md` is the Agent's L0 entry each round.

## gitignore recommendations

```
harness/out/
harness/pre/
harness/.pytest-tmp/
```

Local trial runs and one-off artifacts stay out of the repo.

## Single source of truth (what to read)

| You want to know… | Read first |
|-------------------|------------|
| What tasks remain | Unchecked items in `todo.md` |
| Hand off to a new session | PROGRESS "Current state" + "In progress" |
| Why you cannot change it that way | `DECISIONS.md` |
| Known tech debt | `code_review/open-findings.md` |
| Pre-implementation plan | `plans/` |
