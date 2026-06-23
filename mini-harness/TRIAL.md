# 5 分钟上手 mini-harness

面向第一次试用的小伙伴。读完按场景操作即可；细节见 [README.md](README.md) 与根目录 [AGENTS.md](AGENTS.md)。

## 你将得到什么

- Agent 每回合须先调用 **mini-harness skill**：`harness/skills/mini-harness/SKILL.md` → 根 `AGENTS.md`（Playbook 正文）→ `harness/PROGRESS.md` + `harness/todo.md`
- 改运行时代码前须写 **验收标准（AC）** 并 **人工确认**
- 任务结束归档到 `harness/backlog/`，状态写入 `PROGRESS.md`

## 前置条件

- 能跑 Python 3.10+（`python` 或 `py` 均可）
- 使用 Cursor、Claude Code 或 Codex 之一与 Agent 对话

---

## 场景 A：仓库里已有 `harness/`（最常见）

团队仓库已执行过 `install`，你**不必**单独装插件。

1. 用 IDE 打开仓库根目录。
2. **新开一个 Agent 会话**，第一句话建议：

   ```text
   先调用 mini-harness skill：读 harness/skills/mini-harness/SKILL.md 和 AGENTS.md、harness/PROGRESS.md、harness/todo.md，再帮我做下一件事：……
   ```

3. 提一个**很小**的需求（例如改一句文档、加一个小函数）。
4. 观察 Agent 是否：
   - 在 `harness/todo.md` 登记任务并写 AC；
   - 复述 AC 请你确认（勾选「**AC 已确认**」后才应写代码/测试）。

**健康检查（可选）**：

```bash
python harness/scripts/mini_harness.py doctor --root .
# Windows 若无 python 命令，可用：py harness/scripts/mini_harness.py doctor --root .
```

应看到 `ok: true`，`warnings` 为空。

---

## 场景 B：在自己的新仓库启用

1. 拿到 `mini-harness/` 目录（拷贝、子模块或压缩包）。
2. 在**目标仓库根目录**执行：

   ```bash
   python mini-harness/scripts/mini_harness.py install --root .
   python harness/scripts/mini_harness.py doctor --root .
   ```

3. 确认生成了 `AGENTS.md`、`harness/`、`tests/`。
4. 新开 Agent 会话，同场景 A 第 2 步。
5. **（Python 项目，可选）** 让 Agent 按 `harness/skills/python-code-style/SKILL.md` 初始化 `pyproject.toml` 与 `harness/DECISIONS.md` 中的验证命令。

---

## 场景 C：可选 — 安装 Cursor 插件（Session 提醒）

仅想要「每次开聊提醒读 Playbook」时再做；**不装也能用**场景 A/B。

1. 将 `mini-harness/` 复制或符号链接到：

   ```text
   ~/.cursor/plugins/local/mini-harness
   ```

2. 重启 Cursor。
3. 仍需在目标仓库执行场景 B 的 `install`（插件 ≠ 仓库激活）。

Claude Code：`claude --plugin-dir /path/to/mini-harness`  
Codex：从市场安装后须信任钩子并**新开会话**。

---

## 试用时建议这样跟 Agent 说话

| 阶段 | 你可以说 |
|------|----------|
| 开聊 | 「先读 AGENTS.md 和 harness 状态文件」 |
| 提需求 | 「先登记 todo 和 AC，等我确认 AC 再实现」 |
| 做完后 | 「按 AGENTS §5 归档 todo 并更新 PROGRESS」 |
| 走 subagent | 「读 `harness/skills/tdd/SKILL.md`，不要用全局 skills」 |

---

## 怎样算试用成功

- [ ] `doctor` 通过（`ok: true`，无 warnings）
- [ ] 改代码前 `harness/todo.md` 有 AC，且 **AC 已确认** 已勾选
- [ ] 未确认 AC 前 Agent 没有直接写实现/测试
- [ ] 小任务完成后 `todo` 已归档或清空，`PROGRESS.md` 有更新
- [ ] （完整流程时）`harness/acceptance/` 有验收报告

---

## 常见问题

**Q：必须装插件吗？**  
不必。仓库里有 `harness/` 和 `AGENTS.md` 就能用；插件只多 Session 开场提醒。

**Q：`python` 找不到？**  
Windows 试 `py`；macOS/Linux 试 `python3`，或安装 Python 3.10+ 并加入 PATH。

**Q：Agent 跳过 todo / AC 怎么办？**  
直接提醒：「按 AGENTS.md 硬约束，先登记 todo 并完成 AC 核对」。流程是软约束，需要你盯一下。

**Q：同名 skill 读错了？**  
在任务里写明仓库路径，例如 `harness/skills/acceptance-verification/SKILL.md`，不要用 `~/.agents/skills/`。

**Q：`install` 会覆盖我的 `AGENTS.md` 吗？**  
若仓库已有 `AGENTS.md`，默认**不覆盖**；全新仓库会自动复制 Playbook。

---

## 反馈给我们

试用后请记录：

1. 哪一步卡住（命令、路径、宿主）？
2. Agent 是否遵守 AC 核对？
3. `doctor` 输出是否全绿？

维护者文档见 [skills/mini-harness/SKILL.md](skills/mini-harness/SKILL.md) 的「维护者与权威源」。
