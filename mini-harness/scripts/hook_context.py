"""Build host-specific SessionStart context for mini-harness plugin sessions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CONTEXT_ACTIVE = """本仓库已启用 mini-harness。

开始任何用户任务前，必须先调用 using-harness skill：
1. 阅读 `harness/skills/using-harness/SKILL.md`（工作流入口）
2. 需要逐步操作时阅读 `harness/skills/using-harness/references/workflow.md`
3. 并行阅读 `harness/PROGRESS.md` 与 `harness/todo.md`

若 todo 含运行时代码任务且「AC 已确认」未勾选，须先与用户核对 AC，不得启动 TDD 或编写实现。
不要仅因本提醒被注入就修改文件。
"""

CONTEXT_PLUGIN_ONLY = """已安装 mini-harness 插件；本仓库尚未执行 harness install（无 `harness/.mini-harness.json`）。

开始任何用户任务前，先调用 **using-harness skill**：
1. 阅读插件内 `skills/using-harness/SKILL.md`（工作流入口）
2. 细则见同目录 `references/workflow.md`

若任务需要 todo、PROGRESS、AC 归档等持久状态，须先在仓库根执行 install（`python mini-harness/scripts/mini_harness.py install --root .`，或请用户授权）。

不要仅因本提醒被注入就修改文件。
"""


def build_output(host: str, root: str | Path) -> dict[str, Any]:
    """Return the context envelope expected by the selected host."""
    root_path = Path(root).resolve()
    marker = root_path / "harness" / ".mini-harness.json"
    if marker.is_file():
        try:
            payload = json.loads(marker.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
        context = CONTEXT_ACTIVE if isinstance(payload, dict) and payload.get("active") is True else CONTEXT_PLUGIN_ONLY
    else:
        context = CONTEXT_PLUGIN_ONLY

    if host in {"claude", "codex"}:
        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }
    if host == "cursor":
        return {"additional_context": context}
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
