# 🖥️ 宿主支持

插件共享 `skills/`、`hooks/` 与安装器。各宿主通过仓库 **marketplace** + 插件 **manifest** 一键安装。

装插件 → **立即可用** `using-harness`；要在项目里持久化 `harness/` → 目标仓库再跑 `install`（见 [lifecycle.md](lifecycle.md)）。

---

## Claude Code

```text
/plugin marketplace add HYX-LHJ/mini-harness
/plugin install mini-harness@mini-harness
```

本地开发：`claude --plugin-dir /path/to/mini-harness/mini-harness`

---

## Cursor

1. [Cursor Dashboard](https://cursor.com/dashboard) → **Plugins**
2. **Import Marketplace** → `https://github.com/HYX-LHJ/mini-harness`
3. 安装 **mini-harness**

本地：`~/.cursor/plugins/local/mini-harness` → 指向仓库 `mini-harness/` 目录，重载窗口。

---

## Codex

```bash
codex plugin marketplace add github.com/HYX-LHJ/mini-harness
codex plugin install mini-harness
```

信任 Session Start 钩子后**新开会话**。

---

## 清单与钩子

| 宿主 | Marketplace | Manifest | Session 钩子 |
|------|-------------|----------|-------------|
| Claude Code | `.claude-plugin/marketplace.json` | `.claude-plugin/plugin.json` | `hooks/claude/` |
| Codex | `.agents/plugins/marketplace.json` | `.codex-plugin/plugin.json` | `hooks/hooks.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `.cursor-plugin/plugin.json` | `hooks/cursor/` |

钩子每轮提醒：**先读 using-harness**（已 install → `harness/skills/…`，否则插件 `skills/…`）。钩子关了也要手动遵守。

---

## ⚠️ 常见坑

| 坑 | 对策 |
|----|------|
| 只装插件没在仓库 `install` | 无 `harness/todo`、无 PROGRESS |
| 读了 `~/.agents/skills/` 同名 Skill | 任务里写明 `harness/skills/...` 路径 |
| Codex 未信任钩子 | 新会话 + 信任后重开 |
