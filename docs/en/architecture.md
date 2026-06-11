# Architecture

round-harness uses a **two-layer architecture**: the Skill package scaffolds once; the harness directory holds ongoing collaboration state.

### Two layers

```text
round-harness repo                    your project repo
┌─────────────────────┐              ┌─────────────────────┐
│ agent-harness-en/      │  init script │ AGENTS.md           │
│  SKILL.md           │ ──────────►  │ pytest.ini          │
│  templates/         │              │ harness/            │
│  bundled/scripts/   │              │  todo, PROGRESS, …  │
└─────────────────────┘              └─────────────────────┘
```

**Principles:**

1. **Skill vs harness** — Skill can be upgraded/reinstalled; harness lives in your repo
2. **Files as state** — Agents read files each round, not chat history
3. **Single source of truth** — Each information type has one canonical location

### Standard harness tree

```text
harness/
├── index.md              # L0 entry
├── todo.md               # Weekly tasks (only place to check boxes)
├── PROGRESS.md           # Snapshot: branch, gates, in-progress tasks
├── DECISIONS.md          # Active architecture constraints
├── plans/                # Plan documents
├── docs/                 # Collaboration docs (plan-mode.md)
├── code_review/          # Review reports + open-findings
├── code_simplifier/      # Simplify reports
├── tests/                # Unit tests
├── scripts/              # lint_src, sync_progress, archive_harness_todo
├── backlog/              # Archived todos / decisions
└── sql/                  # Optional DDL docs
```

Details: [agent-harness-en/references/directory-layout.md](../../agent-harness-en/references/directory-layout.md)

### Single source of truth

| Question | Read |
|----------|------|
| What tasks remain? | `harness/todo.md` unchecked items |
| How to onboard a new session? | `PROGRESS.md` "current state" + "in progress" |
| Why can't we change X? | `harness/DECISIONS.md` |
| Known tech debt? | `code_review/open-findings.md` |
| Pre-implementation plan? | `harness/plans/` |
| What should agent do each round? | Project root `AGENTS.md` |

**Priority:** `AGENTS.md` > Skill `SKILL.md`.

### Naming conventions

| Type | Format | Example |
|------|--------|---------|
| Plan | `YYYY-MM-DD-topic.md` | `2026-06-11-user-auth.md` |
| Code review | `YYYY-MM-DD_topic.md` | `2026-06-11_user-auth-review.md` |
| Code simplifier | same as review | `2026-06-11_user-auth.md` |

### Template placeholders

`init_harness.py` substitutes in templates:

| Placeholder | Default |
|-------------|---------|
| `{{PROJECT_NAME}}` | folder name |
| `{{SRC_DIR}}` | `src` |
| `{{DEV_BRANCH}}` / `{{TEST_BRANCH}}` | `dev` / `test` |
| `{{LINT_CMD}}` / `{{PYTEST_CMD}}` | platform-specific venv commands |

### Maintenance scripts

Copied from `bundled/scripts/` to `harness/scripts/`:

| Script | Role |
|--------|------|
| `lint_src.py` | ruff + pyright on `src/` |
| `sync_progress.py` | Refresh PROGRESS mechanical sections |
| `archive_harness_todo.py` | Archive completed weekly todos |

### Relationship to business code

```text
your-repo/
├── src/          # Business code (tdd + code-review required when changed)
├── harness/      # Collaboration control plane (not runtime)
├── AGENTS.md
└── pytest.ini
```
