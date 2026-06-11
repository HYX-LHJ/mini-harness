# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-11

### Changed

- Split into two Skill packages: `agent-harness-zh/` (Chinese) and `agent-harness-en/` (English)
- Documentation split into `docs/zh-CN/` and `docs/en/`
- Removed legacy `agent-harness/` path; use `--skill agent-harness-zh` or `agent-harness-en`

## [1.0.0] - 2026-06-11

### Added

- Portable `agent-harness` Skill package with `init_harness.py` scaffold
- Standard harness layout: `harness/`, `AGENTS.md`, gate scripts, todo/PROGRESS/DECISIONS workflow
- Bilingual documentation (English + 中文): README, docs/, CONTRIBUTING
- Multi-tool install support: Cursor, Codex, Claude Code, universal `~/.agents/skills/`, Skills CLI
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) for Skills CLI / plugin discovery
- [`package.json`](package.json) repository metadata
- GitHub Issue / PR templates and CI scaffold validation workflow

[1.0.0]: https://github.com/HYX-LHJ/round-harness/releases/tag/v1.0.0
