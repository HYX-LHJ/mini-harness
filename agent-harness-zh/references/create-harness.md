# 创建 harness — Agent 执行清单

他人安装 **agent-harness-zh** Skill 后，用**同一套 Agent 对话**即可在任意仓库生成标准 harness。本文是 Agent 逐步清单。

## 用户怎么说会触发

- 「创建 harness」「初始化 harness」「搭建 agent 工程」
- 「帮我装 agent-harness」「搭建协作目录」

## Agent 必做步骤（按序，不得跳步）

### 1. 定位 skill 目录

`SKILL_ROOT` = 本 Skill 安装路径（`agent-harness-zh/` 目录），因工具而异：

| 工具 | 个人路径 | 项目路径 |
|------|----------|----------|
| Cursor | `~/.cursor/skills/agent-harness-zh/` | `<repo>/.cursor/skills/agent-harness-zh/` |
| Codex | `$CODEX_HOME/skills/agent-harness-zh/` | — |
| Claude Code | `~/.claude/skills/agent-harness-zh/` | `<repo>/.claude/skills/agent-harness-zh/` |
| 通用 | `~/.agents/skills/agent-harness-zh/` | `<repo>/.agents/skills/agent-harness-zh/` |

或通过 Skills CLI：`npx skills add HYX-LHJ/round-harness --skill agent-harness-zh`

脚本路径：`<SKILL_ROOT>/scripts/init_harness.py`

详见 [installation.md](installation.md)

### 2. 确认目标仓库

- `REPO_ROOT` = 用户指定目录，默认当前工作区根
- 若已存在 `harness/index.md` 且用户未要求覆盖 → 询问是否 `--force`

### 3. 收集参数（可推断则用默认）

| 参数 | 默认 | 何时改 |
|------|------|--------|
| `--project-name` | 文件夹名 | 用户指定项目名 |
| `--src-dir` | `src` | 业务代码不在 `src/` |
| `--dev-branch` / `--test-branch` | `dev` / `test` | 团队分支不同 |
| `--lint-cmd` / `--pytest-cmd` | 见模板 | 非 Windows 或无 venv 时改路径 |

Linux/macOS 示例：

```bash
--lint-cmd '.venv/bin/python harness/scripts/lint_src.py'
--pytest-cmd '.venv/bin/python -m pytest'
```

### 4. 执行脚手架（Agent 必须亲自运行）

```bash
python <SKILL_ROOT>/scripts/init_harness.py --root <REPO_ROOT> --project-name <NAME>
```

退出码非 0 → 只修脚手架，不向用户宣称完成。

### 5. 验证（脚本内置 + Agent 目视）

必须全部存在：

```
AGENTS.md
pytest.ini
harness/index.md
harness/todo.md
harness/PROGRESS.md
harness/DECISIONS.md
harness/docs/plan-mode.md
harness/scripts/lint_src.py
harness/scripts/sync_progress.py
harness/scripts/archive_harness_todo.py
harness/code_review/index.md
harness/code_simplifier/index.md
harness/plans/index.md
harness/tests/index.md
```

### 6. 收尾告知用户

向用户说明：

1. 已生成标准 harness（目录树 + Playbook + 维护脚本）
2. 后续每回合 Agent 读 `AGENTS.md` + `harness/todo.md` / `PROGRESS.md`
3. 建议安装配套 Skill：`tdd`、`code-review-expert`、`code-simplifier`
4. 有 `src/` 且要跑通门禁时：配置 `.venv`、`ruff`、`pyright`、`pytest`

### 7. 不要做的事

- **不要**手写简化版 harness 代替跑 `init_harness.py`
- **不要**跳过 `AGENTS.md` 或 `pytest.ini`
- **不要**在未初始化完成时开始改业务代码

## 生成物说明

| 产物 | 说明 |
|------|------|
| 目录树 | `backlog/`、`plans/`、`docs/`、`code_review/`、`code_simplifier/`、`tests/`、`scripts/`、`sql/` |
| `AGENTS.md` | 通用 Playbook；项目约束用 `DECISIONS.md` 补充 |
| 维护脚本 | `lint_src`、`sync_progress`、`archive_harness_todo`（随 skill 捆绑） |
| `pytest.ini` | `harness/tests` + 排除 `integration` |
| `harness/docs/plan-mode.md` | Plan 模式细则 |

业务专属内容（API 文档、DDL、集成测）由用户在 `harness/docs/`、`harness/sql/`、`harness/tests/` 自行补充。
