# python-testing-patterns — 详细模式与示例

## 基础模式

### 模式 1：基础 pytest 测试

```python
# test_calculator.py
import pytest

class Calculator:
    """用于测试的简单计算器。"""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def test_addition():
    """测试加法。"""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0


def test_subtraction():
    """测试减法。"""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 5) == -5


def test_multiplication():
    """测试乘法。"""
    calc = Calculator()
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(0, 5) == 0


def test_division():
    """测试除法。"""
    calc = Calculator()
    assert calc.divide(6, 3) == 2
    assert calc.divide(5, 2) == 2.5


def test_division_by_zero():
    """测试除以零时抛出错误。"""
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(5, 0)
```

### 模式 2：用于 Setup 与 Teardown 的 Fixtures

```python
# test_database.py
import pytest
from typing import Generator

class Database:
    """简单数据库类。"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

    def connect(self):
        """连接数据库。"""
        self.connected = True

    def disconnect(self):
        """断开数据库连接。"""
        self.connected = False

    def query(self, sql: str) -> list:
        """执行查询。"""
        if not self.connected:
            raise RuntimeError("Not connected")
        return [{"id": 1, "name": "Test"}]


@pytest.fixture
def db() -> Generator[Database, None, None]:
    """提供已连接数据库的 fixture。"""
    # Setup
    database = Database("sqlite:///:memory:")
    database.connect()

    # 提供给测试
    yield database

    # Teardown
    database.disconnect()


def test_database_query(db):
    """使用 fixture 测试数据库查询。"""
    results = db.query("SELECT * FROM users")
    assert len(results) == 1
    assert results[0]["name"] == "Test"


@pytest.fixture(scope="session")
def app_config():
    """会话级 fixture——每个测试会话创建一次。"""
    return {
        "database_url": "postgresql://localhost/test",
        "api_key": "test-key",
        "debug": True
    }


@pytest.fixture(scope="module")
def api_client(app_config):
    """模块级 fixture——每个测试模块创建一次。"""
    # 设置昂贵资源
    client = {"config": app_config, "session": "active"}
    yield client
    # 清理
    client["session"] = "closed"


def test_api_client(api_client):
    """使用 api client fixture 进行测试。"""
    assert api_client["session"] == "active"
    assert api_client["config"]["debug"] is True
```

### 模式 3：参数化测试

```python
# test_validation.py
import pytest

def is_valid_email(email: str) -> bool:
    """检查邮箱是否有效。"""
    return "@" in email and "." in email.split("@")[1]


@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("test.user@domain.co.uk", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@domain", False),
    ("", False),
])
def test_email_validation(email, expected):
    """使用多种输入测试邮箱校验。"""
    assert is_valid_email(email) == expected


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -5, -10),
])
def test_addition_parameterized(a, b, expected):
    """使用多组参数测试加法。"""
    from test_calculator import Calculator
    calc = Calculator()
    assert calc.add(a, b) == expected


# 使用 pytest.param 处理特殊情况
@pytest.mark.parametrize("value,expected", [
    pytest.param(1, True, id="positive"),
    pytest.param(0, False, id="zero"),
    pytest.param(-1, False, id="negative"),
])
def test_is_positive(value, expected):
    """使用自定义测试 ID。"""
    assert (value > 0) == expected
```

### 模式 4：使用 unittest.mock 进行 Mock

```python
# test_api_client.py
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

class APIClient:
    """简单 API 客户端。"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_user(self, user_id: int) -> dict:
        """从 API 获取用户。"""
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, data: dict) -> dict:
        """创建新用户。"""
        response = requests.post(f"{self.base_url}/users", json=data)
        response.raise_for_status()
        return response.json()


def test_get_user_success():
    """使用 mock 测试成功的 API 调用。"""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        user = client.get_user(1)

        assert user["id"] == 1
        assert user["name"] == "John Doe"
        mock_get.assert_called_once_with("https://api.example.com/users/1")


def test_get_user_not_found():
    """测试 404 错误的 API 调用。"""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            client.get_user(999)


@patch("requests.post")
def test_create_user(mock_post):
    """使用装饰器语法测试用户创建。"""
    client = APIClient("https://api.example.com")

    mock_post.return_value.json.return_value = {"id": 2, "name": "Jane Doe"}
    mock_post.return_value.raise_for_status.return_value = None

    user_data = {"name": "Jane Doe", "email": "jane@example.com"}
    result = client.create_user(user_data)

    assert result["id"] == 2
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args.kwargs["json"] == user_data
```

### 模式 5：测试异常

```python
# test_exceptions.py
import pytest

def divide(a: float, b: float) -> float:
    """将 a 除以 b。"""
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a / b


def test_zero_division():
    """测试除以零时抛出异常。"""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_zero_division_with_message():
    """测试异常消息。"""
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        divide(5, 0)


def test_type_error():
    """测试类型错误异常。"""
    with pytest.raises(TypeError, match="must be numbers"):
        divide("10", 5)


def test_exception_info():
    """测试访问异常信息。"""
    with pytest.raises(ValueError) as exc_info:
        int("not a number")

    assert "invalid literal" in str(exc_info.value)
```

高级模式（异步测试、monkeypatch、临时文件、conftest 配置、基于属性的测试、数据库测试、CI/CD 集成与配置文件）请参阅 [advanced-patterns.md](advanced-patterns.md)

## 测试设计原则

### 每个测试只验证一种行为

每个测试应只验证一种行为，便于定位失败原因并维护测试。

```python
# 不好——测试多种行为
def test_user_service():
    user = service.create_user(data)
    assert user.id is not None
    assert user.email == data["email"]
    updated = service.update_user(user.id, {"name": "New"})
    assert updated.name == "New"

# 好——聚焦的测试
def test_create_user_assigns_id():
    user = service.create_user(data)
    assert user.id is not None

def test_create_user_stores_email():
    user = service.create_user(data)
    assert user.email == data["email"]

def test_update_user_changes_name():
    user = service.create_user(data)
    updated = service.update_user(user.id, {"name": "New"})
    assert updated.name == "New"
```

### 测试错误路径

除正常路径外，务必测试失败场景。

```python
def test_get_user_raises_not_found():
    with pytest.raises(UserNotFoundError) as exc_info:
        service.get_user("nonexistent-id")

    assert "nonexistent-id" in str(exc_info.value)

def test_create_user_rejects_invalid_email():
    with pytest.raises(ValueError, match="Invalid email format"):
        service.create_user({"email": "not-an-email"})
```
