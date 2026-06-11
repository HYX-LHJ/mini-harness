# Harness 周回顾（Agent）

**目的**：保证 Agent 每回合读到的 harness 内容**全是活跃态**——无过时结论、无已关闭技术债、无历史任务堆在入口文件里。

**执行方**：主 Agent 通读本文并**逐项落盘**；不靠专用「周回顾脚本」代替判断。可派遣 **explore** Subagent 对照 `src/`、部署与对外文档，核实「活跃」是否仍成立。

**触发**（见根 [AGENTS.md](../../AGENTS.md)「周回顾回合」）：

- **每周一**，本仓库**当天第一个 Agent 会话**，在承接用户其它任务之前必须先做周回顾。
- **新自然周**首个非周一会话（上周未做）——同样必须先做。
- 用户可随时说「执行 harness 周回顾」补做；用户明确「跳过本周回顾」时可跳过。

常规每回合仍走 [AGENTS.md](../../AGENTS.md)；本文是**额外**的每周一次归档回合。

---

## 回合顺序

1. **门禁（前）** — `lint_src.py` + `pytest`
2. **登记** [todo.md](../todo.md)：`task：harness 周回顾（YYYY-MM-DD）`，子项对应下文 §2 各表（可勾 `- [ ]`）
3. **按下表逐项处理** — 先迁出非活跃内容，再重写活跃文件
4. **跨周 todo** — 仓库根目录：`python harness/scripts/archive_harness_todo.py`（将上周及更早 task 迁入 [backlog/archive.md](../backlog/archive.md)）
5. **`sync_progress.py`** — 刷新 PROGRESS 机械章节
6. **手写** PROGRESS「当前状态」「下一步」「已知问题」；在「当前状态」加一句：`本周 harness 周回顾已完成（YYYY-MM-DD）`
7. **门禁（后）** — 同上
8. **勾完** todo 子项，向用户简短汇总：迁了哪些、活跃面还剩什么

**本回合默认不改 `src/`**（除非用户另开实现 task）。

---

## Agent 可读面 — 活跃 vs 归档

下列路径是 Agent **常规回合可能读到**的全部 harness 面（含 L0 入口与各 `index.md` 下钻）。周回顾须保证：**左侧「活跃文件」里不出现右侧「应迁出」类内容**。

### L0 — 每回合入口

| 活跃文件 | 应只保留什么 | 迁出去哪 | 周回顾动作 |
|----------|--------------|----------|------------|
| [todo.md](../todo.md) | **当前自然周**未勾 / 已勾 task | [backlog/archive.md](../backlog/archive.md) | 跑 `archive_harness_todo.py`；确认无上周日期块残留 |
| [PROGRESS.md](../PROGRESS.md) §当前状态 | ≤5 bullet，**现状**与阻塞缺口 | （删，不归档） | 删已交付、已上线、已不再影响接手的句子；勿当 changelog |
| [PROGRESS.md](../PROGRESS.md) §下一步 | 近 1～2 周**仍有效**意向 | （删，不归档） | 已完成删；用户已确认「不做」的标暂缓并链 plan；不必全进 todo |
| [PROGRESS.md](../PROGRESS.md) §已知问题 | 仅 **open / deferred / observe** 的 P0–P2 | 已关闭 → open-findings 归档 | 与 open-findings **活跃表**逐条对齐；无则写「暂无」 |
| [PROGRESS.md](../PROGRESS.md) §已完成 | **本周**全勾 task 名（机械） | 更早 → backlog/archive | 依赖 archive 脚本；勿手工堆历史 |
| [PROGRESS.md](../PROGRESS.md) §进行中 | 有未勾子项的 task（机械） | — | 依赖 sync；确认与 todo 一致 |
| [DECISIONS.md](../DECISIONS.md) | 仍约束实现的条目（约 15～25 条） | [backlog/decisions-archive.md](../backlog/decisions-archive.md) | 作废 / 被取代 / 仅历史背景 → 归档；同主题合并 |

### 方案与审查

| 活跃文件 | 应只保留什么 | 迁出去哪 | 周回顾动作 |
|----------|--------------|----------|------------|
| [plans/index.md](../plans/index.md) | 未实现、**待用户确认**、或仍影响排期的方案 | 正文保留，索引标「已实现」 | 已实现改状态；长期「待确认」→ 与用户确认关闭或续做 |
| [code_review/open-findings.md](../code_review/open-findings.md) | **open / deferred / observe** 行 | [open-findings-closed.md](../code_review/open-findings-closed.md) | **closed** 行与 `<details>` 历史块全部迁出；主表勿留占位+真项重复 |
| [code_review/index.md](../code_review/index.md) | 近 **4 周**报告索引（约 15～20 行） | [archive-index.md](../code_review/archive-index.md) | 更早表格行下移归档；**报告 `.md` 正文不删** |
| [code_simplifier/index.md](../code_simplifier/index.md) | 近 4 周索引 | 可自建 `archive-index.md` 或并入 backlog 说明 | 同上，仅动索引表 |

### 索引与对接文档

| 活跃文件 | 应只保留什么 | 迁出去哪 | 周回顾动作 |
|----------|--------------|----------|------------|
| [index.md](../index.md) | 入口说明、**活跃**维护约定 | — | 检查无失效链接、无重复/矛盾约定 |
| [docs/index.md](index.md) | 当前有效文档链接 | — | 移除已删文档链接 |
| 项目对接文档（如 `docs/api_*.md` 等） | 与**当前**对外契约一致 | — | 若 DECISIONS / `src/` 已变而文档未跟 → 登记 todo 或当回合修文档 |
| [plans/*.md](../plans/) 正文 | 未关闭方案的全文 | — | 已实现方案在文首标「已实现」；勿删文件 |

### 只读归档（Agent 周回顾后**不应**当首要上下文读）

| 路径 | 说明 |
|------|------|
| [backlog/archive.md](../backlog/archive.md) | 历史周 todo |
| [backlog/decisions-archive.md](../backlog/decisions-archive.md) | 作废决策 |
| [code_review/open-findings-closed.md](../code_review/open-findings-closed.md) | 已关闭 findings |
| [code_review/archive-index.md](../code_review/archive-index.md) | 历史审查索引 |
| `code_review/YYYY-MM-DD_*.md` | 审查正文（按索引查，非每回合通读） |

---

## 逐项验收标准（完成前自检）

- [ ] 新会话只读 L0 + 各活跃 index，**30 秒内**能判断：要做什么、卡什么、债还有什么
- [ ] open-findings **主表**无 `closed`、无大块 `<details>` 历史
- [ ] PROGRESS「已知问题」与 open-findings 活跃行**一致**
- [ ] PROGRESS「当前状态 / 下一步」**无**已交付功能的复述
- [ ] DECISIONS 条数可控，且无「已被代码推翻」的约束
- [ ] todo 仅含**本周**任务块
- [ ] `archive_harness_todo.py` 已跑（或等价手工归档）
- [ ] `sync_progress.py` 已跑，门禁全绿

---

## 结合项目现状（必做判断）

归档不只是「剪切粘贴」，须对照**当前**仓库与运行态：

| 检查 | 怎么做 |
|------|--------|
| 技术债仍成立？ | deferred / observe 对照 `src/`、单测、[DECISIONS.md](../DECISIONS.md)、项目对接文档（如 `docs/api_*.md`） |
| 决策仍约束实现？ | 已在代码 / 文档落地的，重复决策合并或归档 |
| Plan 仍待做？ | 「待用户确认」超过 30 天 → 对话向用户确认 |
| 部署 / DDL 缺口 | 仍阻塞则留在 PROGRESS「当前状态」；已做完则删 |
| 联调/部署假设 | 文档中的假设是否与现网、上游一致 |

可选：Task **explore** 分模块扫 `src/`，只回报与 harness **矛盾**处，勿通读大 diff。

---

## 不要做什么

- **不要**删 `code_review/*.md`、`plans/*.md` 正文（只动索引与 open-findings 主表）。
- **不要**把已关闭项抄回 PROGRESS 或 todo。
- **不要**在周回顾回合改 `src/`（除非用户明确另开 task）。
- **不要**用脚本批量改文案代替上表判断——`archive_harness_todo.py` / `sync_progress.py` 仅负责 todo 周界与 PROGRESS 机械章节。
