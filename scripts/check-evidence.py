#!/usr/bin/env python3
"""Check that the numbers in README.md still match evidence/metrics.json.

The README quotes measured numbers; the JSON holds the measurement. Two copies
of the same fact drift the moment one is edited, and the drift is invisible
because both look authoritative. This script makes the drift loud.

Exit codes
    0  README agrees with the evidence
    1  a number in README disagrees with the evidence
    2  the check could not run -- the table or the totals sentence was not
       found, so nothing was verified. Not success.

    python3 scripts/check-evidence.py
    python3 scripts/check-evidence.py --self-test   # prove the rules can fail
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_CANNOT_VERIFY = 0, 1, 2
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
METRICS = ROOT / "evidence" / "metrics.json"
README = ROOT / "README.md"

ROW = re.compile(
    r"^\|\s*\[`(?P<repo>[a-z0-9-]+)`\]\([^)]*\)\s*\|[^|]*\|\s*"
    r"(?P<collected>\d+|—)\s*\|\s*(?P<passed>\d+|—)\s*\|\s*$",
    re.MULTILINE,
)
TOTAL = re.compile(
    r"\*\*Итого (?P<bots>[\d ]+) тестов\*\*.*?"
    r"\((?P<bots_passed>[\d ]+) проходят, (?P<bots_skipped>[\d ]+) пропущены\) плюс "
    r"(?P<core>[\d ]+) в общей библиотеке `botkit-core` "
    r"\((?P<core_passed>[\d ]+) проходят, (?P<core_skipped>[\d ]+) пропущены\): "
    r"\*\*(?P<all>[\d ]+) собранных, (?P<all_passed>[\d ]+) проходящих, "
    r"(?P<all_skipped>[\d ]+) пропущенных\*\*",
    re.DOTALL,
)


def as_int(value: str) -> int:
    return int(value.replace(" ", "").replace("\u00a0", ""))


def verify(readme_text: str, metrics: dict) -> list[str]:
    """Every disagreement between the prose and the measurement."""
    problems: list[str] = []
    flat = re.sub(r"\s+", " ", readme_text)

    rows = {m.group("repo"): m for m in ROW.finditer(readme_text)}
    for entry in metrics["repositories"]:
        repo = entry["repo"]
        row = rows.get(repo)
        if row is None:
            problems.append(f"README has no table row for {repo}")
            continue
        if row.group("collected") == "—":
            problems.append(f"README row for {repo} has no test count")
            continue
        if as_int(row.group("collected")) != entry["collected"]:
            problems.append(
                f"{repo}: README says {row.group('collected')} collected, "
                f"evidence says {entry['collected']}"
            )
        if as_int(row.group("passed")) != entry["passed"]:
            problems.append(
                f"{repo}: README says {row.group('passed')} passed, "
                f"evidence says {entry['passed']}"
            )

    m = TOTAL.search(flat)
    if m is None:
        problems.append("cannot find the totals sentence in README; wording changed?")
        return problems

    expected = {
        "bots": metrics["totals"]["bots"]["collected"],
        "bots_passed": metrics["totals"]["bots"]["passed"],
        "bots_skipped": metrics["totals"]["bots"]["skipped"],
        "core": metrics["totals"]["core"]["collected"],
        "core_passed": metrics["totals"]["core"]["passed"],
        "core_skipped": metrics["totals"]["core"]["skipped"],
        "all": metrics["totals"]["all"]["collected"],
        "all_passed": metrics["totals"]["all"]["passed"],
        "all_skipped": metrics["totals"]["all"]["skipped"],
    }
    for key, want in expected.items():
        got = as_int(m.group(key))
        if got != want:
            problems.append(f"totals.{key}: README says {got}, evidence says {want}")

    return problems


def self_test(readme_text: str, metrics: dict) -> bool:
    """Break each rule on purpose and require the checker to notice."""
    cases: list[tuple[str, str, dict]] = []
    original = readme_text

    mutated = original.replace("| 185 | 179 |", "| 184 | 179 |", 1)
    cases.append(("row count changed", mutated, metrics))

    mutated = original.replace("| 185 | 179 |", "| 185 | 178 |", 1)
    cases.append(("row passed changed", mutated, metrics))

    mutated = re.sub(r"^\| \[`botkit-leadgen`\].*\n", "", original, count=1, flags=re.MULTILINE)
    cases.append(("row deleted", mutated, metrics))

    mutated = original.replace("**Итого 1 439 тестов**", "**Итого 1 438 тестов**", 1)
    cases.append(("total changed", mutated, metrics))

    mutated = original.replace("1 537 собранных", "1 536 собранных", 1)
    cases.append(("all-total changed", mutated, metrics))

    ok = True
    for name, text, data in cases:
        problems = verify(text, data)
        if problems:
            print(f"ok   self-test: {name} is caught ({problems[0]})")
        else:
            print(f"FAIL self-test: {name} was not caught")
            ok = False
    return ok


def main() -> int:
    if not METRICS.is_file() or not README.is_file():
        print("cannot verify: evidence/metrics.json or README.md is missing", file=sys.stderr)
        return EXIT_CANNOT_VERIFY
    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    readme_text = README.read_text(encoding="utf-8")

    if "--self-test" in sys.argv:
        return EXIT_OK if self_test(readme_text, metrics) else EXIT_FAIL

    problems = verify(readme_text, metrics)
    if problems:
        print(f"README disagrees with evidence/metrics.json ({len(problems)} problem(s))")
        for p in problems:
            print(f"  {p}")
        return EXIT_FAIL
    print(f"README agrees with evidence/metrics.json ({len(metrics['repositories'])} repositories)")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
