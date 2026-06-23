from __future__ import annotations

import json
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EXPECTED_SKILLS = {
    "acceptance-verification",
    "brainstorming",
    "code-review-expert",
    "code-simplifier",
    "mini-harness",
    "python-code-style",
    "python-testing-patterns",
    "tdd",
}


def test_three_host_manifests_share_identity_and_components() -> None:
    manifests = [
        PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
        PLUGIN_ROOT / ".cursor-plugin" / "plugin.json",
    ]

    parsed = [json.loads(path.read_text(encoding="utf-8")) for path in manifests]

    assert {manifest["name"] for manifest in parsed} == {"mini-harness"}
    assert {manifest["version"] for manifest in parsed} == {"0.1.0"}
    assert all(manifest.get("description") for manifest in parsed)


def test_shared_skills_follow_agent_skills_contract() -> None:
    skills_root = PLUGIN_ROOT / "skills"
    skill_dirs = {path.name for path in skills_root.iterdir() if path.is_dir()}
    assert skill_dirs == EXPECTED_SKILLS

    for skill_name in EXPECTED_SKILLS:
        assert SKILL_NAME.fullmatch(skill_name)
        text = (skills_root / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert f"name: {skill_name}" in text
        assert "description:" in text


def test_template_is_generic_and_contains_no_project_residue() -> None:
    template_root = PLUGIN_ROOT / "assets" / "harness-template"
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace") for path in template_root.rglob("*") if path.is_file()
    ).lower()

    forbidden = [
        "img_flow",
        "gemini",
        "minio",
        "ai_image_",
        "businessid",
        "e:\\img_flow",
        "origin/dev",
    ]
    assert [term for term in forbidden if term in text] == []


def test_all_skill_markdown_links_resolve() -> None:
    markdown_link = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
    missing: list[str] = []
    for skill_file in (PLUGIN_ROOT / "skills").glob("*/SKILL.md"):
        text = skill_file.read_text(encoding="utf-8")
        for match in markdown_link.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (skill_file.parent / target).exists():
                missing.append(f"{skill_file.relative_to(PLUGIN_ROOT)} -> {target}")

    assert missing == []


def test_hook_configs_reference_host_specific_session_start_scripts() -> None:
    expected = [
        (PLUGIN_ROOT / "hooks" / "claude" / "hooks.json", "SessionStart", "hooks/claude/session_start.py"),
        (PLUGIN_ROOT / "hooks" / "hooks.json", "SessionStart", "hooks/codex/session_start.py"),
        (PLUGIN_ROOT / "hooks" / "cursor" / "hooks.json", "sessionStart", "hooks/cursor/session_start.py"),
    ]
    for path, event, script in expected:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert event in payload["hooks"]
        assert script in path.read_text(encoding="utf-8").replace("\\", "/")


def test_playbook_covers_ac_contract_archival_and_harness_skills() -> None:
    text = (PLUGIN_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    required = (
        "AC 已确认",
        "任务归档",
        "harness/backlog/",
        "harness/skills/",
        "~/.agents/skills/",
        "并行规则",
    )
    missing = [phrase for phrase in required if phrase not in text]
    assert missing == [], f"AGENTS.md missing: {missing}"


def test_template_todo_includes_ac_confirmation_block() -> None:
    todo = (PLUGIN_ROOT / "assets" / "harness-template" / "harness" / "todo.md").read_text(
        encoding="utf-8"
    )
    assert "### AC 核对" in todo
    assert "**AC 已确认**" in todo


def test_mini_harness_skill_documents_canonical_plugin_root() -> None:
    text = (PLUGIN_ROOT / "skills" / "mini-harness" / "SKILL.md").read_text(encoding="utf-8")
    assert "唯一权威源" in text
    assert "mini-harness/" in text
