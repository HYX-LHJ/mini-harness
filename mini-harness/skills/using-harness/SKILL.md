---
name: using-harness
description: 插件安装后或仓库已激活 harness 时使用；初始化 harness、遵循 mini-harness 协作工作流、动手实现用户任务前须先调用本技能。
compatibility: 仓库管理与生命周期钩子需要 Python 3.10+。
---

# 使用 Harness

mini-harness 是 **Skill 集合包**。本 Skill 是**工作流入口**——告诉 Agent 何时读状态、何时调用哪个专项 Skill；**不是**塞满条文的 Playbook。逐步细则见 [references/workflow.md](references/workflow.md)。

**平台层**（插件受管）：`harness/skills/`、`rules/`、通用模板。  
**项目层**（项目自有、可进化）：`harness/profile/PROJECT.md`（每回合必读）、`harness/DECISIONS.md`（按主题的重大决策）。

## 开场（每回合必做）

动手改文件前：

1. **确认路径**（下表）
2. **读状态**：已 `install` 则并行读 `harness/PROGRESS.md`、`harness/todo.md`、`harness/profile/PROJECT.md`；**Plan / 架构 / 跨模块**时加读 `harness/DECISIONS.md` 相关主题
3. **跟流程**：按 [workflow.md](references/workflow.md) 执行——有变更先 todo；运行时代码须 **AC 核对** 后再 TDD / 实现

勿跳过本 Skill；勿用 `~/.agents/skills/` 替代插件或 `harness/skills/` 下的内置 Skill。

## 路径

| | 仅插件（未 `install`） | 仓库已 `install` |
|---|------------------------|------------------|
| 本 Skill | `skills/using-harness/SKILL.md` | `harness/skills/using-harness/SKILL.md` |
| 其它 Skill | `skills/<name>/SKILL.md` | `harness/skills/<name>/SKILL.md` |
| 项目画像（每回合） | — | `harness/profile/PROJECT.md` |
| 重大决策（按主题） | — | `harness/DECISIONS.md` |
| 工具链 | — | 仓库根 `pyproject.toml`；可选 `harness/.mini-harness.json` → `commands.gate` |
| 编码规范 | `rules/python-coding-conventions.md` | `harness/rules/python-coding-conventions.md` |
| 状态文件 | 无；只读可直接答 | `harness/PROGRESS.md`、`todo.md` 等 |

`install` 说明见 [lifecycle.md](references/lifecycle.md)。

## 硬约束

1. **有文件变更** → 先登记 `harness/todo.md`（只读任务除外）
2. **改运行时代码** → todo 含 AC，并在 `tests/` 有对应测试
3. **AC 已确认** → 与用户核对意图并勾选前，不得 TDD 或写实现
4. **遵守项目画像** → `profile/PROJECT.md` 中的可执行规则优先于通用默认；**门禁以 `pyproject.toml` / `commands.gate` 为准**
5. **尊重重大决策** → Plan 或改动触及 `DECISIONS.md` 已记录结论时，不得静默推翻；须新 todo + 用户确认
6. **范围** → 不覆盖用户无关改动
7. **Subagent** → 测试（`tdd` + `python-testing-patterns`）、验收、审查、提交前精炼须走 subagent；主 Agent 不代劳
8. **进化须确认** → 重大取舍写 `DECISIONS.md`（对应主题）；可执行规则写 `PROJECT.md`；`evolution.jsonl` 只追加
9. **并行** → 无依赖冲突时同消息启动可并行 subagent（见 workflow）

## 流程一览

```text
读状态（含 profile）→ [Plan + brainstorming + DECISIONS?] → todo + AC 核对 → subagent(测试) → 实现 → 门禁
  → subagent(验收 ∥ 审查) → [进化提案?] → 归档 → PROGRESS
提交：subagent(精炼) → subagent(审查) → git
```

逐步说明、并行表、Subagent 表、Harness 目录 → **[workflow.md](references/workflow.md)**

## 参考

| 文档 | 内容 |
|------|------|
| [workflow.md](references/workflow.md) | 逐步流程、并行、Subagent、进化仪式 |
| [lifecycle.md](references/lifecycle.md) | install / update / doctor |
| [host-support.md](references/host-support.md) | 各宿主插件与钩子 |
| [portability.md](references/portability.md) | 可移植性边界 |
