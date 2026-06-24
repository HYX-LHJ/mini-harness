---
name: using-harness
description: mini-harness 工作流入口 Skill。仓库存在 harness/、PROGRESS.md、todo.md，或用户要改代码/加功能/修 bug/提交/新会话接手/跑 install 时，必须先读本 Skill——即使用户只说「帮我改一下」未提 harness。也用于 update、doctor。务必用 harness/skills/ 副本，禁止 ~/.agents/skills/ 同名 Skill 替代。
compatibility: install / update / doctor 需要 Python 3.10+。
---

# 🧭 使用 Harness（工作流入口）

mini-harness 是一组 **Agent Skills**，本文件是**工作流入口**——告诉你每回合先读什么、何时调用哪个专项 Skill。细则见 [references/workflow.md](references/workflow.md)。

| 层级 | 内容 | 谁维护 |
|------|------|--------|
| 🏗️ 平台层 | `harness/skills/`、模板 | 插件 `update` 同步 |
| 🎯 项目层 | `profile/PROJECT.md`、`DECISIONS.md` | 项目团队，`update` 不覆盖 |

---

## 开场（每回合必做）

动手改任何文件之前：

1. **确认路径**（见下表）
2. **读状态** — 并行打开 `PROGRESS.md`、`todo.md`、`profile/PROJECT.md`；Plan / 架构 / 跨模块时加读 `DECISIONS.md` 相关主题
3. **跟流程** — [workflow.md](references/workflow.md)：有变更先 todo；运行时代码须 **AC 已确认** 后再 TDD / 实现

> ⚠️ 跳过本 Skill 或用 `~/.agents/skills/` 同名 Skill 替代 `harness/skills/`，容易丢状态、丢门禁。

---

## 路径

| | 仅插件（未 `install`） | 仓库已 `install` |
|---|------------------------|------------------|
| 本 Skill | `skills/using-harness/SKILL.md` | `harness/skills/using-harness/SKILL.md` |
| 其它 Skill | `skills/<name>/SKILL.md` | `harness/skills/<name>/SKILL.md` |
| 项目画像 | — | `harness/profile/PROJECT.md` |
| 重大决策 | — | `harness/DECISIONS.md` |
| 工具链 | — | `pyproject.toml`；可选 `.mini-harness.json` → `commands.gate` |
| 状态 | — | `PROGRESS.md`、`todo.md` |

`install` / `update` / `doctor` → [lifecycle.md](references/lifecycle.md)

---

## 硬约束

这些规则存在，是因为**新会话没有聊天记忆**——文件才是真相源。

1. **有文件变更** → 先登记 `todo.md`（纯只读诊断除外）
2. **改运行时代码** → todo 含 AC，且 `tests/` 有对应测试
3. **AC 已确认** → 用户核对意图并勾选前，不写实现、不跑 TDD
4. **遵守项目画像** → `PROJECT.md` 优先于通用默认；门禁以 `pyproject.toml` / `commands.gate` 为准
5. **尊重重大决策** → 触及 `DECISIONS.md` 已记录结论时，须新 todo + 用户确认，勿静默推翻
6. **范围** → 不覆盖用户无关改动
7. **Subagent** → 测试、验收、审查、提交前精炼走 subagent；主 Agent 不代劳
8. **进化须确认** → 重大取舍 → `DECISIONS` 对应主题；可执行规则 → `PROJECT.md`；`evolution.jsonl` 只追加
9. **并行** → 无依赖冲突时同消息启动可并行 subagent（见 workflow **并行规则**）

---

## 流程一览

```text
📖 读状态 → [📝 Plan?] → todo + AC 核对 → 🧪 subagent(测试) → ⚡ 实现 → 🚦 门禁
  → ✅ 验收 ∥ 🔍 审查 → [🌱 进化?] → 📁 归档 → PROGRESS
提交：✨ 精炼 → 🔍 审查 → git
```

逐步说明 → **[workflow.md](references/workflow.md)**

---

## 参考

| 文档 | 内容 |
|------|------|
| [workflow.md](references/workflow.md) | 逐步流程、并行、Subagent、进化 |
| [lifecycle.md](references/lifecycle.md) | install / update / doctor |
| [host-support.md](references/host-support.md) | Cursor · Codex · Claude Code |
| [skill-index.md](references/skill-index.md) | Skill 速查与误用 |
| [portability.md](references/portability.md) | 可移植性边界 |
