---
name: python-testing-patterns
description: 使用 pytest、fixtures、mock 和测试驱动开发实现全面的测试策略。适用于编写 Python 测试、搭建测试套件或落实测试最佳实践。
---

# Python 测试模式

使用 pytest、fixtures、mock、参数化以及测试驱动开发实践，在 Python 中实现稳健测试策略的全面指南。

## 何时使用本技能

- 为 Python 代码编写单元测试
- 对照 `harness/todo.md` 中的 AC 编写验收级测试（可放在 `tests/acceptance/`）
- 搭建测试套件与测试基础设施
- 实施测试驱动开发（TDD）
- 为 API 与服务创建集成测试
- Mock 外部依赖与服务
- 测试异步代码与并发操作
- 在 CI/CD 中配置持续测试
- 实施基于属性的测试
- 测试数据库操作
- 调试失败的测试

## 核心概念

### 1. 测试类型

- **单元测试**：在隔离环境中测试单个函数/类
- **集成测试**：测试组件之间的交互
- **功能测试**：端到端测试完整功能
- **性能测试**：衡量速度与资源占用

### 2. 测试结构（AAA 模式）

- **Arrange（准备）**：设置测试数据与前置条件
- **Act（执行）**：运行被测代码
- **Assert（断言）**：验证结果

### 3. 测试覆盖率

- 衡量测试实际执行了哪些代码
- 识别未覆盖的代码路径
- 追求有意义的覆盖率，而非单纯追求高百分比

### 4. 测试隔离

- 测试应相互独立
- 测试之间不应共享状态
- 每个测试应自行清理

## 快速入门

```python
# test_example.py
def add(a, b):
    return a + b

def test_add():
    """基础测试示例。"""
    result = add(2, 3)
    assert result == 5

def test_add_negative():
    """使用负数进行测试。"""
    assert add(-1, 1) == 0

# 运行：pytest test_example.py
```

## 详细模式与示例

详细模式文档位于 `references/details.md`。当上文导航层级不足以解决问题时，请阅读该文件。

## 测试最佳实践

### 测试组织

```python
# tests/
#   __init__.py
#   conftest.py           # 共享 fixtures
#   test_unit/            # 单元测试
#     test_models.py
#     test_utils.py
#   test_integration/     # 集成测试
#     test_api.py
#     test_database.py
#   test_e2e/            # 端到端测试
#     test_workflows.py
```

### 测试命名约定

常见模式：`test_<单元>_<场景>_<预期结果>`。请根据团队偏好调整。

```python
# 模式：test_<单元>_<场景>_<预期>
def test_create_user_with_valid_data_returns_user():
    ...

def test_create_user_with_duplicate_email_raises_conflict():
    ...

def test_get_user_with_unknown_id_returns_none():
    ...

# 良好的测试名——清晰且具描述性
def test_user_creation_with_valid_data():
    """名称清楚说明被测内容。"""
    pass

def test_login_fails_with_invalid_password():
    """名称描述预期行为。"""
    pass

def test_api_returns_404_for_missing_resource():
    """明确输入与预期结果。"""
    pass

# 糟糕的测试名——应避免
def test_1():  # 缺乏描述性
    pass

def test_user():  # 过于笼统
    pass

def test_function():  # 未说明测什么
    pass
```

### 测试重试行为

使用 mock 的 side_effect 验证重试逻辑是否正确。

```python
from unittest.mock import Mock

def test_retries_on_transient_error():
    """测试服务在瞬时故障时会重试。"""
    client = Mock()
    # 失败两次后成功
    client.request.side_effect = [
        ConnectionError("Failed"),
        ConnectionError("Failed"),
        {"status": "ok"},
    ]

    service = ServiceWithRetry(client, max_retries=3)
    result = service.fetch()

    assert result == {"status": "ok"}
    assert client.request.call_count == 3

def test_gives_up_after_max_retries():
    """测试达到最大重试次数后停止重试。"""
    client = Mock()
    client.request.side_effect = ConnectionError("Failed")

    service = ServiceWithRetry(client, max_retries=3)

    with pytest.raises(ConnectionError):
        service.fetch()

    assert client.request.call_count == 3

def test_does_not_retry_on_permanent_error():
    """测试永久性错误不会触发重试。"""
    client = Mock()
    client.request.side_effect = ValueError("Invalid input")

    service = ServiceWithRetry(client, max_retries=3)

    with pytest.raises(ValueError):
        service.fetch()

    # 仅调用一次——ValueError 不重试
    assert client.request.call_count == 1
```

### 使用 Freezegun Mock 时间

在测试中使用 freezegun 控制时间，使依赖时间的行为可预测。

```python
from freezegun import freeze_time
from datetime import datetime, timedelta

@freeze_time("2026-01-15 10:00:00")
def test_token_expiry():
    """测试令牌在正确时间过期。"""
    token = create_token(expires_in_seconds=3600)
    assert token.expires_at == datetime(2026, 1, 15, 11, 0, 0)

@freeze_time("2026-01-15 10:00:00")
def test_is_expired_returns_false_before_expiry():
    """测试有效期内令牌未过期。"""
    token = create_token(expires_in_seconds=3600)
    assert not token.is_expired()

@freeze_time("2026-01-15 12:00:00")
def test_is_expired_returns_true_after_expiry():
    """测试超过有效期后令牌已过期。"""
    token = Token(expires_at=datetime(2026, 1, 15, 11, 30, 0))
    assert token.is_expired()

def test_with_time_travel():
    """使用 freeze_time 上下文测试跨时间行为。"""
    with freeze_time("2026-01-01") as frozen_time:
        item = create_item()
        assert item.created_at == datetime(2026, 1, 1)

        # 时间向前推进
        frozen_time.move_to("2026-01-15")
        assert item.age_days == 14
```

### 测试标记

```python
# test_markers.py
import pytest

@pytest.mark.slow
def test_slow_operation():
    """标记慢速测试。"""
    import time
    time.sleep(2)


@pytest.mark.integration
def test_database_integration():
    """标记集成测试。"""
    pass


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """临时跳过测试。"""
    pass


@pytest.mark.skipif(os.name == "nt", reason="Unix only test")
def test_unix_specific():
    """条件跳过。"""
    pass


@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    """标记预期失败。"""
    assert False


# 运行示例：
# pytest -m slow          # 仅运行慢速测试
# pytest -m "not slow"    # 跳过慢速测试
# pytest -m integration   # 运行集成测试
```

### 覆盖率报告

```bash
# 安装 coverage
pip install pytest-cov

# 带覆盖率运行测试
pytest --cov=myapp tests/

# 生成 HTML 报告
pytest --cov=myapp --cov-report=html tests/

# 覆盖率低于阈值时失败
pytest --cov=myapp --cov-fail-under=80 tests/

# 显示未覆盖行
pytest --cov=myapp --cov-report=term-missing tests/
```

高级模式（异步测试、monkeypatch、基于属性的测试、数据库测试、CI/CD 集成与配置）请参阅 [references/advanced-patterns.md](references/advanced-patterns.md)
