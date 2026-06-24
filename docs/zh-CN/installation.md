# 🔌 安装指南

mini-harness 以**宿主插件**分发，支持 Claude Code、Cursor、Codex。

| 步骤 | 得到什么 |
|------|----------|
| 装插件 | Skills + Session 钩子 |
| 仓库 `install` | 持久化 `harness/` 状态 |

---

## 一键安装插件

| 宿主 | 操作 |
|------|------|
| **Claude Code** | `/plugin marketplace add HYX-LHJ/mini-harness` → `/plugin install mini-harness@mini-harness` |
| **Cursor** | Dashboard → Plugins → Import `https://github.com/HYX-LHJ/mini-harness` → 安装 **mini-harness** |
| **Codex** | `codex plugin marketplace add github.com/HYX-LHJ/mini-harness` → `codex plugin install mini-harness` |

然后在**目标项目**激活：

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

---

<details>
<summary>📖 各宿主详细步骤</summary>

### Claude Code

```text
/plugin marketplace add HYX-LHJ/mini-harness
/plugin install mini-harness@mini-harness
```

本地：`claude --plugin-dir /path/to/repo/mini-harness`

### Cursor

1. [Cursor Dashboard](https://cursor.com/dashboard) → **Plugins**
2. Import → `https://github.com/HYX-LHJ/mini-harness`
3. 安装 **mini-harness**

本地：`~/.cursor/plugins/local/mini-harness` → 重载窗口

### Codex

```bash
codex plugin marketplace add github.com/HYX-LHJ/mini-harness
codex plugin install mini-harness
```

信任钩子 → **新开会话**

</details>

---

## 两层关系

| | 内容 | 必须？ |
|--|------|--------|
| 1️⃣ 插件 | 上表一键安装 | 推荐 |
| 2️⃣ 激活 | `mini_harness.py install` | **是**（生成 harness） |

### 清单位置

| 宿主 | Marketplace | Manifest |
|------|-------------|----------|
| Claude Code | `.claude-plugin/marketplace.json` | `mini-harness/.claude-plugin/plugin.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `mini-harness/.cursor-plugin/plugin.json` |
| Codex | `.agents/plugins/marketplace.json` | `mini-harness/.codex-plugin/plugin.json` |

---

## 仅克隆 + 激活（不装插件）

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
cd your-project
python /path/to/mini-harness/mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

---

## 维护命令

```bash
python harness/scripts/mini_harness.py install --root .   # 同步
python harness/scripts/mini_harness.py update --root .  # 刷新受管文件
python harness/scripts/mini_harness.py doctor --root .  # 健康检查
python harness/scripts/mini_harness.py uninstall --root .
```

---

## ✅ 验证

1. **插件**：宿主里能看到 `using-harness` Skill；Codex 须信任钩子
2. **仓库**：`doctor` → `ok: true`；存在 `harness/skills/using-harness/SKILL.md`

Python 3.10+（Windows 可用 `py`）。安装器仅用标准库。

更多 → [host-support.md](../../mini-harness/skills/using-harness/references/host-support.md)
