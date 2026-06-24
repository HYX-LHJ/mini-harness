# 🗺️ Skill 速查

主 Agent 每回合先读 [SKILL.md](../SKILL.md)。下表帮助**选对 Skill**（路径均在 `harness/skills/`）。

| Skill | 何时用 | 谁执行 |
|-------|--------|--------|
| **using-harness** | 每回合开场；存在 `harness/` 即优先 | 主 Agent |
| **brainstorming** | Plan、方案对比、需求不清 | 主 Agent |
| **tdd** | AC 已确认后、写运行时代码前 | Subagent |
| **python-testing-patterns** | 与 tdd 同批；pytest/fixture/mock | Subagent |
| **acceptance-verification** | 实现完成、交付前 | Subagent |
| **code-review-expert** | 实现后；提交前再复核 | Subagent |
| **code-simplifier** | 用户要 commit/push 前 | Subagent |
| **python-code-style** | 仓库**首次**初始化 Python 工具链 | 主 Agent（一次） |

---

## 常见误用

| ❌ 不要 | ✅ 应该 |
|---------|---------|
| 用 `~/.agents/skills/tdd` | `harness/skills/tdd/SKILL.md` |
| AC 未确认就 TDD | 先 todo + 用户勾选 **AC 已确认** |
| 实现完只跑 pytest 当验收 | 启动 **acceptance-verification** subagent |
| 提交前只 simplify 不 review | workflow 串行：精炼 → 审查 |
| 日常改代码读 python-code-style | 只初始化读一次 |

---

## 并行提示

- 实现后：**acceptance-verification** ∥ **code-review-expert**
- TDD 等待：subagent 写测试 ∥ 主 Agent 预读（不写实现）

详见 [workflow.md](workflow.md)。
