# 计划模式

在以下情况实施前先制定计划：需求不明确、存在有意义的方案权衡，或变更影响对外契约、数据、安全、并发、发布或多个模块边界。

将经批准的重要设计记录在 `harness/plans/` 下。小而明显的变更无需设计仪式，**但验收标准仍须写入 `harness/todo.md`**。

## Plan 文档建议结构

```markdown
# 标题

## 背景与目标

## 范围与非目标

## 方案（或方案比较）

## 验收标准

| ID | 场景 / 预期 | 级别 | 验证 |
|----|-------------|------|------|
| AC-1 | … | MUST-AUTO | 自动化 |
| AC-2 | … | MUST-MANUAL | 手测 |

## 测试与验收证据

（关键路径、需新增的 acceptance 测试等）
```

## 与 todo 的关系

- **验收契约的执行锚点是 `harness/todo.md`**，不是 plan 文件。
- Plan 批准后：将「验收标准」表**同步**到当前任务的 todo（可摘要 + 链接回本 plan）。
- 无 Plan 的小任务：直接在 todo 中写「验收标准」，不必创建 plan 文件。
- **AC 同步到 todo 后，须完成「AC 核对」并勾选「AC 已确认」，方可进入 TDD**（见 `AGENTS.md` §3.1）。
- `acceptance-verification` subagent 以 todo 为主、plan 为辅（仅当 todo 链接了 plan）；并先检查 AC 契约是否已确认。
