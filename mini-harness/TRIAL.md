# ⏱️ 5 分钟上手 mini-harness

第一次试用？读完选一个场景开干。细节 → [README](../README.md) · [using-harness Skill](skills/using-harness/SKILL.md)

---

## 你将得到什么

- 🧭 每回合先读 **using-harness** → `PROGRESS` + `todo` + `PROJECT`
- ✅ 改运行时代码前写 **AC**，且 **AC 已确认** 才实现
- 📁 任务结束归档 `backlog/`，刷新 `PROGRESS`

---

## 前置

- Python 3.10+（`python` 或 `py`）
- Cursor / Claude Code / Codex 任一

---

## 场景 A：仓库已有 `harness/` ✨ 最常见

团队已 `install`，你**不必**单独装插件。

1. IDE 打开仓库根
2. **新开 Agent 会话**，第一句：

   ```text
   先调用 using-harness：读 harness/skills/using-harness/SKILL.md、PROGRESS.md、todo.md、profile/PROJECT.md，再帮我：……
   ```

3. 提个**很小**的需求（改一句文档、加个小函数）
4. 观察是否：登记 todo + AC → 请你确认 **AC 已确认** 后才写代码

**可选健康检查：**

```bash
python harness/scripts/mini_harness.py doctor --root .
```

要看到 `ok: true`。

---

## 场景 B：自己的新仓库 🆕

1. 拿到 `mini-harness/`（克隆/拷贝）
2. 在目标仓库根：

   ```bash
   python mini-harness/scripts/mini_harness.py install --root .
   python harness/scripts/mini_harness.py doctor --root .
   ```

3. 确认有 `harness/`、`tests/`
4. 新开 Agent，同场景 A 第 2 步
5. **（Python 可选）** 按 `python-code-style` Skill 配 `pyproject.toml` + `commands.gate`

---

## 场景 C：装 Cursor 插件（可选）🔌

插件 = Skills + Session 提醒。**不装也能用**场景 A/B。

1. `mini-harness/` → `~/.cursor/plugins/local/mini-harness`
2. 重启 Cursor
3. 目标仓库仍要跑场景 B 的 `install`

Claude：`claude --plugin-dir /path/to/mini-harness`  
Codex：市场安装 → 信任钩子 → 新会话

---

## 💬 跟 Agent 怎么说

| 阶段 | 你可以说 |
|------|----------|
| 开聊 | 「先读 harness/skills/using-harness/SKILL.md 和 harness 状态」 |
| 提需求 | 「先登记 todo 和 AC，等我确认 AC 再实现」 |
| 做完 | 「按 workflow 归档 todo 并更新 PROGRESS」 |
| Subagent | 「读 harness/skills/tdd/SKILL.md，不要用全局 skills」 |

---

## ✅ 试用成功 checklist

- [ ] `doctor` 通过
- [ ] 改代码前 todo 有 AC，且 **AC 已确认** 已勾选
- [ ] 未确认前 Agent 没直接写实现
- [ ] 小任务完成后 todo 已归档，`PROGRESS` 有更新
- [ ] （完整流程）`harness/acceptance/` 有报告

---

## ❓ FAQ

**必须装插件吗？** 不必。有 `harness/` 就能用；插件多 Session 提醒。

**`python` 找不到？** Windows 试 `py`；或装 Python 3.10+ 加 PATH。

**Agent 跳过 todo？** 提醒：「按 using-harness 硬约束，先 todo + AC 核对」。

**读错同名 Skill？** 任务里写 `harness/skills/...` 路径。

**根目录有 AGENTS.md？** v2.1+ 工作流在 `harness/skills/using-harness/SKILL.md`，`install` 不覆盖你的 AGENTS.md。

---

## 下一步

- [docs/zh-CN/getting-started.md](../docs/zh-CN/getting-started.md)
- [using-harness/references/workflow.md](skills/using-harness/references/workflow.md)
