# Rules

本目录存放 **mini-harness 自带的通用编码规范**（与具体业务无关），安装后同步到目标仓库的 `harness/rules/`。

与 `harness/skills/` 的区别：

| | `harness/rules/` | `harness/skills/` |
|---|------------------|-------------------|
| 用途 | 通用编码规范、风格约定（宜常驻 context） | 流程 Skill（按需读取） |
| 典型加载 | 宿主 Rules / CLAUDE.md 引用 | Agent 按 `AGENTS.md` 时机读取 |

## 文件

| 文件 | 说明 |
|------|------|
| [python-coding-conventions.md](python-coding-conventions.md) | 通用 Python 编码规范 |

## 宿主接入

规则正文以安装后的 `harness/rules/` 为准。各宿主需自行接线才能常驻加载，例如：

- **Cursor**：`.cursor/rules/*.mdc`（`alwaysApply: true`），正文可用 `@harness/rules/python-coding-conventions.md` 引用。
- **Claude Code**：项目根目录 `CLAUDE.md` 引用 `@AGENTS.md` 与 `@harness/rules/python-coding-conventions.md`，或复制到 `.claude/rules/`（无 `paths` 则会话启动加载）。

**不要**在本目录写入仓库专属路径或业务规则。

## 项目扩展

仓库可在 `harness/rules/` 下**新增**项目专属规则文件；mini-harness 更新时只刷新其管理的模板文件，不覆盖项目自行添加的文件（与 skills 行为一致）。
