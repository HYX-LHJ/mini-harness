# 🚀 快速入门

几分钟在你的项目里激活 mini-harness。

---

## 前置条件

| 依赖 | 说明 |
|------|------|
| 🤖 Agent 工具 | Cursor · Codex · Claude Code |
| 🐍 Python 3.10+ | 跑 `mini_harness.py` 与钩子 |
| 📦 Git 仓库 | 目标项目建议已 `git init` |

Python 门禁（初始化后，经 `python-code-style` 配置）：

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\pip install ruff pytest mypy
# Unix:    .venv/bin/pip install ruff pytest mypy
```

---

## 1️⃣ 获取插件

市场安装（推荐）或克隆仓库。**装插件就能用 `using-harness` Skill** — 不必先 `install`。

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
```

| 宿主 | 本地试玩 |
|------|----------|
| Cursor | `mini-harness/` → `~/.cursor/plugins/local/mini-harness` |
| Claude Code | `claude --plugin-dir /path/to/mini-harness` |
| Codex | 市场安装 → 信任钩子 → 新会话 |

详见 [installation.md](installation.md)。

---

## 2️⃣ 在仓库激活 harness

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**或对 Agent 说：**

> 在当前仓库初始化 mini-harness — 执行 install 和 doctor。

会得到：`harness/`、`tests/`、`harness/skills/`。**不会**创建根 `AGENTS.md` — 工作流在 `harness/skills/using-harness/SKILL.md`。

| 参数 | 说明 |
|------|------|
| `--root` | 目标仓库根（默认 `.`） |

已有用户自有的 `AGENTS.md` → 原样保留。

---

## 3️⃣ 内置 Skill（已打包）

激活后在 `harness/skills/`：

| Skill | 时机 |
|-------|------|
| `tdd` + `python-testing-patterns` | 写运行时代码前（subagent） |
| `acceptance-verification` | 实现后（subagent） |
| `code-review-expert` | 实现后 / 提交前（subagent） |
| `code-simplifier` | 提交前（subagent） |
| `brainstorming` | Plan 模式 |
| `python-code-style` | 初始化一次（Python 工具链） |

任务里写 **`harness/skills/tdd/SKILL.md`**，别用 `~/.agents/skills/`。

---

## 4️⃣ 定制项目

| 写什么 | 放哪 |
|--------|------|
| 每回合遵守的规则 | `harness/profile/PROJECT.md` |
| 重大架构取舍 | `harness/DECISIONS.md`（按主题） |
| 协作文档 | `harness/docs/` |

---

## ✅ 验证

`doctor` → `ok: true`，且无 warnings；存在：

```text
harness/index.md, todo.md, PROGRESS.md
harness/skills/using-harness/SKILL.md
harness/scripts/mini_harness.py
tests/
```

对 Agent：「读 `harness/skills/using-harness/SKILL.md` 和 `PROGRESS.md`，总结当前状态」。

---

## ❓ 常见问题

**已有 `harness/`？** 安装器保留项目自有文件；受管模板幂等更新。跑 `doctor` 查漂移。

**非 Python？** 可跳过 `python-code-style`；纯文档仓库也能用 harness。

**Agent 跳过 todo / AC？** 提醒按 using-harness **硬约束** — 先 todo，**AC 已确认** 再实现。

---

## 下一步

- [architecture.md](architecture.md) — 🏗️ 目录设计
- [workflow.md](workflow.md) — 🔄 回合与提交
- [installation.md](installation.md) — 🔌 多宿主安装
- [TRIAL.md](../../mini-harness/TRIAL.md) — ⏱️ 5 分钟试用
