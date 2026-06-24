# 📝 计划模式（Plan）

在动手写运行时代码前，先想清楚：**需求清不清？有没有真选项？会不会动到契约？**

小改动 obvious → 跳过 plan 文件，**但 AC 仍要写进 todo**。

满足任一 → 先 [brainstorming](../skills/brainstorming/SKILL.md) + 本模式：

- 目标或成功标准模糊
- 2+ 种有实质取舍的方案
- 影响 API、数据、安全、并发、发布或多模块

---

## Plan 文档模板

保存到 `harness/plans/YYYY-MM-DD-主题.md`：

```markdown
# 标题

## 背景与目标

## 范围与非目标

## 方案（或方案比较）

## 验收标准

| ID | 场景 / 预期 | 级别 | 验证 |
|----|-------------|------|------|
| AC-1 | … | MUST-AUTO | pytest / … |
| AC-2 | … | MUST-MANUAL | 手测步骤 |

## 测试与验收证据
```

---

## 与 todo 的关系

| 规则 | 说明 |
|------|------|
| **执行锚点** | `todo.md`，不是 plan |
| 批准后 | AC 表**同步**到 todo（可链回 plan） |
| 无 plan 的小任务 | 直接在 todo 写 AC |
| 进入 TDD 前 | todo 须勾选 `- [x] **AC 已确认**` |
| 验收 | `acceptance-verification` 以 todo 为主；plan 仅作补充 |

完整流程 → [workflow.md](../skills/using-harness/references/workflow.md)
