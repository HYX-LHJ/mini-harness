# 🔄 协作工作流（细则）

`using-harness` 的**操作手册**。入口摘要见 [SKILL.md](../SKILL.md)。

---

## 并行规则

在不违反步骤依赖的前提下，尽量并行——这是 harness 比「单线程聊天」快的原因。

| 阶段 | ⚡ 可并行 | 🔗 必须串行 |
|------|----------|------------|
| 读状态 | `PROGRESS` + `todo` + `PROJECT`；Plan 时加 `DECISIONS` | — |
| TDD 等待 | subagent 写测试 ∥ 主 Agent 预读 AC、`PROJECT`、相关 `DECISIONS`、待改模块（**不写**运行时代码） | 测试交付 → 实现 |
| 实现后 | `acceptance-verification` ∥ `code-review-expert`（同一条消息） | 实现完成 → 质检；精炼 → 提交前审查 |
| 小修复检 | 可再次并行验收 + 审查 | `code-simplifier` 改代码后须串行审查 |

**本地门禁**（实现后、启动验收/审查前）：跑 `commands.gate` 或 `PROJECT.md` 中的一键命令，把结果附在 subagent 任务说明里。

**合并报告后**：MUST 级 AC 未过或 **AC-CONTRACT** 未确认 → 阻塞交付；P0/P1 审查项须修复。

---

## Subagent 分工

以下步骤**必须**用 subagent（Task）启动，路径见 [SKILL.md § 路径](../SKILL.md#路径)。

| Skill | 时机 | 产出 |
|-------|------|------|
| `tdd` + `python-testing-patterns` | 写运行时代码**之前** | `tests/` 中 failing 测试（red） |
| `acceptance-verification` | 实现完成后 | `harness/acceptance/` 报告 |
| `code-review-expert` | 实现后（可并行）；提交前再复核 | `harness/code_review/` 报告 |
| `code-simplifier` | 用户要求提交/推送前 | `harness/code_simplifier/` 记录 |

仅改 Markdown 或非执行模板 → 跳过测试与验收 subagent。

---

## 流程总览

```text
只读：读状态 → 回答（不登记 todo）

常规：
 读状态 → [Plan] → todo + AC → AC 已确认
  → subagent(测试) ∥ 预读 → 实现 → 门禁
  → 验收 ∥ 审查 → 修复 → [进化?] → 任务归档 → PROGRESS

交付（串行）：
  精炼 → 审查 → 提交 → PROGRESS
```

### 1️⃣ 读状态

并行读 `PROGRESS.md`、`todo.md`、`profile/PROJECT.md`。Plan / 跨模块 / 质疑历史取舍 → 加读 `DECISIONS.md` 相关主题。

### 2️⃣ Plan

需求含糊、多方案、动契约或跨模块 → 读 [brainstorming](../../brainstorming/SKILL.md)。方案进 `plans/`，**AC 同步到 todo**，用户确认后再写代码。小修复可跳过。

### 3️⃣ AC 核对（人工门禁）

自动化只能验证「实现是否符合 AC」，不能证明「AC 是否符合用户意图」。

在 todo「AC 核对」节：

1. 起草 AC，向用户复述每条场景与预期
2. 确认后勾选 `- [x] **AC 已确认**`
3. **未勾选前**：不启动 TDD、不写运行时代码；验收判 **Overall: FAIL (AC-CONTRACT)**

### 4️⃣ todo

有变更先写 `todo.md`。涉及运行时代码须含 **验收标准** 表（AC-1…：场景、MUST-AUTO / MUST-MANUAL / SHOULD、验证方式）及 **AC 核对** 节。

### 5️⃣ 开发与测试

启动 subagent 跑 `tdd` + `python-testing-patterns`，在 `tests/` 写 **failing 测试**。

等待期间主 Agent 可预读 AC、`PROJECT`、相关 `DECISIONS`、待改模块——**不得**提前写运行时代码。

### 6️⃣ 验收、审查与收尾

1. 门禁通过后，**同一条消息**并行启动验收 + 审查
2. 合并报告，修阻塞项
3. **进化提案（可选）**：重大取舍 → `DECISIONS` 对应主题；可执行规则 → `PROJECT.md`；确认后追加 `evolution.jsonl`
4. 勾完 todo
5. **任务归档**：
   - 复制任务块到 `harness/backlog/YYYY-MM-DD-<简述>.md`
   - 更新 `backlog/index.md`
   - `todo.md` 重置为空闲模板
6. 更新 `PROGRESS.md`

### 7️⃣ Git 提交

用户要求提交时（**串行**）：`code-simplifier` → `code-review-expert` → 按策略提交（不 force push）→ 刷新 `PROGRESS.md`

---

## 内置 Skill 索引

| Skill | 时机 | 执行方 |
|-------|------|--------|
| [python-code-style](../../python-code-style/SKILL.md) | 仅仓库初始化 | 主 Agent |
| [brainstorming](../../brainstorming/SKILL.md) | Plan | 主 Agent |
| [tdd](../../tdd/SKILL.md) | 写运行时代码前 | Subagent |
| [python-testing-patterns](../../python-testing-patterns/SKILL.md) | 写运行时代码前 | Subagent |
| [acceptance-verification](../../acceptance-verification/SKILL.md) | 实现后 | Subagent |
| [code-review-expert](../../code-review-expert/SKILL.md) | 实现后 / 提交前 | Subagent |
| [code-simplifier](../../code-simplifier/SKILL.md) | 提交前 | Subagent |

遵循 `pyproject.toml` / `commands.gate` 与 `profile/PROJECT.md`。测试在仓库根 `tests/`。

---

## 📂 Harness 目录

| 路径 | 用途 |
|------|------|
| `todo.md` | 当前任务与 AC |
| `PROGRESS.md` | 状态快照 |
| `DECISIONS.md` | 按主题的重大决策 |
| `profile/PROJECT.md` | 项目画像（每回合必读） |
| `profile/evolution.jsonl` | 进化审计 |
| `plans/` | 待确认方案 |
| `skills/` | 内置 Skill 副本 |
| `acceptance/`、`code_review/`、`code_simplifier/` | 报告 |
| `backlog/` | 归档 |
