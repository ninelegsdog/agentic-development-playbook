# Evidence

`metrics.json` is the measured state of the ten public repositories the playbook
refers to. The README quotes this file; the file is the source of truth when the
two disagree.

## What was measured

For each repository, at the commit recorded in its `sha` field:

| Field | Meaning |
|---|---|
| `collected` | tests pytest collected (`pytest --collect-only -q`) |
| `passed`, `skipped`, `failed` | outcome of the real run (`pytest -q`) |
| `coverage` | total coverage reported by that repository's own pytest-cov configuration |
| `coverage_gate_percent` | the `--cov-fail-under` value in that repository's `pyproject.toml` |
| `gate_passed` | coverage at or above the gate **and** the suite exited 0 |
| `command` | the exact command used |

Totals are in `totals.bots`, `totals.core` and `totals.all`.

## Raw output

`raw/<repository>.txt` holds the tail of the actual pytest run — the coverage
table, the skipped tests and the final line — so the summary in `metrics.json`
can be checked without a network round trip. The commit, command and exit code
are in the file header.

## How to reproduce

```bash
git clone https://github.com/ninelegsdog/botkit-bookingbot
cd botkit-bookingbot
git checkout a43321f
uv sync --frozen --all-extras
uv run pytest -q
```

Repeat for each entry. `botkit-core` ships no `uv.lock`, so `--frozen` fails
there; use `uv sync --all-extras`.

Measured on 2026-10-28 with Python 3.13.14 and uv 0.11.32 on Linux x86_64.
Coverage can move by a few tenths of a percent with a different dependency
resolution; the gate result is the assertion that matters, and it is recorded
per repository.

## What this file does not prove

This is **E1** for test counts and coverage: anyone can re-run the command at
the same commit. It is not evidence that:

- the bots answer right now — a green deploy run (**E2**) proves an image was
  built and pushed, not that the process is healthy;
- the production host is reachable or correctly configured;
- the tests are good tests. A passing suite proves the assertions hold, not that
  they are the right assertions. The review checklists exist for that reason.

Claims that are self-reported carry **E3** in the text; claims about future work
carry **E4**. Unmarked numbers in the README are E1 and trace back to this file.

## A note on the 32% figure

An earlier version of the README said measured coverage was "about 32%". That
number is reproducible only with `pytest --collect-only`, which imports modules
and runs no tests, so pytest-cov reports coverage of almost nothing (26.46% for
`botkit-bookingbot`, for example). It is an artefact of the measurement, not a
property of the code. The real runs are in `metrics.json`.
