---
name: mini-harness
description: 初始化、更新、检查或移除小型 Agent harness 仓库。当用户要在仓库中启用 mini-harness、初始化 harness 目录与 tests 目录、配置 AGENTS.md 工作流或登记任务时使用。
compatibility: 仓库管理与生命周期钩子需要 Python 3.10+。
---

# Mini Harness

将 mini-harness 安装到目标仓库：创建 `harness/` 目录结构、同步内置 Skills 与脚本，并把 Playbook 复制到项目根目录 `AGENTS.md`。日常执行流程以根目录 `AGENTS.md` 为准。

## 原则

- harness 保持与具体业务无关；项目规则写在 `harness/DECISIONS.md` 或项目文档。
- 保留仓库已有、且不由 harness 管理的文件（含已有 `AGENTS.md`）。
- 不猜测构建、测试、lint、分支、发布或部署命令。
- 插件安装与仓库激活是两步：先有插件，再在目标仓库执行 `install`。

## 仓库初始化（Agent 执行清单）

用户要求**初始化 mini-harness** 或**为新仓库启用 harness** 时，按顺序完成：

### 1. 安装 harness 目录与内置内容

从插件根目录（首次）或目标仓库内脚本执行：

```text
python scripts/mini_harness.py install --root <repository>
# 或已安装后：
python harness/scripts/mini_harness.py install --root .
```

安装器会：

- 创建 `harness/` 及 `PROGRESS.md`、`todo.md`、`DECISIONS.md` 等模板文件；
- 创建仓库根目录 `tests/`（全部测试文件存放于此）；
- 将内置 Skills 同步到 `harness/skills/`；
- 将管理脚本同步到 `harness/scripts/`；
- 在 `harness/.package/` 保存版本快照，供后续 `update` 使用。

安装后运行 `doctor` 确认健康（含 `harness/rules/`、`harness/acceptance/` 与 `.package` 漂移提示）：

```text
python harness/scripts/mini_harness.py doctor --root .
```

### 2. 复制 Playbook 到项目根目录 `AGENTS.md`

插件根目录的 [AGENTS.md](../../AGENTS.md) 是 **Agent Harness Playbook**（流程、硬约束、内置 Skill 表）。

- **仓库尚无 `AGENTS.md`**：`install` 会自动将其复制到项目根目录。
- **仓库已有 `AGENTS.md`**：安装器**不会覆盖**项目自有内容。由你判断：
  - 将 Playbook 作为新的根 `AGENTS.md`，并把原项目说明迁入 `harness/DECISIONS.md` 或保留为独立章节；或
  - 在征得用户同意后，用 Playbook 替换或合并根 `AGENTS.md`。

初始化完成后，Agent 每回合以根目录 `AGENTS.md` 为工作流入口，并配合 `harness/PROGRESS.md`、`harness/todo.md` 使用。

### 3. 用 `python-code-style` 初始化 Python 工具链（仅初始化一次）

若仓库含 Python 代码（或即将引入），在**初始化阶段**读取一次内置 Skill：

`harness/skills/python-code-style/SKILL.md`

按该 Skill 配置 `pyproject.toml`、Ruff、pytest、mypy 等；将**工具链与验证命令**摘要写入 `harness/DECISIONS.md`。**编码规范由独立 Skill 负责，不在本步处理。** 日常开发不再读取此 Skill。

不要把完整工具配置正文复制进 `AGENTS.md`；权威来源为 `pyproject.toml` + `DECISIONS.md` 中的工具链摘要。

## 维护者与权威源

**`mini-harness/` 插件目录是唯一权威源**（Playbook、`skills/`、`scripts/`、`rules/`、`assets/harness-template/`）。已激活仓库中的 `harness/` 与根 `AGENTS.md` 均由安装器同步产出，**不是**编辑起点。

变更流程（开发仓库或 monorepo 内）：

1. **只改** `mini-harness/` 下对应文件；
2. 在目标仓库根执行 `python mini-harness/scripts/mini_harness.py install --root <repo>`（或已激活后 `python harness/scripts/mini_harness.py install --root .`）；
3. 运行 `python harness/scripts/mini_harness.py doctor --root .`，确认无漂移 warnings；
4. 运行 `python -m pytest mini-harness/tests`。

若先在已激活仓库改了 `harness/skills/` 或根 `AGENTS.md`，**必须回写** `mini-harness/` 后再执行 install，否则 `doctor` 会报漂移且新仓库 `install` 会分发旧内容。

## 日常维护命令

```text
python harness/scripts/mini_harness.py update --root .
python harness/scripts/mini_harness.py doctor --root .
python harness/scripts/mini_harness.py uninstall --root .
```

## 参考

- 可移植性边界：[references/portability.md](references/portability.md)
- 各宿主插件与 Hook：[references/host-support.md](references/host-support.md)
