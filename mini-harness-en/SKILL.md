---
name: mini-harness-en
description: >-
  Scaffold a standard Agent harness in any repo: run init_harness.py to generate
  harness/, AGENTS.md, pytest.ini, gate scripts, and the full todo/PROGRESS/DECISIONS/plans/code_review
  workflow; weekly harness review on Mondays. Works with Cursor, Codex, Claude Code, and Skills CLI.
  Always enable when the user asks to create, initialize, or install a harness.
metadata:
  version: "1.2.0"
  repository: mini-harness
  locale: en
  install-cli: "npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -g -y"
---

# Agent Harness

**Primary goal**: After installation, use the **same Agent conversation** to generate a **standard, complete** harness collaboration workspace in any repo (Cursor / Codex / Claude Code, etc.).

For day-to-day development, follow the generated `AGENTS.md` for regular and commit rounds. Recommended companion Skills: `tdd`, `code-review-expert`, `code-simplifier`.

Install paths: [references/installation.md](references/installation.md) · Chinese Skill: [../mini-harness-zh](../mini-harness-zh/) · Docs: [../docs/en/](../docs/en/)

---

## Create harness (Agent must do this)

When the user asks to "create / initialize harness", **you must run the script** — do not hand-write a simplified directory instead.

### Steps

1. **Locate `SKILL_ROOT`** — the parent directory of this file. Script path:
   `SKILL_ROOT/scripts/init_harness.py`

2. **Confirm `REPO_ROOT`** — user-specified directory, default workspace root. If `harness/index.md` already exists and the user did not request overwrite → ask whether to use `--force`.

3. **Run the scaffold** (Agent runs it directly):

```bash
python <SKILL_ROOT>/scripts/init_harness.py --root <REPO_ROOT> --project-name <project-name>
```

On non-Windows or without `.venv\Scripts`, append:

```bash
--lint-cmd '.venv/bin/python harness/scripts/lint_src.py' \
--pytest-cmd '.venv/bin/python -m pytest'
```

4. **Check exit code** — if non-zero, fix the scaffold only; do not tell the user it is complete.

5. **Deliver a summary to the user**:
   - Generated: full `harness/` tree, `AGENTS.md`, `pytest.ini`, maintenance scripts
   - Each round: read `AGENTS.md` + `harness/todo.md` / `PROGRESS.md`
   - Recommended companion Skills: `tdd`, `code-review-expert`, `code-simplifier`

Step-by-step checklist: [references/create-harness.md](references/create-harness.md)

### What the script generates

| Artifact | Description |
|----------|-------------|
| `AGENTS.md` | Playbook (rounds, Subagent, gates, commit) |
| `pytest.ini` | `harness/tests`, excludes `integration` |
| `harness/index.md` | L0 master index + PROGRESS writing guide |
| `harness/todo.md` | Weekly task board |
| `harness/PROGRESS.md` | Mechanical sections + human-written sections |
| `harness/DECISIONS.md` | Active decisions |
| `harness/docs/plan-mode.md` | Plan mode details |
| `harness/docs/weekly-review.md` | Monday Agent weekly review: active/archive checklist |
| `harness/plans/`, `code_review/`, `code_simplifier/`, `backlog/`, `tests/`, `scripts/`, `sql/` | Each with `index.md` |
| `harness/scripts/*.py` | `lint_src`, `sync_progress`, `archive_harness_todo` |

---

## Install this Skill

Copy the entire `mini-harness-en/` directory to:

| Tool | Personal | Project (repo) |
|------|----------|----------------|
| **Cursor** | `~/.cursor/skills/mini-harness-en/` | `<repo>/.cursor/skills/mini-harness-en/` |
| **Codex** | `$CODEX_HOME/skills/mini-harness-en/` | — |
| **Claude Code** | `~/.claude/skills/mini-harness-en/` | `<repo>/.claude/skills/mini-harness-en/` |
| **Universal** | `~/.agents/skills/mini-harness-en/` | `<repo>/.agents/skills/mini-harness-en/` |

**Skills CLI:** `npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -g -y`

- **Do not** put it in `~/.cursor/skills-cursor/` (Cursor built-in)
- **Codex**: after install, prompt the user to **restart**
- **Claude Code**: project path is `.claude/skills/` at the **git repo root**

See [references/installation.md](references/installation.md) for details.

After install, tell the Agent: **"Use mini-harness-en to create harness in this repository"**

---

## Daily rounds (when harness already exists)

Priority: **project-root `AGENTS.md` > this Skill**.

```
Regular: gates(before) → read harness → [Plan] → register todo → [change src/? → tdd] → implement → [code-review] → gates(after) → PROGRESS

Weekly review: gates(before) → weekly-review.md → archive/rewrite harness → archive_harness_todo + sync_progress → gates(after) → PROGRESS

Commit: …regular wrap-up… → code-simplifier → second code-review → dev → test → refresh PROGRESS again
```

### Weekly review round

**First Agent session each Monday** in this repo (or first session of a new calendar week if last week was skipped) must run harness weekly review before other user tasks. Details: `harness/docs/weekly-review.md`. **No dedicated weekly review script** — Agent writes each item per the doc; may invoke `archive_harness_todo.py` and `sync_progress.py`.

| Skill | When | Executor |
|-------|------|----------|
| **tdd** | After registering todo, before changing `src/` | Main Agent |
| **code-review-expert** | Changed `src/` this round (wrap-up) | Subagent |
| **code-simplifier** | User commits and delivery includes `src/` | Subagent |

Subagent artifacts: [references/subagent-artifacts.md](references/subagent-artifacts.md)

> Subagent dispatch varies by tool (Cursor Task, Claude Code subagent, etc.); **harness directories and `AGENTS.md` rules are tool-agnostic**.

### Gates (default)

```powershell
.\.venv\Scripts\python.exe harness/scripts/lint_src.py
.\.venv\Scripts\python.exe -m pytest
```

Wrap-up: `python harness/scripts/sync_progress.py` (`--skip-gates` see [references/bootstrap-config.md](references/bootstrap-config.md))

---

## Further reading

| Document | Content |
|----------|---------|
| [references/installation.md](references/installation.md) | Multi-tool install paths |
| [references/create-harness.md](references/create-harness.md) | Create harness Agent checklist |
| [references/directory-layout.md](references/directory-layout.md) | Directory tree |
| [references/plan-mode.md](references/plan-mode.md) | Major-task Plan |
| [references/progress-todo.md](references/progress-todo.md) | todo / PROGRESS / DECISIONS |
| [references/subagent-artifacts.md](references/subagent-artifacts.md) | Review/refinement artifacts |
| [references/commit-workflow.md](references/commit-workflow.md) | Commit discipline |
| [README.md](README.md) | Skill package overview (English) |
| [../README.md](../README.md) | Repository overview (English) |
| [../README.zh-CN.md](../README.zh-CN.md) | Repository overview (Chinese) |
| [../mini-harness-zh](../mini-harness-zh) | Chinese Skill package |
