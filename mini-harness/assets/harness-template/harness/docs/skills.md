# 🧩 Skills

mini-harness 是 **Skill 集合包** — 工作流不靠长 prompt，靠可发现的 Skill 文件。

| 层级 | 路径 | 作用 |
|------|------|------|
| **入口** | `skills/using-harness/SKILL.md` | 每回合先读 |
| **细则** | `skills/using-harness/references/workflow.md` | 流程、并行、Subagent |
| **速查** | `skills/using-harness/references/skill-index.md` | 何时用哪个 Skill |
| **专项** | `skills/tdd/` 等 | 按需调用 |

---

## 路径规则

- ✅ `harness/skills/<name>/SKILL.md`
- ❌ `~/.agents/skills/` 同名替代

`harness/.package/` 是更新快照；日常以 `harness/skills/` 为准。

项目还可通过宿主配置添加**额外** Skill；已是权威来源时，不要把通用指引重复抄进 harness 其它文件。
