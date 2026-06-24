# 🚀 Getting Started

Activate mini-harness in your project in a few minutes.

---

## Prerequisites

| Dependency | Notes |
|------------|-------|
| 🤖 Agent tool | Cursor · Codex · Claude Code |
| 🐍 Python 3.10+ | For `mini_harness.py` and hooks |
| 📦 Git repo | Target project should be `git init` |

Python gates (after init via `python-code-style`):

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\pip install ruff pytest mypy
# Unix:    .venv/bin/pip install ruff pytest mypy
```

---

## 1️⃣ Get the plugin

Install from marketplace or clone. **Plugin alone gives you `using-harness`** — no repo `install` required yet.

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
```

| Host | Local dev |
|------|-----------|
| Cursor | `mini-harness/` → `~/.cursor/plugins/local/mini-harness` |
| Claude Code | `claude --plugin-dir /path/to/mini-harness` |
| Codex | Marketplace → trust hooks → new session |

See [installation.md](installation.md).

---

## 2️⃣ Activate harness in your repo

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**Or tell the agent:**

> Initialize mini-harness in this repo — run install and doctor.

You get `harness/`, `tests/`, `harness/skills/`. **No** root `AGENTS.md` — workflow lives in `harness/skills/using-harness/SKILL.md`.

| Flag | Meaning |
|------|---------|
| `--root` | Target repo root (default `.`) |

User-owned root `AGENTS.md` is preserved.

---

## 3️⃣ Built-in skills (bundled)

After activate, skills live in `harness/skills/`:

| Skill | When |
|-------|------|
| `tdd` + `python-testing-patterns` | Before runtime code (subagent) |
| `acceptance-verification` | After implement (subagent) |
| `code-review-expert` | After implement / before commit (subagent) |
| `code-simplifier` | Before commit (subagent) |
| `brainstorming` | Plan mode |
| `python-code-style` | Once at init (Python toolchain) |

Always reference **`harness/skills/tdd/SKILL.md`** — not `~/.agents/skills/`.

---

## 4️⃣ Customize

| What | Where |
|------|-------|
| Rules agent obeys each round | `harness/profile/PROJECT.md` |
| Major decisions | `harness/DECISIONS.md` (by topic) |
| Collab docs | `harness/docs/` |

---

## ✅ Verify

`doctor` → `ok: true`, no warnings; plus:

```text
harness/index.md, todo.md, PROGRESS.md
harness/skills/using-harness/SKILL.md
harness/scripts/mini_harness.py
tests/
```

Ask agent: “Read `harness/skills/using-harness/SKILL.md` and `PROGRESS.md`, summarize state.”

---

## ❓ FAQ

**Already have `harness/`?** Installer keeps project-owned files; run `doctor` for drift.

**Not Python?** Skip `python-code-style`; docs-only repos work fine.

**Agent skips todo / AC?** Remind: using-harness **hard constraints** — todo first, **AC confirmed** before code.

---

## Next

- [architecture.md](architecture.md) — 🏗️ layout
- [workflow.md](workflow.md) — 🔄 rounds & commit
- [installation.md](installation.md) — 🔌 multi-host install
- [TRIAL.md](../../mini-harness/TRIAL.md) — ⏱️ 5-min trial
