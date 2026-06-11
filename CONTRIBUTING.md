# Contributing / 参与贡献

**Languages:** [English](#english) · [中文](#中文)

---

<a id="english"></a>

## English

Thank you for contributing to round-harness! This repo contains the portable `agent-harness/` Skill and documentation for **Cursor, Codex, Claude Code**, and universal skill loaders.

### What to contribute

- **Bug fixes** — scaffold script, templates, docs
- **Template improvements** — `agent-harness/templates/`
- **Documentation** — `docs/`, `agent-harness/references/`, bilingual updates
- **Multi-tool support** — install paths, compatibility notes

**Open an Issue first** for:

- Changing default collaboration flow (`AGENTS.md` template hard constraints)
- Renaming or removing standard harness paths
- Behavior that conflicts with `SKILL.md`

### Development

```bash
git clone https://github.com/<your-org>/round-harness.git
cd round-harness
```

No third-party Python dependencies; `init_harness.py` uses the stdlib only.

**Verify scaffold** in a temp directory:

```bash
mkdir /tmp/harness-test && cd /tmp/harness-test
git init
python /path/to/round-harness/agent-harness/scripts/init_harness.py --root .
```

Dry run:

```bash
python agent-harness/scripts/init_harness.py --root /tmp/harness-test --dry-run
```

### Commit messages

- 1–2 sentences explaining **why**
- English or Chinese — match recent repo style

### Pull requests

1. Branch from `main`
2. One focused topic per PR
3. Describe: motivation, scope (templates / scripts / docs / SKILL), how to verify

### Directory conventions

| Path | Notes |
|------|-------|
| `agent-harness/SKILL.md` | Agent instructions; keep in sync with `references/` and templates |
| `agent-harness/templates/` | Placeholders: `{{PROJECT_NAME}}`, etc. |
| `agent-harness/scripts/init_harness.py` | Update `REQUIRED_PATHS` when templates change |
| `docs/installation.md` | Canonical multi-tool install guide |
| `docs/*.md` | Bilingual: English + 中文 sections |

### Reporting issues

Use GitHub Issue templates (Bug / Feature) when possible:

- [.github/ISSUE_TEMPLATE/bug_report.yml](.github/ISSUE_TEMPLATE/bug_report.yml)
- [.github/ISSUE_TEMPLATE/feature_request.yml](.github/ISSUE_TEMPLATE/feature_request.yml)

Include: OS, Python version, full command line, actual vs expected output, agent tool used (Cursor / Codex / Claude Code / Skills CLI).

Security issues: see [SECURITY.md](SECURITY.md) — do not file public issues.

---

<a id="chinese"></a>

## 中文

感谢关注 round-harness！本仓库包含可移植的 `agent-harness/` Skill 及面向 **Cursor、Codex、Claude Code** 与通用 Skill 加载器的文档。

### 可贡献内容

- **Bug 修复** — 脚手架脚本、模板、文档
- **模板改进** — `agent-harness/templates/`
- **文档** — `docs/`、`agent-harness/references/`、中英双语更新
- **多工具支持** — 安装路径、兼容性说明

以下变更请**先开 Issue**：

- 改变默认协作流程（`AGENTS.md` 模板硬约束）
- 重命名或删除 harness 标准路径
- 与 `SKILL.md` 冲突的行为变更

### 开发环境

```bash
git clone https://github.com/<your-org>/round-harness.git
cd round-harness
```

无第三方 Python 依赖；`init_harness.py` 仅使用标准库。

**验证脚手架**（临时目录）：

```bash
mkdir /tmp/harness-test && cd /tmp/harness-test
git init
python /path/to/round-harness/agent-harness/scripts/init_harness.py --root .
```

干跑：

```bash
python agent-harness/scripts/init_harness.py --root /tmp/harness-test --dry-run
```

### Commit message

- 1–2 句，说明 **why**
- 中文或英文均可，与近期 commit 风格一致

### Pull Request

1. 从 `main` 拉分支
2. 每 PR 聚焦单一主题
3. 说明：动机、影响范围、验证方式

### 目录约定

| 路径 | 注意 |
|------|------|
| `agent-harness/SKILL.md` | Agent 指令；与 `references/`、模板保持一致 |
| `agent-harness/templates/` | 占位符 `{{PROJECT_NAME}}` 等 |
| `agent-harness/scripts/init_harness.py` | 模板变更时同步 `REQUIRED_PATHS` |
| `docs/installation.md` | 多工具安装 canonical 文档 |
| `docs/*.md` | 中英双语：English + 中文 分区 |

### Issue 报告

请优先使用 GitHub Issue 模板：

- [bug_report.yml](.github/ISSUE_TEMPLATE/bug_report.yml)
- [feature_request.yml](.github/ISSUE_TEMPLATE/feature_request.yml)

请包含：操作系统、Python 版本、完整命令行、实际与期望行为、使用的 Agent 工具（Cursor / Codex / Claude Code / Skills CLI）。

安全问题：见 [SECURITY.md](SECURITY.md)，勿公开提 Issue。
