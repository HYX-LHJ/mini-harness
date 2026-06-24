# 仓库生命周期

插件一键安装后即可使用 **using-harness** 与全部内置 Skill（`skills/`）。在**目标项目**执行 `install` 会额外同步 `harness/` 状态目录、`tests/` 与仓库内 Skill 副本。

## 原则

- harness 保持与具体业务无关；可执行规则写在 `harness/profile/PROJECT.md`；重大取舍写在 `harness/DECISIONS.md`（按主题）。
- 不猜测构建、测试、lint、分支、发布或部署命令。
- 插件安装与仓库激活是两步：先有插件，再在目标仓库执行 `install`。

## 初始化清单

用户要求**初始化 mini-harness** 或**为新仓库启用 harness** 时：

### 1. 安装 harness 目录与内置内容

```text
python scripts/mini_harness.py install --root <repository>
# 或已安装后：
python harness/scripts/mini_harness.py install --root .
```

安装器会：

- 创建 `harness/` 及 `PROGRESS.md`、`todo.md`、`DECISIONS.md` 等模板文件；
- **不会**创建或覆盖仓库根 `AGENTS.md`（v2.1+ 工作流在 `harness/skills/using-harness/SKILL.md`）；
- 创建仓库根目录 `tests/`；
- 将内置 Skills 同步到 `harness/skills/`（含本 Skill 正文）；
- 将管理脚本同步到 `harness/scripts/`；
- 在 `harness/.package/` 保存版本快照。

安装后运行 `doctor`：

```text
python harness/scripts/mini_harness.py doctor --root .
```

### 2. Python 工具链（仅一次）

若仓库含 Python 代码，读取 `harness/skills/python-code-style/SKILL.md`，配置 `pyproject.toml` 并在 `harness/.mini-harness.json` → `commands.gate` 登记验证命令。

## 维护者与权威源

**`mini-harness/` 插件目录是唯一权威源**。已激活仓库中的 `harness/` 由安装器同步产出，**不是**编辑起点。

变更流程：

1. **只改** `mini-harness/` 下对应文件（尤其是 `skills/using-harness/SKILL.md`）；
2. 在目标仓库执行 `install`；
3. 运行 `doctor`；维护者另在本地运行 `pytest mini-harness/tests`（不上传 GitHub）。

## 日常维护命令

```text
python harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py update --root .
python harness/scripts/mini_harness.py doctor --root .
python harness/scripts/mini_harness.py uninstall --root .
```
