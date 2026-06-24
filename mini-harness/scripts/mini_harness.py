"""Install, inspect, update, or remove the generic mini-harness template."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

SCRIPT_FILE = Path(__file__)
PLUGIN_ROOT = SCRIPT_FILE.resolve().parents[1]
TEMPLATE_VERSION = "0.4.0"
MARKER_RELATIVE = Path("harness/.mini-harness.json")
LEGACY_AGENTS_RELATIVE = Path("AGENTS.md")
LEGACY_PACKAGE_PLAYBOOK = Path("harness/.package/AGENTS.md")
LEGACY_SKILL_DIR = Path("harness/skills/mini-harness")
BUNDLE_NAMES = ("skills", "scripts", "rules")
TEMPLATE_BUNDLE = "template"
EXPOSED_BUNDLES = {
    "skills": Path("harness/skills"),
    "scripts": Path("harness/scripts"),
    "rules": Path("harness/rules"),
}


def _render(text: str) -> str:
    return text.replace("{{TODAY}}", date.today().isoformat())


LEGACY_PLAYBOOK_MARKERS = (
    "# Agent Harness Playbook",
    "harness/skills/mini-harness/",
)


def _running_from_repo_harness_scripts(script_file: Path) -> bool:
    resolved = script_file.resolve()
    parent = resolved.parent
    return parent.name == "scripts" and parent.parent.name == "harness"


def _should_force_sync_bundles(script_file: Path) -> bool:
    """Force-sync managed bundles from .package when run from plugin or repo harness/scripts."""
    return _plugin_root(script_file) is not None or _running_from_repo_harness_scripts(script_file)


def _looks_like_harness_playbook_agents(text: str) -> bool:
    return any(marker in text for marker in LEGACY_PLAYBOOK_MARKERS)


def _repo_root_from_script(script_file: Path) -> Path | None:
    """Resolve repository root when invoked via harness/scripts/mini_harness.py."""
    if not _running_from_repo_harness_scripts(script_file):
        return None
    return script_file.resolve().parents[2]


def _plugin_root(script_file: Path) -> Path | None:
    resolved = script_file.resolve()
    parent = resolved.parent
    if parent.name == "scripts" and parent.parent.name == "mini-harness":
        return parent.parent
    return None


def _package_root(repo_root: Path) -> Path:
    return repo_root / "harness" / ".package"


def _template_root(repo_root: Path, script_file: Path) -> Path:
    package_template = _package_root(repo_root) / TEMPLATE_BUNDLE
    if package_template.is_dir():
        return package_template
    plugin = _plugin_root(script_file)
    if plugin:
        return plugin / "assets" / "harness-template"
    msg = "找不到模板：请先通过插件运行 install，或确保 harness/.package/template 存在"
    raise FileNotFoundError(msg)


def _should_skip_bundle_path(relative: Path) -> bool:
    return any(part == "__pycache__" for part in relative.parts) or relative.suffix == ".pyc"


def _iter_relative_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    files = sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())
    return [path for path in files if not _should_skip_bundle_path(path)]


def _mirror_tree(source: Path, destination: Path) -> bool:
    changed = False
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        if _should_skip_bundle_path(relative):
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        if not target.exists() or target.read_bytes() != data:
            target.write_bytes(data)
            changed = True
    return changed


def _refresh_package_mirror(repo_root: Path, script_file: Path) -> bool:
    plugin = _plugin_root(script_file)
    if plugin is None:
        return False
    package = _package_root(repo_root)
    mappings = [
        (plugin / "skills", package / "skills"),
        (plugin / "scripts", package / "scripts"),
        (plugin / "rules", package / "rules"),
        (plugin / "assets" / "harness-template", package / TEMPLATE_BUNDLE),
    ]
    changed = False
    for source, destination in mappings:
        if source.is_dir() and _mirror_tree(source, destination):
            changed = True
    return changed


def _template_files(template_root: Path) -> list[Path]:
    return _iter_relative_files(template_root)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_marker(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _marker_payload(
    *,
    managed_files: list[str],
    managed_hashes: dict[str, str],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "template_version": TEMPLATE_VERSION,
        "active": True,
        "managed_files": sorted(managed_files),
        "managed_hashes": dict(sorted(managed_hashes.items())),
        "commands": {"gate": [], "progress_sync": []},
        "runtime_paths": [],
        "test_paths": [],
    }


def _sync_managed_text_file(
    *,
    root_path: Path,
    relative_name: str,
    desired: str,
    managed_files: set[str],
    managed_hashes: dict[str, str],
    previous_managed: set[str],
    previous_hashes: dict[str, str],
    force: bool = False,
) -> bool:
    changed = False
    target = root_path / relative_name
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(desired, encoding="utf-8")
        managed_files.add(relative_name)
        managed_hashes[relative_name] = _sha256(desired)
        return True

    if relative_name not in previous_managed and not force:
        return False

    current = target.read_text(encoding="utf-8")
    if force or previous_hashes.get(relative_name) == _sha256(current):
        if current != desired:
            target.write_text(desired, encoding="utf-8")
            changed = True
        managed_files.add(relative_name)
        managed_hashes[relative_name] = _sha256(desired)
    return changed


def _read_file_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _sync_managed_tree(
    *,
    root_path: Path,
    source_root: Path,
    dest_prefix: Path,
    managed_files: set[str],
    managed_hashes: dict[str, str],
    previous_managed: set[str],
    previous_hashes: dict[str, str],
    render: Callable[[str], str] | None = None,
    force: bool = False,
) -> bool:
    changed = False
    prefix = dest_prefix.as_posix().rstrip("/")
    for relative in _iter_relative_files(source_root):
        relative_name = f"{prefix}/{relative.as_posix()}"
        raw = _read_file_text(source_root / relative)
        desired = render(raw) if render else raw
        if _sync_managed_text_file(
            root_path=root_path,
            relative_name=relative_name,
            desired=desired,
            managed_files=managed_files,
            managed_hashes=managed_hashes,
            previous_managed=previous_managed,
            previous_hashes=previous_hashes,
            force=force,
        ):
            changed = True
    return changed


def _file_digest(path: Path) -> str:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return hashlib.sha256(data).hexdigest()
    return _sha256(text)


def _register_managed_tree(
    root_path: Path,
    dest_prefix: Path,
    managed_files: set[str],
    managed_hashes: dict[str, str],
) -> None:
    prefix = dest_prefix.as_posix().rstrip("/")
    source_root = root_path / dest_prefix
    for relative in _iter_relative_files(source_root):
        relative_name = f"{prefix}/{relative.as_posix()}"
        content_path = source_root / relative
        managed_files.add(relative_name)
        managed_hashes[relative_name] = _file_digest(content_path)


RETIRED_MANAGED_PREFIXES = (
    "harness/Agents.md",
    "harness/.package/Agents.md",
    "harness/AGENTS.md",
    "harness/.package/AGENTS.md",
    "harness/skills/mini-harness/",
)


def _prune_retired_managed_files(
    root_path: Path,
    managed_files: set[str],
    managed_hashes: dict[str, str],
) -> bool:
    changed = False
    for relative in list(managed_files):
        if not any(relative.startswith(prefix) for prefix in RETIRED_MANAGED_PREFIXES):
            continue
        target = root_path / relative
        if target.is_file():
            target.unlink()
            changed = True
        managed_files.discard(relative)
        managed_hashes.pop(relative, None)
    for prefix in RETIRED_MANAGED_PREFIXES:
        directory = root_path / prefix.rstrip("/")
        if directory.is_dir():
            for path in sorted(directory.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink(missing_ok=True)
            try:
                directory.rmdir()
            except OSError:
                pass
    return changed


def _prune_legacy_playbook_artifacts(
    root_path: Path,
    marker: dict[str, Any],
    managed_files: set[str],
    managed_hashes: dict[str, str],
) -> bool:
    """Remove AGENTS.md playbook files from pre-0.4.0 installs; never touch user-owned AGENTS.md."""
    changed = False
    previous_managed = {str(path) for path in marker.get("managed_files", [])}
    agents_mode = str(marker.get("agents_mode", ""))
    harness_owned_agents = (
        LEGACY_AGENTS_RELATIVE.as_posix() in previous_managed
        or agents_mode in {"created", "managed"}
    )

    for legacy_path in (
        root_path / LEGACY_PACKAGE_PLAYBOOK,
        root_path / "harness" / "AGENTS.md",
        root_path / "harness" / "Agents.md",
        root_path / "harness" / ".package" / "AGENTS.md",
        root_path / "harness" / ".package" / "Agents.md",
    ):
        if legacy_path.is_file():
            legacy_path.unlink()
            changed = True

    agents_path = root_path / LEGACY_AGENTS_RELATIVE
    if agents_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
        if harness_owned_agents or _looks_like_harness_playbook_agents(agents_text):
            agents_path.unlink()
            changed = True

    for rel in (LEGACY_AGENTS_RELATIVE.as_posix(), LEGACY_PACKAGE_PLAYBOOK.as_posix()):
        managed_files.discard(rel)
        managed_hashes.pop(rel, None)
    return changed


def _prune_legacy_skill_directory(
    root_path: Path,
    managed_files: set[str],
    managed_hashes: dict[str, str],
) -> bool:
    """Remove renamed workflow skill directory from pre-0.4.0 installs."""
    changed = False
    legacy = root_path / LEGACY_SKILL_DIR
    if legacy.is_dir():
        shutil.rmtree(legacy)
        changed = True
    prefix = LEGACY_SKILL_DIR.as_posix().rstrip("/")
    for relative in list(managed_files):
        if relative == prefix or relative.startswith(f"{prefix}/"):
            managed_files.discard(relative)
            managed_hashes.pop(relative, None)
    return changed


def install(root: str | Path, *, script_file: Path | None = None) -> dict[str, Any]:
    """Install the template without overwriting repository-owned files."""
    script = script_file or SCRIPT_FILE
    root_path = Path(root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    package_root = _package_root(root_path)

    changed = _refresh_package_mirror(root_path, script)
    template_root = _template_root(root_path, script)

    marker_path = root_path / MARKER_RELATIVE
    previous = _read_marker(marker_path)
    previous_managed = {str(path) for path in previous.get("managed_files", [])}
    previous_hashes = {
        str(path): str(digest)
        for path, digest in previous.get("managed_hashes", {}).items()
        if isinstance(path, str) and isinstance(digest, str)
    }
    managed_files = set(previous_managed)
    managed_hashes = dict(previous_hashes)

    if _prune_retired_managed_files(root_path, managed_files, managed_hashes):
        changed = True
    if _prune_legacy_playbook_artifacts(root_path, previous, managed_files, managed_hashes):
        changed = True
    if _prune_legacy_skill_directory(root_path, managed_files, managed_hashes):
        changed = True

    if _plugin_root(script) is not None and package_root.is_dir():
        for bundle in (*BUNDLE_NAMES, TEMPLATE_BUNDLE):
            bundle_path = package_root / bundle
            if bundle_path.is_dir():
                _register_managed_tree(
                    root_path,
                    Path("harness") / ".package" / bundle,
                    managed_files,
                    managed_hashes,
                )

    sync_from_plugin = _plugin_root(script) is not None
    force_sync_bundles = _should_force_sync_bundles(script)

    for bundle in BUNDLE_NAMES:
        source = package_root / bundle
        exposed = EXPOSED_BUNDLES[bundle]
        if source.is_dir() and _sync_managed_tree(
            root_path=root_path,
            source_root=source,
            dest_prefix=exposed,
            managed_files=managed_files,
            managed_hashes=managed_hashes,
            previous_managed=previous_managed,
            previous_hashes=previous_hashes,
            force=force_sync_bundles,
        ):
            changed = True

    for relative in _template_files(template_root):
        relative_name = relative.as_posix()
        desired = _render((template_root / relative).read_text(encoding="utf-8"))
        if _sync_managed_text_file(
            root_path=root_path,
            relative_name=relative_name,
            desired=desired,
            managed_files=managed_files,
            managed_hashes=managed_hashes,
            previous_managed=previous_managed,
            previous_hashes=previous_hashes,
        ):
            changed = True

    payload = _marker_payload(
        managed_files=sorted(managed_files),
        managed_hashes=managed_hashes,
    )
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if not marker_path.exists() or marker_path.read_text(encoding="utf-8") != serialized:
        marker_path.parent.mkdir(parents=True, exist_ok=True)
        marker_path.write_text(serialized, encoding="utf-8")
        changed = True

    return {"changed": changed, "root": str(root_path), "managed_files": sorted(managed_files)}


def _normalized_text_digest(path: Path) -> str:
    """Hash file text with normalized newlines for cross-platform drift checks."""
    text = path.read_text(encoding="utf-8")
    return _sha256(text.replace("\r\n", "\n").replace("\r", "\n"))


def _collect_package_drift(root_path: Path) -> list[str]:
    """Compare exposed harness bundles with the .package snapshot."""
    warnings: list[str] = []
    package_root = _package_root(root_path)
    if not package_root.is_dir():
        return warnings

    for bundle, exposed in EXPOSED_BUNDLES.items():
        source = package_root / bundle
        if not source.is_dir():
            continue
        for relative in _iter_relative_files(source):
            relative_name = relative.as_posix()
            package_file = source / relative
            exposed_file = root_path / exposed / relative
            exposed_name = f"{exposed.as_posix()}/{relative_name}"
            if not exposed_file.is_file():
                warnings.append(f"缺少 {exposed_name}（.package 快照中存在）；运行 update 同步")
                continue
            if _normalized_text_digest(package_file) != _normalized_text_digest(exposed_file):
                warnings.append(
                    f"{exposed_name} 与 harness/.package/{bundle}/{relative_name} 不一致；"
                    "运行 update 同步"
                )

    return warnings


def doctor(root: str | Path) -> dict[str, Any]:
    """Check whether a repository has a coherent active installation."""
    root_path = Path(root).resolve()
    issues: list[str] = []
    warnings: list[str] = []
    marker_path = root_path / MARKER_RELATIVE

    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        marker = {}
        issues.append("缺少 harness/.mini-harness.json")
    except json.JSONDecodeError:
        marker = {}
        issues.append("harness/.mini-harness.json 格式无效")

    if marker and marker.get("active") is not True:
        issues.append("mini-harness 未激活")

    marker_version = marker.get("template_version")
    if isinstance(marker_version, str) and marker_version and marker_version != TEMPLATE_VERSION:
        warnings.append(
            f"harness/.mini-harness.json 的 template_version 为 {marker_version}，"
            f"当前安装脚本为 {TEMPLATE_VERSION}；运行 update 同步"
        )

    skill_path = root_path / "harness" / "skills" / "using-harness" / "SKILL.md"
    if not skill_path.is_file():
        issues.append("缺少 harness/skills/using-harness/SKILL.md")
    elif "硬约束" not in skill_path.read_text(encoding="utf-8"):
        issues.append("harness/skills/using-harness/SKILL.md 不是 using-harness 工作流 Skill")

    for required in (
        "harness/PROGRESS.md",
        "harness/todo.md",
        "harness/DECISIONS.md",
        "harness/rules/index.md",
        "harness/rules/python-coding-conventions.md",
        "harness/acceptance/index.md",
        "harness/scripts/mini_harness.py",
        "tests/README.md",
    ):
        if not (root_path / required).is_file():
            issues.append(f"缺少 {required}")

    legacy_package_playbook = root_path / LEGACY_PACKAGE_PLAYBOOK
    if legacy_package_playbook.is_file():
        warnings.append(
            "发现过时的 harness/.package/AGENTS.md；运行 "
            "`python harness/scripts/mini_harness.py update --root .` 清理"
        )

    root_agents = root_path / LEGACY_AGENTS_RELATIVE
    if root_agents.is_file():
        agents_text = root_agents.read_text(encoding="utf-8")
        if _looks_like_harness_playbook_agents(agents_text):
            warnings.append(
                "发现仓库根 AGENTS.md（v2.1 前 harness 旧 Playbook）；运行 update 清理。"
                "工作流现位于 harness/skills/using-harness/SKILL.md"
            )
        else:
            warnings.append(
                "仓库根存在 AGENTS.md（非 harness 管理）；v2.1+ 工作流在 "
                "harness/skills/using-harness/SKILL.md"
            )

    pkg_installer = root_path / "harness" / ".package" / "scripts" / "mini_harness.py"
    live_installer = root_path / "harness" / "scripts" / "mini_harness.py"
    if (
        pkg_installer.is_file()
        and live_installer.is_file()
        and _normalized_text_digest(pkg_installer) != _normalized_text_digest(live_installer)
    ):
        warnings.append(
            "harness/scripts/mini_harness.py 与 harness/.package 不一致（可能为旧版安装器）；"
            "运行 `python harness/scripts/mini_harness.py update --root .` 同步"
        )

    if marker.get("active") is True and not issues:
        warnings.extend(_collect_package_drift(root_path))

    return {
        "ok": not issues,
        "issues": issues,
        "warnings": warnings,
        "root": str(root_path),
    }


def uninstall(root: str | Path) -> dict[str, Any]:
    """Remove only files recorded as managed by mini-harness."""
    root_path = Path(root).resolve()
    marker_path = root_path / MARKER_RELATIVE
    if not marker_path.exists():
        return {"changed": False, "root": str(root_path)}

    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        marker = {}

    for relative in marker.get("managed_files", []):
        relative_name = str(relative)
        target = root_path / relative_name
        if target.is_file() and target != marker_path:
            target.unlink()

    marker_path.unlink(missing_ok=True)
    harness_root = root_path / "harness"
    if harness_root.exists():
        directories = sorted((path for path in harness_root.rglob("*") if path.is_dir()), reverse=True)
        for directory in directories:
            try:
                directory.rmdir()
            except OSError:
                pass
        try:
            harness_root.rmdir()
        except OSError:
            pass

    return {"changed": True, "root": str(root_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description="管理通用 mini-harness 安装")
    parser.add_argument("action", choices=("install", "update", "doctor", "uninstall"))
    parser.add_argument("--root", default=".", help="仓库根目录，默认为当前目录")
    args = parser.parse_args()

    if args.action in {"install", "update"}:
        result = install(args.root)
    elif args.action == "doctor":
        result = doctor(args.root)
    else:
        result = uninstall(args.root)

    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if hasattr(sys.stdout, "buffer"):
        sys.stdout.buffer.write(payload.encode("utf-8"))
    else:
        sys.stdout.write(payload)
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
