# Python 测试模式 — 高级参考

高级测试模式，涵盖异步代码、monkeypatch、临时文件、conftest 配置、基于属性的测试、数据库测试、CI/CD 集成与配置。

## 模式 6：测试异步代码

```python
# test_async.py
import pytest
import asyncio

async def fetch_data(url: str) -> dict:
    """异步获取数据。"""
    await asyncio.sleep(0.1)
    return {"url": url, "data": "result"}


@pytest.mark.asyncio
async def test_fetch_data():
    """测试异步函数。"""
    result = await fetch_data("https://api.example.com")
    assert result["url"] == "https://api.example.com"
    assert "data" in result


@pytest.mark.asyncio
async def test_concurrent_fetches():
    """测试并发异步操作。"""
    urls = ["url1", "url2", "url3"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

    assert len(results) == 3
    assert all("data" in r for r in results)


@pytest.fixture
async def async_client():
    """异步 fixture。"""
    client = {"connected": True}
    yield client
    client["connected"] = False


@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    """使用异步 fixture 进行测试。"""
    assert async_client["connected"] is True
```

## 模式 7：使用 Monkeypatch 进行测试

```python
# test_environment.py
import os
import pytest

def get_database_url() -> str:
    """从环境变量获取数据库 URL。"""
    return os.environ.get("DATABASE_URL", "sqlite:///:memory:")


def test_database_url_default():
    """测试默认数据库 URL。"""
    # 若已设置，将使用实际环境变量
    url = get_database_url()
    assert url


def test_database_url_custom(monkeypatch):
    """使用 monkeypatch 测试自定义数据库 URL。"""
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    assert get_database_url() == "postgresql://localhost/test"


def test_database_url_not_set(monkeypatch):
    """测试未设置环境变量时。"""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_database_url() == "sqlite:///:memory:"


class Config:
    """配置类。"""

    def __init__(self):
        self.api_key = "production-key"

    def get_api_key(self):
        return self.api_key


def test_monkeypatch_attribute(monkeypatch):
    """测试 monkeypatch 对象属性。"""
    config = Config()
    monkeypatch.setattr(config, "api_key", "test-key")
    assert config.get_api_key() == "test-key"
```

## 模式 8：临时文件与目录

```python
# test_file_operations.py
import pytest
from pathlib import Path

def save_data(filepath: Path, data: str):
    """将数据保存到文件。"""
    filepath.write_text(data)


def load_data(filepath: Path) -> str:
    """从文件加载数据。"""
    return filepath.read_text()


def test_file_operations(tmp_path):
    """使用临时目录测试文件操作。"""
    # tmp_path 是 pathlib.Path 对象
    test_file = tmp_path / "test_data.txt"

    # 保存数据
    save_data(test_file, "Hello, World!")

    # 验证文件存在
    assert test_file.exists()

    # 加载并验证数据
    data = load_data(test_file)
    assert data == "Hello, World!"


def test_multiple_files(tmp_path):
    """使用多个临时文件进行测试。"""
    files = {
        "file1.txt": "Content 1",
        "file2.txt": "Content 2",
        "file3.txt": "Content 3"
    }

    for filename, content in files.items():
        filepath = tmp_path / filename
        save_data(filepath, content)

    # 验证所有文件已创建
    assert len(list(tmp_path.iterdir())) == 3

    # 验证内容
    for filename, expected_content in files.items():
        filepath = tmp_path / filename
        assert load_data(filepath) == expected_content
```

## 模式 9：自定义 Fixtures 与 Conftest

```python
# conftest.py
"""所有测试的共享 fixtures。"""
import pytest

@pytest.fixture(scope="session")
def database_url():
    """为所有测试提供数据库 URL。"""
    return "postgresql://localhost/test_db"


@pytest.fixture(autouse=True)
def reset_database(database_url):
    """每个测试前自动运行的 fixture。"""
    # Setup：清空数据库
    print(f"Clearing database: {database_url}")
    yield
    # Teardown：清理
    print("Test completed")


@pytest.fixture
def sample_user():
    """提供示例用户数据。"""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }


@pytest.fixture
def sample_users():
    """提供示例用户列表。"""
    return [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"},
        {"id": 3, "name": "User 3"},
    ]


# 参数化 fixture
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def db_backend(request):
    """使用不同数据库后端运行测试的 fixture。"""
    return request.param


def test_with_db_backend(db_backend):
    """该测试将使用不同后端运行 3 次。"""
    print(f"Testing with {db_backend}")
    assert db_backend in ["sqlite", "postgresql", "mysql"]
```

## 模式 10：基于属性的测试

```python
# test_properties.py
from hypothesis import given, strategies as st
import pytest

def reverse_string(s: str) -> str:
    """反转字符串。"""
    return s[::-1]


@given(st.text())
def test_reverse_twice_is_original(s):
    """属性：反转两次得到原字符串。"""
    assert reverse_string(reverse_string(s)) == s


@given(st.text())
def test_reverse_length(s):
    """属性：反转后长度不变。"""
    assert len(reverse_string(s)) == len(s)


@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """属性：加法满足交换律。"""
    assert a + b == b + a


@given(st.lists(st.integers()))
def test_sorted_list_properties(lst):
    """属性：排序后的列表有序。"""
    sorted_lst = sorted(lst)

    # 长度相同
    assert len(sorted_lst) == len(lst)

    # 元素齐全
    assert set(sorted_lst) == set(lst)

    # 已排序
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
```

## 测试数据库代码

```python
# test_database_models.py
import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()


class User(Base):
    """用户模型。"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """创建用于测试的内存数据库。"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()


def test_create_user(db_session):
    """测试创建用户。"""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.name == "Test User"


def test_query_user(db_session):
    """测试查询用户。"""
    user1 = User(name="User 1", email="user1@example.com")
    user2 = User(name="User 2", email="user2@example.com")

    db_session.add_all([user1, user2])
    db_session.commit()

    users = db_session.query(User).all()
    assert len(users) == 2


def test_unique_email_constraint(db_session):
    """测试邮箱唯一约束。"""
    from sqlalchemy.exc import IntegrityError

    user1 = User(name="User 1", email="same@example.com")
    user2 = User(name="User 2", email="same@example.com")

    db_session.add(user1)
    db_session.commit()

    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

## CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov=myapp --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## 配置文件

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=myapp
    --cov-report=term-missing
markers =
    slow: marks tests as slow
    integration: marks integration tests
    unit: marks unit tests
    e2e: marks end-to-end tests
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "-v",
    "--cov=myapp",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["myapp"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```
