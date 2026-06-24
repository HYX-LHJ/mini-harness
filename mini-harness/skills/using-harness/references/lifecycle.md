# 🌱 仓库生命周期

插件装好后就能用 **using-harness** 与全部内置 Skill。在**目标项目**跑 `install` 才会生成 `harness/` 状态目录。

---

## 原则

- harness **与业务无关**；可执行规则 → `profile/PROJECT.md`；重大取舍 → `DECISIONS.md`（按主题）
- **不猜测**构建、测试、lint、分支、发布命令
- **两步走**：先装插件 → 再在目标仓库 `install`

---

## 初始化清单

用户要**初始化 harness** 或**为新仓库启用**时：

### 1️⃣ 安装 harness 目录

```bash
python mini-harness/scripts/mini_harness.py install --root .
# 已 install 后：
python harness/scripts/mini_harness.py install --root .
```

安装器会：

- 📁 创建 `harness/`（`PROGRESS`、`todo`、`DECISIONS`、模板等）
- 🧪 创建仓库根 `tests/`
- 📦 同步 `harness/skills/`、`harness/scripts/`
- 💾 在 `harness/.package/` 保存版本快照
- ✅ **不会**覆盖 `profile/`；**不会**创建根 `AGENTS.md`

装完跑 doctor：

```bash
python harness/scripts/mini_harness.py doctor --root .
```

看到 `ok: true` 即可开 Agent 会话。

### 2️⃣ Python 工具链（仅一次，可选）

仓库有 Python 代码 → 读 `harness/skills/python-code-style/SKILL.md`，配置 `pyproject.toml` 并在 `commands.gate` 登记门禁。

---

## 维护者：权威源在哪

**只改 `mini-harness/` 插件目录**。各仓库里的 `harness/` 是安装器**产出物**，不是编辑起点。

```text
改 mini-harness/skills/… → 目标仓库 install → doctor → 本地 pytest mini-harness/tests
```

---

## 日常命令

```bash
python harness/scripts/mini_harness.py install --root .   # 同步
python harness/scripts/mini_harness.py update --root .    # 从 .package 刷新受管文件
python harness/scripts/mini_harness.py doctor --root .    # 健康检查
python harness/scripts/mini_harness.py uninstall --root . # 移除受管 harness
```
