# 提交回合与纪律

用户说「提交」「推送」「commit」「push」且未指定分支时，在**常规回合收尾之后**执行。

## 顺序（不得跳过或调换）

1. 常规收尾完成（含 code-review 落盘、门禁后）
2. **code-simplifier**（交付含业务代码时）→ 落盘 → 门禁
3. **二次 code-review-expert** → 落盘；有问题则修复并重新门禁
4. Git：`dev` → commit → push → merge `test` → push → 回 `dev`
5. `sync_progress.py` + 手写 PROGRESS

仅 harness/文档、无业务代码时可跳过步骤 2–3。

## 提交前检查清单

```
- [ ] 在开发分支（默认 dev）
- [ ] git status / diff 无密钥、无本地联调临时代码
- [ ] lint + pytest 全绿
- [ ] src/ 变更均有对应测试变更
- [ ] code_review / code_simplifier 报告已落盘
- [ ] todo 已勾选
```

## 合并非快进

停止并向用户说明；不得 `push --force`（除非用户明确要求且了解后果）。

## commit message

- 1–2 句，说明 **why** 而非罗列 what
- 遵循仓库近期 `git log` 风格

## 刷新 PROGRESS 时机

- 每回合收尾
- **commit 且 push 完成后必须再刷**，使远程/HEAD 与快照一致
