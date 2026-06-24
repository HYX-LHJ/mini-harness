---
name: code-review-expert
description: 资深代码审查（SOLID、安全、架构异味）。实现完成后、git commit/push/提 PR 前，或用户说 review、审查、能合并吗、有没有漏洞时，必须用本 Skill。可与 acceptance-verification 并行。默认只出报告；用户明确要求才改代码。
---

# 🔍 代码审查专家

对当前 git 变更做结构化审查。默认**只输出报告**，用户确认前不实施修改。

---

## 严重级别

| 级别 | 含义 | 处理 |
|------|------|------|
| **P0** | 安全、数据丢失、正确性 | 🛑 必须阻止合并 |
| **P1** | 逻辑错误、严重 SOLID、性能回退 | 合并前修复 |
| **P2** | 异味、可维护性 | 本 PR 或后续 |
| **P3** | 风格、命名 | 可选 |

---

## 工作流

### 1️⃣ 摸清范围

`git status` · `git diff` · 必要时 `rg` 查用法与契约。标出入口、所有权、关键路径（认证、支付、写库、网络）。

| 情况 | 做法 |
|------|------|
| 无 diff | 问用户是否审 staged 或指定提交 |
| 大 diff (>500 行) | 先按模块汇总再分批 |
| 混合关注点 | 按功能分组，不按文件顺序 |

### 2️⃣ SOLID + 架构

读 [solid-checklist.md](references/solid-checklist.md)。重构建议说明**为何**能改善内聚/耦合，给增量方案而非大爆炸重写。

### 3️⃣ 可删除候选

读 [removal-plan.md](references/removal-plan.md)。区分可立即删 vs 需计划后删。

### 4️⃣ 安全扫描

读 [security-checklist.md](references/security-checklist.md)：注入、XSS、SSRF、AuthZ 缺口、密钥泄露、竞态/TOCTOU 等。说明可利用性与影响。

### 5️⃣ 代码质量

读 [code-quality-checklist.md](references/code-quality-checklist.md)：错误处理、N+1、边界条件、静默失败。

### 6️⃣ 输出报告

写入 `harness/code_review/YYYY-MM-DD_<主题>.md`：

```markdown
## Code Review Summary

**Files reviewed**: X files, Y lines
**Overall**: APPROVE | REQUEST_CHANGES | COMMENT

---

## Findings

### P0 - Critical
…

### P1 - High
1. **[file:line]** 标题
   - 问题
   - 建议

### P2 / P3
…

---

## Next Steps

发现 P0: _ P1: _ … — 请选择：Fix all / Fix P0-P1 / 指定项 / 仅审查
```

无问题时说明已查范围与残余风险。

---

## 参考清单

| 文件 | 用途 |
|------|------|
| [solid-checklist.md](references/solid-checklist.md) | SOLID 异味 |
| [security-checklist.md](references/security-checklist.md) | 安全 |
| [code-quality-checklist.md](references/code-quality-checklist.md) | 错误处理、性能 |
| [removal-plan.md](references/removal-plan.md) | 删除计划模板 |
