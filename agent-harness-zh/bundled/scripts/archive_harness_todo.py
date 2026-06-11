"""将 harness/todo.md 中早于当前自然周的内容归档到 harness/backlog/，并同步 PROGRESS「已完成」。

自然周：周一 00:00 ~ 周日（与 todo 块首行 YYYY-MM-DD 对齐）。
用法（仓库根目录）：
  .venv\\Scripts\\python.exe harness/scripts/archive_harness_todo.py
  .venv\\Scripts\\python.exe harness/scripts/archive_harness_todo.py --dry-run
  .venv\\Scripts\\python.exe harness/scripts/archive_harness_todo.py --sync-progress
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # 仓库根目录（脚本位于 harness/scripts/）
TODO_PATH = ROOT / "harness" / "todo.md"
PROGRESS_PATH = ROOT / "harness" / "PROGRESS.md"
BACKLOG_DIR = ROOT / "harness" / "backlog"
ARCHIVE_PATH = BACKLOG_DIR / "archive.md"

DATE_LINE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s*$")
TASK_LINE = re.compile(r"^task：(.+)\s*$")
UNCHECKED_LINE = re.compile(r"^- \[ \]")
PROGRESS_SECTION = re.compile(r"(?ms)^(## 已完成)\n\n.*?(?=^## )")


def monday_of(d: date) -> date:
    return d - timedelta(days=d.weekday())


def sunday_of(d: date) -> date:
    return monday_of(d) + timedelta(days=6)


def week_range_label(start: date, end: date) -> str:
    return f"{start.isoformat()} ~ {end.isoformat()}"


def parse_blocks(text: str) -> list[tuple[date | None, str]]:
    """按日期行切分块；无日期的前导块 date 为 None。"""
    lines = text.splitlines()
    blocks: list[tuple[date | None, list[str]]] = []
    current_date: date | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_date, current_lines
        if current_lines:
            blocks.append((current_date, current_lines))
        current_date = None
        current_lines = []

    for line in lines:
        m = DATE_LINE.match(line.strip())
        if m:
            flush()
            current_date = date.fromisoformat(m.group(1))
            current_lines = [line]
        else:
            if not current_lines and not blocks:
                current_lines = [line] if line.strip() else []
            else:
                current_lines.append(line)
    flush()
    return [(d, "\n".join(ls).rstrip()) for d, ls in blocks if "\n".join(ls).strip()]


def block_week_key(block_date: date | None, fallback: date) -> tuple[date, date]:
    d = block_date or fallback
    start = monday_of(d)
    end = sunday_of(d)
    return start, end


def group_by_week(blocks: list[tuple[date | None, str]]) -> dict[tuple[date, date], list[str]]:
    groups: dict[tuple[date, date], list[str]] = {}
    fallback = date.today()
    for block_date, body in blocks:
        key = block_week_key(block_date, fallback)
        groups.setdefault(key, []).append(body)
    return groups


def format_week_section(start: date, end: date, bodies: list[str]) -> str:
    header = week_range_label(start, end)
    content = "\n\n".join(bodies)
    return f"{header}\n\n{content}"


def read_archive_sections(path: Path) -> dict[tuple[date, date], str]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    sections: dict[tuple[date, date], str] = {}
    parts = re.split(r"\n(?=\d{4}-\d{2}-\d{2} ~ \d{4}-\d{2}-\d{2}\n)", text.strip())
    for part in parts:
        part = part.strip()
        if not part:
            continue
        first_line, _, rest = part.partition("\n")
        m = re.match(r"^(\d{4}-\d{2}-\d{2}) ~ (\d{4}-\d{2}-\d{2})$", first_line.strip())
        if not m:
            continue
        start = date.fromisoformat(m.group(1))
        end = date.fromisoformat(m.group(2))
        sections[(start, end)] = rest.strip()
    return sections


def write_archive(sections: dict[tuple[date, date], str]) -> None:
    BACKLOG_DIR.mkdir(parents=True, exist_ok=True)
    ordered = sorted(sections.keys())
    chunks = []
    for key in ordered:
        start, end = key
        body = sections[key].strip()
        chunks.append(format_week_section(start, end, [body]) if body else week_range_label(start, end))
    ARCHIVE_PATH.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")


def todo_body_without_header(raw: str) -> str:
    body = raw
    if body.startswith("# 当前周任务板"):
        _, _, body = body.partition("---\n")
        body = body.lstrip("\n")
    return body


def iter_task_sections(body: str) -> list[tuple[str, str]]:
    """按 ``task：`` 切分任务块，返回 ``(任务名, 块正文)`` 列表。

    ``parse_blocks`` 按日期切分；同一日期下多个 ``task：`` 须单独统计完成/进行中。
    """
    sections: list[tuple[str, str]] = []
    task_name: str | None = None
    lines: list[str] = []

    def flush() -> None:
        nonlocal task_name, lines
        if task_name is not None:
            sections.append((task_name, "\n".join(lines)))
        task_name = None
        lines = []

    for line in body.splitlines():
        stripped = line.strip()
        if DATE_LINE.match(stripped):
            # 日期行由 parse_blocks 处理；勿并入上一 task 正文
            continue
        m = TASK_LINE.match(stripped)
        if m:
            flush()
            task_name = m.group(1)
            lines = []
        elif task_name is not None:
            lines.append(line)
    flush()
    return sections


def completed_task_names_from_body(body: str) -> list[str]:
    """本周 todo 正文中，子项全部 [x] 的 task 名称（保持出现顺序）。"""
    names: list[str] = []
    for task_name, task_body in iter_task_sections(body):
        has_unchecked = False
        has_checked = False
        for line in task_body.splitlines():
            stripped = line.strip()
            if UNCHECKED_LINE.match(stripped):
                has_unchecked = True
            if stripped.startswith("- [x]"):
                has_checked = True
        if not has_unchecked and has_checked:
            names.append(task_name)
    return names


def in_progress_task_names_from_body(body: str) -> list[str]:
    names: list[str] = []
    for task_name, task_body in iter_task_sections(body):
        for line in task_body.splitlines():
            if UNCHECKED_LINE.match(line.strip()):
                names.append(task_name)
                break
    return names


def format_progress_completed(names: list[str]) -> str:
    intro = (
        "仅列**本周** `todo.md` 中子项已全部 `[x]` 的 `task：`；"
        "更早交付见 [backlog/archive.md](backlog/archive.md)，不在此保留。"
    )
    if not names:
        bullets = "- （本周尚无已全部完成的 task）"
    else:
        bullets = "\n".join(f"- {n}" for n in names)
    return f"## 已完成\n\n{intro}\n\n{bullets}\n\n"


def format_progress_in_progress(names: list[str]) -> str:
    if not names:
        body = "-"
    else:
        body = "\n".join(f"- {n}" for n in names)
    return f"## 进行中\n\n{body}\n\n"


def sync_progress_from_todo(*, dry_run: bool = False) -> None:
    body = todo_body_without_header(TODO_PATH.read_text(encoding="utf-8"))
    completed = completed_task_names_from_body(body)
    in_progress = in_progress_task_names_from_body(body)

    progress = PROGRESS_PATH.read_text(encoding="utf-8")
    new_completed = format_progress_completed(completed)
    if not PROGRESS_SECTION.search(progress):
        msg = "PROGRESS.md missing ## 已完成 section"
        raise ValueError(msg)
    progress = PROGRESS_SECTION.sub(new_completed, progress, count=1)

    in_prog_re = re.compile(r"(?ms)^(## 进行中)\n\n.*?(?=^## )")
    if not in_prog_re.search(progress):
        msg = "PROGRESS.md missing ## 进行中 section"
        raise ValueError(msg)
    progress = in_prog_re.sub(format_progress_in_progress(in_progress), progress, count=1)

    if dry_run:
        print(f"completed: {completed}", file=sys.stderr)
        print(f"in_progress: {in_progress}", file=sys.stderr)
        return

    PROGRESS_PATH.write_text(progress, encoding="utf-8")
    print(
        f"Synced PROGRESS completed ({len(completed)}) / in_progress ({len(in_progress)})",
        file=sys.stderr,
    )


def current_week_header(today: date | None = None) -> str:
    today = today or date.today()
    start = monday_of(today)
    end = sunday_of(today)
    return (
        "# 当前周任务板\n\n"
        f"**本周**：{week_range_label(start, end)}（周一～周日）\n\n"
        "历史周任务见 [backlog/archive.md](backlog/archive.md)。\n"
        "跨周归档：仓库根目录执行 `python harness/scripts/archive_harness_todo.py`。\n\n"
        "---\n"
    )


def run(*, dry_run: bool = False, today: date | None = None) -> None:
    today = today or date.today()
    current_key = (monday_of(today), sunday_of(today))

    raw = TODO_PATH.read_text(encoding="utf-8")
    body = todo_body_without_header(raw)

    blocks = parse_blocks(body)
    groups = group_by_week(blocks)

    archive_sections = read_archive_sections(ARCHIVE_PATH)
    for key, bodies in groups.items():
        if key == current_key:
            continue
        merged = "\n\n".join(bodies).strip()
        prev = archive_sections.get(key, "").strip()
        if prev:
            archive_sections[key] = prev + "\n\n" + merged
        else:
            archive_sections[key] = merged

    current_blocks = groups.get(current_key, [])
    new_todo = current_week_header(today)
    if current_blocks:
        new_todo += "\n\n".join(current_blocks) + "\n"
    else:
        new_todo += f"\n{today.isoformat()}\n\n- （本周尚无任务块）\n"

    if dry_run:
        print(f"current week: {week_range_label(*current_key)}", file=sys.stderr)
        print(f"archive weeks: {len([k for k in groups if k != current_key])}", file=sys.stderr)
        print(f"todo lines: {len(new_todo.splitlines())}", file=sys.stderr)
        return

    write_archive(archive_sections)
    TODO_PATH.write_text(new_todo, encoding="utf-8")
    sync_progress_from_todo()
    print(f"Archived to {ARCHIVE_PATH.relative_to(ROOT)}", file=sys.stderr)
    print(f"todo.md kept week {week_range_label(*current_key)}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive harness/todo.md by calendar week.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--sync-progress",
        action="store_true",
        help="Only rewrite PROGRESS 已完成/进行中 from current todo.md",
    )
    parser.add_argument(
        "--today",
        type=lambda s: date.fromisoformat(s),
        default=None,
        help="Override today (YYYY-MM-DD) for testing",
    )
    args = parser.parse_args()
    if args.sync_progress:
        sync_progress_from_todo(dry_run=args.dry_run)
        return
    run(dry_run=args.dry_run, today=args.today)


if __name__ == "__main__":
    main()
