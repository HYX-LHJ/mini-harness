# Security Policy / 安全策略

**Languages:** [English](#english) · [中文](#中文)

---

<a id="english"></a>

## English

### Supported versions

| Version | Supported |
|---------|-----------|
| 2.0.x   | Yes       |
| 1.x     | No (deprecated skill packages removed) |

### Reporting a vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, email the maintainers or use GitHub **Private vulnerability reporting** (if enabled on the repository).

Include:

- Description of the issue
- Steps to reproduce
- Impact assessment (e.g. arbitrary code execution via installer or hooks)
- Suggested fix if you have one

We aim to acknowledge reports within **7 days**.

### Scope

This project ships:

- Documentation and harness templates (markdown)
- `mini_harness.py` installer and session-start hooks (Python stdlib only)

It does **not** run as a network service. Primary risks are malicious template content or unsafe script/hook behavior when activating user repositories.

---

<a id="chinese"></a>

## 中文

### 受支持版本

| 版本 | 支持 |
|------|------|
| 2.0.x | 是 |
| 1.x | 否（旧 Skill 包已移除） |

### 报告漏洞

**请勿在公开 GitHub Issue 中报告安全漏洞。**

请通过邮件联系维护者，或使用 GitHub **私有漏洞报告**（若仓库已启用）。

请包含：

- 问题描述
- 复现步骤
- 影响评估（例如安装器或钩子是否可能导致任意代码执行）
- 修复建议（如有）

我们将在 **7 天内**确认收到。

### 范围

本项目包含：

- 文档与 harness 模板（Markdown）
- `mini_harness.py` 安装器与 Session Start 钩子（仅 Python 标准库）

**不作为网络服务运行**。主要风险来自恶意模板内容，或在用户仓库中执行安装器/钩子时的不安全行为。
