---
name: goal-md
description: >-
  为复杂、长时间运行的优化任务构造 GOAL.md（适应度函数 + 改进循环 + 行动清单）。
  当任务没有单一「完成」标准、需要 Agent 自主多轮迭代、用户希望「给个数字让它自己跑」、
  或用户提到 GOAL.md、goal-md、自主改进、overnight loop、收敛目标时使用。
  与 mini-harness 的 todo/AC 流程互补：AC 管单次交付，GOAL.md 管可度量的持续改进。
compatibility: 评分脚本需要 Python 3.10+；bash 可选。
---

# GOAL.md 自主改进

将 **「更好」** 从主观感受变成 **可计算分数**，再交给 Agent 在改进循环中自主推进。模式源自 [jmilinovich/goal-md](https://github.com/jmilinovich/goal-md)（Karpathy autoresearch 的泛化）。

**适用**：测试覆盖率拉升、文档质量、性能基线、技术债清理、契约一致性——任何需要先 **造尺子** 再 **优化** 的任务。

**不适用**：单次明确变更（加字段、修 typo）、用户已给出完整 AC 的小功能——走 [using-harness](../using-harness/SKILL.md) 常规范式即可。

## 与 mini-harness 的关系

| 维度 | 常规 harness（todo + AC） | GOAL.md 模式 |
|------|---------------------------|--------------|
| 完成标准 | 用户确认的 AC 勾选 | 适应度函数分数 + 停止条件 |
| 迭代记录 | `harness/todo.md`、`PROGRESS.md` | `harness/goal/iterations.jsonl`（追加）+ 可选同步 `PROGRESS.md` |
| 状态目录 | `harness/` 各索引子目录 | `harness/goal/`（见 `index.md`） |
| 测试策略 | TDD subagent 先行 | 评分脚本门禁 + 针对性补测 |
| 停止 | AC 全绿 | 收敛阈值 / 停滞 / 最大轮次 |

二者可并存：在 `harness/todo.md` 登记元任务「执行 `harness/goal/GOAL.md`：xxx」；规格与迭代落在 `harness/goal/`（**不得**放到仓库根或其它目录）。

**前置**：须已 `install` harness；`init_goal.py` 在 `harness/goal/` 脚手架。

## 快速启动

### 1. 判断任务类型

满足 **任一** 即启用本 Skill：

- 用户说「让它自己跑到 XX 分」「overnight」「多轮改进」
- 成功标准需 **构造指标**（无现成 `pytest --cov` 式标量）
- 预估 **>3 轮** 才能收敛，且每轮可独立验证

### 2. 脚手架

路径因宿主上下文而异：

| 上下文 | `init_goal.py` 路径 |
|--------|---------------------|
| 目标仓库已 `install` | `harness/skills/goal-md/scripts/init_goal.py` |
| 仅安装插件（未 `install`） | `skills/goal-md/scripts/init_goal.py`（插件根目录） |
| 本 monorepo 维护者 | `mini-harness/skills/goal-md/scripts/init_goal.py` |

```bash
# 示例（目标仓库已 install）
python harness/skills/goal-md/scripts/init_goal.py --name "提升测试覆盖率到 90%"
```

生成于 **`harness/goal/`**：`index.md`、`GOAL.md`、`score.py`、`iterations.jsonl`（空）。`harness/index.md` 已含 `goal/` 入口。

### 3. 定制适应度函数

编辑 `harness/goal/score.py` 中的 `REQUIRED_*` 与 `score_*()` 函数。必须：

- 可重复运行、确定性、通常 **<2 分钟**
- 支持 `--json` 输出 `{"score": N, "max": M, "components": {...}}`
- 文档写在 `harness/goal/GOAL.md` 的 Metric Definition 节

评分配方见 [references/scoring-recipes.md](references/scoring-recipes.md)。

### 4. 填写 GOAL.md 五要素

按 [references/template.md](references/template.md) 填写：

1. **Fitness function** — `harness/goal/score.py`
2. **Improvement loop** — 测量 → 诊断最弱项 → 行动 → 验证 → 保留或回滚
3. **Action catalog** — 按影响力排序的具体动作表
4. **Operating mode** — Converge / Continuous / Supervised
5. **Constraints** — 不可触碰的红线（密钥、删测试、改评分脚本等）

### 5. 执行改进循环

```
repeat:
  0. 读 harness/goal/iterations.jsonl — 避免重复失败实验
  1. python harness/goal/score.py --json  → before
  2. 找最弱 component
  3. 从 Action Catalog 选最高影响动作
  4. 实现变更
  5. 快速验证（如 pytest -q 相关子集）
  6. python harness/goal/score.py --json  → after
  7. 分数上升 → 原子 commit；否则 revert
  8. 追加 harness/goal/iterations.jsonl 一行
  9. 检查停止条件
```

提交信息：`[G:72→85] component: 简述`

### 6. 收敛报告

循环结束时更新 `harness/goal/GOAL.md` 底部 **When to Stop** 块，并刷新 `harness/PROGRESS.md`。

## 运行模式

| 模式 | 何时用 | 停止 |
|------|--------|------|
| **Converge** | 有明确目标分或组件阈值 | 达标、停滞、达最大轮次 |
| **Continuous** | 用户离开、希望持续打磨 | 人工中断 |
| **Supervised** | 高风险变更、早期不信任 | 每 N 轮或触及 File Map 中敏感路径时暂停 |

详见 [references/operating-modes.md](references/operating-modes.md)。

## 指标可变性（Metric Mutability）

| 模式 | Agent 权限 |
|------|------------|
| **Locked** | 不能改评分脚本 |
| **Split** | 可改测量工具，不能改「好」的定义 |
| **Open** | 可改一切（早期探索用） |

默认推荐 **Split**：防止 Agent 通过改尺子刷分。

## mini-harness 集成清单

启用 GOAL.md 时：

- [ ] `harness/todo.md` 登记元任务并链向 `harness/goal/GOAL.md`
- [ ] **不要** 为每轮迭代重写 AC——用 `harness/goal/iterations.jsonl`
- [ ] 每轮仍遵守 Constraints（不提交 `.env`、不删测试刷分）
- [ ] 涉及运行时代码变更时，补或修 `tests/` 后再计分
- [ ] 本地门禁失败时 **不得** 声称分数提升
- [ ] 收敛后走常规 `acceptance-verification`（若用户要交付）

细则见 [references/harness-integration.md](references/harness-integration.md)。

## 硬约束

1. **分数只来自评分脚本** — 禁止手写或估算
2. **每轮原子 commit** — 便于 `git revert`
3. **分数下降必须回滚** — 不得带回归进入下一轮
4. **禁止刷分** — 不删测试、不 `# noqa` 堆叠、不弱化 `harness/goal/score.py`（除非 Open 模式且用户批准）
5. **`harness/goal/iterations.jsonl` 只追加** — 不删历史
6. **产物只在 `harness/goal/`** — 不得写到仓库根或其它目录

## 参考

| 文档 | 内容 |
|------|------|
| [references/template.md](references/template.md) | GOAL.md 全文模板 |
| [references/scoring-recipes.md](references/scoring-recipes.md) | 常见领域评分配方 |
| [references/operating-modes.md](references/operating-modes.md) | 三种运行模式 |
| [references/harness-integration.md](references/harness-integration.md) | 与 todo/AC/subagent 协作 |
| [references/examples.md](references/examples.md) | 上游与通用评分配方实例 |

## 工具脚本

| 脚本 | 用途 |
|------|------|
| `scripts/init_goal.py` | 初始化 `harness/goal/`（index、GOAL、score、iterations） |
| `assets/score.py.template` | 通用评分脚本起点 |
| `assets/GOAL.template.md` | GOAL.md 起点 |
