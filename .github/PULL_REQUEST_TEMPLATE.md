## Summary / 摘要

-

## Scope / 影响范围

- [ ] `mini-harness-zh/` or `mini-harness-en/`
- [ ] `mini-harness-zh/scripts/init_harness.py` / `mini-harness-en/scripts/init_harness.py`
- [ ] `templates/` (zh and/or en)
- [ ] `docs/en/` / `docs/zh-CN/`
- [ ] `README.md` / `README.zh-CN.md`

## Test plan / 验证方式

```bash
python mini-harness-zh/scripts/init_harness.py --root /tmp/harness-test-zh --dry-run
python mini-harness-zh/scripts/init_harness.py --root /tmp/harness-test-zh
python mini-harness-en/scripts/init_harness.py --root /tmp/harness-test-en --dry-run
python mini-harness-en/scripts/init_harness.py --root /tmp/harness-test-en
```

- [ ] Both skill packages scaffold successfully / 两个 Skill 包脚手架均通过

Closes #
