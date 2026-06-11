# Skill 安装路径（多工具）— mini-harness-zh

完整文档：[docs/zh-CN/installation.md](../../../docs/zh-CN/installation.md) · 英文 Skill：[mini-harness-en](../../mini-harness-en/)

## 支持的工具

| 工具 | 个人路径 | 项目路径 |
|------|----------|----------|
| Cursor | `~/.cursor/skills/mini-harness-zh/` | `<repo>/.cursor/skills/mini-harness-zh/` |
| Codex | `$CODEX_HOME/skills/mini-harness-zh/` | — |
| Claude Code | `~/.claude/skills/mini-harness-zh/` | `<repo>/.claude/skills/mini-harness-zh/` |
| 通用 | `~/.agents/skills/mini-harness-zh/` | `<repo>/.agents/skills/mini-harness-zh/` |

## Skills CLI

```bash
npx skills add HYX-LHJ/mini-harness --list
npx skills add HYX-LHJ/mini-harness --skill mini-harness-zh -g -y
npx skills add HYX-LHJ/mini-harness --skill mini-harness-en -g -y   # 英文版
```

## 规则

- 复制**整个** `mini-harness-zh/` 目录（含 `SKILL.md`）
- Cursor：**勿**放入 `~/.cursor/skills-cursor/`
- Codex：安装后**重启**
- `SKILL_ROOT` = 本文件所在目录的上一级
