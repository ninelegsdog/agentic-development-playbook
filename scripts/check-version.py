#!/usr/bin/env python3
"""Check that the version surfaces agree.

The document is cited by version (CITATION.cff), released by tag, and
changelogged by section. Three copies of the same number drift the moment one
is edited. This script makes the drift loud.

Exit codes
    0  version, tag and changelog agree
    1  they disagree
    2  cannot verify (missing files or no tags)

    python3 scripts/check-version.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_CANNOT_VERIFY = 0, 1, 2
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def latest_tag() -> str | None:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "describe", "--tags", "--abbrev=0", "--match", "v*"],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        return None
    tag = out.stdout.strip()
    return tag.removeprefix("v")


def citation_version() -> str | None:
    p = ROOT / "CITATION.cff"
    if not p.is_file():
        return None
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^version:\s*(.+?)\s*$", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return None


def _version_ge(a: str, b: str) -> bool:
    def parts(v: str) -> tuple[int, ...]:
        return tuple(int(x) for x in v.split(".") if x.isdigit())
    return parts(a) >= parts(b)
    p = ROOT / "CHANGELOG.md"
    if not p.is_file():
        return False
    return re.search(rf"^## \[{re.escape(version)}\]", p.read_text(encoding="utf-8"), re.MULTILINE) is not None


def main() -> int:
    tag = latest_tag()
    if tag is None:
        print("cannot verify: no v* tag found", file=sys.stderr)
        return EXIT_CANNOT_VERIFY
    cit = citation_version()
    if cit is None:
        print("cannot verify: CITATION.cff has no version", file=sys.stderr)
        return EXIT_CANNOT_VERIFY
    problems = []
    if cit != tag and not _version_ge(cit, tag):
        problems.append(f"CITATION.cff version {cit} is older than latest tag {tag}")
    if not changelog_has(cit):
        problems.append(f"CHANGELOG.md has no section for [{cit}]")
    if tag and not changelog_has(tag):
        problems.append(f"CHANGELOG.md has no section for the latest tag [{tag}]")
    if problems:
        print("version surfaces disagree:")
        for p in problems:
            print(f"  {p}")
        return EXIT_FAIL
    print(f"version surfaces agree: citation={cit}, latest tag={tag}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
