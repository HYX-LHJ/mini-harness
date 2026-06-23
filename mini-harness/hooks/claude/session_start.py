"""Compatibility entrypoint for hosts that prefer a hook-local script."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], "--host", "claude"]
runpy.run_path(str(Path(__file__).resolve().parents[2] / "scripts" / "hook_context.py"), run_name="__main__")
