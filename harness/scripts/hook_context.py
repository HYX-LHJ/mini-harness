"""Build host-specific SessionStart context for active mini-harness repositories."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CONTEXT = """本仓库已启用 mini-harness。

开始工作前，请先阅读项目根目录 `AGENTS.md`（Agent Harness Playbook），再阅读 `harness/PROGRESS.md` 与 `harness/todo.md`。
若 todo 含运行时代码任务且「AC 已确认」未勾选，须先与用户核对 AC，不得启动 TDD 或编写实现。
不要仅因本提醒被注入就修改文件。
"""


def _is_active(root: Path) -> bool:
    marker = root / "harness" / ".mini-harness.json"
    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False
    return isinstance(payload, dict) and payload.get("active") is True


def build_output(host: str, root: str | Path) -> dict[str, Any]:
    """Return the context envelope expected by the selected host."""
    root_path = Path(root).resolve()
    if not _is_active(root_path):
        return {}
    if host in {"claude", "codex"}:
        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": CONTEXT,
            }
        }
    if host == "cursor":
        return {"additional_context": CONTEXT}
    raise ValueError(f"不支持的宿主: {host}")


def _root_from_input(raw: str) -> Path:
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if isinstance(payload, dict):
        for key in ("cwd", "workspace_root", "workspaceRoot"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return Path(value)
    return Path.cwd()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, choices=("claude", "codex", "cursor"))
    args = parser.parse_args()
    output = build_output(args.host, _root_from_input(sys.stdin.read()))
    payload = json.dumps(output, ensure_ascii=False) + "\n"
    if hasattr(sys.stdout, "buffer"):
        sys.stdout.buffer.write(payload.encode("utf-8"))
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
