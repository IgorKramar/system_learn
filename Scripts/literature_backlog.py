#!/usr/bin/env python3
"""Пересчитать таблицу stub-литературы в System/literature-backlog.md по wikilink из Notes/."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def vault_root() -> Path:
    return Path(__file__).resolve().parent.parent


def count_note_links_to_literature(root: Path) -> dict[str, int]:
    notes = root / "Notes"
    lit = root / "Literature"
    basenames = [f.stem for f in lit.glob("*.md")]
    pat_cache: dict[str, re.Pattern[str]] = {}
    counts = {b: 0 for b in basenames}
    for nf in notes.glob("*.md"):
        text = nf.read_text(encoding="utf-8")
        for b in basenames:
            if b not in pat_cache:
                pat_cache[b] = re.compile(r"\[\[" + re.escape(b) + r"(?:\||\]\])")
            counts[b] += len(pat_cache[b].findall(text))
    return counts


def stub_rows(root: Path, counts: dict[str, int]) -> list[str]:
    lit = root / "Literature"
    rows: list[tuple[int, str, str, str, str]] = []
    for f in sorted(lit.glob("*.md")):
        t = f.read_text(encoding="utf-8")
        if "literature_status: deep" in t:
            continue
        b = f.stem
        ym = re.search(r"^year:\s*(\d+)", t, re.M)
        year = ym.group(1) if ym else ""
        cid = re.search(r"^card_id:\s*(\S+)", t, re.M)
        cid = cid.group(1).strip("`'\"") if cid else ""
        st = re.search(r"^literature_status:\s*(\S+)", t, re.M)
        st = st.group(1) if st else ""
        rows.append((counts.get(b, 0), b, year, cid, st))
    rows.sort(key=lambda x: (-x[0], x[1]))
    out = [
        "| Приоритет (backlinks из Notes) | Файл | Год | card_id | literature_status |\n",
        "|---:|:---|:---|:---|:---|\n",
    ]
    for prio, b, year, cid, st in rows:
        out.append(f"| {prio} | [[{b}]] | {year} | `{cid}` | {st} |\n")
    return out


def splice_table(backlog_text: str, new_table_body: list[str]) -> str:
    lines = backlog_text.splitlines(keepends=True)
    try:
        i = next(i for i, ln in enumerate(lines) if ln.startswith("| Приоритет (backlinks из Notes)"))
    except StopIteration as e:
        raise SystemExit("literature-backlog.md: не найдена строка заголовка таблицы") from e
    try:
        j = next(i for i, ln in enumerate(lines) if ln.startswith("## Связанные"))
    except StopIteration as e:
        raise SystemExit("literature-backlog.md: не найден секция ## Связанные") from e
    return "".join(lines[:i]) + "".join(new_table_body) + "\n" + "".join(lines[j:])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Записать System/literature-backlog.md (иначе печать таблицы в stdout)",
    )
    args = parser.parse_args()
    root = vault_root()
    counts = count_note_links_to_literature(root)
    body = stub_rows(root, counts)
    path = root / "System" / "literature-backlog.md"
    text = path.read_text(encoding="utf-8")
    new_text = splice_table(text, body)
    if args.write:
        path.write_text(new_text, encoding="utf-8")
        print(f"Updated {path.relative_to(root)}")
    else:
        print("".join(body), end="")


if __name__ == "__main__":
    main()
