---
name: code-simplifier
description: 提交前精炼代码（行为不变）。用户要 commit、push、提 PR，或说简化、精炼、清理一下再提交时，按 workflow 在 code-review-expert 前/后串行使用。不要用于日常小改；不要替代审查。
---

# ✨ 代码精炼

**改怎么做，不改做什么。** 所有行为、输出、边界必须与精炼前一致。

---

## 原则

1. **功能不变** — 精炼是重构，不是改需求
2. **跟项目走** — `profile/PROJECT.md`、相关 `DECISIONS`、`commands.gate`
3. **清晰优先** — 减嵌套、去冗余、好命名；避免嵌套三元；**可读 > 行数少**
4. **不过度** — 不删有益抽象，不追求「聪明」一行流
5. **限定范围** — 默认仅本会话改过的代码

---

## 流程

1. 识别近期修改的代码段
2. 找可简化点（重复、命名、结构）
3. 应用项目工具链与规范
4. 跑门禁确认行为不变
5. 记录到 `harness/code_simplifier/YYYY-MM-DD_<主题>.md`（重要变更才写）

---

## 产出

精炼记录（可选）含：改了哪些文件 · 动机 · 确认测试/门禁仍过。

**仅在用户明确要求提交/推送时运行。** 精炼后须再走 `code-review-expert`（见 [workflow](../using-harness/references/workflow.md)）。
