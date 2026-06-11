---
name: agent-harness
description: >-
  在任意仓库脚手架标准 Agent harness：运行 init_harness.py 生成 harness/、AGENTS.md、
  pytest.ini、门禁脚本及 todo/PROGRESS/DECISIONS/plans/code_review 全流程。适用于
  Cursor、Codex、Claude Code、Skills CLI。用户说创建/初始化 harness、搭建协作目录、
  装 harness 时务必启用。Scaffold standard agent harness in any repo; use on create/init
  harness requests.
metadata:
  version: "1.0.0"
  repository: round-harness
  locale: zh-CN
  install-cli: "npx skills add HYX-LHJ/round-harness --skill agent-harness -g -y"
---

# Agent Harness

**首要目的**：安装后，用**相同的 Agent 对话**，在任意仓库生成**标准、完整**的 harness 协作工程（Cursor / Codex / Claude Code 等均可）。

日常开发按生成的 `AGENTS.md` 走常规/提交回合。建议配套 Skill：`tdd`、`code-review-expert`、`code-simplifier`。

安装路径：[references/installation.md](references/installation.md) · 对外文档（中英）：[../README.md](../README.md) · [../README.zh-CN.md](../README.zh-CN.md)

---

## 创建 harness（Agent 必做）

用户要「创建 / 初始化 harness」时，**必须执行脚本**，禁止手写简化目录代替。

### 步骤

1. **定位 `SKILL_ROOT`** — 本文件所在目录的上一级。脚本：
   `SKILL_ROOT/scripts/init_harness.py`

2. **确认 `REPO_ROOT`** — 用户指定目录，默认工作区根。已有 `harness/index.md` 且未要求覆盖 → 先问是否 `--force`。

3. **运行脚手架**（Agent 亲自执行）：

```bash
python <SKILL_ROOT>/scripts/init_harness.py --root <REPO_ROOT> --project-name <项目名>
```

非 Windows 或无 `.venv\Scripts` 时追加：

```bash
--lint-cmd '.venv/bin/python harness/scripts/lint_src.py' \
--pytest-cmd '.venv/bin/python -m pytest'
```

4. **检查退出码** — 非 0 则只修脚手架，不向用户宣称完成。

5. **向用户交付摘要**：
   - 已生成：`harness/` 全树、`AGENTS.md`、`pytest.ini`、维护脚本
   - 后续每回合读 `AGENTS.md` + `harness/todo.md` / `PROGRESS.md`
   - 建议安装配套 Skill：`tdd`、`code-review-expert`、`code-simplifier`

逐步清单：[references/create-harness.md](references/create-harness.md)

### 脚本会生成什么

| 产物 | 说明 |
|------|------|
| `AGENTS.md` | Playbook（回合、Subagent、门禁、提交） |
| `pytest.ini` | `harness/tests`，排除 `integration` |
| `harness/index.md` | L0 总索引 + PROGRESS 写法 |
| `harness/todo.md` | 周任务板 |
| `harness/PROGRESS.md` | 机械章 + 人文章节 |
| `harness/DECISIONS.md` | 活跃决策 |
| `harness/docs/plan-mode.md` | Plan 模式细则 |
| `harness/plans/`、`code_review/`、`code_simplifier/`、`backlog/`、`tests/`、`scripts/`、`sql/` | 各 `index.md` |
| `harness/scripts/*.py` | `lint_src`、`sync_progress`、`archive_harness_todo` |

---

## 安装本 Skill

将 `agent-harness/` 整目录复制到：

| 工具 | 个人 | 项目（仓库） |
|------|------|-------------|
| **Cursor** | `~/.cursor/skills/agent-harness/` | `<repo>/.cursor/skills/agent-harness/` |
| **Codex** | `$CODEX_HOME/skills/agent-harness/` | — |
| **Claude Code** | `~/.claude/skills/agent-harness/` | `<repo>/.claude/skills/agent-harness/` |
| **通用** | `~/.agents/skills/agent-harness/` | `<repo>/.agents/skills/agent-harness/` |

**Skills CLI：** `npx skills add HYX-LHJ/round-harness --skill agent-harness -g -y`

- **勿**放入 `~/.cursor/skills-cursor/`（Cursor 内置）
- **Codex**：安装后提示用户**重启**
- **Claude Code**：项目路径在 **git 仓库根** 的 `.claude/skills/`

详见 [references/installation.md](references/installation.md)

安装后对 Agent 说：**「用 agent-harness 在当前仓库创建 harness」**

---

## 日常回合（harness 已存在时）

优先级：**项目根 `AGENTS.md` > 本 Skill**。

```
常规：门禁(前) → 读 harness → [Plan] → 登记 todo → [改 src/? → tdd] → 实现 → [code-review] → 门禁(后) → PROGRESS

提交：…常规收尾… → code-simplifier → 二次 code-review → dev → test → 再刷 PROGRESS
```

| Skill | 何时 | 执行方 |
|-------|------|--------|
| **tdd** | 登记 todo 后、改 `src/` 前 | 主 Agent |
| **code-review-expert** | 改过 `src/`（收尾） | Subagent |
| **code-simplifier** | 用户提交且含 `src/` | Subagent |

Subagent 落盘：[references/subagent-artifacts.md](references/subagent-artifacts.md)

> Subagent 派遣因工具而异（Cursor Task、Claude Code subagent 等）；**harness 目录与 `AGENTS.md` 规则与工具无关**。

### 门禁（默认）

```powershell
.\.venv\Scripts\python.exe harness/scripts/lint_src.py
.\.venv\Scripts\python.exe -m pytest
```

收尾：`python harness/scripts/sync_progress.py`（`--skip-gates` 见 [references/bootstrap-config.md](references/bootstrap-config.md)）

---

## 延伸阅读

| 文档 | 内容 |
|------|------|
| [references/installation.md](references/installation.md) | 多工具安装路径 |
| [references/create-harness.md](references/create-harness.md) | 创建 harness Agent 清单 |
| [references/directory-layout.md](references/directory-layout.md) | 目录树 |
| [references/plan-mode.md](references/plan-mode.md) | 重大任务 Plan |
| [references/progress-todo.md](references/progress-todo.md) | todo / PROGRESS / DECISIONS |
| [references/subagent-artifacts.md](references/subagent-artifacts.md) | 审查/精炼落盘 |
| [references/commit-workflow.md](references/commit-workflow.md) | 提交纪律 |
| [README.md](README.md) | Skill 包说明（中文） |
| [../README.md](../README.md) | 仓库说明（英文） |
| [../README.zh-CN.md](../README.zh-CN.md) | 仓库说明（中文） |
