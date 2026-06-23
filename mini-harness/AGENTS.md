# Agent Harness Playbook

> **mini-harness 核心 Skill 正文。** 本文件由 `mini-harness` Skill 分发；每回合须先遵循本 Playbook，再执行用户任务。Skill 入口：`harness/skills/mini-harness/SKILL.md`（插件内为 `skills/mini-harness/SKILL.md`）。

项目业务规则写在 `harness/DECISIONS.md` 或项目文档，不写入本文件。

## 硬约束

1. 有文件变更时，先登记 `harness/todo.md`。
2. 修改运行时代码时，须在 todo 中写明 **验收标准（AC）**；同步在 `tests/` 新增或修改对应测试。
3. **AC 人工核对**：todo 中 AC 写好后，须与用户确认任务意图一致，并勾选「**AC 已确认**」。**未确认前不得启动 TDD 或编写实现**（避免 AC 写错导致测试与验收全绿但做错事）。
4. 只处理当前任务范围；不得覆盖、回滚或提交用户已有的无关改动。
5. **编写正式任务代码前的测试**须通过 subagent 执行 `tdd` + `python-testing-patterns`；**实现完成后的验收**、**代码审查**与 **提交前精炼**须通过 subagent 执行 `acceptance-verification`、`code-review-expert`、`code-simplifier`（见「Subagent 执行」）。主 Agent 不得跳过 subagent 自行替代上述步骤。
6. **允许并行**的步骤见「并行规则」；无依赖冲突时主 Agent 应在同一条消息中同时启动可并行的 subagent，以缩短链路耗时。

## Subagent 执行

下列步骤 **必须**通过 subagent（Task）启动，读取并遵循 **`harness/skills/` 下对应 `SKILL.md`**（任务说明中写明仓库内路径，例如 `harness/skills/tdd/SKILL.md`；**不得**依赖全局 `~/.agents/skills/` 等同名 skill），将产出交回主 Agent 后继续；不得省略 subagent 步骤。

| Skill | 触发时机 | Subagent 产出 |
|------|----------|---------------|
| `tdd` + `python-testing-patterns` | **主 Agent 编写正式运行时代码之前** | `tests/` 中与本任务 AC 对应的 failing 测试（red 阶段） |
| `acceptance-verification` | 主 Agent 完成运行时代码编写后 | 验收报告（`harness/acceptance/`） |
| `code-review-expert` | 实现完成后（可与验收**并行**）；Git 提交前须再复核 | 审查报告（`harness/code_review/`） |
| `code-simplifier` | 用户要求提交或推送之前 | 精炼报告（`harness/code_simplifier/`） |

**主 Agent** 在 subagent 交付测试后：按 red-green-refactor 编写运行时代码（green / refactor），并确保 diff 含对应测试。仅改 Markdown 或非执行模板时跳过测试 subagent、验收 subagent 与 §4 开发节。

## 并行规则

在**不违反步骤间硬依赖**的前提下，下列并行可显著缩短链路；主 Agent 应主动采用。

| 阶段 | 可并行 | 必须串行 |
|------|--------|----------|
| 读状态 | `PROGRESS.md`、`todo.md`、`DECISIONS.md` 同时读取 | — |
| TDD 等待期 | subagent 写测试 ∥ 主 Agent 预读 AC、`DECISIONS`、编码规范、待改模块（**不得**提前写运行时代码） | subagent 交付测试 → 主 Agent 实现 |
| 实现后质检 | `acceptance-verification` ∥ `code-review-expert`（同一条消息启动两个 subagent） | 实现完成 → 验收/审查；精炼 → 提交前审查 |
| 修复后复检 | 小范围修复后可再次并行验收 + 审查 | `code-simplifier` 改代码后须串行审查 |

**主 Agent 本地门禁**（实现完成后、启动验收/审查 subagent 之前）：

```bash
pytest
ruff check agent tests
mypy agent
```

将结果附在 subagent 任务说明中，subagent 侧重对照 AC / diff 写报告，避免重复探索与重复跑测。

**合并两份报告后**：验收 MUST 级 AC 未通过仍阻塞交付；**AC 契约未确认（AC-CONTRACT）** 亦阻塞交付；审查 P0/P1 须修复。主 Agent 统一排期修复，不必等两份报告先后返回再动手。

## 内置 Skill

路径：`harness/skills/`。

| Skill | 读取时机 | 执行方式 |
|------|----------|----------|
| [python-code-style](harness/skills/python-code-style/SKILL.md) | 仅仓库初始化时，配置 Python 工具链 | 主 Agent |
| [brainstorming](harness/skills/brainstorming/SKILL.md) | 做 Plan 时（必须） | 主 Agent |
| [tdd](harness/skills/tdd/SKILL.md) | 主 Agent 编写运行时代码**之前**（与 `python-testing-patterns` 同时） | **Subagent**（仅写测试） |
| [python-testing-patterns](harness/skills/python-testing-patterns/SKILL.md) | 主 Agent 编写运行时代码**之前**（与 `tdd` 同时） | **Subagent**（仅写测试） |
| [acceptance-verification](harness/skills/acceptance-verification/SKILL.md) | 运行时代码编写完成后（可与 `code-review-expert` 并行） | **Subagent** |
| [code-review-expert](harness/skills/code-review-expert/SKILL.md) | 实现完成后（可与验收并行）；提交前须再复核 | **Subagent** |
| [code-simplifier](harness/skills/code-simplifier/SKILL.md) | Git 提交之前 | **Subagent** |

## 编码规范 Rules

路径：`harness/rules/`。存放 **mini-harness 自带的通用编码规范**（与按需读取的 Skills 区分）；项目专属约定写入 `harness/DECISIONS.md` 或在 `harness/rules/` 下新增文件。

| 文件 | 说明 |
|------|------|
| [python-coding-conventions.md](harness/rules/python-coding-conventions.md) | Python 编码规范 |

修改 Python 运行时代码前，阅读 `harness/rules/` 中已完善的规范；并按宿主要求接线到 Cursor Rules 或 Claude Code（见 `harness/rules/index.md`）。

## 测试目录

测试文件放在仓库根目录 `tests/`。与用户可感知行为相关的验收测试可放在 `tests/acceptance/`（见 `harness/DECISIONS.md` 或项目约定）。

## 流程

```text
只读：读状态（并行） → 回答 / 诊断

常规：
 读状态（并行） → [Plan] → todo（含 AC）→ **AC 核对（人工）**
  → subagent(写测试) ∥ 主 Agent 预读 AC/规范/模块
  → 主 Agent 实现 → 本地 pytest/ruff/mypy
  → subagent(验收) ∥ subagent(审查) → 主 Agent 合并修复 → 归档 todo → PROGRESS

交付（须串行）：
  subagent(code-simplifier) → subagent(code-review) → 提交 / 推送 → PROGRESS
```

### 只读任务

不登记 todo。

### 1. 读状态

并行读取：

- `harness/PROGRESS.md`
- `harness/todo.md`
- 需要长期约束时：`harness/DECISIONS.md`

其它从 `harness/index.md` 下钻。

### 2. Plan

需求含糊、多方案、影响契约或跨模块时，先做 Plan。

做 Plan 时必须读 `brainstorming`；方案写入 `harness/plans/`，**验收标准同步到 `harness/todo.md`**，用户确认后再实现。小修复可跳过 Plan，**不可跳过 todo 中的 AC**。

### 3.1 AC 核对（人工门禁）

自动化与 `acceptance-verification` 只能回答 **「实现是否符合 AC」**，无法证明 **「AC 是否符合用户/任务意图」**。AC 一旦写偏，TDD 与验收会连锁误判。

在 todo 的「AC 核对」节中：

1. 主 Agent 起草 AC 后，用自然语言向用户复述每条 AC 的场景与预期，请用户确认或修正。
2. 用户确认后，勾选 `- [x] **AC 已确认**`。
3. **未勾选前**：不得启动 TDD subagent、不得编写运行时代码；`acceptance-verification` 须判 **Overall: FAIL (AC-CONTRACT)**。

### 3. todo

有变更先登记 `harness/todo.md`。

**涉及运行时代码**时，todo 须含 **验收标准** 表（AC-1、AC-2…），列明场景/预期、级别（MUST-AUTO / MUST-MANUAL / SHOULD）、验证方式；并含 **AC 核对** 节（见 §3.1）。无 Plan 时 AC 直接写在此；有 Plan 时从 plan 同步并保留 plan 链接。实现勾选项与 AC ID 对应。

### 4. 开发与测试

修改运行时代码时，先 **启动 subagent** 执行 `tdd` 与 `python-testing-patterns`，对照 todo 中的 AC 在 `tests/` 编写 **failing 测试**（red）。

**TDD subagent 运行期间**，主 Agent 可并行完成实现前阅读（不得提前编写运行时代码）：

1. `harness/todo.md` 中的验收标准
2. `harness/DECISIONS.md` 或项目开发规范
3. 修改 Python 代码时，`harness/rules/` 中的编码规范
4. 待修改模块的现有实现

subagent 交付测试后，主 Agent **随后**编写运行时代码（green / refactor），并本地跑通门禁（见「并行规则」）。

Subagent 只负责测试；运行时代码由主 Agent 编写。diff 须同时含测试与实现。仅改 Markdown 或非执行模板时跳过测试 subagent、验收 subagent 与本节。

### 5. 验收、Review 与收尾

1. 本地门禁通过后，**同一条消息并行启动** `acceptance-verification` 与 `code-review-expert` subagent；任务说明中附上 pytest / ruff / mypy 结果
2. 主 Agent 合并两份报告，统一修复阻塞项（验收 MUST 级 AC、审查 P0/P1）
3. 若仍有阻塞，修复后可再次并行验收 + 审查，直至无阻塞项
4. 勾完 todo（含全部 AC）
5. **任务归档**（全部 MUST 级 AC 通过且无阻塞审查项后执行）：
   - 将当前 `harness/todo.md` 中的任务块（标题、范围、Plan 链接、AC 核对、验收标准、实现勾选）复制到 `harness/backlog/YYYY-MM-DD-<任务简述>.md`
   - 在 `harness/backlog/index.md` 追加一行：`- YYYY-MM-DD · 任务标题 — [验收](acceptance/...) · [审查](code_review/...) · [归档](backlog/...)`
   - 将 `harness/todo.md` 重置为空闲模板：保留文件头「进行中的任务」、当天日期行、`暂无进行中的任务。` 及 HTML 注释中的可复制任务结构（与 `harness/.package/template/harness/todo.md` 一致；将模板中的 `{{TODAY}}` 替换为当天 `YYYY-MM-DD`）
6. 更新 `harness/PROGRESS.md`：
   - 「当前状态」：反映仓库最新事实（勿堆砌已归档任务的 AC 细节）
   - 「已完成」：追加本条一行摘要，链接受收报告（及 plan 若存在）
   - 「进行中」：清空（无新任务时写 `-`）
   - 「已知问题」：同步 `doctor` warnings 或其它阻塞项；无则写 `-`

### 6. Git 提交

用户要求提交或推送时，提交前按顺序（**不可并行**：精炼会改代码，审查须看最新 diff）：

1. **启动 subagent** 执行 `code-simplifier`（若实际改动了代码，再走下一步），报告写入 `harness/code_simplifier/`
2. **启动 subagent** 执行 `code-review-expert`，确认无阻塞项
3. 按仓库分支与提交策略操作

冲突、非快进或权限问题时停止，不 force push。完成后刷新 `harness/PROGRESS.md`。

## Harness 目录

| 路径 | 用途 |
|------|------|
| `harness/todo.md` | 当前任务与 **验收标准（AC）** |
| `harness/PROGRESS.md` | 当前状态 |
| `harness/DECISIONS.md` | 长期约束 |
| `harness/plans/` | 待确认方案（AC 须同步到 todo） |
| `harness/skills/` | 内置 Skill |
| `harness/rules/` | 编码规范等常驻规则 |
| `harness/acceptance/` | 验收报告 |
| `harness/code_review/` | 审查报告 |
| `harness/code_simplifier/` | 精炼记录 |
| `harness/backlog/` | 归档 |
