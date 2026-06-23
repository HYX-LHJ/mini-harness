from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("host", ["claude", "codex", "cursor"])
def test_inactive_repository_emits_plugin_only_context(hook_context, host: str, tmp_path: Path) -> None:
    output = hook_context.build_output(host, tmp_path)
    if host == "cursor":
        text = output["additional_context"]
    else:
        text = output["hookSpecificOutput"]["additionalContext"]
    assert "using-harness skill" in text
    assert "skills/using-harness/SKILL.md" in text
    assert "references/workflow.md" in text
    assert "尚未执行 harness install" in text


@pytest.mark.parametrize("host", ["claude", "codex"])
def test_claude_and_codex_emit_hook_specific_context(hook_context, host: str, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text(json.dumps({"active": True}), encoding="utf-8")

    output = hook_context.build_output(host, tmp_path)

    specific = output["hookSpecificOutput"]
    assert specific["hookEventName"] == "SessionStart"
    assert "using-harness skill" in specific["additionalContext"]
    assert "harness/skills/using-harness/SKILL.md" in specific["additionalContext"]
    assert "references/workflow.md" in specific["additionalContext"]
    assert "harness/PROGRESS.md" in specific["additionalContext"]
    assert "AGENTS.md" not in specific["additionalContext"]


def test_cursor_emits_additional_context(hook_context, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text(json.dumps({"active": True}), encoding="utf-8")

    output = hook_context.build_output("cursor", tmp_path)

    assert "using-harness skill" in output["additional_context"]
    assert "AGENTS.md" not in output["additional_context"]


def test_disabled_marker_emits_plugin_only_context(hook_context, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text(json.dumps({"active": False}), encoding="utf-8")

    text = hook_context.build_output("codex", tmp_path)["hookSpecificOutput"]["additionalContext"]
    assert "skills/using-harness/SKILL.md" in text


def test_invalid_marker_emits_plugin_only_context(hook_context, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text("{broken", encoding="utf-8")

    text = hook_context.build_output("claude", tmp_path)["hookSpecificOutput"]["additionalContext"]
    assert "skills/using-harness/SKILL.md" in text


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
