# Contributing / 参与贡献

**Languages:** [English](#english) · [中文](#中文)

---

<a id="english"></a>

## English

Thank you for contributing to mini-harness! This repo contains the **`mini-harness/` plugin** — the single authoritative source for the mini-harness skill, other skills, installer, and templates. It supports **Cursor, Codex, and Claude Code**.

### What to contribute

- **Bug fixes** — `mini_harness.py`, hooks, templates, docs
- **Template improvements** — `mini-harness/assets/harness-template/`
- **Skills** — `mini-harness/skills/`
- **Documentation** — `docs/en/`, `docs/zh-CN/`, skill `references/`
- **Host support** — plugin manifests, session-start hooks

**Open an Issue first** for:

- Changing default collaboration flow (`mini-harness/skills/using-harness/SKILL.md` hard constraints)
- Renaming or removing standard harness paths
- Behavior that conflicts with a skill `SKILL.md`

### Development

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
cd mini-harness
```

No third-party Python dependencies; the installer uses the stdlib only.

**Verify the plugin** in a temp directory:

```bash
mkdir /tmp/harness-test && cd /tmp/harness-test
git init
python /path/to/mini-harness/mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**Run plugin tests:**

```bash
python -m pytest mini-harness/tests
```

### Maintainer workflow

`mini-harness/` is the **only authoritative source**. After editing the mini-harness skill, other skills, or templates:

1. Change files under `mini-harness/` only
2. Re-run `install` on target repos
3. Run `doctor` and `pytest mini-harness/tests`

See [mini-harness/skills/using-harness/SKILL.md](mini-harness/skills/using-harness/SKILL.md) — section「维护者与权威源」.

### Commit messages

- 1–2 sentences explaining **why**
- English or Chinese — match recent repo style

### Pull requests

1. Branch from `main`
2. One focused topic per PR
3. Describe: motivation, scope (plugin / templates / docs / hooks), how to verify

### Directory conventions

| Path | Notes |
|------|-------|
| `mini-harness/` | **Authoritative plugin** — `skills/using-harness/SKILL.md`, `skills/`, `scripts/`, `assets/harness-template/` |
| `mini-harness/tests/` | Plugin installer and hook tests |
| `README.md` / `README.zh-CN.md` | External repo overview |
| `docs/en/` / `docs/zh-CN/` | External documentation |

**Do not commit** `harness/` or `tests/` in this repo — they are `install` output (gitignored). Verify in a temp directory instead.

### Reporting issues

Use GitHub Issue templates (Bug / Feature) when possible:

- [.github/ISSUE_TEMPLATE/bug_report.yml](.github/ISSUE_TEMPLATE/bug_report.yml)
- [.github/ISSUE_TEMPLATE/feature_request.yml](.github/ISSUE_TEMPLATE/feature_request.yml)

Include: OS, Python version, full command line, actual vs expected output, agent tool used (Cursor / Codex / Claude Code).

Security issues: see [SECURITY.md](SECURITY.md) — do not file public issues.

---

<a id="中文"></a>

## 中文

感谢参与 mini-harness！本仓库以 **`mini-harness/` 插件**为唯一权威源，包含 mini-harness skill、其它 Skills、安装器与模板，支持 **Cursor、Codex、Claude Code**。

### 可贡献内容

- **缺陷修复** — `mini_harness.py`、钩子、模板、文档
- **模板改进** — `mini-harness/assets/harness-template/`
- **Skills** — `mini-harness/skills/`
- **文档** — `docs/zh-CN/`、`docs/en/`、skill `references/`
- **宿主支持** — 插件清单、Session Start 钩子

以下情况**请先开 Issue**：

- 修改默认协作流程（`mini-harness/skills/using-harness/SKILL.md` 硬约束）
- 重命名或删除标准 harness 路径
- 与某个 Skill `SKILL.md` 冲突的行为变更

### 开发环境

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
cd mini-harness
```

安装器仅使用 Python 标准库，无第三方依赖。

**在临时目录验证插件：**

```bash
mkdir /tmp/harness-test && cd /tmp/harness-test
git init
python /path/to/mini-harness/mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**运行插件测试：**

```bash
python -m pytest mini-harness/tests
```

### 维护者流程

**只改** `mini-harness/` 下的权威源文件，然后在目标仓库重新 `install`，并运行 `doctor` 与 `pytest mini-harness/tests`。

详见 [mini-harness/skills/using-harness/SKILL.md](mini-harness/skills/using-harness/SKILL.md)「维护者与权威源」。

### 提交信息

- 1–2 句话说明 **为什么**
- 中文或英文均可，与近期仓库风格一致

### Pull Request

1. 从 `main` 拉分支
2. 一个 PR 一个主题
3. 说明动机、范围（插件 / 模板 / 文档 / 钩子）、验证方式

### 目录约定

| 路径 | 说明 |
|------|------|
| `mini-harness/` | **权威插件** — `skills/using-harness/SKILL.md`、`skills/`、`scripts/`、`assets/harness-template/` |
| `mini-harness/tests/` | 安装器与钩子测试 |
| `README.md` / `README.zh-CN.md` | 对外仓库概览 |
| `docs/zh-CN/` / `docs/en/` | 对外文档 |

**勿提交**本仓库的 `harness/`、`tests/` — 它们是 `install` 产物（已 gitignore）。请在临时目录验证。

### 报告问题

尽量使用 GitHub Issue 模板（Bug / Feature）：

- [.github/ISSUE_TEMPLATE/bug_report.yml](.github/ISSUE_TEMPLATE/bug_report.yml)
- [.github/ISSUE_TEMPLATE/feature_request.yml](.github/ISSUE_TEMPLATE/feature_request.yml)

请附上：操作系统、Python 版本、完整命令行、实际与预期输出、使用的 Agent 工具（Cursor / Codex / Claude Code）。

安全问题见 [SECURITY.md](SECURITY.md) — 请勿公开提 Issue。
