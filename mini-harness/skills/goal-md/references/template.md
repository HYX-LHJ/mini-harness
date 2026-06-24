# GOAL.md 模板

复制到 `harness/goal/GOAL.md`（推荐用 `init_goal.py` 脚手架）并填写 `[]` 占位符。

目录索引见 [harness/goal/index.md](../../../assets/harness-template/harness/goal/index.md)（install 后位于 `harness/goal/index.md`）。

## Fitness Function

```bash
python harness/goal/score.py           # 人类可读
python harness/goal/score.py --json    # 机器可读
```

（其余章节结构与 `assets/GOAL.template.md` 相同；路径均相对于 `harness/goal/`。）

## File Map

| File | Role | Editable? |
|------|------|-----------|
| `harness/goal/score.py` | Fitness function | No (agent) |
| `harness/goal/GOAL.md` | This file | Yes |
| `harness/goal/iterations.jsonl` | Iteration log | Append only |
| `harness/goal/index.md` | Directory index | Yes |
