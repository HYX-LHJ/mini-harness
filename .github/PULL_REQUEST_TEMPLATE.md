## Summary / 摘要

-

## Scope / 影响范围

- [ ] `mini-harness/` (plugin — authoritative source)
- [ ] `mini-harness/scripts/mini_harness.py`
- [ ] `mini-harness/assets/harness-template/`
- [ ] `mini-harness/skills/` or `mini-harness/hooks/`
- [ ] `docs/en/` / `docs/zh-CN/`
- [ ] `README.md` / `README.zh-CN.md`

## Test plan / 验证方式

```bash
python mini-harness/scripts/mini_harness.py install --root /tmp/harness-test
python /tmp/harness-test/harness/scripts/mini_harness.py doctor --root /tmp/harness-test
```

维护者本地（gitignore，不上传 GitHub）：

```bash
python -m pytest mini-harness/tests
python mini-harness/evals/ab_test.py
```

- [ ] Install + doctor pass / 安装与健康检查通过
- [ ] Local plugin tests + profile A/B eval pass (maintainers) / 本地测试与 A/B 评测通过

Closes #
