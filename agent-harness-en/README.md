# agent-harness-en

**Agent Skill package** for Cursor, Codex, Claude Code, and similar tools — part of [round-harness](../README.md). Package docs are **English** by default.

Public repository overview: [README.md (English)](../README.md) · [README.zh-CN.md (Chinese)](../README.zh-CN.md) · [agent-harness-zh (Chinese Skill)](../agent-harness-zh)

## Purpose

After installing this Skill, tell your Agent one sentence to generate a standard harness workspace in **any repository** (directory tree + `AGENTS.md` + gate scripts + collaboration workflow).

## Install

Full instructions: [docs/installation.md](../docs/installation.md)

```bash
npx skills add HYX-LHJ/round-harness --skill agent-harness-en -g -y
```

Or copy `agent-harness-en/` to `~/.cursor/skills/`, `~/.claude/skills/`, `~/.codex/skills/`, `~/.agents/skills/`, etc.

## Usage

Tell the Agent:

> Use agent-harness-en to create harness in this repository

Or run directly:

```bash
python path/to/agent-harness-en/scripts/init_harness.py --root /path/to/repo --project-name my_api
```

## Package layout

```text
agent-harness-en/
├── SKILL.md              # Agent main instructions (English)
├── references/           # Agent reference docs (English)
├── templates/            # Scaffold templates (English; written to user repo)
├── bundled/scripts/      # Bundled maintenance scripts
└── scripts/init_harness.py
```

## Language convention

| Scope | Language |
|-------|----------|
| `agent-harness-en/` (SKILL, references, templates) | **English** |
| `agent-harness-zh/` | **Chinese** — see [agent-harness-zh](../agent-harness-zh) |
| Repository root `README.md` / `README.zh-CN.md`, `docs/` | **Separate EN/ZH docs** |
| User-repo scaffold output (`AGENTS.md`, `harness/`) | **English** (default templates) |

## Further reading for Agents

| Document | Content |
|----------|---------|
| [SKILL.md](SKILL.md) | Create harness and daily rounds |
| [references/](references/) | Install, layout, Plan, commit, etc. |
