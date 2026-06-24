# 评分脚本配方

`harness/goal/score.py` 必须输出 JSON：

```json
{
  "score": 72,
  "max": 100,
  "components": {
    "tests": {"score": 50, "max": 50, "passed": 120, "failed": 0}
  }
}
```

## 配方速查

| 领域 | 主指标 | 实现提示 |
|------|--------|----------|
| 测试覆盖率 | `pytest --cov` 行覆盖率 | `coverage json` + 读 `totals.percent_covered` |
| 项目健康 | 测试 + lint + 依赖 + 文档 | 见 `assets/score.py.template` |
| API 契约 | 路由 vs OpenAPI/文档字段匹配 | 自定义 checker，按端点计分 |
| 文档质量 | 链接检查 + 示例可运行 + 术语一致 | 多 component 加权；考虑 **双分**（文档分 + 工具分） |
| 性能 | p95 延迟 / 吞吐 | `wrk`/`k6` 输出解析；Continuous 模式 |
| 技术债 | ruff + mypy error 数 | `max(0, max - errors)` |

## 双分模式（Split 推荐）

当 Agent 需要 **先修测量工具** 再修被测对象时：

```json
{
  "score": 65,
  "max": 100,
  "instrument_score": 40,
  "instrument_max": 50,
  "components": { ... }
}
```

在 `harness/goal/GOAL.md` 写明：**instrument 分低于 80% 时，不得为了抬主分而改被测内容去迎合坏掉的 linter**。

## 实现原则

1. **快** — 默认门禁 <2 分钟；慢指标拆到单独 marker
2. **确定性** — 同一代码库连续两次运行分数一致
3. **可分解** — 返回 `components`，方便找最弱项
4. **防刷分** — 不把「删除代码」算作覆盖率提升 unless 明确在 Action Catalog 中

## Python 脚本骨架

从 `assets/score.py.template` 复制。核心结构：

```python
def compute_score() -> dict:
    components = {
        "tests": score_tests(),
        "lint": score_lint(),
    }
    return {
        "score": sum(c["score"] for c in components.values()),
        "max": sum(c["max"] for c in components.values()),
        "components": components,
    }
```

## 集成测试分轨

与 img_flow 类似：默认 `pytest.ini` 排除 `integration`，评分只跑单元门禁；Phase-2 GOAL 可对 `-m integration` 单独打分。
