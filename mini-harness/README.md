# mini-harness

面向 Claude Code、Codex 与 Cursor 的通用仓库工作流插件。

**第一次试用？** 阅读 [TRIAL.md](TRIAL.md)（约 5 分钟上手）。

插件打包了共享的 Agent Skills 目录，以及各宿主专用的清单与 Session Start 钩子。安装插件后工作流即可使用；在仓库中激活是独立、非破坏性的显式步骤。

## 在仓库中激活

```text
python scripts/mini_harness.py install --root /path/to/repository
python scripts/mini_harness.py doctor --root /path/to/repository
```

安装器会：

- 保留 `harness/` 下由项目自行维护的文件（若仓库根目录已有用户自有的 `AGENTS.md`，**不会**删除或覆盖）；
- 将 **Skills**、**scripts** 与模板快照迁移到目标仓库的 `harness/`；
- 创建仓库根目录 `tests/`；
- 不猜测项目的构建或测试命令。

激活后，仓库内典型布局：

```text
harness/
  skills/           # 内置 Agent Skills（含 using-harness/SKILL.md 工作流）
  scripts/          # install / update / doctor
  PROGRESS.md
  todo.md
  ...
tests/              # 全部测试文件
```

工作流入口在插件 `skills/using-harness/SKILL.md`（细则在同目录 `references/workflow.md`）；`install` 会同步到 `harness/skills/using-harness/`。安装插件后即可按该 Skill 工作。

目标项目执行 `install` 后，团队成员即可使用 `harness/skills/` 与 `harness/scripts/`，无需每人单独配置插件路径。

## 维护 mini-harness（权威源）

本目录 **`mini-harness/` 是唯一权威源**。using-harness Skill、其它 Skills、安装器与模板的变更须**先在此修改**，再同步到已激活仓库：

```text
python mini-harness/scripts/mini_harness.py install --root /path/to/repository
python harness/scripts/mini_harness.py doctor --root /path/to/repository
python -m pytest mini-harness/tests
```

勿只改已激活仓库内的 `harness/skills/` 而忘记回写插件——`doctor` 会检测 `.package` 漂移，新仓库 `install` 也会分发过时内容。详见 `skills/using-harness/SKILL.md` 的「维护者与权威源」。

## 宿主一键安装

| 宿主 | Marketplace 清单 | 安装方式 |
|------|------------------|----------|
| Claude Code | `.claude-plugin/marketplace.json` | `/plugin marketplace add HYX-LHJ/mini-harness` |
| Cursor | `.cursor-plugin/marketplace.json` | Dashboard → Import `https://github.com/HYX-LHJ/mini-harness` |
| Codex | `.agents/plugins/marketplace.json` | `codex plugin marketplace add github.com/HYX-LHJ/mini-harness` |

安装插件后，在目标项目执行 `install` 激活 harness。详见 [skills/using-harness/references/host-support.md](skills/using-harness/references/host-support.md)。

## 宿主包（本地开发）

- Claude Code：`.claude-plugin/plugin.json`
- Codex：`.codex-plugin/plugin.json`
- Cursor：`.cursor-plugin/plugin.json`

### Claude Code

本地测试：

```text
claude --plugin-dir /path/to/mini-harness
```

团队分发时，通过 Claude Code 插件市场发布同一目录。Claude 清单会显式选择 Claude 钩子适配器。

### Codex

通过 Codex 市场条目暴露该目录，再从市场安装 `mini-harness`。安装后请开启新会话。Codex 用户须在钩子执行前审阅并信任插件钩子。

### Cursor

本地测试时，将本目录复制或符号链接到：

```text
~/.cursor/plugins/local/mini-harness
```

重启 Cursor 或重新加载窗口。更广泛分发时，通过 Cursor 市场发布同一目录。

## 运行时依赖

安装器与 Session Start 钩子需要 Python 3.10 及以上，且可通过 `python` 调用。这是插件运行时依赖，不要求目标仓库使用特定语言或框架。

## 验证

```text
python -m pytest mini-harness/tests
python scripts/mini_harness.py doctor --root /path/to/repository
```
