from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("host", ["claude", "codex", "cursor"])
def test_inactive_repository_returns_no_context(hook_context, host: str, tmp_path: Path) -> None:
    assert hook_context.build_output(host, tmp_path) == {}


@pytest.mark.parametrize("host", ["claude", "codex"])
def test_claude_and_codex_emit_hook_specific_context(hook_context, host: str, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text(json.dumps({"active": True}), encoding="utf-8")

    output = hook_context.build_output(host, tmp_path)

    specific = output["hookSpecificOutput"]
    assert specific["hookEventName"] == "SessionStart"
    assert "AGENTS.md" in specific["additionalContext"]
    assert "mini-harness skill" in specific["additionalContext"]
    assert "harness/skills/mini-harness/SKILL.md" in specific["additionalContext"]
    assert "harness/PROGRESS.md" in specific["additionalContext"]


def test_cursor_emits_additional_context(hook_context, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text(json.dumps({"active": True}), encoding="utf-8")

    output = hook_context.build_output("cursor", tmp_path)

    assert "AGENTS.md" in output["additional_context"]
    assert "mini-harness skill" in output["additional_context"]


def test_disabled_marker_returns_no_context(hook_context, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text(json.dumps({"active": False}), encoding="utf-8")

    assert hook_context.build_output("codex", tmp_path) == {}


def test_invalid_marker_fails_open(hook_context, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text("{broken", encoding="utf-8")

    assert hook_context.build_output("claude", tmp_path) == {}


@pytest.mark.parametrize(
    ("host", "context_key"),
    [
        ("claude", "hookSpecificOutput"),
        ("codex", "hookSpecificOutput"),
        ("cursor", "additional_context"),
    ],
)
def test_host_entrypoint_emits_valid_json(host: str, context_key: str, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text(json.dumps({"active": True}), encoding="utf-8")
    script = Path(__file__).resolve().parents[1] / "hooks" / host / "session_start.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps({"cwd": str(tmp_path)}),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0
    assert context_key in json.loads(result.stdout)
