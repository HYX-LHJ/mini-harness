"""goal-md integration coherence — docs, paths, and package contract."""

from __future__ import annotations

import json
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parent
TEMPLATE = PLUGIN_ROOT / "assets" / "harness-template" / "harness"

HARNESS_GOAL_PREFIX = "harness/goal/"

DOC_MUST_CONTAIN: list[tuple[str, tuple[str, ...]]] = [
    ("mini-harness/skills/using-harness/SKILL.md", ("goal-md", "harness/goal")),
    ("mini-harness/skills/using-harness/references/workflow.md", ("harness/goal", "goal-md")),
    ("mini-harness/assets/harness-template/harness/docs/skills.md", ("harness/goal", "goal-md")),
    ("docs/zh-CN/workflow.md", ("harness/goal",)),
    ("docs/en/workflow.md", ("harness/goal",)),
    ("docs/zh-CN/getting-started.md", ("harness/goal",)),
    ("docs/en/getting-started.md", ("harness/goal",)),
    ("docs/zh-CN/architecture.md", ("harness/goal", "goal-md")),
    ("docs/en/architecture.md", ("harness/goal", "goal-md")),
    ("mini-harness/skills/goal-md/SKILL.md", ("harness/goal",)),
]

GOAL_AC_EXEMPTION_MARKERS = (
    "harness/goal/iterations.jsonl",
    "元任务",
    "meta",
)

FORBIDDEN_GOAL_PATHS = (
    "仓库根 `GOAL.md`",
    "repo-root `GOAL.md`",
    "root / \"GOAL.md\"",
    'root / "GOAL.md"',
    "scripts/score.py",
)

FORBIDDEN_RESIDUE = ("e:\\img_flow", "e:/img_flow")


def test_goal_md_listed_in_package_contract() -> None:
    from test_package_contract import EXPECTED_SKILLS

    assert "goal-md" in EXPECTED_SKILLS


def test_doc_files_mention_harness_goal_paths() -> None:
    missing: list[str] = []
    for rel, needles in DOC_MUST_CONTAIN:
        path = REPO_ROOT / rel
        assert path.is_file(), f"missing file: {rel}"
        text = path.read_text(encoding="utf-8")
        if not any(n in text for n in needles):
            missing.append(f"{rel} needs one of {needles}")
    assert missing == [], "\n".join(missing)


def test_workflow_documents_goal_ac_exemption() -> None:
    workflow = (PLUGIN_ROOT / "skills/using-harness/references/workflow.md").read_text(encoding="utf-8")
    assert HARNESS_GOAL_PREFIX in workflow
    assert any(m in workflow for m in GOAL_AC_EXEMPTION_MARKERS), (
        "workflow must state GOAL uses harness/goal/iterations.jsonl / meta-task"
    )


def test_skill_docs_do_not_place_goal_at_repo_root() -> None:
    paths = [
        PLUGIN_ROOT / "skills/goal-md/SKILL.md",
        PLUGIN_ROOT / "skills/goal-md/references/harness-integration.md",
        PLUGIN_ROOT / "skills/goal-md/scripts/init_goal.py",
    ]
    violations: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_GOAL_PATHS:
            if forbidden in text:
                violations.append(f"{path.relative_to(PLUGIN_ROOT)} contains {forbidden!r}")
    assert violations == [], "\n".join(violations)


def test_harness_template_indexes_goal_directory() -> None:
    index = (TEMPLATE / "index.md").read_text(encoding="utf-8")
    assert "[goal/](goal/)" in index or "goal/" in index
    assert (TEMPLATE / "goal" / "index.md").is_file()


def test_init_goal_targets_harness_goal() -> None:
    init = (PLUGIN_ROOT / "skills/goal-md/scripts/init_goal.py").read_text(encoding="utf-8")
    assert "harness/goal" in init
    assert "harness/" in init and "not found" in init


def test_goal_md_skill_paths_cover_plugin_and_harness() -> None:
    skill = (PLUGIN_ROOT / "skills/goal-md/SKILL.md").read_text(encoding="utf-8")
    assert "harness/skills/goal-md" in skill
    assert "skills/goal-md" in skill


def test_examples_avoid_private_project_paths() -> None:
    examples = (PLUGIN_ROOT / "skills/goal-md/references/examples.md").read_text(encoding="utf-8")
    hits = [term for term in FORBIDDEN_RESIDUE if term in examples]
    assert hits == [], f"examples.md must not reference private paths: {hits}"


def test_examples_reference_harness_goal() -> None:
    examples = (PLUGIN_ROOT / "skills/goal-md/references/examples.md").read_text(encoding="utf-8")
    assert "harness/goal" in examples


def test_goal_md_markdown_links_resolve() -> None:
    link = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
    skill_root = PLUGIN_ROOT / "skills" / "goal-md"
    missing: list[str] = []
    for md in skill_root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for match in link.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (md.parent / target).exists():
                missing.append(f"{md.relative_to(PLUGIN_ROOT)} -> {target}")
    assert missing == []


def test_three_host_manifests_include_goal_md() -> None:
    for host in (".claude-plugin", ".codex-plugin", ".cursor-plugin"):
        manifest = json.loads((PLUGIN_ROOT / host / "plugin.json").read_text(encoding="utf-8"))
        skills_dir = (PLUGIN_ROOT / manifest["skills"].removeprefix("./")).resolve()
        assert (skills_dir / "goal-md" / "SKILL.md").is_file()
