# 宿主支持

插件共享 `skills/`、`hooks/` 与安装器；各宿主通过仓库根目录的 **marketplace 清单** 与插件目录内的 **manifest** 完成一键安装。

## 一键安装（插件）

安装插件后，在**目标项目**执行 `mini_harness.py install` 激活 harness（见 [SKILL.md](../SKILL.md)）。

### Claude Code

在 Claude Code 会话中：

```text
/plugin marketplace add HYX-LHJ/mini-harness
/plugin install mini-harness@mini-harness
```

或 CLI：

```bash
claude plugin marketplace add HYX-LHJ/mini-harness
claude plugin install mini-harness@mini-harness
```

本地开发：

```bash
claude --plugin-dir /path/to/mini-harness/mini-harness
```

### Cursor

**从 GitHub 导入（推荐）**

1. 打开 [Cursor Dashboard](https://cursor.com/dashboard) → **Settings** → **Plugins**
2. **Import Marketplace**（或 Team Marketplaces → Add Marketplace）
3. 粘贴仓库 URL：`https://github.com/HYX-LHJ/mini-harness`
4. 在 Cursor 插件面板安装 **mini-harness**

**本地开发**

```text
~/.cursor/plugins/local/mini-harness  →  克隆仓库中的 mini-harness/ 目录
```

重启 Cursor 或执行 **Developer: Reload Window**。

### Codex

```bash
codex plugin marketplace add github.com/HYX-LHJ/mini-harness
codex plugin install mini-harness
```

首次启用插件钩子时，在 Codex 中审阅并信任 Session Start 钩子，然后**新开会话**。

个人市场（`~/.agents/plugins/marketplace.json`）也可指向本仓库克隆路径进行本地测试。

## 清单与钩子

| 宿主 | 仓库 marketplace | 插件 manifest | Session Start 钩子 |
|------|------------------|---------------|-------------------|
| Claude Code | `.claude-plugin/marketplace.json` | `mini-harness/.claude-plugin/plugin.json` | `hooks/claude/hooks.json` |
| Codex | `.agents/plugins/marketplace.json` | `mini-harness/.codex-plugin/plugin.json` | `hooks/hooks.json`（默认） |
| Cursor | `.cursor-plugin/marketplace.json` | `mini-harness/.cursor-plugin/plugin.json` | `hooks/cursor/hooks.json` |

Codex 要求用户审阅并信任插件捆绑的钩子。任何宿主上，钩子都可能被托管策略禁用。仓库仍可使用，因为 `AGENTS.md` 是持久的工作流入口；钩子仅是提醒。
