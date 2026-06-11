# {{PROJECT_NAME}} — Agent Playbook

给智能体：每回合做什么、何时停、产物写哪。**Skill 细则见 Skill 自身**；本文只做编排与硬约束。

**优先级**：本文 > Skill。不得跳过 todo 登记、不得代替 lint + pytest 门禁、**凡改 `{{SRC_DIR}}/` 必须同步补测**（无例外）。

---

## 角色分工

| 角色 | 职责 |
|------|------|
| **主 Agent**（当前会话） | 门禁、`harness/todo.md` / `PROGRESS.md`、实现与小修、对用户汇总 |
| **Subagent**（Cursor **Task**） | **code-review**、**code-simplifier**、代码库探索、上下文大的摸底；主 Agent 负责登记 → 派遣 → 收稿 → **落盘** |

**禁止**：主 Agent 在对话里通读大 diff 后自写完整审查/精炼报告正文（Subagent 专责产出；主 Agent 仅整理落盘与对用户摘要）。

---

## 流程总览

每用户输入 = 一回合。先走**常规回合**；用户要求提交时，在常规收尾基础上追加**提交回合**。

```
常规：门禁(前) → 读 harness → [Plan] → 登记 todo → [改 {{SRC_DIR}}/? → 启动 tdd] → 实现 → [code-review] → 门禁(后) → PROGRESS

提交：…常规收尾… → code-simplifier → 二次 code-review → {{DEV_BRANCH}} 提交 → 同步 {{TEST_BRANCH}} → 再刷 PROGRESS
```

| 路径 | 触发 | 额外步骤 |
|------|------|----------|
| **常规回合** | 每次用户输入 | 改 `{{SRC_DIR}}/` 须 todo 后立即启动 tdd，收尾做 code-review |
| **提交回合** | 「提交」「推送」「commit」「push」等 | 交付含 `{{SRC_DIR}}/` 须 simplify + 二次 code-review，再 Git 工作流 |

---

## Skill 触发

| Skill | 何时启用 | 执行方 | 跳过条件 |
|-------|----------|--------|----------|
| **`tdd`** | 登记 todo **后**、改 `{{SRC_DIR}}/` **前** | 主 Agent | 本回合不改 `{{SRC_DIR}}/` |
| **`code-review-expert`** | 本回合改过 `{{SRC_DIR}}/`（收尾） | **Subagent** | 未改 `{{SRC_DIR}}/`，或用户明确跳过 |
| **`code-simplifier`** | 用户要求提交且交付含 `{{SRC_DIR}}/` | **Subagent** | 仅 harness 文档/脚本 |
| **`code-review-expert`**（二次） | `code-simplifier` 之后、commit 之前 | **Subagent** | 同 code-simplifier |

---

## Subagent 产物（硬约束）

以下步骤**未完成则回合不得收尾**（提交回合同理：缺报告不得 `git commit`）。

### code-review-expert

1. **派遣**：Task + 本回合 diff + `code-review-expert` Skill。
2. **正文**：结构化审查（严重度；结论 APPROVE / REQUEST_CHANGES / COMMENT）。
3. **落盘**（主 Agent，**必须**）：
   - `harness/code_review/YYYY-MM-DD_主题简述.md`
   - [code_review/index.md](harness/code_review/index.md) 顶部新增一行
   - 未关闭 **P0/P1** → [open-findings.md](harness/code_review/open-findings.md)
4. **禁止**：仅以聊天代替落盘。

### code-simplifier

1. **派遣**：Task + 待提交 `{{SRC_DIR}}/` diff + `code-simplifier` Skill。
2. **实施**：Subagent 简化代码并简述改动。
3. **落盘**（主 Agent，**必须**）：
   - `harness/code_simplifier/YYYY-MM-DD_主题简述.md`
   - [code_simplifier/index.md](harness/code_simplifier/index.md) 顶部新增一行
4. **后续**：精炼后重新门禁；含 `{{SRC_DIR}}/` 须二次 code-review。

---

## 常规回合

### 1. 门禁（前）

失败则**只修门禁**，不推进用户任务。

```powershell
{{LINT_CMD}}
{{PYTEST_CMD}}
```

### 2. 读上下文

`harness/PROGRESS.md`、`harness/todo.md`；重大任务前 [plan-mode.md](harness/docs/plan-mode.md)；架构边界 `harness/DECISIONS.md`。

### 3. Plan（重大任务）

满足 plan-mode 触发条件 → `harness/plans/` → **等用户确认** → 再登记 todo。**未确认前不得改 `{{SRC_DIR}}/`**。

### 4. 登记 todo

有变更必先登记 `harness/todo.md`。

### 5. 启动 tdd → 实现（改 `{{SRC_DIR}}/` 时）

1. 登记 todo 后**立即**启用 **tdd** Skill；**不得**先改 `{{SRC_DIR}}/` 再补测。
2. 先 `harness/tests/` → 再 `{{SRC_DIR}}/`。
3. 仅改 `{{SRC_DIR}}/` 无测试不得收尾/提交。

### 6. 收尾

- 改过 `{{SRC_DIR}}/` → Task + code-review-expert → 落盘 `harness/code_review/`
- 勾 todo → 门禁（后）
- `sync_progress.py` → 手写 PROGRESS（见 [harness/index.md](harness/index.md)）

---

## 提交回合

### A. 提交前精炼（含 `{{SRC_DIR}}/` 时不得跳过）

1. code-simplifier → 落盘 → 门禁
2. 二次 code-review-expert → 落盘
3. 仅 harness 时可跳过

### B. Git 工作流（{{DEV_BRANCH}} → {{TEST_BRANCH}}）

1. 确认在 `{{DEV_BRANCH}}`
2. `git status` / `git diff` 排除密钥与临时联调
3. 门禁全绿 → commit → push `{{DEV_BRANCH}}`
4. merge `{{TEST_BRANCH}}` → push → 回 `{{DEV_BRANCH}}`
5. 推送后 `sync_progress.py` + 手写 PROGRESS

### 提交纪律

- 先 `{{DEV_BRANCH}}` 再 `{{TEST_BRANCH}}`
- 默认不提交：密钥、`.env` 实值、`harness/out/`、`harness/pre/`、未请求的联调代码
- 项目特定「不得提交」路径写入 `harness/DECISIONS.md`

---

## 测试与验证

| 环节 | 要求 |
|------|------|
| **编写** | 改 `{{SRC_DIR}}/` 须先 tdd；测试与实现同批交付 |
| **执行** | 每回合首尾各跑门禁 |
| **范围** | 默认 `pytest` 排除 `@pytest.mark.integration` |

## 质量门禁

| 命令 | 范围 |
|------|------|
| `harness/scripts/lint_src.py` | `{{SRC_DIR}}/`（ruff + pyright） |
| `pytest` | `harness/tests/` 单元测试 |

失败：不得推进任务；修到全绿后从门禁（前）重来。细节见 [harness/index.md](harness/index.md)。

---

## Harness 产物

| 文件 / 目录 | 要点 |
|-------------|------|
| **todo.md** | 有变更必先登记 |
| **PROGRESS.md** | 脚本写机械章；主 Agent 手写「当前状态」「已知问题」「下一步」 |
| **DECISIONS.md** | 活跃约束 |
| **plans/** | 用户确认前不得改 `{{SRC_DIR}}/` |
| **code_review/** | 审查须落盘 + index + open-findings |
| **code_simplifier/** | 提交前精炼须落盘 |

路径索引：[harness/index.md](harness/index.md)。
