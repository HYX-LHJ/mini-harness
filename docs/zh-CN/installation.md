# 安装指南

mini-harness 是**可移植插件**，包含共享 Skills、宿主清单与 Session Start 钩子。插件安装与仓库激活是**两个独立步骤**。

### 两步流程

| 步骤 | 内容 | 是否必须 |
|------|------|----------|
| 1. 插件 | 安装宿主插件（可选提醒） | 否 — 仓库激活即可使用 |
| 2. 激活 | 在目标仓库执行 `mini_harness.py install` | **是** |

### 支持的宿主

| 宿主 | 清单 | 钩子 |
|------|------|------|
| [Cursor](https://cursor.com/) | `.cursor-plugin/plugin.json` | `hooks/cursor/hooks.json` |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `.claude-plugin/plugin.json` | `hooks/claude/hooks.json` |
| [Codex](https://github.com/openai/codex) | `.codex-plugin/plugin.json` | `hooks/codex/hooks.json` |

钩子提醒 Agent 读取 `AGENTS.md`；Playbook 才是持久的工作流入口。

### 方式一 — 克隆 + 激活（推荐）

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
cd your-project
python /path/to/mini-harness/mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**Windows（PowerShell）：**

```powershell
python mini-harness\scripts\mini_harness.py install --root .
python harness\scripts\mini_harness.py doctor --root .
```

### 方式二 — 将插件纳入仓库

提交插件目录，团队共享同一版本：

```text
your-repo/
├── mini-harness/          # 插件源码（或子模块）
├── AGENTS.md              # install 后生成
├── harness/               # install 后生成
└── tests/
```

团队成员 pull 后执行 `python harness/scripts/mini_harness.py install --root .`。

### 方式三 — 宿主插件（可选）

<a id="cursor"></a>

#### Cursor

本地测试 — 复制或符号链接：

```text
~/.cursor/plugins/local/mini-harness  →  /path/to/mini-harness
```

重启 Cursor 或重新加载窗口。

<a id="claude-code"></a>

#### Claude Code

```bash
claude --plugin-dir /path/to/mini-harness
```

团队分发可通过 Claude Code 插件市场发布。

<a id="codex"></a>

#### Codex

从 Codex 市场安装 `mini-harness`。执行前须**审阅并信任**捆绑钩子。安装后**新开会话**。

### 维护命令（已激活仓库）

```bash
python harness/scripts/mini_harness.py install --root .   # 同步模板与 Skills
python harness/scripts/mini_harness.py update --root .
python harness/scripts/mini_harness.py doctor --root .
python harness/scripts/mini_harness.py uninstall --root .
```

### 验证

1. `doctor` → `ok: true`，`warnings` 为空
2. 仓库根目录有 `AGENTS.md`
3. 存在 `harness/skills/mini-harness/SKILL.md`
4. 新 Agent 会话：「读 AGENTS.md 和 harness 状态文件」

### 运行时要求

- Python 3.10+，可通过 `python`（Windows 可用 `py`）调用
- 安装器本身无第三方依赖
- 不规定目标仓库的语言或框架

### 维护者说明

**只改** `mini-harness/`（权威源），再在目标仓库重新 `install`。见 [mini-harness/skills/mini-harness/SKILL.md](../../mini-harness/skills/mini-harness/SKILL.md)。
