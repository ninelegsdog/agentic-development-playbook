#!/usr/bin/env python3
"""Small, uncontroversial markdown hygiene checks.

This is deliberately not markdownlint: the author's style uses long lines and
intentional formatting that a full linter would fight. Only rules that never
conflict with that style are enforced here.

Exit codes
    0  clean
    1  a file violates a rule
    2  no markdown files found

    python3 scripts/check-markdown.py
    python3 scripts/check-markdown.py --self-test
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_CANNOT_VERIFY = 0, 1, 2
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def verify(root: Path) -> list[str]:
    problems: list[str] = []
    files = sorted(p for p in root.rglob("*.md") if ".git" not in p.parts and p.name != "README.v1.0.0.md")
    if not files:
        return ["__NO_FILES__"]
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(root))
        if not text.endswith("\n"):
            problems.append(f"{rel}: missing final newline")
        fence = False
        h1_lines = []
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("```") or line.strip().startswith("~~~"):
                fence = not fence
                continue
            if fence:
                continue
            if line != line.rstrip() and not (len(line) - len(line.rstrip()) == 2 and line.endswith("  ")):
                problems.append(f"{rel}:{i}: trailing whitespace")
            if line.startswith("# "):
                h1_lines.append(i)
        if len(h1_lines) > 1:
            problems.append(f"{rel}: {len(h1_lines)} H1 headings (expected at most one): {h1_lines}")
    return problems


def self_test() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "a.md").write_text("# Title\n\nbody\n", encoding="utf-8")
        if verify(root):
            print("FAIL self-test: clean file reported problems")
            ok = False
        else:
            print("ok   self-test: clean file passes")
        # missing final newline
        (root / "b.md").write_text("# T\n\nbody", encoding="utf-8")
        if any("missing final newline" in p for p in verify(root)):
            print("ok   self-test: missing newline is caught")
        else:
            print("FAIL self-test: missing newline not caught")
            ok = False
        # trailing whitespace
        (root / "c.md").write_text("# T\n\nbody   \n", encoding="utf-8")
        if any("trailing whitespace" in p for p in verify(root)):
            print("ok   self-test: trailing whitespace is caught")
        else:
            print("FAIL self-test: trailing whitespace not caught")
            ok = False
        # two H1
        (root / "d.md").write_text("# A\n\n# B\n", encoding="utf-8")
        if any("H1 headings" in p for p in verify(root)):
            print("ok   self-test: duplicate H1 is caught")
        else:
            print("FAIL self-test: duplicate H1 not caught")
            ok = False
    return ok


def main() -> int:
    if "--self-test" in sys.argv:
        return EXIT_OK if self_test() else EXIT_FAIL
    problems = verify(ROOT)
    if problems == ["__NO_FILES__"]:
        print("cannot verify: no markdown files found", file=sys.stderr)
        return EXIT_CANNOT_VERIFY
    if problems:
        print(f"markdown hygiene: {len(problems)} problem(s)")
        for p in problems:
            print(f"  {p}")
        return EXIT_FAIL
    count = len([p for p in ROOT.rglob("*.md") if ".git" not in p.parts])
    print(f"markdown hygiene: clean ({count} files)")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
