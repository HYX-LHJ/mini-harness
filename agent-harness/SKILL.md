---
name: agent-harness
description: >-
  Scaffold and run a standard Agent harness in any repository: run init_harness.py
  to create harness/, AGENTS.md, pytest.ini, gate scripts, and the full
  todo/PROGRESS/DECISIONS/plans/code_review workflow. Portable across Cursor,
  Codex, Claude Code, Skills CLI (npx skills), and any agent that loads SKILL.md
  directories. Use whenever the user asks to create or initialize harness, set up
  agent engineering, bootstrap AGENTS.md, or adopt structured Agent round workflows
  — even if they only say "搭建协作目录" or "装 harness".
metadata:
  version: "1.0.0"
  repository: round-harness
  install-cli: "npx skills add HYX-LHJ/round-harness --skill agent-harness -g -y"
---

# Agent Harness

**Purpose:** After install, the **same agent conversation** scaffolds a **standard, complete** harness in any repository — on **Cursor, Codex, Claude Code**, or other SKILL.md-compatible agents.

Daily work follows the generated `AGENTS.md`. Recommended companion skills: `tdd`, `code-review-expert`, `code-simplifier`.

Install paths: [references/installation.md](references/installation.md) · Human docs: [docs/installation.md](../../docs/installation.md)

---

## Create harness (agent MUST)

When the user asks to create / initialize harness, **run the script** — do not hand-write a simplified directory.

### Steps

1. **Locate `SKILL_ROOT`** — parent of this file's directory. Script:
   `SKILL_ROOT/scripts/init_harness.py`

2. **Confirm `REPO_ROOT`** — user's target repo (default: workspace root). If `harness/index.md` exists and user did not ask to overwrite → ask about `--force`.

3. **Run scaffold** (agent executes):

```bash
python <SKILL_ROOT>/scripts/init_harness.py --root <REPO_ROOT> --project-name <name>
```

On non-Windows or without `.venv\Scripts`, append:

```bash
--lint-cmd '.venv/bin/python harness/scripts/lint_src.py' \
--pytest-cmd '.venv/bin/python -m pytest'
```

4. **Check exit code** — non-zero: fix scaffold only; do not claim success.

5. **Deliver summary** to user:
   - Generated: full `harness/` tree, `AGENTS.md`, `pytest.ini`, maintenance scripts
   - Each round: read `AGENTS.md` + `harness/todo.md` / `PROGRESS.md`
   - Recommend companion skills: `tdd`, `code-review-expert`, `code-simplifier`

Checklist: [references/create-harness.md](references/create-harness.md)

### What the script generates

| Artifact | Description |
|----------|-------------|
| `AGENTS.md` | Playbook (rounds, subagents, gates, commits) |
| `pytest.ini` | `harness/tests`, excludes `integration` |
| `harness/index.md` | L0 index + PROGRESS guide |
| `harness/todo.md` | Weekly task board |
| `harness/PROGRESS.md` | Mechanical + human sections |
| `harness/DECISIONS.md` | Active decisions |
| `harness/docs/plan-mode.md` | Plan mode rules |
| `harness/plans/`, `code_review/`, `code_simplifier/`, `backlog/`, `tests/`, `scripts/`, `sql/` | Each with `index.md` |
| `harness/scripts/*.py` | `lint_src`, `sync_progress`, `archive_harness_todo` |

---

## Install this skill

Copy the entire `agent-harness/` directory to a skill path for the user's tool:

| Tool | Personal | Project (repo) |
|------|----------|----------------|
| **Cursor** | `~/.cursor/skills/agent-harness/` | `<repo>/.cursor/skills/agent-harness/` |
| **Codex** | `$CODEX_HOME/skills/agent-harness/` | — |
| **Claude Code** | `~/.claude/skills/agent-harness/` | `<repo>/.claude/skills/agent-harness/` |
| **Universal** | `~/.agents/skills/agent-harness/` | `<repo>/.agents/skills/agent-harness/` |

**Skills CLI:** `npx skills add HYX-LHJ/round-harness@agent-harness -g -y`

- **Do not** put in `~/.cursor/skills-cursor/` (Cursor built-ins)
- **Codex:** tell user to restart Codex after install
- **Claude Code:** project path is `.claude/skills/` at **git repo root**

Full guide: [references/installation.md](references/installation.md)

After install, user can say: **"Use agent-harness to create harness in this repository"** (or Chinese equivalent).

---

## Daily rounds (harness already exists)

Priority: **project root `AGENTS.md` > this Skill**.

```
Regular: gates(before) → read harness → [Plan] → register todo → [change src/? → tdd] → implement → [code-review] → gates(after) → PROGRESS

Commit: …regular wrap-up… → code-simplifier → 2nd code-review → dev → test → refresh PROGRESS
```

| Skill | When | Executor |
|-------|------|----------|
| **tdd** | After todo, before `src/` changes | Main agent |
| **code-review-expert** | After `src/` changes (wrap-up) | Subagent |
| **code-simplifier** | User commits with `src/` changes | Subagent |

Subagent artifacts: [references/subagent-artifacts.md](references/subagent-artifacts.md)

> Subagent dispatch differs by tool (Cursor Task, Claude Code subagents, etc.). Harness **file layout and `AGENTS.md` rules are tool-agnostic**.

### Default gates

```powershell
.\.venv\Scripts\python.exe harness/scripts/lint_src.py
.\.venv\Scripts\python.exe -m pytest
```

Wrap-up: `python harness/scripts/sync_progress.py` (`--skip-gates`: [references/bootstrap-config.md](references/bootstrap-config.md))

---

## Further reading

| Doc | Content |
|-----|---------|
| [references/installation.md](references/installation.md) | Multi-tool install paths |
| [references/create-harness.md](references/create-harness.md) | Create harness checklist |
| [references/directory-layout.md](references/directory-layout.md) | Directory tree |
| [references/plan-mode.md](references/plan-mode.md) | Plan mode for major tasks |
| [references/progress-todo.md](references/progress-todo.md) | todo / PROGRESS / DECISIONS |
| [references/subagent-artifacts.md](references/subagent-artifacts.md) | Review / simplify artifacts |
| [references/commit-workflow.md](references/commit-workflow.md) | Commit discipline |
| [README.md](README.md) | Human quick reference |
| [../../docs/installation.md](../../docs/installation.md) | Full bilingual install guide |
