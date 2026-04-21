#!/usr/bin/env python3
"""Проверка: все [[target]] в vault указывают на существующий stem (.md в корне, Notes, Literature, Definitions, System)."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def vault_root() -> Path:
    return Path(__file__).resolve().parent.parent


def collect_stems(root: Path) -> set[str]:
    stems: set[str] = set()
    for d in (root, root / "Notes", root / "Literature", root / "Definitions", root / "System"):
        if d.is_dir():
            for p in d.glob("*.md"):
                stems.add(p.stem)
    return stems


def main() -> int:
    root = vault_root()
    stems = collect_stems(root)
    missing: list[tuple[str, str]] = []
    scan_dirs = [root, root / "Notes", root / "Literature", root / "Definitions", root / "System"]
    for d in scan_dirs:
        if not d.is_dir():
            continue
        for p in d.glob("*.md"):
            text = p.read_text(encoding="utf-8")
            for m in re.finditer(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]", text):
                t = m.group(1).strip()
                if t.startswith("http") or "/" in t:
                    continue
                if t not in stems:
                    missing.append((str(p.relative_to(root)), t))
    if missing:
        print("Missing wikilink targets:", len(missing), file=sys.stderr)
        for path, target in missing[:50]:
            print(f"  {path} -> [[{target}]]", file=sys.stderr)
        if len(missing) > 50:
            print(f"  ... and {len(missing) - 50} more", file=sys.stderr)
        return 1
    print("OK: all wikilink targets resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
