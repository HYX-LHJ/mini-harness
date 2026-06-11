# Skill 安装路径（多工具）— agent-harness-zh

完整文档：[docs/zh-CN/installation.md](../../../docs/zh-CN/installation.md) · 英文 Skill：[agent-harness-en](../../agent-harness-en/)

## 支持的工具

| 工具 | 个人路径 | 项目路径 |
|------|----------|----------|
| Cursor | `~/.cursor/skills/agent-harness-zh/` | `<repo>/.cursor/skills/agent-harness-zh/` |
| Codex | `$CODEX_HOME/skills/agent-harness-zh/` | — |
| Claude Code | `~/.claude/skills/agent-harness-zh/` | `<repo>/.claude/skills/agent-harness-zh/` |
| 通用 | `~/.agents/skills/agent-harness-zh/` | `<repo>/.agents/skills/agent-harness-zh/` |

## Skills CLI

```bash
npx skills add HYX-LHJ/mini-harness --list
npx skills add HYX-LHJ/mini-harness --skill agent-harness-zh -g -y
npx skills add HYX-LHJ/mini-harness --skill agent-harness-en -g -y   # 英文版
```

## 规则

- 复制**整个** `agent-harness-zh/` 目录（含 `SKILL.md`）
- Cursor：**勿**放入 `~/.cursor/skills-cursor/`
- Codex：安装后**重启**
- `SKILL_ROOT` = 本文件所在目录的上一级
