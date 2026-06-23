# 宿主支持

插件共享一个 `skills/` 目录，并为各宿主提供专用清单与 Session Start 钩子。

| 宿主 | 清单 | 钩子配置 |
|------|------|----------|
| Claude Code | `.claude-plugin/plugin.json` | `hooks/claude/hooks.json` |
| Codex | `.codex-plugin/plugin.json` | `hooks/codex/hooks.json` |
| Cursor | `.cursor-plugin/plugin.json` | `hooks/cursor/hooks.json` |

Codex 要求用户审阅并信任插件捆绑的钩子。任何宿主上，钩子都可能被托管策略禁用。仓库仍可使用，因为
`AGENTS.md` 是持久的工作流入口；钩子仅是提醒。
