# Harness 目录布局

非业务运行时目录，与 `src/` 并列。协作规则以项目根 `AGENTS.md` 为准。

## 标准树

```
harness/
├── index.md                 # 总索引（L0 入口）
├── todo.md                  # 当前周任务板（唯一可勾选处）
├── PROGRESS.md              # 快照：分支、diff、门禁、进行中 task
├── DECISIONS.md             # 活跃架构 / 边界约束
├── backlog/
│   ├── index.md
│   ├── archive.md           # 历史周 todo
│   └── decisions-archive.md # 已作废决策
├── plans/
│   ├── index.md
│   └── YYYY-MM-DD-主题.md
├── docs/
│   ├── index.md
│   └── plan-mode.md         # Plan 流程细则
├── code_review/
│   ├── index.md
│   ├── open-findings.md
│   └── YYYY-MM-DD_主题.md
├── code_simplifier/
│   ├── index.md
│   └── YYYY-MM-DD_主题.md
├── tests/                   # 或与 pytest.ini 指向的目录一致
│   └── index.md
├── scripts/
│   ├── index.md
│   ├── lint_src.py          # 项目定制
│   ├── sync_progress.py     # 刷新 PROGRESS 机械章节
│   └── archive_harness_todo.py  # 跨周归档 todo
└── sql/                     # 可选：DDL
    └── index.md
```

## 命名约定

| 类型 | 格式 | 示例 |
|------|------|------|
| Plan | `YYYY-MM-DD-主题.md` | `2026-01-15-user-auth.md` |
| Code review | `YYYY-MM-DD_主题简述.md` | `2026-01-20-user-auth-review.md` |
| Code simplifier | 同 review | `2026-01-20-user-auth.md` |

日期在前，便于排序。

## index.md 规则

每个子目录一个 `index.md`：用途一句话 + 指向该目录下文件的表格（新 → 旧）。`harness/index.md` 是 Agent 每回合的 L0 入口。

## gitignore 建议

```
harness/out/
harness/pre/
harness/.pytest-tmp/
```

本地试跑、一次性产物不进仓库。

## 单一真相（读什么）

| 你想知道… | 优先看 |
|-----------|--------|
| 还有什么 task 要做 | `todo.md` 未勾选项 |
| 新会话接手 | PROGRESS「当前状态」+「进行中」 |
| 为什么不能那样改 | `DECISIONS.md` |
| 已知技术债 | `code_review/open-findings.md` |
| 实施前方案 | `plans/` |
