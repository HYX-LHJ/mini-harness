# 🔧 mini-harness 插件目录

面向 **Claude Code · Codex · Cursor** 的通用仓库工作流插件。

**⏱️ 第一次试用？** → [TRIAL.md](TRIAL.md)（约 5 分钟）

装插件即用 Skills + Session 钩子；在目标仓库 `install` 才会生成持久化 `harness/`。

---

## 在仓库激活

```bash
python scripts/mini_harness.py install --root /path/to/repository
python scripts/mini_harness.py doctor --root /path/to/repository
```

安装器会：

- 📦 同步 `harness/skills/`、`harness/scripts/`、模板快照
- 🧪 创建仓库根 `tests/`
- 🎯 脚手架 `profile/`（`update` 不覆盖）
- ✅ 保留项目自有文件；不覆盖根 `AGENTS.md`
- 🚫 不猜测项目的构建/测试命令

典型布局：

```text
harness/
  skills/        # using-harness、tdd、review…
  scripts/       # install / update / doctor
  profile/       # PROJECT.md（每回合必读）
  PROGRESS.md, todo.md, …
tests/
```

**工作流入口：** `skills/using-harness/SKILL.md`

---

## 🛠️ 维护者：权威源

**只改本目录 `mini-harness/`**，再同步到已激活仓库：

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

本地验证（gitignore，不上 GitHub）：`pytest mini-harness/tests`

勿只改各仓里的 `harness/skills/` 不回写插件 — `doctor` 会报漂移。

---

## 🔌 宿主一键安装

| 宿主 | Marketplace | 安装 |
|------|-------------|------|
| Claude Code | `.claude-plugin/marketplace.json` | `/plugin marketplace add HYX-LHJ/mini-harness` |
| Cursor | `.cursor-plugin/marketplace.json` | Import `https://github.com/HYX-LHJ/mini-harness` |
| Codex | `.agents/plugins/marketplace.json` | `codex plugin marketplace add github.com/HYX-LHJ/mini-harness` |

详情 → [host-support.md](skills/using-harness/references/host-support.md)

---

## 📦 内置 Skills

| Skill | 用途 |
|-------|------|
| `using-harness` | 🧭 工作流入口（每回合先读） |
| `brainstorming` | 💡 Plan / 方案对比 |
| `tdd` | 🧪 红-绿-重构 |
| `python-testing-patterns` | pytest 模式 |
| `acceptance-verification` | ✅ 对照 AC 验收 |
| `code-review-expert` | 🔍 代码审查 |
| `code-simplifier` | ✨ 提交前精炼 |
| `python-code-style` | 🐍 仅初始化工具链 |

---

## ⚙️ 运行时

Python 3.10+（`python` 可调用）。不要求目标仓库特定语言。

```bash
python harness/scripts/mini_harness.py doctor --root .
```
