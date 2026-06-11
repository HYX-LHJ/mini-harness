"""在目标仓库生成标准 agent-harness 工程。

从 skill 包 ``templates/`` 与 ``bundled/scripts/`` 落盘完整目录树、门禁脚本、
``AGENTS.md``、``pytest.ini``。已存在文件默认跳过（``--force`` 覆盖）。

用法（在**待初始化仓库**根目录，或指定 ``--root``）::

    python <skill-dir>/scripts/init_harness.py --root .
    python <skill-dir>/scripts/init_harness.py --root . --project-name my_api

Agent 标准调用见 skill ``SKILL.md``「创建 harness」。

Examples:
    输入：空 git 仓库 + --root .
    输出：harness/ 全树、AGENTS.md、pytest.ini、三门禁脚本
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "templates"
BUNDLED_SCRIPTS = SKILL_ROOT / "bundled" / "scripts"

PLACEHOLDER_DEFAULTS = {
    "PROJECT_NAME": "my-project",
    "SRC_DIR": "src",
    "DEV_BRANCH": "dev",
    "TEST_BRANCH": "test",
    "LINT_CMD": r".\.venv\Scripts\python.exe harness/scripts/lint_src.py",
    "PYTEST_CMD": r".\.venv\Scripts\python.exe -m pytest",
}

REQUIRED_PATHS = [
    "AGENTS.md",
    "pytest.ini",
    "harness/index.md",
    "harness/todo.md",
    "harness/PROGRESS.md",
    "harness/DECISIONS.md",
    "harness/docs/plan-mode.md",
    "harness/plans/index.md",
    "harness/code_review/index.md",
    "harness/code_review/open-findings.md",
    "harness/code_simplifier/index.md",
    "harness/scripts/lint_src.py",
    "harness/scripts/sync_progress.py",
    "harness/scripts/archive_harness_todo.py",
    "harness/scripts/index.md",
    "harness/tests/index.md",
    "harness/backlog/archive.md",
]


def _monday_of_week(d: date) -> date:
    return d - timedelta(days=d.weekday())


def _sunday_of_week(d: date) -> date:
    return _monday_of_week(d) + timedelta(days=6)


def _substitute(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def _write_if_missing(
    path: Path,
    content: str,
    *,
    force: bool,
    dry_run: bool,
) -> bool:
    if path.exists() and not force:
        print(f"skip (exists): {path}")
        return False
    if dry_run:
        print(f"would write: {path}")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"wrote: {path}")
    return True


def _copy_if_missing(src: Path, dst: Path, *, force: bool, dry_run: bool) -> bool:
    if dst.exists() and not force:
        print(f"skip (exists): {dst}")
        return False
    if dry_run:
        print(f"would copy: {src} -> {dst}")
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"copied: {dst}")
    return True


def _ensure_gitignore(root: Path, *, dry_run: bool) -> None:
    gitignore = root / ".gitignore"
    ignore_lines = ["harness/out/", "harness/pre/", "harness/.pytest-tmp/"]
    if dry_run:
        print(f"would ensure .gitignore lines: {ignore_lines}")
        return
    if gitignore.exists():
        existing = gitignore.read_text(encoding="utf-8")
        to_add = [line for line in ignore_lines if line not in existing]
        if to_add:
            gitignore.write_text(existing.rstrip() + "\n" + "\n".join(to_add) + "\n", encoding="utf-8")
            print(f"appended to .gitignore: {', '.join(to_add)}")
    else:
        gitignore.write_text("\n".join(ignore_lines) + "\n", encoding="utf-8")
        print(f"wrote: {gitignore}")


def _run_sync_progress(root: Path, *, dry_run: bool) -> None:
    script = root / "harness" / "scripts" / "sync_progress.py"
    if dry_run or not script.is_file():
        return
    py = sys.executable
    venv_py = root / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if venv_py.is_file():
        py = str(venv_py)
    try:
        subprocess.run(
            [py, str(script), "--skip-gates"],
            cwd=root,
            check=False,
        )
    except OSError as exc:
        print(f"warn: sync_progress skipped ({exc})", file=sys.stderr)


def verify_harness(root: Path) -> list[str]:
    """返回缺失的必需路径（相对 root）。"""
    missing: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (root / rel).is_file():
            missing.append(rel)
    return missing


def init_harness(
    root: Path,
    *,
    project_name: str,
    src_dir: str,
    dev_branch: str,
    test_branch: str,
    lint_cmd: str,
    pytest_cmd: str,
    force: bool,
    dry_run: bool,
    skip_sync: bool,
) -> list[str]:
    """在 ``root`` 下生成标准 harness；返回验证缺失列表。"""
    today = date.today()
    week_start = _monday_of_week(today).isoformat()
    week_end = _sunday_of_week(today).isoformat()
    mapping = {
        **PLACEHOLDER_DEFAULTS,
        "PROJECT_NAME": project_name,
        "SRC_DIR": src_dir,
        "DEV_BRANCH": dev_branch,
        "TEST_BRANCH": test_branch,
        "LINT_CMD": lint_cmd,
        "PYTEST_CMD": pytest_cmd,
        "WEEK_START": week_start,
        "WEEK_END": week_end,
        "TODAY": today.isoformat(),
    }

    harness = root / "harness"

    text_templates: dict[Path, Path] = {
        TEMPLATES / "harness-index.md": harness / "index.md",
        TEMPLATES / "todo.md": harness / "todo.md",
        TEMPLATES / "PROGRESS.md": harness / "PROGRESS.md",
        TEMPLATES / "DECISIONS.md": harness / "DECISIONS.md",
        TEMPLATES / "code-review-index.md": harness / "code_review" / "index.md",
        TEMPLATES / "open-findings.md": harness / "code_review" / "open-findings.md",
        TEMPLATES / "code-simplifier-index.md": harness / "code_simplifier" / "index.md",
        TEMPLATES / "plan-template.md": harness / "plans" / "_template.md",
        TEMPLATES / "plans-index.md": harness / "plans" / "index.md",
        TEMPLATES / "scripts-index.md": harness / "scripts" / "index.md",
        TEMPLATES / "tests-index.md": harness / "tests" / "index.md",
        TEMPLATES / "docs-index.md": harness / "docs" / "index.md",
        TEMPLATES / "docs-plan-mode.md": harness / "docs" / "plan-mode.md",
        TEMPLATES / "backlog-index.md": harness / "backlog" / "index.md",
        TEMPLATES / "sql-index.md": harness / "sql" / "index.md",
        TEMPLATES / "AGENTS.md": root / "AGENTS.md",
        TEMPLATES / "pytest.ini": root / "pytest.ini",
    }

    for src, dst in text_templates.items():
        if not src.is_file():
            print(f"warn: missing template {src}", file=sys.stderr)
            continue
        content = _substitute(src.read_text(encoding="utf-8"), mapping)
        _write_if_missing(dst, content, force=force, dry_run=dry_run)

    backlog_files = {
        harness / "backlog" / "archive.md": "# 历史周任务\n\n（跨周归档自 todo.md）\n",
        harness / "backlog" / "decisions-archive.md": "# 已归档决策\n\n",
    }
    for path, content in backlog_files.items():
        _write_if_missing(path, content, force=force, dry_run=dry_run)

    tests_gitkeep = harness / "tests" / ".gitkeep"
    if not tests_gitkeep.exists() or force:
        if dry_run:
            print(f"would write: {tests_gitkeep}")
        else:
            tests_gitkeep.parent.mkdir(parents=True, exist_ok=True)
            tests_gitkeep.write_text("", encoding="utf-8")
            print(f"wrote: {tests_gitkeep}")

    for name in ("lint_src.py", "sync_progress.py", "archive_harness_todo.py"):
        src = BUNDLED_SCRIPTS / name
        dst = harness / "scripts" / name
        if src.is_file():
            _copy_if_missing(src, dst, force=force, dry_run=dry_run)
        else:
            print(f"warn: bundled script missing {src}", file=sys.stderr)

    _ensure_gitignore(root, dry_run=dry_run)

    if not dry_run and not skip_sync:
        _run_sync_progress(root, dry_run=dry_run)

    if dry_run:
        return []
    return verify_harness(root)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold standard agent harness in a repository.",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--project-name", default=None, help="Project display name (default: folder name)")
    parser.add_argument("--src-dir", default="src")
    parser.add_argument("--dev-branch", default="dev")
    parser.add_argument("--test-branch", default="test")
    parser.add_argument("--lint-cmd", default=PLACEHOLDER_DEFAULTS["LINT_CMD"])
    parser.add_argument("--pytest-cmd", default=PLACEHOLDER_DEFAULTS["PYTEST_CMD"])
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-sync", action="store_true", help="Skip post-init sync_progress.py")
    args = parser.parse_args()

    root = args.root.resolve()
    project_name = args.project_name or root.name

    missing = init_harness(
        root,
        project_name=project_name,
        src_dir=args.src_dir,
        dev_branch=args.dev_branch,
        test_branch=args.test_branch,
        lint_cmd=args.lint_cmd,
        pytest_cmd=args.pytest_cmd,
        force=args.force,
        dry_run=args.dry_run,
        skip_sync=args.skip_sync,
    )

    if args.dry_run:
        return 0

    if missing:
        print("\nVERIFY FAILED — missing:", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 1

    print("\nVERIFY OK — harness scaffold complete.")
    print("Next: install companion skills (tdd, code-review-expert, code-simplifier).")
    print("Playbook: AGENTS.md | Index: harness/index.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
