---
name: python-code-style
description: 仅在仓库初始化 mini-harness 时使用。配置 Python 工具链（pyproject.toml、Ruff、pytest、mypy 等），并将工具链与验证命令摘要写入 harness/DECISIONS.md。不含编码规范；编码规范由独立 Skill 负责。日常开发不要读取本 Skill。
---

# Python 工具链初始化（仅 harness 初始化时）

## 适用范围

**本 Skill 仅在「初始化 mini-harness / 为新仓库启用 harness」时读取一次。**

- **要读**：用户要求初始化 harness，且仓库含 Python 代码（或即将引入）。
- **不要读**：日常改代码、写测试、Code Review、提交前精炼。
- **不负责**：命名、导入风格、docstring、类型注解写法等**编码规范**（由仓库另行提供的编码规范 Skill 负责；若尚未添加，初始化阶段也不要在本 Skill 中代写）。

初始化完成后，工具链的权威来源为 **`pyproject.toml`（及同类配置文件）** 与 **`harness/DECISIONS.md` 中的工具链摘要**。

## 初始化目标

完成一次性的 **Python 工具链** 落地：

1. 发现仓库现状（Python 版本、已有配置、目录布局、依赖方式）；
2. 创建或补齐 `pyproject.toml`（Ruff、pytest、mypy 等 dev 工具配置）；
3. 将**工具链与验证命令**摘要写入 `harness/DECISIONS.md`；
4. 可选：在 `harness/.mini-harness.json` 的 `commands.gate` 中登记验证命令；
5. 运行一次完整验证，确认通过或记录已知遗留项。

未经授权不要安装工具或依赖；不要对无关文件做大规模自动修复。

## 初始化工作流

### 1. 发现现状

确定：

- 支持的 Python 版本；
- 是否已有 `pyproject.toml`、`ruff.toml`、mypy / pyright 配置、pytest 配置；
- 运行时代码目录与测试目录（例如 `agent/`、`tests/`）；
- 包管理方式（setuptools、hatch、poetry 等）。

当 mini-harness 已激活时，验证命令以 `harness/.mini-harness.json` 的 `commands.gate` 或 `harness/DECISIONS.md` 为准；二者皆空则在本 Skill 执行过程中提议最小门禁并写入 `DECISIONS.md`。

### 2. 配置工具

仅在缺少配置或用户明确要求时修改：

| 工具 | 配置位置 | 要点 |
|------|----------|------|
| 项目元数据 | `[project]`、`requires-python`、dev 依赖 | 与仓库实际版本一致 |
| Ruff | `[tool.ruff]` | 目标版本、行宽、`src` 路径、lint 规则集 |
| pytest | `[tool.pytest.ini_options]` | `testpaths`、`pythonpath` |
| mypy | `[tool.mypy]` | 检查范围、Python 版本、严格度、第三方 stub override |

变更须最小化，并说明对现有代码的影响。不要擅自更改 Python 版本、行宽或规则集，除非与仓库现状一致或用户确认。

#### mypy（默认类型检查器）

初始化时应配置静态类型检查，与 Ruff、pytest 同级纳入门禁。优先 **mypy**；若仓库已使用 pyright / basedpyright，沿用并在 `DECISIONS.md` 中说明，勿重复引入。

**dev 依赖**（示例）：

```toml
[project.optional-dependencies]
dev = [
    # ...
    "mypy>=1.8.0",
]
```

**最小配置**（示例，路径按仓库调整）：

```toml
[tool.mypy]
python_version = "3.11"
files = ["agent"]
warn_return_any = true
warn_unused_ignores = true
check_untyped_defs = true
no_implicit_optional = true

[[tool.mypy.overrides]]
module = ["openai.*", "rich.*"]
ignore_missing_imports = true
```

- `files` / `packages` 指向运行时代码；测试目录是否纳入由仓库决定。
- 不要一步启用 `strict = true`，除非现有代码已就绪。
- 缺 stub 的第三方库用 `[[tool.mypy.overrides]]`，勿全局关闭类型检查。
- 若 mypy 报错：修复明显问题；其余记入 `harness/PROGRESS.md`「已知问题」。

### 3. 将工具链摘要写入 DECISIONS.md

**仅写入工具链相关信息**，例如：

- Python 版本；
- 运行时代码与测试目录；
- 各工具及配置所在文件；
- 可复制粘贴的验证命令（须含 lint、format、类型检查、测试）。

**不要**在本步写入命名、docstring、注释风格等编码规范；留待编码规范 Skill 或用户后续补充。

### 4. 初始化验证

建议顺序：

```bash
ruff check <src> <tests>
ruff format --check <src> <tests>
mypy <src>
pytest
```

确认通过，或将遗留项记入 `harness/PROGRESS.md`。更新 `harness/PROGRESS.md` 的验证与当前状态。

## 实用兜底（仅当缺少配置且初始化需要默认值时）

- Ruff：行宽 100，规则集 E/F/I/UP/B 可作为起点；
- mypy：`check_untyped_defs = true`，第三方缺 stub 时用 per-module override；
- 初始化阶段不对全仓库做无关格式化，除非用户要求或门禁必需。

## 与其他 Skill 的边界

| Skill | 关系 |
|-------|------|
| `mini-harness` | 先完成 install；本 Skill 是其初始化清单第 3 步 |
| `harness/rules/` | 编码规范常驻规则（`python-coding-conventions.md`） |
| `tdd` / `python-testing-patterns` | 日常改运行时代码前使用 |
| `code-review-expert` | 日常编码完成后审查 |
| `code-simplifier` | 提交前精炼 |

本 Skill **只负责工具链初始化**；编码规范与日常代码质量由编码规范 Skill、`DECISIONS.md`、工具门禁与其余 Skill 分担。
