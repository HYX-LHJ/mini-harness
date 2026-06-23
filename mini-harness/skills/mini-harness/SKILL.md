---
name: mini-harness
description: mini-harness 工作流 Skill 入口：执行任务前须先遵循项目根 AGENTS.md（Playbook 正文）与 harness 状态文件。亦用于初始化、更新、检查 harness 仓库。
compatibility: 仓库管理与生命周期钩子需要 Python 3.10+。
---

# Mini Harness

mini-harness 是 **Skill 集合包**。本 Skill 是工作流入口；**执行正文为项目根 `AGENTS.md`**（Agent Harness Playbook）。`harness/skills/` 下的其它 Skill（tdd、code-review-expert 等）在 Playbook 流程中按需调用。

## 每回合入口（必须先执行）

收到用户任务后、动手改文件前，**必须先调用本 Skill**：

1. 阅读项目根 **`AGENTS.md`**（本 Skill 的 Playbook 正文，含硬约束与流程）
2. 并行阅读 **`harness/PROGRESS.md`**、**`harness/todo.md`**（需要长期约束时加读 `harness/DECISIONS.md`）
3. 严格按 `AGENTS.md` 执行；有文件变更先登记 todo；涉及运行时代码须 AC 核对

未激活 harness 的仓库：Playbook 源文件在插件 `mini-harness/AGENTS.md`；执行 `install` 后会复制到项目根。

**不要**跳过本步直接实现；**不要**用全局 `~/.agents/skills/` 等同名 Skill 替代 `harness/skills/` 下的内置 Skill。

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

### 2. 复制 Playbook 到项目根 `AGENTS.md`

插件根目录的 [AGENTS.md](../../AGENTS.md) 是 **本 Skill 的 Playbook 正文**（流程、硬约束、内置 Skill 表）。

- **仓库尚无 `AGENTS.md`**：`install` 会自动将其复制到项目根目录。
- **仓库已有 `AGENTS.md`**：安装器**不会覆盖**项目自有内容。由你判断：
  - 将 Playbook 作为新的根 `AGENTS.md`，并把原项目说明迁入 `harness/DECISIONS.md` 或保留为独立章节；或
  - 在征得用户同意后，用 Playbook 替换或合并根 `AGENTS.md`。

初始化完成后，每回合以本 Skill 入口 + 根目录 `AGENTS.md` 为工作流起点，并配合 `harness/PROGRESS.md`、`harness/todo.md` 使用。

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
