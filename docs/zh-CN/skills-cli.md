# Skills CLI 指南

### 前置条件

- [Node.js](https://nodejs.org/) 18+（可用 `npx`）
- 可访问 GitHub

### 发现本仓库中的 Skill

```bash
npx skills add HYX-LHJ/mini-harness --list
```

应能看到 **`agent-harness-zh`**（由 [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) 声明）。

### 安装

```bash
# 全局 — 本机所有项目可用
npx skills add HYX-LHJ/mini-harness --skill agent-harness-zh -g -y

# 项目级 — 可提交到团队仓库
npx skills add HYX-LHJ/mini-harness --skill agent-harness-zh -y

# 简写（等同 --skill agent-harness-zh）
npx skills add HYX-LHJ/mini-harness@agent-harness-zh -g -y
```

### 指定 Agent 工具

```bash
# 仅安装到 Cursor + Claude Code + Codex
npx skills add HYX-LHJ/mini-harness \
  --skill agent-harness-zh \
  -a cursor -a claude-code -a codex \
  -g -y
```

| 工具 | `--agent` 参数 | 全局安装路径 |
|------|----------------|-------------|
| Cursor | `cursor` | `~/.cursor/skills/agent-harness-zh/` |
| Claude Code | `claude-code` | `~/.claude/skills/agent-harness-zh/` |
| Codex | `codex` | `~/.codex/skills/agent-harness-zh/` |
| 通用 | `amp`、`opencode` 等 | `~/.agents/skills/agent-harness-zh/` |

完整列表：[vercel-labs/skills README](https://github.com/vercel-labs/skills#supported-agents)

### 不安装直接试用

```bash
npx skills use HYX-LHJ/mini-harness@agent-harness-zh --agent claude-code
```

### 管理已安装 Skill

```bash
npx skills list              # 查看已安装
npx skills update agent-harness-zh -y
npx skills remove agent-harness-zh -y
npx skills find harness      # 在 skills.sh 生态搜索
```

### 在项目中锁定版本

将 [`.skills.json.example`](../.skills.json.example) 复制为 `.skills.json`：

```json
{
  "skills": [
    {
      "name": "agent-harness-zh",
      "remote": "HYX-LHJ/mini-harness",
      "skill": "agent-harness-zh"
    }
  ]
}
```

### CI 中安装

```bash
npx skills add HYX-LHJ/mini-harness \
  --skill agent-harness-zh \
  -g -a cursor -y
```

### 安装后

1. 按需重启 Agent 工具（Codex 须重启）
2. 在目标仓库说：「用 agent-harness-zh 在当前仓库创建 harness」
