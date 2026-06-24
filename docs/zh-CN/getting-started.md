# 快速入门

本文介绍如何在项目中激活 mini-harness。

### 前置条件

| 依赖 | 说明 |
|------|------|
| Agent 工具 | Cursor、Codex 或 Claude Code |
| Python 3.10+ | 运行 `mini_harness.py` 与 Session 钩子 |
| Git 仓库 | 目标项目建议已 `git init` |

目标项目跑通门禁（经 `python-code-style` 配置后）：

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\pip install ruff pytest mypy
# Unix:    .venv/bin/pip install ruff pytest mypy
```

### 第一步 — 获取插件

通过市场安装（推荐）或克隆仓库。**安装插件后即可使用 `skills/using-harness/SKILL.md`** — 无需先执行仓库 `install`。

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
```

**宿主插件**（Skills + 可选 Session 开场提醒）：

| 宿主 | 本地测试 |
|------|----------|
| Cursor | 复制/符号链接 `mini-harness/` → `~/.cursor/plugins/local/mini-harness` |
| Claude Code | `claude --plugin-dir /path/to/mini-harness` |
| Codex | 从市场安装；信任钩子；新开会话 |

详见 [installation.md](installation.md)。

### 第二步 — 在仓库中激活 harness

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**通过 Agent（推荐）：**

> 在当前仓库初始化 mini-harness — 执行 install 和 doctor。

安装器会创建 `harness/`、`tests/`，将内置 Skill 同步到 `harness/skills/`，并写入 `harness/scripts/mini_harness.py`。**不会**在项目根创建或覆盖 `AGENTS.md` — 工作流在 `harness/skills/using-harness/SKILL.md`（安装插件后即可使用）。

| 参数 | 说明 |
|------|------|
| `--root` | 目标仓库根目录（默认当前目录） |

若仓库根目录已有用户自有的 `AGENTS.md`，`install` 会原样保留。

### 第三步 — 内置 Skill（无需单独安装）

激活后 Skill 位于 `harness/skills/`：

| Skill | 时机 |
|-------|------|
| `tdd` + `python-testing-patterns` | 编写运行时代码前（subagent） |
| `acceptance-verification` | 实现完成后（subagent） |
| `code-review-expert` | 实现完成后（subagent） |
| `code-simplifier` | 提交前（subagent） |
| `brainstorming` | 做 Plan 时 |
| `python-code-style` | 初始化时一次（Python 工具链） |

任务中写明仓库路径，例如 `harness/skills/tdd/SKILL.md`，**不要**用全局 `~/.agents/skills/`。

### 第四步 — 定制

- 可执行规则 → `harness/profile/PROJECT.md`
- 重大决策 → `harness/DECISIONS.md`（按主题）
- 协作文档 → `harness/docs/`
- 编码规范 → `harness/rules/`

### 验证

`doctor` 返回 `ok: true` 且无 warnings，且存在：

```text
harness/index.md、harness/todo.md、harness/PROGRESS.md
harness/scripts/mini_harness.py
harness/skills/using-harness/SKILL.md
tests/
```

对 Agent 说：「读 harness/skills/using-harness/SKILL.md 和 harness/PROGRESS.md，总结当前状态」。

### 常见问题

**已有 `harness/`？** 安装器保留项目自有文件；受管模板幂等更新。运行 `doctor` 检查漂移。

**非 Python 项目？** 可跳过 `python-code-style`；纯文档仓库也能用 harness。

**Agent 跳过 todo / AC？** 提醒按 using-harness skill 硬约束 — 先登记 todo 并确认 AC 再实现。

### 下一步

- [architecture.md](architecture.md) — 目录设计
- [workflow.md](workflow.md) — 回合与提交
- [installation.md](installation.md) — 多宿主安装完整指南
- [TRIAL.md](../../mini-harness/TRIAL.md) — 5 分钟试用
