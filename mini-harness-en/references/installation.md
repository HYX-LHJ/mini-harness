# Skill install paths (multi-tool)

When explaining install options to the user, pick paths based on their tool. Full docs: [docs/en/installation.md](../../../docs/en/installation.md)

## Supported tools

| Tool | Personal path | Project path |
|------|---------------|--------------|
| Cursor | `~/.cursor/skills/mini-harness-en/` | `<repo>/.cursor/skills/mini-harness-en/` |
| Codex | `$CODEX_HOME/skills/mini-harness-en/` | — |
| Claude Code | `~/.claude/skills/mini-harness-en/` | `<repo>/.claude/skills/mini-harness-en/` |
| Universal | `~/.agents/skills/mini-harness-en/` | `<repo>/.agents/skills/mini-harness-en/` |

## Skills CLI

```bash
npx skills add HYX-LHJ/mini-harness --list
npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -g -y   # global
npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -y      # project
npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -a cursor -a claude-code -a codex -g -y
```

See [docs/en/skills-cli.md](../../../docs/en/skills-cli.md) for details.

## Rules

- Copy the **entire** `mini-harness-en/` directory (including `SKILL.md`)
- Cursor: **do not** put it in `~/.cursor/skills-cursor/`
- Codex: after install, prompt the user to **restart Codex**
- Claude Code: project-level path is `.claude/skills/` at the **git repo root**
- Locate `SKILL_ROOT`: parent directory of this file (`mini-harness-en/`)

Public install docs (EN/ZH): [docs/README.md](../../../docs/README.md)
