#!/usr/bin/env python3
"""Verify that the Russian chapters still contain the v1.0.0 README body.

This is a MIGRATION check, not a permanent gate: it compares the chapters in
docs/ru/ against the frozen snapshot evidence/README.v1.0.0.md and reports any
paragraph of the old body that is missing from the new structure. Run it after
a split or a merge; it is expected to be re-pointed (or retired) once the
chapters are edited independently.

Exit codes
    0  every paragraph of the old body is present in the chapters
    1  at least one paragraph is missing
    2  the frozen snapshot or the chapters are missing -- nothing verified

    python3 scripts/check-doc-split.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_CANNOT_VERIFY = 0, 1, 2
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SNAPSHOT = ROOT / "evidence" / "README.v1.0.0.md"
CHAPTERS = ROOT / "docs" / "ru"


def normalize(text: str) -> str:
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", lambda m: m.group(0).split("]")[0] + "]", text)
    return re.sub(r"\s+", " ", text).strip()


def paragraphs(text: str) -> list[str]:
    out = []
    for block in re.split(r"\n\s*\n", text):
        n = normalize(block)
        if len(n) >= 40 and not n.startswith("#") and not n.startswith(">"):
            out.append(n)
    return out


def main() -> int:
    if not SNAPSHOT.is_file() or not CHAPTERS.is_dir():
        print("cannot verify: snapshot or docs/ru/ is missing", file=sys.stderr)
        return EXIT_CANNOT_VERIFY
    old = paragraphs(SNAPSHOT.read_text(encoding="utf-8"))
    new_text = "\n\n".join(p.read_text(encoding="utf-8") for p in sorted(CHAPTERS.glob("*.md")))
    new_norm = normalize(new_text)
    missing = [p for p in old if p not in new_norm]
    if missing:
        print(f"migration lost {len(missing)} paragraph(s):")
        for p in missing[:10]:
            print(f"  - {p[:80]}...")
        return EXIT_FAIL
    print(f"migration is lossless: {len(old)} paragraphs present in {len(list(CHAPTERS.glob('*.md')))} chapters")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
