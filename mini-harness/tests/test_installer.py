from __future__ import annotations

import importlib.util
import json
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def test_install_initializes_generic_harness(installer, tmp_path: Path) -> None:
    result = installer.install(tmp_path)

    assert result["changed"] is True
    skill = tmp_path / "harness" / "skills" / "using-harness" / "SKILL.md"
    assert skill.is_file()
    assert "硬约束" in skill.read_text(encoding="utf-8")
    assert not (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / "harness" / "PROGRESS.md").is_file()
    marker = json.loads((tmp_path / "harness" / ".mini-harness.json").read_text(encoding="utf-8"))
    assert marker["active"] is True
    assert marker["template_version"] == "0.4.0"
    assert marker["commands"]["gate"] == []
    assert "agents_mode" not in marker


def test_install_copies_skills_scripts_and_package(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)

    assert (tmp_path / "tests" / "README.md").is_file()
    assert not (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / "harness" / "skills" / "using-harness" / "SKILL.md").is_file()
    assert (tmp_path / "harness" / "skills" / "brainstorming" / "SKILL.md").is_file()
    assert (tmp_path / "harness" / "scripts" / "mini_harness.py").is_file()
    assert (tmp_path / "harness" / "rules" / "python-coding-conventions.md").is_file()
    assert (tmp_path / "harness" / "acceptance" / "index.md").is_file()
    assert (tmp_path / "harness" / "skills" / "acceptance-verification" / "SKILL.md").is_file()
    assert (tmp_path / "harness" / ".package" / "skills" / "tdd" / "SKILL.md").is_file()
    assert (tmp_path / "harness" / ".package" / "rules" / "python-coding-conventions.md").is_file()
    assert not (tmp_path / "harness" / ".package" / "AGENTS.md").exists()
    assert not (tmp_path / "harness" / "AGENTS.md").exists()


def test_repo_local_installer_can_update(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)
    script_path = tmp_path / "harness" / "scripts" / "mini_harness.py"
    spec = importlib.util.spec_from_file_location("repo_mini_harness", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    second = module.install(tmp_path)

    assert second["changed"] is False
    assert module.doctor(tmp_path)["ok"] is True


def test_install_preserves_existing_agents_and_is_idempotent(installer, tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# Existing rules\n\nKeep this.\n", encoding="utf-8")

    first = installer.install(tmp_path)
    first_text = agents.read_text(encoding="utf-8")
    second = installer.install(tmp_path)

    assert first["changed"] is True
    assert second["changed"] is False
    assert first_text == agents.read_text(encoding="utf-8")
    assert first_text == "# Existing rules\n\nKeep this.\n"
    assert (tmp_path / "harness" / "PROGRESS.md").is_file()


def test_install_does_not_overwrite_existing_project_extension(installer, tmp_path: Path) -> None:
    extension = tmp_path / "harness" / "docs" / "project-notes.md"
    extension.parent.mkdir(parents=True)
    extension.write_text("project-owned", encoding="utf-8")

    installer.install(tmp_path)

    assert extension.read_text(encoding="utf-8") == "project-owned"


def test_update_refreshes_unmodified_managed_files(installer, monkeypatch, tmp_path: Path) -> None:
    installer.install(tmp_path)
    progress = tmp_path / "harness" / "PROGRESS.md"
    original_render = installer._render
    monkeypatch.setattr(
        installer,
        "_render",
        lambda text: original_render(text).replace(
            "初始化 mini-harness",
            "已更新初始化 mini-harness",
        ),
    )

    result = installer.install(tmp_path)

    assert result["changed"] is True
    assert "已更新初始化 mini-harness" in progress.read_text(encoding="utf-8")


def test_update_preserves_modified_managed_files(installer, monkeypatch, tmp_path: Path) -> None:
    installer.install(tmp_path)
    progress = tmp_path / "harness" / "PROGRESS.md"
    progress.write_text("# Project-owned progress\n", encoding="utf-8")
    original_render = installer._render
    monkeypatch.setattr(
        installer,
        "_render",
        lambda text: original_render(text).replace(
            "初始化 mini-harness",
            "已更新初始化 mini-harness",
        ),
    )

    installer.install(tmp_path)

    assert progress.read_text(encoding="utf-8") == "# Project-owned progress\n"


def test_plugin_install_force_syncs_modified_skill_bundle(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)
    skill = tmp_path / "harness" / "skills" / "using-harness" / "SKILL.md"
    skill.write_text("# tampered\n", encoding="utf-8")
    canonical = (PLUGIN_ROOT / "skills" / "using-harness" / "SKILL.md").read_text(encoding="utf-8")

    installer.install(tmp_path)

    assert skill.read_text(encoding="utf-8") == canonical


def test_doctor_reports_healthy_install(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)

    report = installer.doctor(tmp_path)

    assert report["ok"] is True
    assert report["issues"] == []
    assert report["warnings"] == []


def test_doctor_reports_missing_rules(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)
    (tmp_path / "harness" / "rules" / "index.md").unlink()

    report = installer.doctor(tmp_path)

    assert report["ok"] is False
    assert any("harness/rules/index.md" in issue for issue in report["issues"])


def test_doctor_warns_on_package_drift(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)
    skill = tmp_path / "harness" / "skills" / "tdd" / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    report = installer.doctor(tmp_path)

    assert report["ok"] is True
    assert any("harness/skills/tdd/SKILL.md" in warning for warning in report["warnings"])
    assert any("update" in warning for warning in report["warnings"])


def test_install_supports_unicode_and_space_paths(installer, tmp_path: Path) -> None:
    repository = tmp_path / "示例 repository"

    installer.install(repository)

    assert installer.doctor(repository)["ok"] is True


def test_uninstall_removes_managed_content_and_preserves_project_files(installer, tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# Existing rules\n\nKeep this.\n", encoding="utf-8")
    installer.install(tmp_path)
    project_file = tmp_path / "harness" / "docs" / "project-notes.md"
    project_file.write_text("project-owned", encoding="utf-8")

    result = installer.uninstall(tmp_path)

    assert result["changed"] is True
    assert agents.read_text(encoding="utf-8") == "# Existing rules\n\nKeep this.\n"
    assert project_file.read_text(encoding="utf-8") == "project-owned"
    assert not (tmp_path / "harness" / ".mini-harness.json").exists()


def test_install_migrates_legacy_harness_agents(installer, tmp_path: Path) -> None:
    marker = tmp_path / "harness" / ".mini-harness.json"
    marker.parent.mkdir(parents=True)
    marker.write_text(
        json.dumps(
            {
                "active": True,
                "template_version": "0.3.0",
                "agents_mode": "created",
                "managed_files": ["AGENTS.md", "harness/PROGRESS.md"],
                "managed_hashes": {},
            }
        ),
        encoding="utf-8",
    )
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# Agent Harness Playbook\n", encoding="utf-8")
    package_agents = tmp_path / "harness" / ".package" / "AGENTS.md"
    package_agents.parent.mkdir(parents=True)
    package_agents.write_text("# Agent Harness Playbook\n", encoding="utf-8")

    installer.install(tmp_path)

    assert not agents.exists()
    assert not package_agents.exists()
    assert (tmp_path / "harness" / "skills" / "using-harness" / "SKILL.md").is_file()


def test_install_removes_legacy_playbook_agents_by_fingerprint(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# Agent Harness Playbook\n\nOld content.\n", encoding="utf-8")

    installer.install(tmp_path)

    assert not agents.exists()


def test_repo_installer_force_syncs_scripts_from_package(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)
    repo_script = tmp_path / "harness" / "scripts" / "mini_harness.py"
    canonical = repo_script.read_text(encoding="utf-8")
    repo_script.write_text("# stale\ndef _install_root_playbook():\n    pass\n", encoding="utf-8")

    installer.install(tmp_path, script_file=repo_script)

    assert repo_script.read_text(encoding="utf-8") == canonical


def test_doctor_warns_on_legacy_root_agents(installer, tmp_path: Path) -> None:
    installer.install(tmp_path)
    (tmp_path / "AGENTS.md").write_text("# Agent Harness Playbook\n", encoding="utf-8")

    report = installer.doctor(tmp_path)

    assert any("AGENTS.md" in warning for warning in report["warnings"])
