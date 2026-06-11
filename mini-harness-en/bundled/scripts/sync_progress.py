"""Refresh mechanical sections of harness/PROGRESS.md (git, gates, todo progress).

Keeps ``## Current state``, ``## Known issues``, ``## Next steps`` hand-written by the Main Agent;
syncs the rest from git / gate commands / todo.md.

Usage (from repository root)::

    .venv\\Scripts\\python.exe harness/scripts/sync_progress.py
    .venv\\Scripts\\python.exe harness/scripts/sync_progress.py --dry-run
    .venv\\Scripts\\python.exe harness/scripts/sync_progress.py --skip-gates

Examples:
    Input: working tree has uncommitted changes and pytest 140 passed
    Output: PROGRESS.md sections Latest git info, Test status, lint, Completed, In progress updated
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from archive_harness_todo import sync_progress_from_todo

PROGRESS_PATH = ROOT / "harness" / "PROGRESS.md"
LINT_SCRIPT = ROOT / "harness" / "scripts" / "lint_src.py"
VENV_PYTHON = ROOT / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
HARNESS_PYTEST_TMP = ROOT / "harness" / ".pytest-tmp"

GIT_SECTION = re.compile(r"(?ms)^(## Latest git info)\n\n.*?(?=^## )")
TEST_SECTION = re.compile(r"(?ms)^(## Test status)\n\n.*?(?=^## )")
LINT_SECTION = re.compile(r"(?ms)^(## lint)\n\n.*?(?=^## )")


def _run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _python_exe() -> str:
    if VENV_PYTHON.is_file():
        return str(VENV_PYTHON)
    return sys.executable


def collect_git_info() -> tuple[str, str, str]:
    """Return (branch line, latest commit, working tree summary)."""
    status = _run(["git", "status", "-sb"])
    status_line = (status.stdout or "").strip().splitlines()
    branch = status_line[0] if status_line else "(unable to read git status)"
    if branch.startswith("## "):
        branch = branch[3:]
    elif branch.startswith("# "):
        branch = branch[2:]

    log = _run(["git", "log", "-1", "--oneline"])
    latest = (log.stdout or "").strip() or "(no commits)"

    if status.returncode != 0:
        workspace = "(git status failed)"
    else:
        dirty = [ln for ln in status_line[1:] if ln.strip()]
        if not dirty:
            workspace = "No uncommitted changes"
        else:
            stat = _run(["git", "diff", "--stat"])
            if (stat.stdout or "").strip():
                workspace = "Uncommitted changes; `git diff --stat` summary:\n\n```\n" + stat.stdout.strip() + "\n```"
            else:
                paths = []
                for ln in dirty:
                    parts = ln.strip().split(maxsplit=1)
                    if len(parts) == 2:
                        paths.append(parts[1])
                workspace = "Uncommitted changes: " + ", ".join(paths[:12])
                if len(paths) > 12:
                    workspace += f" (+{len(paths) - 12} more)"

    return branch, latest, workspace


def extract_pytest_summary(output: str, *, returncode: int) -> str:
    """Extract final pytest terminal summary; avoid matching error diagnostic lines."""
    summary_pattern = re.compile(
        r"^=+\s+.*\b(?:passed|failed|error|errors|skipped|deselected)\b.*\s+=+$",
        re.IGNORECASE,
    )
    for raw_line in reversed(output.splitlines()):
        line = raw_line.strip()
        if summary_pattern.match(line):
            return line
    return f"exit {returncode}"


def pytest_command(py: str) -> list[str]:
    """Build pytest command; disable cache to avoid local cache permission differences."""
    return [
        py,
        "-m",
        "pytest",
        "-p",
        "no:cacheprovider",
    ]


def pytest_temp_root() -> Path:
    """Temp directory for a single pytest subprocess (under ``harness/.pytest-tmp``)."""
    return HARNESS_PYTEST_TMP / f"run-{os.getpid()}-{uuid4().hex}"


def cleanup_pytest_temp(temp_root: Path) -> None:
    """Remove pytest temp directory; fail silently (do not mask pytest exit code)."""
    shutil.rmtree(temp_root, ignore_errors=True)


def pytest_env(temp_root: Path | None = None) -> dict[str, str]:
    """Build pytest subprocess env; Temp fixed under harness to avoid system Temp permission issues."""
    root = temp_root or pytest_temp_root()
    root.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    temp_text = str(root)
    env["TMP"] = temp_text
    env["TEMP"] = temp_text
    env["PYTEST_DEBUG_TEMPROOT"] = temp_text
    return env


def collect_gate_results(*, skip_gates: bool) -> tuple[str, str]:
    """Return (test status bullet, lint bullet)."""
    today = date.today().isoformat()
    if skip_gates:
        return (
            f"- (not run; `--skip-gates`)",
            f"- (not run; `--skip-gates`)",
        )

    py = _python_exe()
    lint_proc = _run([py, str(LINT_SCRIPT)])
    lint_ok = lint_proc.returncode == 0
    lint_line = (
        f"- `harness/scripts/lint_src.py`: ruff + pyright **passed**, 0 errors ({today}, `src/` only)"
        if lint_ok
        else f"- `harness/scripts/lint_src.py`: **failed** exit {lint_proc.returncode} ({today})"
    )

    temp_root = pytest_temp_root()
    try:
        pytest_proc = _run(pytest_command(py), cwd=ROOT, env=pytest_env(temp_root))
    finally:
        cleanup_pytest_temp(temp_root)
    summary = extract_pytest_summary(pytest_proc.stdout or "", returncode=pytest_proc.returncode)
    test_line = f"- `pytest` (unit tests): **{summary}** ({today})"

    return test_line, lint_line


def format_git_section(branch: str, latest: str, workspace: str) -> str:
    body = (
        f"- **Branch**: `{branch}`\n"
        f"- **Latest commit**: `{latest}`\n"
        f"- **Working tree**: {workspace}\n"
    )
    return f"## Latest git info\n\n{body}\n"


def format_test_section(test_line: str) -> str:
    intro = "- **Unit tests** (`harness/tests/`, gate scope):"
    return f"## Test status\n\n{intro}\n\n{test_line}\n\n"


def format_lint_section(lint_line: str) -> str:
    return f"## lint\n\n{lint_line}\n\n"


def replace_section(progress: str, pattern: re.Pattern[str], replacement: str) -> str:
    if not pattern.search(progress):
        msg = f"PROGRESS.md missing section for pattern {pattern.pattern[:40]}"
        raise ValueError(msg)
    return pattern.sub(replacement, progress, count=1)


def sync_progress(*, dry_run: bool = False, skip_gates: bool = False) -> None:
    """Sync PROGRESS mechanical sections and todo → Completed/In progress."""
    if not dry_run:
        sync_progress_from_todo()

    progress = PROGRESS_PATH.read_text(encoding="utf-8")
    branch, latest, workspace = collect_git_info()
    test_line, lint_line = collect_gate_results(skip_gates=skip_gates)

    progress = replace_section(progress, GIT_SECTION, format_git_section(branch, latest, workspace))
    progress = replace_section(progress, TEST_SECTION, format_test_section(test_line))
    progress = replace_section(progress, LINT_SECTION, format_lint_section(lint_line))

    if dry_run:
        print(progress, file=sys.stderr)
    else:
        PROGRESS_PATH.write_text(progress, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync mechanical sections of harness/PROGRESS.md")
    parser.add_argument("--dry-run", action="store_true", help="Print merged PROGRESS to stderr; do not write")
    parser.add_argument(
        "--skip-gates",
        action="store_true",
        help="Skip lint/pytest (only refresh git + todo sections)",
    )
    args = parser.parse_args()

    sync_progress(dry_run=args.dry_run, skip_gates=args.skip_gates)
    if not args.dry_run:
        print(f"Updated {PROGRESS_PATH.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
