---
name: acceptance-verification
description: 对照 harness todo 的 AC 验收「是否做了对的事」。运行时代码实现完成、交付或审查前必须用本 Skill（常为 subagent）；用户问「符合 AC 吗」「验收一下」「能交付吗」时也用。不替代 todo 里 AC 已确认 的人工勾选。与 code-review-expert 分工：本 Skill 验任务契合，审查看代码质量与安全。
---

# ✅ 验收验证

验证 **「是否做了对的事」**（task-fit），不是代码好不好看。

| | acceptance-verification | code-review-expert |
|--|-------------------------|-------------------|
| 视角 | 👤 用户 / 任务 | 👷 工程师 |
| 对照 | todo 中的 AC | diff、架构、安全 |
| 典型问题 | AC 未确认、AC 偏了、没覆盖 | SOLID、漏洞 |

---

## 两层验收（别混）

| 层 | 问题 | 手段 | 时机 |
|----|------|------|------|
| **契约** | AC 是否符合用户意图 | 人工核对（todo「AC 已确认」） | 实现**前** |
| **实现** | 代码是否满足 AC 条文 | 测试 + diff | 实现**后**（本 Skill） |

契约层未过 → 即使 MUST-AUTO 全绿，**Overall 不得 PASS**。

---

## 契约来源（优先级）

1. `harness/todo.md`「验收标准」— 主来源
2. `harness/plans/` — 仅当 todo 链接了 plan
3. `tests/` — 自动化证据
4. `git diff` — 范围对应

todo 缺 AC 且涉及运行时代码 → **Overall: FAIL**，须先补 AC。

---

## AC 级别

| 级别 | 含义 | 未过 |
|------|------|------|
| **MUST-AUTO** | 须有自动化测试 | 阻塞 |
| **MUST-MANUAL** | 须手测或用户确认 | 阻塞 |
| **SHOULD** | 建议 | 记入报告 |

---

## 工作流

### 0️⃣ AC 契约核对（阻塞）

| 检查 | 未满足 |
|------|--------|
| `- [x] **AC 已确认**` 已勾选 | **FAIL (AC-CONTRACT)**，不继续 |
| AC 与任务范围无明显矛盾 | 疑点 → FAIL 或 Clarify AC |

### 1️⃣ 读契约

提取 todo 标题、范围、Plan 链接、AC 表；`git status` / `git diff` 看变更范围。

### 2️⃣ 逐条 AC

每条：PASS / FAIL / PARTIAL / UNVERIFIED（MUST 级 UNVERIFIED 视为未过）。

检查：MUST 全覆盖 · 无非目标能力 · 测用户可感知行为 · AC 与测试可追溯。

### 3️⃣ 跑自动化

按 `pyproject.toml`、`commands.gate` 或 `PROJECT.md` 跑相关测试，记录与 AC 映射。

### 4️⃣ 写报告

保存到 `harness/acceptance/YYYY-MM-DD-<简述>.md`：

```markdown
## Acceptance Verification Summary

**Task**: …
**Plan**: 无 / plans/xxx.md
**Overall**: PASS | FAIL | FAIL (AC-CONTRACT) | PARTIAL
**Blocking**: 是 / 否

---

## AC 契约核对

| 检查项 | 状态 | 说明 |
|--------|------|------|
| AC 已确认已勾选 | PASS / FAIL | |
| AC 与意图一致 | PASS / FAIL / 待确认 | |

---

## AC Coverage

| AC | 级别 | 状态 | 证据 |
|----|------|------|------|
| AC-1 | MUST-AUTO | PASS | tests/... |

---

## Gaps vs Task Intent

- …

---

## Next Steps

1. Confirm AC / Fix and re-verify / Clarify AC / Accept with documented gaps
```

**PASS** = 契约核对过 + 无 MUST 级 FAIL/UNVERIFIED。

默认**不改代码**，除非用户要求修复。
