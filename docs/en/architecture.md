# Architecture

mini-harness uses a **two-layer architecture**: the plugin scaffolds once; the harness directory holds ongoing collaboration state.

### Two layers

```text
mini-harness repo                    your project repo
┌─────────────────────┐              ┌─────────────────────┐
│ mini-harness/         │  install     │ AGENTS.md           │
│  AGENTS.md (source)   │ ──────────►  │ harness/            │
│  skills/, scripts/    │              │  todo, PROGRESS, …  │
│  assets/template/     │              │ tests/              │
└─────────────────────┘              └─────────────────────┘
```

**Principles:**

1. **Plugin vs harness** — Plugin can be upgraded; harness lives in your repo
2. **Files as state** — Agents read files each round, not chat history
3. **Single source of truth** — Each information type has one canonical location
4. **Authoritative source** — Edit `mini-harness/` only; `install` syncs to repos

### Standard harness tree

```text
your-repo/
├── AGENTS.md                 # Playbook (project root)
├── tests/                    # All tests
└── harness/
    ├── index.md              # L0 entry
    ├── todo.md               # Current task + AC (only place to check boxes)
    ├── PROGRESS.md           # Snapshot: state, in-progress, completed
    ├── DECISIONS.md          # Long-term constraints
    ├── skills/               # Built-in skills (tdd, review, …)
    ├── rules/                # Coding conventions
    ├── scripts/              # mini_harness.py (install/update/doctor)
    ├── plans/                # Plan documents
    ├── acceptance/           # Acceptance reports
    ├── docs/                 # Collaboration docs (plan-mode, weekly-review)
    ├── code_review/          # Review reports + open-findings
    ├── code_simplifier/      # Simplify reports
    ├── backlog/              # Archived todos
    └── .package/             # Version snapshot for drift detection
```

### Single source of truth

| Question | Read |
|----------|------|
| What tasks remain? | `harness/todo.md` unchecked items |
| How to onboard a new session? | `PROGRESS.md` "current state" + "in progress" |
| Why can't we change X? | `harness/DECISIONS.md` |
| Known tech debt? | `code_review/open-findings.md` |
| Pre-implementation plan? | `harness/plans/` |
| What should agent do each round? | Project root `AGENTS.md` |
| Which skill to use? | `harness/skills/<name>/SKILL.md` |

**Priority:** `AGENTS.md` > skill `SKILL.md` in `harness/skills/`.

### Naming conventions

| Type | Format | Example |
|------|--------|---------|
| Plan | `YYYY-MM-DD-topic.md` | `2026-06-11-user-auth.md` |
| Code review | `YYYY-MM-DD_topic.md` | `2026-06-11_user-auth-review.md` |
| Acceptance | `YYYY-MM-DD_topic.md` | `2026-06-11_user-auth-acceptance.md` |
| Backlog archive | `YYYY-MM-DD-topic.md` | `2026-06-11-user-auth.md` |

### Installer commands

| Command | Role |
|---------|------|
| `install` | Create/sync harness, skills, scripts, rules, AGENTS.md |
| `update` | Refresh managed files from `.package` snapshot |
| `doctor` | Health check + drift warnings |
| `uninstall` | Remove managed harness (preserves project extensions) |

### Relationship to business code

```text
your-repo/
├── src/ or agent/    # Business code (tdd + review required when changed)
├── harness/          # Collaboration control plane (not runtime)
├── AGENTS.md
└── tests/            # Tests at repo root (not harness/tests/)
```

Gate commands (pytest, ruff, mypy) are project-specific — configured via `python-code-style` into `pyproject.toml` and summarized in `DECISIONS.md`.
