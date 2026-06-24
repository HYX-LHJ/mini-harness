---
name: tdd
description: 测试驱动开发（红-绿-重构）。用户要加功能、修 bug、写测试，或说「先写测试」「TDD」「红绿重构」；harness todo 已勾选 AC 已确认、准备写运行时代码时，必须用本 Skill（常为 subagent）。禁止水平切片。即使用户只说「加个接口」，在 harness 流程下写实现前也应先写 failing 测试。
---

# 🧪 测试驱动开发（TDD）

## 核心理念

好测试描述系统**做什么**，不绑定**怎么做**——通过公共接口走真实路径，重构后仍应通过。

| ✅ 好测试 | ❌ 坏测试 |
|----------|----------|
| 公共 API、可感知行为 | mock 内部、测私有方法 |
| 像规格说明 | 重命名函数就挂 |

示例 → [references/tests.md](references/tests.md) · mock → [references/mocking.md](references/mocking.md)

---

## ⛔ 反模式：水平切片

**不要**先写完全部测试再写全部实现。

```text
❌ 水平：test1,2,3,4,5 → impl1,2,3,4,5
✅ 垂直：test1→impl1 → test2→impl2 → …
```

批量写测试会锁死想象的行为；垂直切片每轮都基于刚写出的真实代码。

---

## 工作流

### 1️⃣ 规划

写任何测试前：

- 读 `harness/todo.md` 的 **AC**（主来源）
- 确认 `- [x] **AC 已确认**` 已勾选——**未勾选则停止**，先与用户核对 AC
- 与用户确认：公共接口长什么样？哪些行为最值得测？

深度模块与可测试接口 → [deep-modules.md](references/deep-modules.md) · [interface-design.md](references/interface-design.md)

> 你无法测试一切。把精力放在关键路径和复杂逻辑。

### 2️⃣ Tracer bullet

```text
RED   → 为第一个行为写测试 → 失败
GREEN → 最少代码通过 → 通过
```

证明端到端路径可行。

### 3️⃣ 增量循环

每个剩余行为：`RED → GREEN`，一次一个测试，只写够通过的代码，不预判后续。

### 4️⃣ 重构

全部绿了之后 → [refactoring.md](references/refactoring.md)：提取重复、加深模块、SOLID。每步后跑测试。**RED 阶段不重构。**

---

## ✅ 每轮自检

- [ ] 测行为，不测实现
- [ ] 只用公共接口
- [ ] 重构后仍应通过
- [ ] 代码对本测试而言最少
- [ ] 无投机性功能
