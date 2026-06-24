# 🏗️ Architecture

mini-harness = **plugin** (scaffold once) + **harness/** (ongoing collaboration state).

---

## Two layers

```text
mini-harness repo                       your project
┌─────────────────────┐              ┌─────────────────────┐
│ mini-harness/         │  install     │ harness/            │
│  skills/using-harness/│ ──────────►  │  skills/, todo,     │
│  skills/, scripts/    │              │  PROGRESS, profile… │
│  assets/template/     │              │ tests/              │
└─────────────────────┘              └─────────────────────┘
         ▲
         │ plugin install — skills + hooks, usable immediately
```

### Principles

1. **Plugin ≠ harness** — plugin delivers skills; `install` scaffolds state
2. **Files as state** — new sessions read files, not chat memory
3. **Single source of truth** — each info type has one home
4. **Authority in plugin** — edit `mini-harness/` only; `install` syncs repos

---

## 📂 Harness tree

```text
your-repo/
├── tests/                    # 🧪 all tests (repo root)
└── harness/
    ├── index.md
    ├── todo.md               # current task + AC
    ├── PROGRESS.md           # snapshot
    ├── DECISIONS.md          # 🏛️ major decisions by topic
    ├── profile/              # 🎯 PROJECT.md, evolution.jsonl (project-owned)
    ├── skills/
    ├── scripts/
    ├── plans/
    ├── acceptance/
    ├── code_review/
    ├── code_simplifier/
    ├── backlog/
    ├── docs/
    └── .package/             # drift detection snapshot
```

---

## 🗺️ Where to look

| Question | Read |
|----------|------|
| What tasks remain? | `todo.md` unchecked items |
| How to hand off a session? | `PROGRESS.md` |
| Why can't we change X? | `DECISIONS.md` (by topic) |
| What agent obeys each round? | `profile/PROJECT.md` |
| Gate commands? | `pyproject.toml` · `commands.gate` |
| Tech debt? | `code_review/open-findings.md` |
| Pre-implementation plan? | `plans/` |
| Workflow entry? | `skills/using-harness/SKILL.md` |
| Which skill? | `skills/<name>/SKILL.md` |

---

## 🌱 Profile & evolution

| Layer | Path | Owner |
|-------|------|-------|
| Platform | `skills/`, templates | plugin `update` |
| Project | `profile/`, `DECISIONS` | team; `update` **never** overwrites profile |

**Major tradeoffs** → `DECISIONS` topic; **actionable rules** → `PROJECT.md`; append `evolution.jsonl` after confirm.

---

## 📝 Naming

| Type | Format | Example |
|------|--------|---------|
| Plan | `YYYY-MM-DD-topic.md` | `2026-06-11-user-auth.md` |
| Review | `YYYY-MM-DD_topic.md` | `2026-06-11_user-auth-review.md` |
| Acceptance | `YYYY-MM-DD_topic.md` | `2026-06-11_user-auth-acceptance.md` |
| Backlog | `YYYY-MM-DD-topic.md` | `2026-06-11-user-auth.md` |

---

## ⚙️ Installer

| Command | Role |
|---------|------|
| `install` | Create/sync harness, skills, scripts |
| `update` | Refresh managed files from `.package` |
| `doctor` | Health check + drift warnings |
| `uninstall` | Remove managed harness |

---

## Business code

```text
your-repo/
├── harness/          # collaboration state
├── src/ or agent/    # business code (tdd + review for changes)
└── tests/            # tests at repo root
```

Gates: `python-code-style` → `pyproject.toml` + `commands.gate`; optional ref in `PROJECT.md`.
