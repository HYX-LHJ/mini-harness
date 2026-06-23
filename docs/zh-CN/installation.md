# 安装指南

mini-harness 以 **宿主插件** 形式分发，支持 Claude Code、Cursor、Codex。安装插件可加载 Skills 与 Session 钩子；在项目中 **`mini_harness.py install`** 才会生成 `harness/` 协作工程。

## 一键安装插件

| 宿主 | 操作 |
|------|------|
| **Claude Code** | `/plugin marketplace add HYX-LHJ/mini-harness`，然后 `/plugin install mini-harness@mini-harness` |
| **Cursor** | Dashboard → Settings → Plugins → **Import Marketplace** → `https://github.com/HYX-LHJ/mini-harness` → 安装 **mini-harness** |
| **Codex** | `codex plugin marketplace add github.com/HYX-LHJ/mini-harness`，然后 `codex plugin install mini-harness` |

安装插件后，在**目标项目**激活 harness：

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

或对 Agent 说：「在当前仓库初始化 mini-harness。」

<details>
<summary>各宿主详细步骤</summary>

### Claude Code

```text
/plugin marketplace add HYX-LHJ/mini-harness
/plugin install mini-harness@mini-harness
```

CLI 等价命令：

```bash
claude plugin marketplace add HYX-LHJ/mini-harness
claude plugin install mini-harness@mini-harness
```

本地开发：`claude --plugin-dir /path/to/repo/mini-harness`

### Cursor

1. 打开 [Cursor Dashboard](https://cursor.com/dashboard) → **Settings** → **Plugins**
2. **Import Marketplace** → 粘贴 `https://github.com/HYX-LHJ/mini-harness`
3. 在插件面板安装 **mini-harness**

本地开发：将 `mini-harness/` 复制或符号链接到 `~/.cursor/plugins/local/mini-harness`，然后重新加载窗口。

### Codex

```bash
codex plugin marketplace add github.com/HYX-LHJ/mini-harness
codex plugin install mini-harness
```

按提示审阅并信任捆绑钩子；**新开会话**。

</details>

---

## 两层关系

| 步骤 | 内容 | 是否必须 |
|------|------|----------|
| 1. 插件 | 上表一键安装 | 推荐（Skills + 钩子） |
| 2. 激活 | 目标仓库执行 `mini_harness.py install` | **是**（生成 harness 文件） |

### 清单位置

| 宿主 | Marketplace（仓库根） | 插件 manifest |
|------|----------------------|---------------|
| Claude Code | `.claude-plugin/marketplace.json` | `mini-harness/.claude-plugin/plugin.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `mini-harness/.cursor-plugin/plugin.json` |
| Codex | `.agents/plugins/marketplace.json` | `mini-harness/.codex-plugin/plugin.json` |

### 方式二 — 仅克隆 + 激活（不装插件）

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
cd your-project
python /path/to/mini-harness/mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

### 维护命令（已激活仓库）

```bash
python harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py update --root .
python harness/scripts/mini_harness.py doctor --root .
python harness/scripts/mini_harness.py uninstall --root .
```

### 验证

1. 插件：宿主中可见 `skills/using-harness/SKILL.md`；Codex 须信任 Session 钩子 — 无需仓库 `install` 即可按 Skill 工作
2. 仓库（`install` 后）：`doctor` → `ok: true`，`warnings` 为空；存在 `harness/skills/using-harness/SKILL.md`

### 运行时要求

Python 3.10+（Windows 可用 `py`）。安装器仅使用标准库。

详见：[host-support.md](../../mini-harness/skills/using-harness/references/host-support.md)
