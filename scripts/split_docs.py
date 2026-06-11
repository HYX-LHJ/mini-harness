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
    "skills-cli": ("Skills CLI", "Skills CLI 指南"),
}

EN_REPL = [
    ("agent-harness/", "mini-harness-en/"),
    ("--skill agent-harness", "--skill mini-harness-en"),
    ("../agent-harness/", "../mini-harness-en/"),
    ("skills/agent-harness/", "skills/mini-harness-en/"),
    ("agent-harness@", "mini-harness-en@"),
    ("agent-harness?", "mini-harness-en?"),
]

ZH_REPL = [
    ("agent-harness/", "mini-harness-zh/"),
    ("--skill agent-harness", "--skill mini-harness-zh"),
    ("../agent-harness/", "../mini-harness-zh/"),
    ("skills/agent-harness/", "skills/mini-harness-zh/"),
    ("agent-harness@", "mini-harness-zh@"),
]


def _apply(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def main() -> None:
    (DOCS / "en").mkdir(exist_ok=True)
    (DOCS / "zh-CN").mkdir(exist_ok=True)
    for path in DOCS.glob("*.md"):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"^# [^\n]+\n\n\*\*Languages:\*\*[^\n]+\n\n---\n\n",
            "",
            text,
        )
        en_m = re.search(
            r'<a id="english"></a>\n\n(.*?)(?=\n---\n\n<a id="chinese">|$)',
            text,
            re.S,
        )
        zh_m = re.search(r'<a id="chinese"></a>\n\n(.*)', text, re.S)
        stem = path.stem
        titles = TITLE_MAP.get(stem, (stem.title(), stem))
        if en_m:
            body = re.sub(r"^## English\n\n", "", en_m.group(1).strip())
            out = f"# {titles[0]}\n\n" + _apply(body, EN_REPL) + "\n"
            (DOCS / "en" / path.name).write_text(out, encoding="utf-8")
        if zh_m:
            body = re.sub(r"^## 中文\n\n", "", zh_m.group(1).strip())
            out = f"# {titles[1]}\n\n" + _apply(body, ZH_REPL) + "\n"
            (DOCS / "zh-CN" / path.name).write_text(out, encoding="utf-8")
    print("split ok")


if __name__ == "__main__":
    main()
