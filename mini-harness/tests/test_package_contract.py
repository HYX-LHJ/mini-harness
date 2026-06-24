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
    "goal-md",
    "using-harness",
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
    assert {manifest["version"] for manifest in parsed} == {"2.2.1"}
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
    skill_roots = list((PLUGIN_ROOT / "skills").glob("*/SKILL.md"))
    skill_roots.extend((PLUGIN_ROOT / "skills" / "using-harness" / "references").glob("*.md"))
    for skill_file in skill_roots:
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


def test_three_host_manifests_point_at_bundled_skills() -> None:
    manifests = [
        PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
        PLUGIN_ROOT / ".cursor-plugin" / "plugin.json",
    ]
    for path in manifests:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        skills_dir = (PLUGIN_ROOT / manifest["skills"].removeprefix("./")).resolve()
        assert skills_dir.is_dir()
        assert (skills_dir / "using-harness" / "SKILL.md").is_file()
        for skill_name in EXPECTED_SKILLS:
            assert (skills_dir / skill_name / "SKILL.md").is_file()


def test_playbook_covers_ac_contract_archival_and_harness_skills() -> None:
    skill = (PLUGIN_ROOT / "skills" / "using-harness" / "SKILL.md").read_text(encoding="utf-8")
    workflow = (PLUGIN_ROOT / "skills" / "using-harness" / "references" / "workflow.md").read_text(
        encoding="utf-8"
    )
    entry_required = (
        "开场",
        "路径",
        "硬约束",
        "references/workflow.md",
        "harness/skills/",
        "~/.agents/skills/",
    )
    detail_required = (
        "AC 已确认",
        "任务归档",
        "harness/backlog/",
        "并行规则",
    )
    missing_entry = [phrase for phrase in entry_required if phrase not in skill]
    missing_detail = [phrase for phrase in detail_required if phrase not in workflow]
    assert missing_entry == [], f"SKILL.md missing: {missing_entry}"
    assert missing_detail == [], f"workflow.md missing: {missing_detail}"


def test_template_todo_includes_ac_confirmation_block() -> None:
    todo = (PLUGIN_ROOT / "assets" / "harness-template" / "harness" / "todo.md").read_text(
        encoding="utf-8"
    )
    assert "### AC 核对" in todo
    assert "**AC 已确认**" in todo


def test_repo_marketplaces_enable_one_click_plugin_install() -> None:
    repo_root = PLUGIN_ROOT.parent
    cursor_marketplace = json.loads(
        (repo_root / ".cursor-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    claude_marketplace = json.loads(
        (repo_root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    codex_marketplace = json.loads(
        (repo_root / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    )

    for marketplace in (cursor_marketplace, claude_marketplace):
        assert marketplace["name"] == "mini-harness"
        assert marketplace["owner"]["name"]
        assert len(marketplace["plugins"]) == 1
        entry = marketplace["plugins"][0]
        assert entry["name"] == "mini-harness"
        assert entry["source"] == "./mini-harness"

    codex_entry = codex_marketplace["plugins"][0]
    assert codex_entry["name"] == "mini-harness"
    assert codex_entry["source"]["path"] == "./mini-harness"
    assert codex_entry["policy"]["installation"] == "AVAILABLE"


def test_mini_harness_skill_documents_canonical_plugin_root() -> None:
    text = (PLUGIN_ROOT / "skills" / "using-harness" / "SKILL.md").read_text(encoding="utf-8")
    assert "开场" in text
    assert "硬约束" in text
    assert "references/workflow.md" in text
    assert "references/lifecycle.md" in text
    assert "工作流入口" in text
