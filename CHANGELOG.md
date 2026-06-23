# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-06-23

### Added

- **`mini-harness/` plugin** — single authoritative source for playbook, skills, installer, hooks, and templates
- `mini_harness.py` installer with `install`, `update`, `doctor`, and `uninstall`
- Built-in skills synced to `harness/skills/` (tdd, acceptance-verification, code-review-expert, …)
- Session-start hooks for Cursor, Codex, and Claude Code
- AC confirmation workflow and `harness/rules/` coding conventions
- Plugin test suite under `mini-harness/tests/`
- [TRIAL.md](mini-harness/TRIAL.md) quick-start guide

### Changed

- **Breaking:** removed `mini-harness-en/` and `mini-harness-zh/` skill packages and `init_harness.py`
- Documentation rewritten for plugin + `install` activation model
- CI validates `mini_harness.py` scaffold and plugin tests
- Tests live at repo root `tests/` (not `harness/tests/`)

### Removed

- `init_harness.py`, `bundled/scripts/` (lint_src, sync_progress, archive_harness_todo)
- Skills CLI dual-package install flow (`docs/en/skills-cli.md`, `docs/zh-CN/skills-cli.md`)
- Default `pytest.ini` scaffold (use `python-code-style` skill instead)

## [1.2.0] - 2026-06-11

### Added

- **Monday Agent weekly review**: `harness/docs/weekly-review.md` scaffolded by `init_harness.py` (zh + en templates)
- Weekly review round in `AGENTS.md`: first session each Monday archives inactive harness content before other tasks
- CI validates `harness/docs/weekly-review.md` after scaffold

## [1.1.0] - 2026-06-11

### Changed

- Renamed project from `round-harness` to `mini-harness` to emphasize lightweight harness scaffolding
- Split into two Skill packages: `mini-harness-zh/` (Chinese) and `mini-harness-en/` (English)
- Documentation split into `docs/zh-CN/` and `docs/en/`
- Renamed Skill packages from `agent-harness-*` to `mini-harness-en/` and `mini-harness-zh/`

## [1.0.0] - 2026-06-11

### Added

- Portable `agent-harness` Skill package with `init_harness.py` scaffold
- Standard harness layout: `harness/`, `AGENTS.md`, gate scripts, todo/PROGRESS/DECISIONS workflow
- Bilingual documentation (English + 中文): README, docs/, CONTRIBUTING
- Multi-tool install support: Cursor, Codex, Claude Code, universal `~/.agents/skills/`, Skills CLI
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) for Skills CLI / plugin discovery
- [`package.json`](package.json) repository metadata
- GitHub Issue / PR templates and CI scaffold validation workflow

[2.0.0]: https://github.com/HYX-LHJ/mini-harness/releases/tag/v2.0.0
[1.2.0]: https://github.com/HYX-LHJ/mini-harness/releases/tag/v1.2.0
[1.1.0]: https://github.com/HYX-LHJ/mini-harness/releases/tag/v1.1.0
[1.0.0]: https://github.com/HYX-LHJ/mini-harness/releases/tag/v1.0.0
