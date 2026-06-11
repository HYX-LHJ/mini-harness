# Subagent 产物 — 硬约束

以下步骤**未完成则回合不得收尾**（提交回合：缺报告不得 `git commit`）。

## code-review-expert

1. **派遣**：主 Agent 用 **Task** 启动 Subagent，附带本回合 diff 与 `code-review-expert` Skill。
2. **正文**：Subagent 输出结构化审查（严重度 P0–P3；结论 APPROVE / REQUEST_CHANGES / COMMENT）。
3. **落盘**（主 Agent，**必须**）：
   - `harness/code_review/YYYY-MM-DD_主题简述.md`
   - [code_review/index.md](../../templates/code-review-index.md) 顶部新增一行
   - 未关闭 P0/P1 → [open-findings.md](../../templates/open-findings.md)
4. **禁止**：仅以聊天代替落盘；禁止无报告即勾 todo / 写 PROGRESS「已完成审查」。

### 严重度

| 级别 | 含义 |
|------|------|
| P0 | 安全/数据丢失，阻塞合并 |
| P1 | 逻辑错误或显著架构问题 |
| P2 | 可维护性 / 扩展性 |
| P3 | 风格与小幅优化 |

## code-simplifier

1. **派遣**：Task + `code-simplifier` Skill，限定待提交业务代码 diff。
2. **实施**：Subagent 在仓库内简化代码（保功能），简述改动点。
3. **落盘**（主 Agent，**必须**）：
   - `harness/code_simplifier/YYYY-MM-DD_主题简述.md`
   - `code_simplifier/index.md` 顶部新增一行
   - 无实质简化时写明「无变更」及原因
4. **后续**：精炼后重新门禁；含业务代码的提交须再跑 code-review-expert（二次）。

## 主 Agent 与 Subagent 边界

| 谁 | 做什么 |
|----|--------|
| Subagent | 读 diff、写审查/精炼**正文**、可选直接改代码（simplifier） |
| 主 Agent | 派遣、收稿、**落盘**、更新 index/open-findings、对用户摘要 |

主 Agent **不得**代替 Subagent 产出完整审查报告正文。
