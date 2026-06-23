# Skills

初始化后，mini-harness 会将内置 Skills 同步到 `harness/skills/`。AI 工具应优先从该目录发现并加载 Skills。

`harness/.package/` 保存用于更新的版本快照；日常使用时以 `harness/skills/` 为准。

仓库也可通过工具支持的其他位置提供额外的项目 Skills。当仓库配置或专用 Skill 已是权威来源时，不要将通用语言或框架指引复制进 harness 其他文件。
