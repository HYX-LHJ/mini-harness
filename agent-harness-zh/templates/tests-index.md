# tests — 单元测试

- 入口：仓库根 [pytest.ini](../../pytest.ini) → 本目录
- 默认门禁：`pytest` 排除 `@pytest.mark.integration` 用例
- **凡改 `{{SRC_DIR}}/` 必须补测**（无例外）；`todo` 登记后**立即**启动 [AGENTS.md](../../AGENTS.md) **tdd** Skill，再改 `{{SRC_DIR}}/`
- 集成测试：在本文件追加 `pytest -m integration …` 说明（非默认门禁）

公共 fixture 见 [conftest.py](conftest.py)（按需创建）。
