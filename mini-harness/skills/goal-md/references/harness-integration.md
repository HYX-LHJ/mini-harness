# 与 mini-harness 集成

## 何时走 GOAL.md 而非纯 todo/AC

```text
用户请求
  ├─ 范围清晰、一次交付 → using-harness 常规流程
  ├─ 需先探索方案 → brainstorming → todo + AC
  └─ 可度量、多轮、无单一 Done → goal-md（本 Skill）
```

GOAL.md **不替代** AC 核对——它替代的是「每轮都要重写 AC」的摩擦。

**前置**：目标仓库须已 `install` harness；GOAL 产物**只**落在 `harness/goal/`，由 `harness/goal/index.md` 索引（`harness/index.md` 含入口）。

## todo.md 登记示例

```markdown
## 当前任务：GOAL — 项目健康度 95+

- [ ] 阅读并执行 `harness/goal/GOAL.md`
- [ ] 基线：`python harness/goal/score.py`
- [ ] 目标：收敛于 ≥95/100 或 GOAL 停止条件

**说明**：迭代细节见 `harness/goal/iterations.jsonl`，不在此重复 AC。
```

## 文件布局

```text
repo-root/
  harness/
    index.md              # L0 — 含 goal/ 入口
    todo.md               # 元任务指针
    PROGRESS.md           # 收敛后可选快照
    goal/
      index.md            # L1 — GOAL 目录索引
      GOAL.md             # 目标规格
      iterations.jsonl    # 追加日志
      score.py            # 适应度函数
```

已 `install` harness 时，Skill 路径：`harness/skills/goal-md/SKILL.md`。仅插件时：`skills/goal-md/SKILL.md`（插件包根目录）。

## 与 subagent 分工

| 步骤 | 执行方 |
|------|--------|
| 写 `harness/goal/*` | 主 Agent（本 Skill） |
| 改进循环各轮 | 主 Agent 或 Task subagent（用户指定 overnight 时） |
| 大改前补测试 | `tdd` subagent（与常规流程相同） |
| 收敛后交付 | `acceptance-verification` + `code-review-expert` |

**不要** 每轮都启动全套 subagent——会拖慢循环。仅在触及运行时代码且缺测试时调 TDD。

## PROGRESS.md 同步

每收敛或每 5 轮，追加：

```markdown
### GOAL.md 快照 (YYYY-MM-DD)

- 分数：72 → 85
- 轮次：3
- 最弱项已处理：lint
- 下一弱项：deps
- 详情：`harness/goal/iterations.jsonl`
```

## 与 DECISIONS.md

长期约束（不可 mock 的 DB、禁止真实 LLM 调用）写入 `harness/DECISIONS.md`，并在 `harness/goal/GOAL.md` Constraints 中 **引用** 而非复制——避免两处漂移。
