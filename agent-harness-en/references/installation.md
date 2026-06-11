# Skill install paths (multi-tool)

When explaining install options to the user, pick paths based on their tool. Full docs: [docs/installation.md](../../../docs/installation.md)

## Supported tools

| Tool | Personal path | Project path |
|------|---------------|--------------|
| Cursor | `~/.cursor/skills/agent-harness-en/` | `<repo>/.cursor/skills/agent-harness-en/` |
| Codex | `$CODEX_HOME/skills/agent-harness-en/` | — |
| Claude Code | `~/.claude/skills/agent-harness-en/` | `<repo>/.claude/skills/agent-harness-en/` |
| Universal | `~/.agents/skills/agent-harness-en/` | `<repo>/.agents/skills/agent-harness-en/` |

## Skills CLI

```bash
npx skills add HYX-LHJ/round-harness --list
npx skills add HYX-LHJ/round-harness --skill agent-harness-en -g -y   # global
npx skills add HYX-LHJ/round-harness --skill agent-harness-en -y      # project
npx skills add HYX-LHJ/round-harness --skill agent-harness-en -a cursor -a claude-code -a codex -g -y
```

See [docs/skills-cli.md](../../../docs/skills-cli.md) for details.

## Rules

- Copy the **entire** `agent-harness-en/` directory (including `SKILL.md`)
- Cursor: **do not** put it in `~/.cursor/skills-cursor/`
- Codex: after install, prompt the user to **restart Codex**
- Claude Code: project-level path is `.claude/skills/` at the **git repo root**
- Locate `SKILL_ROOT`: parent directory of this file (`agent-harness-en/`)

Public install docs (EN/ZH): [docs/installation.md](../../../docs/installation.md)
