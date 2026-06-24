# 🏗️ 架构说明

mini-harness = **插件**（一次性脚手架）+ **harness/**（持续协作状态）。

---

## 两层架构

```text
mini-harness 仓库                     你的项目仓库
┌─────────────────────┐              ┌─────────────────────┐
│ mini-harness/         │  install     │ harness/            │
│  skills/using-harness/│ ──────────►  │  skills/、todo、     │
│  skills/、scripts/    │              │  PROGRESS、profile…  │
│  assets/template/     │              │ tests/              │
└─────────────────────┘              └─────────────────────┘
         ▲
         │ 插件安装 — Skills + 钩子，立即可用
```

### 设计原则

1. **插件 ≠ harness** — 插件给 Skill；`install` 脚手架状态
2. **文件即状态** — 新会话读文件，不赌聊天记忆
3. **单一真相源** — 每类信息有固定落点
4. **权威在插件** — 只改 `mini-harness/`；`install` 同步到各仓

---

## 📂 harness 目录树

```text
your-repo/
├── tests/                    # 🧪 全部测试（仓库根）
└── harness/
    ├── index.md              # 总索引
    ├── todo.md               # 当前任务 + AC（唯一勾选处）
    ├── PROGRESS.md           # 状态快照
    ├── DECISIONS.md          # 🏛️ 按主题的重大决策
    ├── profile/              # 🎯 PROJECT.md、evolution.jsonl（项目自有）
    ├── skills/               # 内置 Skill 副本
    ├── scripts/              # mini_harness.py
    ├── plans/                # 方案
    ├── acceptance/           # 验收报告
    ├── code_review/          # 审查报告
    ├── code_simplifier/      # 精炼记录
    ├── backlog/              # 归档
    ├── docs/                 # plan-mode、weekly-review
    └── .package/             # 版本快照（漂移检测）
```

---

## 🗺️ 单一真相源

| 你想知道… | 去看 |
|-----------|------|
| 还有什么 task | `todo.md` 未勾选项 |
| 新会话怎么接手 | `PROGRESS.md` |
| 为什么不能那样改 | `DECISIONS.md`（按主题） |
| Agent 每回合遵守啥 | `profile/PROJECT.md` |
| 门禁命令 | `pyproject.toml` · `commands.gate` |
| 技术债 | `code_review/open-findings.md` |
| 实施前方案 | `plans/` |
| 工作流入口 | `skills/using-harness/SKILL.md` |
| 用哪个 Skill | `skills/<name>/SKILL.md` |

---

## 🌱 项目画像与进化

| 层级 | 路径 | 维护 |
|------|------|------|
| 平台 | `skills/`、模板 | 插件 `update` |
| 项目 | `profile/`、`DECISIONS` | 团队；`update` **不覆盖** profile |

沉淀：**重大取舍** → `DECISIONS` 对应主题；**可执行规则** → `PROJECT.md`；确认后追加 `evolution.jsonl`。

---

## 📝 命名约定

| 类型 | 格式 | 示例 |
|------|------|------|
| Plan | `YYYY-MM-DD-主题.md` | `2026-06-11-user-auth.md` |
| Review | `YYYY-MM-DD_主题.md` | `2026-06-11_user-auth-review.md` |
| Acceptance | `YYYY-MM-DD_主题.md` | `2026-06-11_user-auth-acceptance.md` |
| Backlog | `YYYY-MM-DD-主题.md` | `2026-06-11-user-auth.md` |

---

## ⚙️ 安装器

| 命令 | 作用 |
|------|------|
| `install` | 创建/同步 harness、skills、scripts |
| `update` | 从 `.package` 刷新受管文件 |
| `doctor` | 健康检查 + 漂移告警 |
| `uninstall` | 移除受管 harness |

---

## 与业务代码

```text
your-repo/
├── harness/          # 协作状态
├── src/ 或 agent/    # 业务代码（改代码走 tdd + review）
└── tests/            # 测试在仓库根
```

门禁：经 `python-code-style` 写入 `pyproject.toml` + `commands.gate`；可选在 `PROJECT.md` 引用。
