from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str) -> ModuleType:
    path = PLUGIN_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def installer() -> ModuleType:
    return load_module("mini_harness_installer", "scripts/mini_harness.py")


@pytest.fixture
def hook_context() -> ModuleType:
    return load_module("mini_harness_hook", "scripts/hook_context.py")
