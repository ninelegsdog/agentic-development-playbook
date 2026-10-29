#!/usr/bin/env python3
"""Check that the reusable templates are actually reusable.

A template that cannot be copied and filled in is not a template, it is a
copy of a document with the answers left in. This checker proves each template
carries at least one unfilled field, uses the agreed placeholder syntax, and
contains no value that should never have been committed.

Exit codes
    0  templates are sane
    1  a template is not reusable
    2  templates/ or its index is missing -- nothing was checked

    python3 scripts/check-templates.py
    python3 scripts/check-templates.py --self-test
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_CANNOT_VERIFY = 0, 1, 2
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TEMPLATES = ROOT / "templates"

RESERVED_IPS = {"127.0.0.1", "0.0.0.0"}
RESERVED_PREFIXES = ("192.0.2.", "198.51.100.", "203.0.113.")


def is_reserved_ip(ip: str) -> bool:
    return ip in RESERVED_IPS or any(ip.startswith(p) for p in RESERVED_PREFIXES)


def verify(templates_dir: Path) -> list[str]:
    problems: list[str] = []
    if not templates_dir.is_dir():
        return ["templates/ directory is missing"]
    index = templates_dir / "README.md"
    if not index.is_file():
        problems.append("templates/README.md is missing")
    files = sorted(p for p in templates_dir.glob("*.md") if p.name != "README.md")
    if not files:
        problems.append("templates/ contains no template files")
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        has_placeholder = bool(re.search(r"<[^<>\n]+>", text))
        has_checklist = "- [ ]" in text
        if not (has_placeholder or has_checklist):
            problems.append(f"{path.name}: no unfilled placeholder <...> and no checklist items")
        if re.search(r"\{\{\s*\w", text):
            problems.append(f"{path.name}: uses {{{{ }}}} placeholder syntax")
        for ip in re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", text):
            if not is_reserved_ip(ip):
                problems.append(f"{path.name}: non-reserved IP address {ip}")
        if re.search(r"/home/[A-Za-z0-9_./-]+", text):
            problems.append(f"{path.name}: contains an absolute home path")
    if index.is_file():
        index_text = index.read_text(encoding="utf-8", errors="replace")
        for path in files:
            if path.name not in index_text:
                problems.append(f"templates/README.md does not mention {path.name}")
    return problems


def make_fixture(root: Path, mutate) -> Path:
    src = TEMPLATES
    dst = root / "templates"
    shutil.copytree(src, dst)
    mutate(dst)
    return dst


def self_test() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        # 1. a template with no placeholder must be caught.
        def drop_placeholder(d: Path) -> None:
            p = d / "AGENTS.md"
            p.write_text(re.sub(r"<[^>]*>", "filled", p.read_text()), encoding="utf-8")
        dst = make_fixture(root, drop_placeholder)
        if any("no unfilled placeholder" in p for p in verify(dst)):
            print("ok   self-test: missing placeholder is caught")
        else:
            print("FAIL self-test: missing placeholder was not caught")
            ok = False

        # 2. {{ }} syntax must be caught.
        root2 = Path(tempfile.mkdtemp())
        def add_mustache(d: Path) -> None:
            (d / "AGENTS.md").write_text(
                (d / "AGENTS.md").read_text() + "\n{{ project_name }}\n", encoding="utf-8")
        dst2 = make_fixture(root2, add_mustache)
        if any("{{" in p for p in verify(dst2)):
            print("ok   self-test: {{ }} syntax is caught")
        else:
            print("FAIL self-test: {{ }} syntax was not caught")
            ok = False
        shutil.rmtree(root2, ignore_errors=True)

        # 3. a non-reserved IP must be caught.
        root3 = Path(tempfile.mkdtemp())
        def add_ip(d: Path) -> None:
            (d / "AGENTS.md").write_text(
                (d / "AGENTS.md").read_text() + "\n10.0.0.5\n", encoding="utf-8")
        dst3 = make_fixture(root3, add_ip)
        if any("non-reserved IP" in p for p in verify(dst3)):
            print("ok   self-test: non-reserved IP is caught")
        else:
            print("FAIL self-test: non-reserved IP was not caught")
            ok = False
        shutil.rmtree(root3, ignore_errors=True)

        # 4. an unindexed template must be caught.
        root4 = Path(tempfile.mkdtemp())
        def add_orphan(d: Path) -> None:
            (d / "orphan.md").write_text("# orphan\n\n<x>\n", encoding="utf-8")
        dst4 = make_fixture(root4, add_orphan)
        if any("does not mention orphan.md" in p for p in verify(dst4)):
            print("ok   self-test: unindexed template is caught")
        else:
            print("FAIL self-test: unindexed template was not caught")
            ok = False
        shutil.rmtree(root4, ignore_errors=True)
    return ok


def main() -> int:
    if not TEMPLATES.is_dir():
        print("cannot verify: templates/ is missing", file=sys.stderr)
        return EXIT_CANNOT_VERIFY
    if "--self-test" in sys.argv:
        return EXIT_OK if self_test() else EXIT_FAIL
    problems = verify(TEMPLATES)
    if problems:
        print(f"templates are not reusable ({len(problems)} problem(s))")
        for p in problems:
            print(f"  {p}")
        return EXIT_FAIL
    count = len([p for p in TEMPLATES.glob("*.md") if p.name != "README.md"])
    print(f"templates are reusable ({count} template(s))")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
