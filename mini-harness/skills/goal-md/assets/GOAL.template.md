# Goal: {{GOAL_NAME}}

> 由 `goal-md` Skill 脚手架生成于 `harness/goal/`。填写 Metric Definition、Action Catalog、Constraints 后删除本提示。

## Fitness Function

```bash
python harness/goal/score.py
python harness/goal/score.py --json
```

### Metric Definition

```
score = tests + lint + deps + docs   (max 100)
```

| Component | Max | What it measures |
|-----------|-----|------------------|
| **tests** | 50 | Default pytest gate |
| **lint** | 25 | ruff errors (1 pt per error deducted) |
| **deps** | 15 | requirements.txt completeness |
| **docs** | 10 | Required docs exist |

### Metric Mutability

- [x] **Split** — Agent may fix code/tests/deps; must not weaken `harness/goal/score.py`

## Operating Mode

- [x] **Converge**

### Stopping Conditions

Stop when ANY of:

- Score reaches **95/100**
- 5 consecutive iterations with no improvement
- 15 iterations completed

## Bootstrap

1. Install deps and test tools (`pytest`, `ruff`)
2. `python harness/goal/score.py` — record baseline
3. Customize `harness/goal/score.py` REQUIRED_* constants

## Improvement Loop

```
repeat:
  0. Read harness/goal/iterations.jsonl
  1. python harness/goal/score.py --json  → before
  2. Weakest component → Action Catalog
  3. Change → verify → score again
  4. Improved? commit. Else revert.
  5. Append harness/goal/iterations.jsonl
```

Commit messages: `[G:NN→NN] component: summary`

## Action Catalog

### tests (target: 50/50)

| Action | Impact | How |
|--------|--------|-----|
| Fix collection/import errors | high | Install missing deps; fix imports |
| Fix failing unit tests | high | Root cause, no skips |

### lint (target: 25/25)

| Action | Impact | How |
|--------|--------|-----|
| `ruff check --fix` | high | Auto-fix safe rules |

## Constraints

1. Score only from `harness/goal/score.py`
2. No deleting tests to green the gate
3. Atomic commits per iteration
4. Revert on score regression

## File Map

| File | Editable? |
|------|-----------|
| `harness/goal/score.py` | No (agent) |
| `harness/goal/GOAL.md` | Yes |
| `harness/goal/iterations.jsonl` | Append only |
| `harness/goal/index.md` | Yes（索引与说明） |

## When to Stop

```
Starting score:
Ending score:
Iterations:
Changes made:
Remaining gaps:
Next actions:
```
