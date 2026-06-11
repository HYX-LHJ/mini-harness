# Skill 安装路径（多工具）

Agent 向用户说明安装方式时，按用户使用的工具选择路径。完整文档：[docs/installation.md](../../../docs/installation.md)

## 支持的工具

| 工具 | 个人路径 | 项目路径 |
|------|----------|----------|
| Cursor | `~/.cursor/skills/agent-harness/` | `<repo>/.cursor/skills/agent-harness/` |
| Codex | `$CODEX_HOME/skills/agent-harness/` | — |
| Claude Code | `~/.claude/skills/agent-harness/` | `<repo>/.claude/skills/agent-harness/` |
| 通用 | `~/.agents/skills/agent-harness/` | `<repo>/.agents/skills/agent-harness/` |

## Skills CLI

```bash
npx skills add HYX-LHJ/round-harness --list
npx skills add HYX-LHJ/round-harness --skill agent-harness -g -y   # 全局
npx skills add HYX-LHJ/round-harness --skill agent-harness -y      # 项目
npx skills add HYX-LHJ/round-harness --skill agent-harness -a cursor -a claude-code -a codex -g -y
```

详见 [docs/skills-cli.md](../../../docs/skills-cli.md)

## 规则

- 复制**整个** `agent-harness/` 目录（含 `SKILL.md`）
- Cursor：**勿**放入 `~/.cursor/skills-cursor/`
- Codex：安装后提示用户**重启 Codex**
- Claude Code：项目级路径在 **git 仓库根** 的 `.claude/skills/`
- 定位 `SKILL_ROOT`：本文件所在目录的上一级（`agent-harness/`）

对外安装说明（中英）：[docs/installation.md](../../../docs/installation.md)
