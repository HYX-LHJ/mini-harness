---
name: code-review-expert
description: "以资深工程师视角对当前 git 变更进行专家级代码审查。检测 SOLID 违规、安全风险，并提出可执行的改进建议。"
---

# 代码审查专家

## 概述

对当前 git 变更进行结构化审查，重点关注 SOLID、架构、可删除候选代码以及安全风险。除非用户要求实施修改，否则默认仅输出审查结果。

## 严重级别

| 级别 | 名称 | 描述 | 处理方式 |
|-------|------|-------------|--------|
| **P0** | 严重 | 安全漏洞、数据丢失风险、正确性缺陷 | 必须阻止合并 |
| **P1** | 高 | 逻辑错误、显著的 SOLID 违规、性能回退 | 合并前应修复 |
| **P2** | 中 | 代码异味、可维护性问题、轻微的 SOLID 违规 | 在本 PR 中修复或创建后续任务 |
| **P3** | 低 | 风格、命名、轻微建议 | 可选改进 |

## 工作流程

### 1) 预检上下文

- 使用 `git status -sb`、`git diff --stat` 和 `git diff` 确定变更范围。
- 如有需要，使用 `rg` 或 `grep` 查找相关模块、用法和契约。
- 识别入口点、所有权边界和关键路径（认证、支付、数据写入、网络）。

**边界情况：**
- **无变更**：若 `git diff` 为空，告知用户并询问是否要审查已暂存的变更或特定提交范围。
- **大型 diff（>500 行）**：先按文件汇总，再按模块/功能区域分批审查。
- **混合关注点**：按逻辑功能分组发现项，而非仅按文件顺序。

### 2) SOLID + 架构异味

- 加载 `references/solid-checklist.md` 获取具体检查提示。
- 关注：
  - **SRP**：承担无关职责的重载模块。
  - **OCP**：为添加行为而频繁修改代码，而非通过扩展点。
  - **LSP**：破坏预期或需要类型检查的子类。
  - **ISP**：包含未使用方法的宽泛接口。
  - **DIP**：高层逻辑与底层实现紧耦合。
- 提出重构建议时，说明*为何*能改善内聚/耦合，并概述最小、安全的拆分方案。
- 若重构非平凡，提出增量计划而非大规模重写。

### 3) 可删除候选 + 迭代计划

- 加载 `references/removal-plan.md` 获取模板。
- 识别未使用、冗余或已被功能开关关闭的代码。
- 区分**可立即安全删除**与**需延后并制定计划**。
- 提供包含具体步骤和检查点（测试/指标）的后续计划。

### 4) 安全与可靠性扫描

- 加载 `references/security-checklist.md` 获取检查覆盖项。
- 检查：
  - XSS、注入（SQL/NoSQL/命令）、SSRF、路径遍历
  - AuthZ/AuthN 缺口、缺失的租户检查
  - 密钥泄露或 API 密钥出现在日志/环境变量/文件中
  - 速率限制、无界循环、CPU/内存热点
  - 不安全的反序列化、弱加密、不安全的默认配置
  - **竞态条件**：并发访问、先检查后执行（check-then-act）、TOCTOU、缺失锁
- 同时说明**可利用性**和**影响**。

### 5) 代码质量扫描

- 加载 `references/code-quality-checklist.md` 获取检查覆盖项。
- 检查：
  - **错误处理**：吞掉异常、过于宽泛的 catch、缺失错误处理、异步错误
  - **性能**：N+1 查询、热路径中的 CPU 密集操作、缺失缓存、无界内存
  - **边界条件**：null/undefined 处理、空集合、数值边界、差一错误（off-by-one）
- 标记可能导致静默失败或生产事故的问题。

### 6) 输出格式

按以下结构组织审查结果：

```markdown
## Code Review Summary

**Files reviewed**: X files, Y lines changed
**Overall assessment**: [APPROVE / REQUEST_CHANGES / COMMENT]

---

## Findings

### P0 - Critical
(none or list)

### P1 - High
1. **[file:line]** Brief title
  - Description of issue
  - Suggested fix

### P2 - Medium
2. (continue numbering across sections)
  - ...

### P3 - Low
...

---

## Removal/Iteration Plan
(if applicable)

## Additional Suggestions
(optional improvements, not blocking)
```

**行内评论**：针对特定文件的发现项使用此格式：
```
::code-comment{file="path/to/file.ts" line="42" severity="P1"}
Description of the issue and suggested fix.
::
```

**干净审查**：若未发现问题，明确说明：
- 已检查的内容
- 未覆盖的区域（例如「未验证数据库迁移」）
- 残余风险或建议的后续测试

### 7) 后续步骤确认

呈现发现项后，询问用户如何继续：

```markdown
---

## Next Steps

I found X issues (P0: _, P1: _, P2: _, P3: _).

**How would you like to proceed?**

1. **Fix all** - I'll implement all suggested fixes
2. **Fix P0/P1 only** - Address critical and high priority issues
3. **Fix specific items** - Tell me which issues to fix
4. **No changes** - Review complete, no implementation needed

Please choose an option or provide specific instructions.
```

**重要**：在用户明确确认之前，不要实施任何修改。这是审查优先的工作流程。

## 资源

### references/

| 文件 | 用途 |
|------|---------|
| `solid-checklist.md` | SOLID 异味提示与重构启发式 |
| `security-checklist.md` | Web/应用安全与运行时风险检查清单 |
| `code-quality-checklist.md` | 错误处理、性能、边界条件 |
| `removal-plan.md` | 删除候选与后续计划模板 |
