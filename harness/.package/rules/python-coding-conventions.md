# Python 代码规范

通用 Python 编码约定，适用于任意 Python 项目；不含具体仓库路径或业务域。

## 适用范围

- 仓库内 Python **运行时代码**与**测试代码**（具体目录由项目自行约定）。

---

## 1. 命名规范

| 类别 | 风格 | 示例 |
|------|------|------|
| 变量、函数 | `snake_case` | `user_name`、`generate_prompt()` |
| 类名 | `PascalCase` | `PromptEngine` |
| 常量 | `UPPER_CASE` | `MAX_RETRY` |
| 布尔变量/属性 | `is_` / `has_` / `can_` 前缀 | `is_ready`、`has_token`、`can_retry` |

```python
user_name = "alex"


def generate_prompt():
    pass


class PromptEngine:
    pass


MAX_RETRY = 3
```

---

## 2. 换行

长参数列表使用 **括号换行**，不使用行尾 `\` 续行。

```python
# 不推荐
result = generate(model=model, messages=messages, temperature=0.7, max_tokens=4096)

# 推荐
result = generate(
    model=model,
    messages=messages,
)
```

---

## 3. 注释规范

注释应解释 **「为什么」**，而不是复述 **「做什么」**。

```python
# 错误：重复代码语义
# 给 user_id 赋值
user_id = payload["user_id"]

# 正确：说明业务或兼容性原因
# 外部接口在部分场景下可能缺失 user_id，需走兜底查询
user_id = payload.get("user_id") or lookup_user_id(payload)
```

---

## 4. Docstring

**公共**函数、类、模块必须编写 docstring，且须写清**本函数**的输入、输出约定，并给出**可复制的调用示例**（输入 → 输出）。

- 一句话说明职责（做什么）。
- **输入**：参数含义、类型、合法取值或边界（可与签名类型注解呼应）。
- **输出**：返回值含义、类型、关键字段；失败时抛何种异常或返回何种哨兵值。
- **示例**：至少一组典型 `输入 → 输出`（doctest 或注释块均可）；有副作用或异步时注明。

```python
def parse_text(text: str) -> dict[str, str | None]:
    """从文本中提取结构化字段。

    Args:
        text: 原始全文；空字符串视为无内容。

    Returns:
        字段字典；无法识别时对应值为 ``None``。

    Raises:
        ValueError: ``text`` 非 ``str`` 时。

    Examples:
        >>> parse_text("name: Alice\\nemail: a@b.com")
        {'name': 'Alice', 'email': 'a@b.com'}

        >>> parse_text("")
        {'name': None, 'email': None}
    """
    ...
```

```python
# 错误：只有一句话，看不出入参/出参
def parse_text(text: str) -> dict:
    """解析文本。"""
    ...
```

---

## 5. 复杂数据结构

模块边界上的复杂结构优先用 `TypedDict` 或 Pydantic `BaseModel` 等明确 schema，避免裸 `dict` / `Any` 传递未文档化的字段。

---

## 6. 异常处理

- **不要**吞掉异常（空 `pass` 或仅 `return` 而无日志、重抛或转换为明确的业务异常）。

```python
# 错误
try:
    data = parse_payload(raw)
except ValueError:
    pass

# 正确
try:
    data = parse_payload(raw)
except ValueError:
    logger.error("解析失败")
    raise
```

---

## 7. 日志规范

- 使用标准库 **`logging`**，**不用** `print` 作为运行期日志。
- 异常场景用 `logger.exception(...)` 保留堆栈。

```python
import logging

logger = logging.getLogger(__name__)

logger.info("开始执行")
logger.exception("执行失败")
```

---

## 8. 函数设计

- **单一职责**：一个函数只做一件事。
- **控制长度**：逻辑超过 **80 行** 应考虑拆分为私有函数或独立模块。
- 复杂分支优先 **早返回**，减少深层嵌套。
