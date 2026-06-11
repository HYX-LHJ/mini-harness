# Architecture / 架构说明

**Languages:** [English](#english) · [中文](#中文)

---

<a id="english"></a>

## English

round-harness uses a **two-layer architecture**: the Skill package scaffolds once; the harness directory holds ongoing collaboration state.

### Two layers

```text
round-harness repo                    your project repo
┌─────────────────────┐              ┌─────────────────────┐
│ agent-harness/      │  init script │ AGENTS.md           │
│  SKILL.md           │ ──────────►  │ pytest.ini          │
│  templates/         │              │ harness/            │
│  bundled/scripts/   │              │  todo, PROGRESS, …  │
└─────────────────────┘              └─────────────────────┘
```

**Principles:**

1. **Skill vs harness** — Skill can be upgraded/reinstalled; harness lives in your repo
2. **Files as state** — Agents read files each round, not chat history
3. **Single source of truth** — Each information type has one canonical location

### Standard harness tree

```text
harness/
├── index.md              # L0 entry
├── todo.md               # Weekly tasks (only place to check boxes)
├── PROGRESS.md           # Snapshot: branch, gates, in-progress tasks
├── DECISIONS.md          # Active architecture constraints
├── plans/                # Plan documents
├── docs/                 # Collaboration docs (plan-mode.md)
├── code_review/          # Review reports + open-findings
├── code_simplifier/      # Simplify reports
├── tests/                # Unit tests
├── scripts/              # lint_src, sync_progress, archive_harness_todo
├── backlog/              # Archived todos / decisions
└── sql/                  # Optional DDL docs
```

Details: [agent-harness/references/directory-layout.md](../agent-harness/references/directory-layout.md)

### Single source of truth

| Question | Read |
|----------|------|
| What tasks remain? | `harness/todo.md` unchecked items |
| How to onboard a new session? | `PROGRESS.md` "current state" + "in progress" |
| Why can't we change X? | `harness/DECISIONS.md` |
| Known tech debt? | `code_review/open-findings.md` |
| Pre-implementation plan? | `harness/plans/` |
| What should agent do each round? | Project root `AGENTS.md` |

**Priority:** `AGENTS.md` > Skill `SKILL.md`.

### Naming conventions

| Type | Format | Example |
|------|--------|---------|
| Plan | `YYYY-MM-DD-topic.md` | `2026-06-11-user-auth.md` |
| Code review | `YYYY-MM-DD_topic.md` | `2026-06-11_user-auth-review.md` |
| Code simplifier | same as review | `2026-06-11_user-auth.md` |

### Template placeholders

`init_harness.py` substitutes in templates:

| Placeholder | Default |
|-------------|---------|
| `{{PROJECT_NAME}}` | folder name |
| `{{SRC_DIR}}` | `src` |
| `{{DEV_BRANCH}}` / `{{TEST_BRANCH}}` | `dev` / `test` |
| `{{LINT_CMD}}` / `{{PYTEST_CMD}}` | platform-specific venv commands |

### Maintenance scripts

Copied from `bundled/scripts/` to `harness/scripts/`:

| Script | Role |
|--------|------|
| `lint_src.py` | ruff + pyright on `src/` |
| `sync_progress.py` | Refresh PROGRESS mechanical sections |
| `archive_harness_todo.py` | Archive completed weekly todos |

### Relationship to business code

```text
your-repo/
├── src/          # Business code (tdd + code-review required when changed)
├── harness/      # Collaboration control plane (not runtime)
├── AGENTS.md
└── pytest.ini
```

---

<a id="chinese"></a>

## 中文

round-harness 采用「**Skill 包 + 目标仓库 harness 工程**」两层架构：Skill 负责**一次性脚手架**，harness 目录负责**持续协作状态**。

### 两层架构

```text
round-harness 仓库                     你的项目仓库
┌─────────────────────┐              ┌─────────────────────┐
│ agent-harness/      │  init 脚本   │ AGENTS.md           │
│  SKILL.md           │ ──────────►  │ pytest.ini          │
│  templates/         │              │ harness/            │
│  bundled/scripts/   │              │  todo、PROGRESS…    │
└─────────────────────┘              └─────────────────────┘
```

**设计原则：**

1. **Skill 与 harness 分离** — Skill 可升级重装；harness 留在项目仓库中版本化
2. **文件即状态** — Agent 每回合读文件，不依赖聊天历史
3. **单一真相源** — 每类信息有固定落点

### harness 标准目录树

```text
harness/
├── index.md              # L0 总索引
├── todo.md               # 当前周任务（唯一可勾选处）
├── PROGRESS.md           # 快照：分支、门禁、进行中 task
├── DECISIONS.md          # 活跃架构约束
├── plans/                # 方案文档
├── docs/                 # 协作细则（含 plan-mode.md）
├── code_review/          # 审查报告 + open-findings
├── code_simplifier/      # 精炼报告
├── tests/                # 单元测试
├── scripts/              # lint_src、sync_progress、archive_harness_todo
├── backlog/              # 历史 todo / 决策归档
└── sql/                  # 可选 DDL 文档
```

细则：[agent-harness/references/directory-layout.md](../agent-harness/references/directory-layout.md)

### 单一真相源

| 你想知道… | 优先看 |
|-----------|--------|
| 还有什么 task | `harness/todo.md` 未勾选项 |
| 新会话如何接手 | `PROGRESS.md`「当前状态」+「进行中」 |
| 为什么不能那样改 | `harness/DECISIONS.md` |
| 已知技术债 | `code_review/open-findings.md` |
| 实施前方案 | `harness/plans/` |
| Agent 每回合做什么 | 项目根 `AGENTS.md` |

**优先级**：`AGENTS.md` > Skill `SKILL.md`。

### 命名约定

| 类型 | 格式 | 示例 |
|------|------|------|
| Plan | `YYYY-MM-DD-主题.md` | `2026-06-11-user-auth.md` |
| Code review | `YYYY-MM-DD_主题.md` | `2026-06-11_user-auth-review.md` |
| Code simplifier | 同 review | `2026-06-11_user-auth.md` |

### 模板占位符

`init_harness.py` 替换模板中的：

| 占位符 | 默认 |
|--------|------|
| `{{PROJECT_NAME}}` | 文件夹名 |
| `{{SRC_DIR}}` | `src` |
| `{{DEV_BRANCH}}` / `{{TEST_BRANCH}}` | `dev` / `test` |
| `{{LINT_CMD}}` / `{{PYTEST_CMD}}` | 平台相关 venv 命令 |

### 维护脚本

从 `bundled/scripts/` 复制到 `harness/scripts/`：

| 脚本 | 职责 |
|------|------|
| `lint_src.py` | 对 `src/` 运行 ruff + pyright |
| `sync_progress.py` | 刷新 PROGRESS 机械章节 |
| `archive_harness_todo.py` | 跨周归档 todo |

### 与业务代码的关系

```text
your-repo/
├── src/          # 业务代码（改动须 tdd + code-review）
├── harness/      # 协作控制平面（非运行时目录）
├── AGENTS.md
└── pytest.ini
```
