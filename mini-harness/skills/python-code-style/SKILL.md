---
name: python-code-style
description: 仅 harness/Python 项目初始化一次。配置 pyproject.toml、Ruff、pytest、mypy 与 commands.gate。用户说初始化 harness、配门禁、setup ruff pytest 且尚无 gate 时用。日常写代码、TDD、review、提交时禁止读本 Skill。
---

# 🐍 Python 工具链初始化（仅一次）

**读一次就够。** 日常开发走 `using-harness` + `tdd`，不要反复打开本 Skill。

| 负责 | 不负责 |
|------|--------|
| `pyproject.toml`、Ruff、pytest、mypy | 命名、docstring、编码风格（项目自定） |
| `commands.gate` 登记 | 往 `DECISIONS.md` 写工具链摘要 |

权威来源：`pyproject.toml` + `commands.gate`。可选在 `profile/PROJECT.md`「本地门禁」引用相同命令。

---

## 目标

1. 🔍 发现现状（Python 版本、已有配置、目录、包管理）
2. ⚙️ 补齐 `pyproject.toml`
3. 📋 写入 `commands.gate`
4. ✅ 跑通门禁，遗留记入 `PROGRESS.md`

未经授权不装依赖、不大规模自动修复。

---

## 步骤

### 1️⃣ 发现

查：`pyproject.toml`、ruff/mypy/pytest 配置、源码与 `tests/` 路径、setuptools/hatch/poetry 等。

`commands.gate` 为空 → 提议最小门禁并写入。

### 2️⃣ 配置工具

| 工具 | 位置 | 要点 |
|------|------|------|
| 元数据 | `[project]` | `requires-python`、dev 依赖 |
| Ruff | `[tool.ruff]` | 版本、行宽、`src`、规则集 |
| pytest | `[tool.pytest.ini_options]` | `testpaths` |
| mypy | `[tool.mypy]` | 范围、严格度、stub override |

默认用 **mypy**；仓库已用 pyright → 沿用并在 `PROJECT.md` 注明。

缺 stub → `[[tool.mypy.overrides]]`，勿全局关类型检查。

### 3️⃣ 登记 gate

```json
{
  "commands": {
    "gate": [
      "ruff check src tests",
      "ruff format --check src tests",
      "mypy src",
      "pytest -q"
    ]
  }
}
```

可选同步到 `profile/PROJECT.md`「本地门禁」。

### 4️⃣ 验证

按 gate 顺序执行；失败项记入 `PROGRESS.md`「已知问题」。

---

## 兜底默认值（仅无配置时）

- Ruff：行宽 100，E/F/I/UP/B
- mypy：`check_untyped_defs = true` + per-module override

---

## 边界

| Skill | 关系 |
|-------|------|
| `using-harness` | 先 install；本 Skill 是初始化第 2 步 |
| `tdd` / `python-testing-patterns` | 日常写代码前 |
| `code-review-expert` | 实现后审查 |
