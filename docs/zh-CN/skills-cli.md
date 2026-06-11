# Skills CLI 指南

### 前置条件

- [Node.js](https://nodejs.org/) 18+（可用 `npx`）
- 可访问 GitHub

### 发现本仓库中的 Skill

```bash
npx skills add HYX-LHJ/mini-harness --list
```

应能看到 **`mini-harness-zh`**（由 [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) 声明）。

### 安装

```bash
# 全局 — 本机所有项目可用
npx skills add HYX-LHJ/mini-harness --skill mini-harness-zh -g -y

# 项目级 — 可提交到团队仓库
npx skills add HYX-LHJ/mini-harness --skill mini-harness-zh -y

# 简写（等同 --skill mini-harness-zh）
npx skills add HYX-LHJ/mini-harness@mini-harness-zh -g -y
```

### 指定 Agent 工具

```bash
# 仅安装到 Cursor + Claude Code + Codex
npx skills add HYX-LHJ/mini-harness \
  --skill mini-harness-zh \
  -a cursor -a claude-code -a codex \
  -g -y
```

| 工具 | `--agent` 参数 | 全局安装路径 |
|------|----------------|-------------|
| Cursor | `cursor` | `~/.cursor/skills/mini-harness-zh/` |
| Claude Code | `claude-code` | `~/.claude/skills/mini-harness-zh/` |
| Codex | `codex` | `~/.codex/skills/mini-harness-zh/` |
| 通用 | `amp`、`opencode` 等 | `~/.agents/skills/mini-harness-zh/` |

完整列表：[vercel-labs/skills README](https://github.com/vercel-labs/skills#supported-agents)

### 不安装直接试用

```bash
npx skills use HYX-LHJ/mini-harness@mini-harness-zh --agent claude-code
```

### 管理已安装 Skill

```bash
npx skills list              # 查看已安装
npx skills update mini-harness-zh -y
npx skills remove mini-harness-zh -y
npx skills find harness      # 在 skills.sh 生态搜索
```

### 在项目中锁定版本

将 [`.skills.json.example`](../.skills.json.example) 复制为 `.skills.json`：

```json
{
  "skills": [
    {
      "name": "mini-harness-zh",
      "remote": "HYX-LHJ/mini-harness",
      "skill": "mini-harness-zh"
    }
  ]
}
```

### CI 中安装

```bash
npx skills add HYX-LHJ/mini-harness \
  --skill mini-harness-zh \
  -g -a cursor -y
```

### 安装后

1. 按需重启 Agent 工具（Codex 须重启）
2. 在目标仓库说：「用 mini-harness-zh 在当前仓库创建 harness」
