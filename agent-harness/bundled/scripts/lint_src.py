"""对 ``src/`` 运行 ruff check、ruff format --check、pyright（供 Agent 本地质量检查）。"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    # scripts/ is under harness/; the repository root is one more level up.
    # We intentionally anchor lint + tools to the repo root `.venv`.
    return Path(__file__).resolve().parent.parent.parent


def _reexec_with_venv_python(root: Path) -> None:
    venv_python = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not venv_python.exists():
        return
    if Path(sys.executable).resolve() == venv_python.resolve():
        return
    script = Path(__file__).resolve()
    os.execv(str(venv_python), [str(venv_python), str(script), *sys.argv[1:]])


def _venv_bin(root: Path) -> Path:
    return root / ".venv" / ("Scripts" if os.name == "nt" else "bin")


def _tool(vb: Path, name: str) -> Path:
    return vb / (f"{name}.exe" if os.name == "nt" else name)


def main() -> int:
    root = _repo_root()
    _reexec_with_venv_python(root)
    vb = _venv_bin(root)
    steps: list[tuple[str, list[str]]] = [
        ("ruff", ["check", "src"]),
        ("ruff", ["format", "--check", "src"]),
        ("pyright", ["src"]),
    ]
    for tool, args_list in steps:
        exe = _tool(vb, tool)
        if not exe.exists():
            print(f"Missing {exe}. From repo root: pip install -e '.[dev]'", file=sys.stderr)
            return 1
        try:
            subprocess.run([str(exe), *args_list], cwd=root, check=True)
        except subprocess.CalledProcessError as e:
            return e.returncode if e.returncode else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
