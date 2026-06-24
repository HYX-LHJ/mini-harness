# 实例

## 项目健康度（Converge）— 通用模板

fresh `pip install` 后默认 pytest 全绿 + ruff 干净。见 `assets/score.py.template`（tests 50 + lint 25 + deps 15 + docs 10）。

典型流程：

1. `python harness/skills/goal-md/scripts/init_goal.py --name "项目健康度 95+"`（须已 `install`）
2. 定制 `harness/goal/score.py` 的 `LINT_PATHS`、`REQUIRED_DOCS`
3. 改进循环直至达标或停滞

## 测试覆盖率（Converge）

见 [goal-md 上游 api-test-coverage 示例](https://github.com/jmilinovich/goal-md/blob/main/examples/api-test-coverage.md)。

## 文档质量（Split + 双分）

见 [goal-md docs-quality 示例](https://github.com/jmilinovich/goal-md/blob/main/examples/docs-quality.md)。

## Phase-2 建议

1. **集成测试门禁** — `harness/goal/GOAL.md` 新 Section 或 `harness/goal/score_integration.py`
2. **产品需求覆盖** — `docs/product-requirements.md` ↔ tests
3. **API 契约漂移** — OpenAPI ↔ routers

每个 Phase 可在 `harness/goal/GOAL.md` 新 Section，或单独评分脚本置于 `harness/goal/`。
