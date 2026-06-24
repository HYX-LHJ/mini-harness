# 运行模式

## Converge（收敛）

**默认推荐。** Agent 跑到停止条件后输出报告并停止。

典型停止条件（满足任一）：

- 总分 ≥ 目标（如 95/100）
- 各 component ≥ 其 max 的 80%
- 连续 N 轮无提升
- 达到最大迭代次数

适合：测试覆盖率、lint 清零、文档完整性、契约对齐。

## Continuous（持续）

**用户离开、希望整夜跑** 时使用。不在 GOAL.md 里写「停」——只写：

- 每轮必须遵守的 Constraints
- 每轮 commit 格式
- 人工中断方式（Ctrl+C / 关闭 session）

适合：性能微调、大规模测试补全（有安全网时）。

**风险**：无停滞检测时可能空转——至少保留「连续 N 轮无提升则暂停并报告」。

## Supervised（监督）

高风险或早期不信任时使用：

- 修改 `File Map` 中标注 **No** 的路径前暂停
- 每 M 轮汇总 diff 请用户确认
- 分数提升但涉及 API 契约变更时暂停

适合：生产配置、鉴权、计费、数据迁移。

## 与 harness subagent 的配合

| 模式 | TDD subagent | 验收 subagent |
|------|--------------|---------------|
| Converge | 补测时按需调用 | 收敛后一次 |
| Continuous | 每轮大改前调用 | 周期末调用 |
| Supervised | 按 File Map | 每 checkpoint |
