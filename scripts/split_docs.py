"""Split bilingual docs/*.md into docs/en/ and docs/zh-CN/."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

TITLE_MAP = {
    "getting-started": ("Getting Started", "快速入门"),
    "installation": ("Installation", "安装指南"),
    "architecture": ("Architecture", "架构说明"),
    "workflow": ("Workflow", "协作流程"),
}

EN_REPL = [
    ("init_harness.py", "mini_harness.py"),
    ("mini-harness-en/", "mini-harness/"),
    ("mini-harness-zh/", "mini-harness/"),
]

ZH_REPL = [
    ("init_harness.py", "mini_harness.py"),
    ("mini-harness-en/", "mini-harness/"),
    ("mini-harness-zh/", "mini-harness/"),
]


def _apply(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def main() -> None:
    for stem, (en_title, zh_title) in TITLE_MAP.items():
        source = DOCS / f"{stem}.md"
        if not source.is_file():
            continue
        raw = source.read_text(encoding="utf-8")
        sections = re.split(r"\n---\n", raw, maxsplit=1)
        if len(sections) != 2:
            continue
        en_body, zh_body = sections
        en_body = en_body.replace(f"# {en_title}", f"# {en_title}", 1)
        zh_body = zh_body.replace(f"# {zh_title}", f"# {zh_title}", 1)
        (DOCS / "en" / f"{stem}.md").write_text(
            _apply(en_body.strip() + "\n", EN_REPL), encoding="utf-8"
        )
        (DOCS / "zh-CN" / f"{stem}.md").write_text(
            _apply(zh_body.strip() + "\n", ZH_REPL), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
