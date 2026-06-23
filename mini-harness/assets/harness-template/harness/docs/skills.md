# Skills

mini-harness 是 **Skill 集合包**：

| 层级 | 路径 | 作用 |
|------|------|------|
| **工作流入口** | `harness/skills/mini-harness/SKILL.md` | 每回合须先调用；指引加载 Playbook |
| **Playbook 正文** | 项目根 `AGENTS.md` | mini-harness 核心 Skill 的执行规范 |
| **专项 Skill** | `harness/skills/tdd/` 等 | 在 Playbook 流程中按需调用 |

初始化后，内置 Skills 同步到 `harness/skills/`。AI 工具应优先从该目录发现并加载 Skills，**不要用**全局 `~/.agents/skills/` 等同名 Skill 替代。

`harness/.package/` 保存用于更新的版本快照；日常使用时以 `harness/skills/` 与根 `AGENTS.md` 为准。

仓库也可通过工具支持的其他位置提供额外的项目 Skills。当仓库配置或专用 Skill 已是权威来源时，不要将通用语言或框架指引复制进 harness 其他文件。
