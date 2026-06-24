#!/usr/bin/env python3
"""Scaffold GOAL.md autonomous improvement files under harness/goal/.

Examples:
    python init_goal.py --name "Raise test coverage to 90%"
    python init_goal.py --root /path/to/repo --name "Docs quality" --force
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
GOAL_INDEX = """# GOAL 自主改进

存放 [goal-md](../../skills/goal-md/SKILL.md) 模式的多轮可度量优化状态。

| 文件 | 用途 |
|------|------|
| [GOAL.md](GOAL.md) | 目标规格（适应度定义、行动清单、约束） |
| [score.py](score.py) | 适应度函数（分数只由此脚本输出） |
| [iterations.jsonl](iterations.jsonl) | 迭代日志（只追加） |

```bash
python harness/goal/score.py
python harness/goal/score.py --json
```

todo 中登记元任务并链向 `GOAL.md`；迭代细节写入 `iterations.jsonl`（不经 per-iteration AC）。
"""


def _write_if_missing(path: Path, content: str, *, force: bool) -> str:
    if path.exists() and not force:
        return "skip"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "write"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize harness/goal/ scaffold")
    parser.add_argument("--name", required=True, help="One-line goal title")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: cwd)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    root = args.root.resolve()
    harness = root / "harness"
    if not harness.is_dir():
        print("error: harness/ not found — run `mini_harness.py install --root .` first", file=sys.stderr)
        return 1

    goal_dir = harness / "goal"
    goal_tpl = (ASSETS / "GOAL.template.md").read_text(encoding="utf-8")
    goal_tpl = goal_tpl.replace("{{GOAL_NAME}}", args.name.strip())
    score_tpl = (ASSETS / "score.py.template").read_text(encoding="utf-8")

    actions: list[tuple[str, Path, str]] = [
        ("harness/goal/index.md", goal_dir / "index.md", GOAL_INDEX),
        ("harness/goal/GOAL.md", goal_dir / "GOAL.md", goal_tpl),
        ("harness/goal/score.py", goal_dir / "score.py", score_tpl),
        ("harness/goal/iterations.jsonl", goal_dir / "iterations.jsonl", ""),
    ]

    for label, path, body in actions:
        result = _write_if_missing(path, body, force=args.force)
        print(f"{result}: {label} -> {path}")

    print("\nNext:")
    print("  1. Edit harness/goal/score.py (REQUIRED_DOCS, REQUIRED_REQUIREMENTS, paths)")
    print("  2. Complete harness/goal/GOAL.md Action Catalog and Constraints")
    print("  3. python harness/goal/score.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
