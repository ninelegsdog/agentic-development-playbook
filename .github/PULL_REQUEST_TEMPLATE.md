## What this changes

<!-- One concern. A factual correction and a restructuring are two pull requests. -->

## Why

<!-- The diff shows what changed. Say why it had to: what was wrong, or what a reader could not do. -->

## Evidence

<!--
For a factual change this is the part that makes it reviewable. Paste the command
and its output, at the commit you ran it against.

    git -C ../botkit-bookingbot rev-parse --short HEAD
    uv run pytest -q

For a navigation change, paste the checker output before and after:

    python3 scripts/check-repo-contract.py . scripts/repo-contract.json
-->

## Checks

- [ ] `python3 scripts/check-repo-contract.py . scripts/repo-contract.json` exits 0, output above.
- [ ] `python3 scripts/check-repo-contract_test.py` exits 0, output above.
- [ ] If a checker rule changed: the new negative test was red before the fix and is green after it.
- [ ] Every number I touched carries a measurement date and the command that produces it.

## Documentation

- [ ] `CHANGELOG.md` updated under `[Unreleased]`.
- [ ] `README.md` updated if a reader-visible claim changed.
- [ ] `AGENTS.md` updated if an agent working here would otherwise get it wrong.

## Security

- [ ] No secret, token, customer identifier, public IP or internal hostname in the diff.
- [ ] Examples use reserved values (`192.0.2.10`, `+7 (999) 000-00-00`).

## AI assistance

- [ ] Parts of this change were agent-generated — described which.
- [ ] The agent ran the checks above, in this repository, and the output is above.
