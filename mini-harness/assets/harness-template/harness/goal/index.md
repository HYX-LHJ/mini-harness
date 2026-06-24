# GOAL 自主改进

存放 [goal-md](../../skills/goal-md/SKILL.md) 模式的多轮可度量优化状态。须先 `install` harness，再由 `init_goal.py` 脚手架本目录。

| 文件 | 用途 |
|------|------|
| [GOAL.md](GOAL.md) | 目标规格（适应度定义、行动清单、约束） |
| [score.py](score.py) | 适应度函数（分数只由此脚本输出） |
| [iterations.jsonl](iterations.jsonl) | 迭代日志（只追加） |

```bash
python harness/goal/score.py
python harness/goal/score.py --json
```

todo 中登记元任务并链向 `GOAL.md`；**不要**每轮重写 AC——迭代细节写入 `iterations.jsonl`。
