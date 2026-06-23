---
name: using-harness
description: 插件安装后或仓库已激活 harness 时使用；初始化 harness、遵循 mini-harness 协作工作流、动手实现用户任务前须先调用本技能。
compatibility: 仓库管理与生命周期钩子需要 Python 3.10+。
---

# 使用 Harness

mini-harness 是 **Skill 集合包**。本 Skill 是**工作流入口**——告诉 Agent 何时读状态、何时调用哪个专项 Skill；**不是**塞满条文的 Playbook。逐步细则见 [references/workflow.md](references/workflow.md)。

业务规则写在 `harness/DECISIONS.md` 或项目文档，不写入本 Skill。

## 开场（每回合必做）

动手改文件前：

1. **确认路径**（下表）
2. **读状态**：已 `install` 则并行读 `harness/PROGRESS.md`、`harness/todo.md`（按需 `DECISIONS.md`）；未 `install` 则只读任务，有持久化需求先 `install` 或征得用户同意
3. **跟流程**：按 [workflow.md](references/workflow.md) 执行；有变更先 todo；运行时代码须 **AC 核对** 后再 TDD / 实现

勿跳过本 Skill；勿用 `~/.agents/skills/` 替代插件或 `harness/skills/` 下的内置 Skill。

## 路径

| | 仅插件（未 `install`） | 仓库已 `install` |
|---|------------------------|------------------|
| 本 Skill | `skills/using-harness/SKILL.md` | `harness/skills/using-harness/SKILL.md` |
| 其它 Skill | `skills/<name>/SKILL.md` | `harness/skills/<name>/SKILL.md` |
| 编码规范 | `rules/python-coding-conventions.md` | `harness/rules/python-coding-conventions.md` |
| 状态文件 | 无；只读可直接答 | `harness/PROGRESS.md`、`todo.md` 等 |

`install` 说明见 [lifecycle.md](references/lifecycle.md)。

## 硬约束

1. **有文件变更** → 先登记 `harness/todo.md`（只读任务除外）
2. **改运行时代码** → todo 含 AC，并在 `tests/` 有对应测试
3. **AC 已确认** → 与用户核对意图并勾选前，不得 TDD 或写实现
4. **范围** → 不覆盖用户无关改动
5. **Subagent** → 测试（`tdd` + `python-testing-patterns`）、验收、审查、提交前精炼须走 subagent；主 Agent 不代劳（细则见 workflow）
6. **并行** → 无依赖冲突时同消息启动可并行 subagent（见 workflow）

## 流程一览

```text
读状态 → [Plan + brainstorming] → todo + AC 核对 → subagent(测试) → 实现 → 门禁
  → subagent(验收 ∥ 审查) → 归档 → PROGRESS
提交：subagent(精炼) → subagent(审查) → git
```

逐步说明、并行表、Subagent 表、Harness 目录 → **[workflow.md](references/workflow.md)**

## 参考

| 文档 | 内容 |
|------|------|
| [workflow.md](references/workflow.md) | 逐步流程、并行、Subagent、目录 |
| [lifecycle.md](references/lifecycle.md) | install / update / doctor |
| [host-support.md](references/host-support.md) | 各宿主插件与钩子 |
| [portability.md](references/portability.md) | 可移植性边界 |
