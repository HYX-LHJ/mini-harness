# 架构说明

mini-harness 采用「**插件 + 目标仓库 harness 工程**」两层架构：插件负责**一次性脚手架**，harness 目录负责**持续协作状态**。

### 两层架构

```text
mini-harness 仓库                     你的项目仓库
┌─────────────────────┐              ┌─────────────────────┐
│ mini-harness/         │  install     │ AGENTS.md           │
│  AGENTS.md（源）      │ ──────────►  │ harness/            │
│  skills/、scripts/    │              │  todo、PROGRESS…    │
│  assets/template/     │              │ tests/              │
└─────────────────────┘              └─────────────────────┘
```

**设计原则：**

1. **插件与 harness 分离** — 插件可升级；harness 留在项目仓库中版本化
2. **文件即状态** — Agent 每回合读文件，不依赖聊天历史
3. **单一真相源** — 每类信息有固定落点
4. **权威源** — 只改 `mini-harness/`；`install` 同步到各仓库

### harness 标准目录树

```text
your-repo/
├── AGENTS.md                 # Playbook（项目根目录）
├── tests/                    # 全部测试
└── harness/
    ├── index.md              # L0 总索引
    ├── todo.md               # 当前任务 + AC（唯一可勾选处）
    ├── PROGRESS.md           # 快照：状态、进行中、已完成
    ├── DECISIONS.md          # 长期约束
    ├── skills/               # 内置 Skill（tdd、review 等）
    ├── rules/                # 编码规范
    ├── scripts/              # mini_harness.py（install/update/doctor）
    ├── plans/                # 方案文档
    ├── acceptance/           # 验收报告
    ├── docs/                 # 协作细则（plan-mode、weekly-review）
    ├── code_review/          # 审查报告 + open-findings
    ├── code_simplifier/      # 精炼报告
    ├── backlog/              # 历史 todo 归档
    └── .package/             # 版本快照（漂移检测）
```

### 单一真相源

| 你想知道… | 优先看 |
|-----------|--------|
| 还有什么 task | `harness/todo.md` 未勾选项 |
| 新会话如何接手 | `PROGRESS.md`「当前状态」+「进行中」 |
| 为什么不能那样改 | `harness/DECISIONS.md` |
| 已知技术债 | `code_review/open-findings.md` |
| 实施前方案 | `harness/plans/` |
| Agent 每回合做什么 | 项目根 `AGENTS.md` |
| 用哪个 Skill | `harness/skills/<name>/SKILL.md` |

**优先级**：`AGENTS.md` > `harness/skills/` 下的 `SKILL.md`。

### 命名约定

| 类型 | 格式 | 示例 |
|------|------|------|
| Plan | `YYYY-MM-DD-主题.md` | `2026-06-11-user-auth.md` |
| Code review | `YYYY-MM-DD_主题.md` | `2026-06-11_user-auth-review.md` |
| Acceptance | `YYYY-MM-DD_主题.md` | `2026-06-11_user-auth-acceptance.md` |
| Backlog 归档 | `YYYY-MM-DD-主题.md` | `2026-06-11-user-auth.md` |

### 安装器命令

| 命令 | 职责 |
|------|------|
| `install` | 创建/同步 harness、skills、scripts、rules、AGENTS.md |
| `update` | 从 `.package` 快照刷新受管文件 |
| `doctor` | 健康检查 + 漂移 warnings |
| `uninstall` | 移除受管 harness（保留项目扩展） |

### 与业务代码的关系

```text
your-repo/
├── src/ 或 agent/    # 业务代码（改动须 tdd + review）
├── harness/          # 协作控制平面（非运行时目录）
├── AGENTS.md
└── tests/            # 测试在仓库根（非 harness/tests/）
```

门禁命令（pytest、ruff、mypy）由项目自定 — 通过 `python-code-style` 写入 `pyproject.toml`，摘要记入 `DECISIONS.md`。
