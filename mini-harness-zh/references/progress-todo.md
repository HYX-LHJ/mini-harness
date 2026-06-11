# todo / PROGRESS / DECISIONS

## todo.md

当前周任务板，**有变更必先登记**。

```markdown
# 当前周任务板

**本周**：YYYY-MM-DD ~ YYYY-MM-DD

历史周任务见 [backlog/archive.md](backlog/archive.md)。

---
YYYY-MM-DD

task：<一句话任务名>

- [ ] 可验收子项 1
- [ ] 可验收子项 2
```

规则：

- 每个 `task：` 下子项须可勾选、可验收。
- 完成打 `[x]`；整 task 子项全 `[x]` 后由 `sync_progress.py` 汇总到 PROGRESS「已完成」。
- 跨周归档：项目 `archive_harness_todo.py` 或手工移入 `backlog/archive.md`。

## PROGRESS.md

### 机械章节（sync_progress.py 或手工维护）

- 最新 git 信息
- 测试状态
- lint
- 已完成（本周全勾 task）
- 进行中（有未勾子项的 task）

### 人文章节（主 Agent 每回合手写）

| 章节 | 写法 |
|------|------|
| **当前状态** | ≤5 bullet；新会话 30 秒内需要的现状；**不要**当 changelog |
| **下一步** | 近期意向（部署、联调、待确认 Plan）；**不必**进 todo；做完删除 |
| **已知问题** | 仅**未关闭** P0/P1/P2；无则写「暂无」 |

**commit/push 后**必须再刷新，避免「当前状态」与 git 哈希不一致。

## DECISIONS.md

活跃约束，目标约 15～25 条。

**写入**：改变后续写法、API 契约、查库口径、部署约束。  
**归档**：被新决策取代 → `backlog/decisions-archive.md`。  
**格式**：日期标题 + 原因 + 否决方案 + 约束 bullet。

普通功能交付记 `plans/` + `todo.md` 即可，不必每条 commit 写 DECISIONS。
