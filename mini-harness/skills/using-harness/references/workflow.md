# 协作工作流（细则）

本文件是 `using-harness` Skill 的**操作细则**。入口与硬约束摘要见 [SKILL.md](../SKILL.md)。

## 并行规则

在**不违反步骤间硬依赖**的前提下，主 Agent 应主动并行以缩短链路。

| 阶段 | 可并行 | 必须串行 |
|------|--------|----------|
| 读状态 | `PROGRESS.md`、`todo.md`、`DECISIONS.md` 同时读取 | — |
| TDD 等待期 | subagent 写测试 ∥ 主 Agent 预读 AC、`DECISIONS`、编码规范、待改模块（**不得**提前写运行时代码） | subagent 交付测试 → 主 Agent 实现 |
| 实现后质检 | `acceptance-verification` ∥ `code-review-expert`（同一条消息启动两个 subagent） | 实现完成 → 验收/审查；精炼 → 提交前审查 |
| 修复后复检 | 小范围修复后可再次并行验收 + 审查 | `code-simplifier` 改代码后须串行审查 |

**本地门禁**（实现完成后、启动验收/审查 subagent 之前）：按 `harness/DECISIONS.md` 或项目约定执行（常见为 `pytest`、ruff、mypy）。将结果附在 subagent 任务说明中。

**合并报告后**：验收 MUST 级 AC 未通过或 **AC-CONTRACT** 未确认仍阻塞交付；审查 P0/P1 须修复。主 Agent 统一排期修复。

## Subagent 分工

下列步骤 **必须**通过 subagent（Task）启动；路径见 [SKILL.md § 路径](../SKILL.md#路径)。**不得**用 `~/.agents/skills/`。

| Skill | 触发时机 | 产出 |
|------|----------|------|
| `tdd` + `python-testing-patterns` | 主 Agent 编写正式运行时代码**之前** | `tests/` 中对应 AC 的 failing 测试（red） |
| `acceptance-verification` | 运行时代码编写完成后 | `harness/acceptance/` 验收报告 |
| `code-review-expert` | 实现完成后（可与验收并行）；提交前须再复核 | `harness/code_review/` 审查报告 |
| `code-simplifier` | 用户要求提交或推送之前 | `harness/code_simplifier/` 精炼记录 |

主 Agent 在 subagent 交付测试后编写运行时代码（green / refactor）。仅改 Markdown 或非执行模板时跳过测试与验收 subagent。

## 流程总览

```text
只读：读状态 → 回答 / 诊断（不登记 todo）

常规：
 读状态 → [Plan] → todo（含 AC）→ AC 核对（人工）
  → subagent(测试) ∥ 主 Agent 预读
  → 主 Agent 实现 → 本地门禁
  → subagent(验收) ∥ subagent(审查) → 修复 → 归档 → PROGRESS

交付（串行）：
  subagent(精炼) → subagent(审查) → 提交 / 推送 → PROGRESS
```

### 1. 读状态

并行读取 `harness/PROGRESS.md`、`harness/todo.md`；需要长期约束时加读 `harness/DECISIONS.md`。其它从 `harness/index.md` 下钻。

### 2. Plan

需求含糊、多方案、影响契约或跨模块时，先读 [brainstorming](../../brainstorming/SKILL.md) 做 Plan。方案写入 `harness/plans/`，**AC 同步到 todo**，用户确认后再实现。小修复可跳过 Plan。

### 3. AC 核对（人工门禁）

自动化与 `acceptance-verification` 只能验证「实现是否符合 AC」，无法证明「AC 是否符合用户意图」。

在 todo 的「AC 核对」节：

1. 起草 AC 后向用户复述每条场景与预期，请确认或修正。
2. 确认后勾选 `- [x] **AC 已确认**`。
3. **未勾选前**：不得启动 TDD subagent、不得编写运行时代码；验收须判 **Overall: FAIL (AC-CONTRACT)**。

### 4. todo

有变更先登记 `harness/todo.md`。涉及运行时代码时须含 **验收标准** 表（AC-1、AC-2…：场景/预期、MUST-AUTO / MUST-MANUAL / SHOULD、验证方式）及 **AC 核对** 节。

### 5. 开发与测试

先启动 subagent 执行 `tdd` 与 `python-testing-patterns`，对照 AC 在 `tests/` 写 **failing 测试**。

TDD subagent 运行期间，主 Agent 可并行阅读 todo AC、`DECISIONS`、编码规范（`harness/rules/`）、待改模块——**不得**提前写运行时代码。

subagent 交付后，主 Agent 编写运行时代码并跑通本地门禁。

### 6. 验收、审查与收尾

1. 本地门禁通过后，**同一条消息并行**启动 `acceptance-verification` 与 `code-review-expert`
2. 合并报告，修复阻塞项（MUST 级 AC、P0/P1）
3. 勾完 todo（含全部 AC）
4. **任务归档**：
   - 复制 todo 任务块到 `harness/backlog/YYYY-MM-DD-<简述>.md`
   - 在 `harness/backlog/index.md` 追加索引
   - 将 `harness/todo.md` 重置为空闲模板
5. 更新 `harness/PROGRESS.md`

### 7. Git 提交

用户要求提交或推送时（**串行**）：

1. subagent `code-simplifier`
2. subagent `code-review-expert`，确认无阻塞项
3. 按仓库策略提交；不 force push。完成后刷新 `PROGRESS.md`。

## 内置 Skill 索引

| Skill | 时机 | 执行方 |
|------|------|--------|
| [python-code-style](../../python-code-style/SKILL.md) | 仅仓库初始化 | 主 Agent |
| [brainstorming](../../brainstorming/SKILL.md) | Plan（必须） | 主 Agent |
| [tdd](../../tdd/SKILL.md) | 写运行时代码前 | Subagent |
| [python-testing-patterns](../../python-testing-patterns/SKILL.md) | 写运行时代码前 | Subagent |
| [acceptance-verification](../../acceptance-verification/SKILL.md) | 实现后 | Subagent |
| [code-review-expert](../../code-review-expert/SKILL.md) | 实现后 / 提交前 | Subagent |
| [code-simplifier](../../code-simplifier/SKILL.md) | 提交前 | Subagent |

修改 Python 代码前阅读 [python-coding-conventions.md](../../../rules/python-coding-conventions.md)。测试放在仓库根 `tests/`。

## Harness 目录

| 路径 | 用途 |
|------|------|
| `harness/todo.md` | 当前任务与 AC |
| `harness/PROGRESS.md` | 状态快照 |
| `harness/DECISIONS.md` | 长期约束 |
| `harness/plans/` | 待确认方案 |
| `harness/skills/` | 内置 Skill 副本 |
| `harness/rules/` | 编码规范 |
| `harness/acceptance/`、`code_review/`、`code_simplifier/` | 报告 |
| `harness/backlog/` | 归档 |
