## Summary / 摘要

<!-- 1–3 bullets: what and why / 用 1–3 条说明改了什么、为什么 -->

-

## Scope / 影响范围

<!-- Check all that apply / 勾选适用项 -->

- [ ] `agent-harness/scripts/init_harness.py`
- [ ] `agent-harness/templates/`
- [ ] `agent-harness/SKILL.md` or `references/`
- [ ] `docs/` (bilingual / 中英双语)
- [ ] Multi-tool install paths / 多工具安装路径
- [ ] GitHub / packaging metadata only

## Test plan / 验证方式

<!-- How did you verify? / 如何验证？ -->

```bash
# Example / 示例
python agent-harness/scripts/init_harness.py --root /tmp/harness-test --dry-run
python agent-harness/scripts/init_harness.py --root /tmp/harness-test
```

- [ ] Dry-run passes / 干跑通过
- [ ] Scaffold creates all required files / 脚手架生成全部必需文件
- [ ] Docs updated (EN + 中文) if behavior changed / 行为变更时已更新双语文档

## Notes / 备注

<!-- Breaking changes, follow-ups, linked issues / 破坏性变更、后续事项、关联 Issue -->

Closes #
