# Skills

mini-harness 是 **Skill 集合包**：

| 层级 | 路径 | 作用 |
|------|------|------|
| **工作流入口** | `harness/skills/using-harness/SKILL.md` | 每回合须先调用；路径、硬约束摘要 |
| **工作流细则** | `harness/skills/using-harness/references/workflow.md` | 逐步流程、并行、Subagent、目录 |
| **专项 Skill** | `harness/skills/tdd/` 等 | 在 workflow 中按需调用 |
| **GOAL 模式** | `harness/skills/goal-md/SKILL.md` | 复杂多轮可度量优化；产物在 `harness/goal/`（见 `index.md`） |

初始化后，内置 Skills 同步到 `harness/skills/`。AI 工具应优先从该目录发现并加载 Skills，**不要用**全局 `~/.agents/skills/` 等同名 Skill 替代。

`harness/.package/` 保存用于更新的版本快照；日常使用时以 `harness/skills/` 为准。

仓库也可通过工具支持的其他位置提供额外的项目 Skills。当仓库配置或专用 Skill 已是权威来源时，不要将通用语言或框架指引复制进 harness 其他文件。
