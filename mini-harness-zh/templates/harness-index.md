# harness — 总索引

非业务运行时目录。协作规则见根 [AGENTS.md](../AGENTS.md)。

## 每回合入口（L0）

| 文件 | 用途 |
|------|------|
| [todo.md](todo.md) | 当前周任务板（唯一可勾选处） |
| [PROGRESS.md](PROGRESS.md) | 快照：分支、diff、门禁、进行中 task |
| [DECISIONS.md](DECISIONS.md) | **活跃**架构 / 边界约束 |
| [backlog/decisions-archive.md](backlog/decisions-archive.md) | 已归档 / 作废决策（只读） |

## 子目录（下钻各 `index.md`）

| 目录 | 索引 |
|------|------|
| [plans/](plans/) | [plans/index.md](plans/index.md) — 重大任务方案 |
| [docs/](docs/) | [docs/index.md](docs/index.md) — 对接、Plan 流程 |
| [code_review/](code_review/) | [code_review/index.md](code_review/index.md) — 审查报告、open-findings |
| [code_simplifier/](code_simplifier/) | [code_simplifier/index.md](code_simplifier/index.md) — 提交前精炼留底 |
| [tests/](tests/) | [tests/index.md](tests/index.md) — pytest |
| [scripts/](scripts/) | [scripts/index.md](scripts/index.md) — 门禁与维护脚本 |
| [sql/](sql/) | [sql/index.md](sql/index.md) — DDL（可选） |
| [backlog/](backlog/) | [backlog/index.md](backlog/index.md) — 历史周 todo |

`harness/pre/`、`harness/out/` 已 **gitignore**，仅本机试跑，不进仓库。

## 测试与门禁

仓库根目录执行（仅单元测试）：

```powershell
{{LINT_CMD}}
{{PYTEST_CMD}}
```

收尾：`python harness/scripts/sync_progress.py`（`--skip-gates` / `--dry-run` 见 [scripts/index.md](scripts/index.md)）。

**每周一**（当天首个 Agent 会话）：须先走 [docs/weekly-review.md](docs/weekly-review.md) 周回顾回合（见 [AGENTS.md](../AGENTS.md)）。

本回合若已 `git commit` 和/或 `git push`，须在推送完成后**再跑一遍** `sync_progress.py` 并手写 PROGRESS 人文章节（见根 [AGENTS.md](../AGENTS.md)）。

## 单一真相（读什么）

| 你想知道… | 优先看 |
|-----------|--------|
| Agent 还有什么 task 要做 | [todo.md](todo.md) 未勾选项 |
| 近期人工/运维意向 | PROGRESS「下一步」 |
| 本周做完了什么 | PROGRESS「已完成」（机械） |
| 代码是否在远程、测试是否绿 | PROGRESS「最新 git」/「测试」/「lint」 |
| 新会话接手上下文 | PROGRESS「当前状态」+「进行中」 |
| 为什么不能那样改 | [DECISIONS.md](DECISIONS.md) |
| 已知技术债 | [open-findings.md](code_review/open-findings.md) |

## PROGRESS.md 写法

主 Agent **手写**「当前状态」「已知问题」「下一步」；其余用 `sync_progress.py`。

- **当前状态**（≤5 bullet）：新会话 30 秒内需要的现状；**不要**当 changelog。
- **下一步**：近期意向；**不必**登记 todo；做完删除。
- **git / 测试 / lint / 已完成 / 进行中**：由 `sync_progress.py` 填充。
- **已知问题**：仅未关闭 P0/P1/P2；无则「暂无」。
- **commit/push 后**：必须再刷新。

## DECISIONS.md 维护

- 活跃文件约 15～25 条；作废 → [backlog/decisions-archive.md](backlog/decisions-archive.md)。
- 改变写法、API 契约、部署约束时写入；普通交付记 `plans/` + `todo.md`。
