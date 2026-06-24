---
name: python-testing-patterns
description: pytest、fixtures、mock、参数化。写 Python 测试、搭 conftest、mock 第三方、测异步/重试、按 todo AC 写 tests/ 时，必须用本 Skill；常与 tdd 一起由 subagent 调用。用户问怎么写 pytest、fixture 怎么设时也用。纯改生产代码且不写测试时不要读。
---

# 🧪 Python 测试模式

pytest、fixtures、mock、参数化与 TDD 实践的速查 + 深度参考。

---

## 何时打开

- 对照 `harness/todo.md` AC 写测试（`tests/` 或 `tests/acceptance/`）
- 搭 `conftest.py`、组织测试目录
- mock 外部服务、测重试/超时/异步
- TDD 红阶段写 failing 测试

---

## 核心概念

| 概念 | 说明 |
|------|------|
| **AAA** | Arrange → Act → Assert |
| **隔离** | 测试互不共享状态 |
| **覆盖率** | 追求有意义的路径，非百分比虚荣 |

测试类型：单元 · 集成 · 端到端 · 性能（按需）

---

## 快速上手

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

```bash
pytest path/to/test_file.py -q
```

---

## 组织建议

```text
tests/
  conftest.py          # 共享 fixtures
  test_unit/
  test_integration/
  test_acceptance/     # 对照 AC（可选）
```

命名：`test_<单元>_<场景>_<预期>` — 读名字就知道测什么。

---

## 常用模式（摘要）

**Mock 重试** — `side_effect` 列表模拟先失败后成功。

**标记** — `@pytest.mark.slow` / `integration` / `skip` / `xfail`。

**覆盖率** — `pytest --cov=pkg --cov-report=term-missing`。

---

## 深度参考

| 文件 | 内容 |
|------|------|
| [references/details.md](references/details.md) | fixtures、参数化、caplog 等 |
| [references/advanced-patterns.md](references/advanced-patterns.md) | 异步、monkeypatch、属性测试、DB、CI |

细节不够时**再读** reference，不要一次全塞进上下文。
