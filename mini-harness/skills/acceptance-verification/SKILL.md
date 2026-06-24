---
name: acceptance-verification
description: 对照任务验收标准（AC）验证实现是否符合用户预期与任务范围。在运行时代码实现完成后、代码审查之前使用；不依赖是否经过规划阶段。
---

# 验收验证

## 概述

验证 **「是否做了对的事」**（task-fit），而非代码质量。对照 `harness/todo.md` 中的验收标准（AC），结合可选的 Plan、测试与 git diff，判断实现是否满足任务本意。默认仅输出验收报告，不修改代码。

与 `code-review-expert` 的分工：

| | acceptance-verification | code-review-expert |
|--|-------------------------|-------------------|
| 视角 | 用户 / 任务 | 工程师 |
| 对照物 | todo 中的 AC（+ 可选 plan） | diff、架构、安全 |
| 典型问题 | AC 未确认、AC 与意图不符、AC 未覆盖 | SOLID 违规、安全漏洞 |

## 两层验收（勿混淆）

| 层 | 问题 | 主要手段 | 时机 |
|----|------|----------|------|
| **契约层** | AC 是否与任务标题、范围、用户意图一致 | **人工核对**（todo「AC 已确认」） | **TDD / 实现前** |
| **实现层** | 代码与测试是否满足 AC 条文 | 自动化测试 + diff | 实现后（本 skill） |

本 skill 负责 **实现层**。若契约层未通过，即使全部 MUST-AUTO 测试通过，也不得 Overall: PASS。

**典型误判**：AC 写偏 → TDD 按错误 AC 写测试 → 实现满足错误 AC → 本 skill 全绿，但交付物不符合用户本意。

## 验收契约来源（优先级）

1. **`harness/todo.md` 的「验收标准」** — 主来源（无论是否做过 Plan）
2. **`harness/plans/`** — 仅当 todo 中链接了 plan 文件时，用于补充范围、非目标与 AC 细节
3. **`tests/`** — 自动化证据（含 `tests/acceptance/` 若存在）
4. **git diff** — 实现范围与 AC 的对应关系

若 todo 缺少「验收标准」且任务涉及运行时代码：**Overall 必须为 FAIL**，报告注明须先补 AC，不得视为通过。

## AC 验证级别

| 级别 | 含义 | 未通过时 |
|------|------|----------|
| **MUST-AUTO** | 须有自动化测试证据 | 阻塞交付 |
| **MUST-MANUAL** | 须手测或用户确认 | 阻塞交付，报告给出手测步骤与结果栏 |
| **SHOULD** | 建议满足 | 记入报告，不单独阻塞 |

## 工作流程

### 0) AC 契约核对（先于逐条 AC，阻塞项）

阅读 `harness/todo.md` 的 **「AC 核对」** 节：

| 检查项 | 未满足时 |
|--------|----------|
| 存在「AC 核对」节，且 `- [x] **AC 已确认**` 已勾选 | **Overall: FAIL (AC-CONTRACT)**，Blocking: 是；**不继续**将 MUST-AUTO 全绿视为通过 |
| AC 表与任务标题 / 范围 / 用户消息无明显矛盾 | 若有疑点：Overall FAIL，Next Step 选 **Clarify AC** |

报告中须单独输出 **「AC 契约核对」** 表（见 §4 模板）。契约层 FAIL 时，实现层 AC 仍可逐条记录，但 **Overall 不得为 PASS**。

### 1) 读取验收契约

- 阅读 `harness/todo.md`，提取任务标题、范围、Plan 链接（若有）及验收标准表。
- 若 todo 链接了 `harness/plans/*.md`，读取其中「验收标准」「范围与非目标」章节。
- 使用 `git status -sb`、`git diff --stat`、`git diff` 确定变更范围。

### 2) 逐条对照 AC（实现层）

对每条 AC（AC-1、AC-2…）：

- **PASS**：有明确证据（通过的测试、diff 中的实现、文档）且与 AC 条文一致
- **FAIL**：实现与 AC 矛盾，或测试失败
- **PARTIAL**：部分满足，或证据不足
- **UNVERIFIED**：无测试且无手测记录（MUST 级视为未通过）

检查：

- 实现是否覆盖全部 MUST 级 AC
- diff 是否引入 plan「非目标」中的能力
- 测试是否验证用户可感知行为（而非仅内部实现细节）
- AC 与 TDD 测试是否一一可追溯
- **契约疑点**（可选）：该条 AC 表述是否可能偏离任务意图——记入「Gaps vs Task Intent」，**不替代** todo 中的人工确认

### 3) 运行自动化证据（若仓库已配置）

- 按 `pyproject.toml`、`commands.gate` 或 `profile/PROJECT.md` 运行相关测试（优先与 AC 关联的用例）。
- 记录通过 / 失败与 AC 的映射。

### 4) 输出报告

将报告写入 `harness/acceptance/`，文件名：`YYYY-MM-DD-<任务简述>.md`（与 todo 任务对应，避免覆盖历史报告）。

```markdown
## Acceptance Verification Summary

**Task**: （来自 todo 标题）
**Plan**: （无 / plans/xxx.md）
**Overall**: PASS | FAIL | FAIL (AC-CONTRACT) | PARTIAL
**Blocking**: 是 / 否

---

## AC 契约核对（MUST-MANUAL，先于实现层）

| 检查项 | 状态 | 说明 |
|--------|------|------|
| todo「AC 已确认」已勾选 | PASS / FAIL | 未勾选 → Overall: FAIL (AC-CONTRACT) |
| AC 与任务范围 / 用户意图一致 | PASS / FAIL / 待用户确认 | 疑点写入 Gaps |

---

## AC Coverage（实现层）

| AC | 级别 | 状态 | 证据 |
|----|------|------|------|
| AC-1 | MUST-AUTO | PASS | tests/... |
| AC-2 | MUST-MANUAL | UNVERIFIED | 需手测：… |

---

## Gaps vs Task Intent

- （与 AC、非目标、用户本意不符的项）

---

## Required Before Delivery

1. …

---

## Manual Test Checklist（若有 MUST-MANUAL）

| 步骤 | 预期 | 结果 |
|------|------|------|
| 1. … | … | 待测 / PASS / FAIL |
```

**PASS 条件**（须同时满足）：

1. **AC 契约核对**通过（「AC 已确认」已勾选，且无未解决的契约疑点）
2. 无 MUST 级实现层 AC 为 FAIL 或 UNVERIFIED

**干净验收**：若全部 MUST 通过，说明已对照内容与残余风险（如未覆盖的边界场景）。

### 5) 后续步骤

```markdown
---

## Next Steps

Overall: FAIL | FAIL (AC-CONTRACT) | PARTIAL — …

1. **Confirm AC** — 在 todo 中完成 AC 核对并勾选「AC 已确认」
2. **Fix and re-verify** — 修复后重新运行验收验证
3. **Clarify AC** — todo 中 AC 与用户意图不一致，需用户确认
4. **Accept with documented gaps** — 用户明确接受遗留项（须写入 PROGRESS）
```

**重要**：在用户确认接受遗留项之前，不要将 FAIL 记为通过。不主动修改运行时代码，除非用户要求修复。
