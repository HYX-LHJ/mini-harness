# agent-harness

[round-harness](../README.zh-CN.md) 的 Cursor / Codex / Claude Code 等 **Agent Skill 包**（包内文档默认**中文**）。

对外仓库说明：[README.md（英文）](../README.md) · [README.zh-CN.md（中文）](../README.zh-CN.md)

## 目的

安装本 Skill 后，对 Agent 说一句话，即可在**任意仓库**生成标准 harness 工程（目录树 + `AGENTS.md` + 门禁脚本 + 协作流程）。

## 安装

完整说明：[docs/installation.md](../docs/installation.md)

```bash
npx skills add HYX-LHJ/round-harness --skill agent-harness -g -y
```

或复制 `agent-harness/` 到 `~/.cursor/skills/`、`~/.claude/skills/`、`~/.codex/skills/`、`~/.agents/skills/` 等。

## 使用

对 Agent 说：

> 用 agent-harness 在当前仓库创建 harness

或：

```bash
python path/to/agent-harness/scripts/init_harness.py --root /path/to/repo --project-name my_api
```

## 包内结构

```text
agent-harness/
├── SKILL.md              # Agent 主指令（中文）
├── references/           # Agent 细则（中文）
├── templates/            # 落盘模板（中文，生成到用户仓库）
├── bundled/scripts/      # 捆绑维护脚本
└── scripts/init_harness.py
```

## 语言约定

| 范围 | 语言 |
|------|------|
| `agent-harness/` 内（SKILL、references、templates） | **中文为主** |
| 仓库根 `README.md` / `README.zh-CN.md`、`docs/` | **中英分文档** |
| 用户仓库初始化产物（`AGENTS.md`、`harness/`） | **中文**（模板默认） |

## Agent 延伸阅读

| 文档 | 内容 |
|------|------|
| [SKILL.md](SKILL.md) | 创建 harness 与日常回合 |
| [references/](references/) | 安装、目录、Plan、提交等细则 |
