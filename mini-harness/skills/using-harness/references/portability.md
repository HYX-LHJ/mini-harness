# 🌍 可移植性边界

mini-harness 模板与 Skills 描述**通用协作**；具体技术栈留给项目自己填。

---

## ✅ 可移植（插件管）

- 状态恢复（PROGRESS、todo）
- 任务登记与 AC 流程
- Subagent 分工与归档
- 验证与评审证据落盘

---

## 🏠 留在项目（插件不管）

- 产品与领域规则 → `profile/PROJECT.md`、`DECISIONS.md`
- 语言/框架约定 → 项目自己的 Cursor rules、lint 配置
- 源码与测试目录名
- lint、测试、构建、部署命令 → `pyproject.toml`、`commands.gate`
- 分支策略、环境、密钥、端点
- 历史任务与评审记录

安装器可创建**空扩展点**，但**不臆造**项目取值——猜错比留空更糟。
