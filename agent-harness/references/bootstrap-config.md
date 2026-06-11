# Bootstrap 后可配置项

创建 harness 的 Agent 步骤见 [create-harness.md](create-harness.md)。

`init_harness.py` 生成骨架后，按项目调整以下项，并写入根 `AGENTS.md`。

## 路径

| 变量 | 默认 | 说明 |
|------|------|------|
| 业务代码目录 | `src/` | 改业务代码须 tdd + code-review |
| 单元测试目录 | `harness/tests/` | 可与 `pytest.ini` 一致 |
| Harness 根 | `harness/` | 不建议改名 |

## 门禁命令

模板默认（Windows venv）：

```powershell
.\.venv\Scripts\python.exe harness/scripts/lint_src.py
.\.venv\Scripts\python.exe -m pytest
```

Linux/macOS 改为 `.venv/bin/python`。无 `lint_src.py` 时可暂用：

```bash
ruff check src/
pyright src/
pytest
```

## Git 分支

| 角色 | 默认 |
|------|------|
| 开发 | `dev` |
| 集成/预发 | `test` |
| 禁止直接提交 | `main` / `master` |

工作流：`dev` commit/push → merge 到 `test` → push → 回到 `dev`。

## 默认不提交

- 本机路径、密钥、`.env` 实值
- `harness/out/`、`harness/pre/` 试跑产物
- 未请求交付的临时联调代码（在项目 DECISIONS 或 AGENTS 中列表明细）

## 捆绑脚本（`init_harness.py` 已落盘）

| 脚本 | 用途 |
|------|------|
| `sync_progress.py` | 刷新 PROGRESS 机械章节 |
| `archive_harness_todo.py` | 跨周归档 todo |
| `lint_src.py` | ruff + pyright 封装（默认检查 `src/`） |

## 安装本 Skill（多工具）

复制整个 `agent-harness/`（含 `SKILL.md`）到对应路径，或使用 Skills CLI：

```bash
npx skills add <owner>/round-harness@agent-harness -g -y
```

| 工具 | 个人路径 | 项目路径 |
|------|----------|----------|
| **Cursor** | `~/.cursor/skills/agent-harness/` | `<repo>/.cursor/skills/agent-harness/` |
| **Codex** | `$CODEX_HOME/skills/agent-harness/` | — |
| **Claude Code** | `~/.claude/skills/agent-harness/` | `<repo>/.claude/skills/agent-harness/` |
| **通用** | `~/.agents/skills/agent-harness/` | `<repo>/.agents/skills/agent-harness/` |

- Cursor：**勿**放入 `~/.cursor/skills-cursor/`
- Codex：安装后**重启**
- 完整说明：[installation.md](installation.md) · [docs/installation.md](../../../docs/installation.md)
