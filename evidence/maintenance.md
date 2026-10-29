# Maintenance

## Monthly (1st of the month)

1. Run `scripts/refresh-evidence.sh`. If it reports drift, review the diff in
   `evidence/metrics.json` and open a PR with the updated numbers and `raw/`.
2. If any number changed, update the inline `[E:<id>]` markers is not needed
   (they point at claim ids, not at values), but check that `check-claims.py`
   still passes.
3. If a claim's `measured_at` is older than 30 days, the scheduled
   `refresh-evidence` workflow fails. Fix by re-measuring, not by bumping the
   date.
4. Bump patch version if a number changed: edit `CITATION.cff`, add a
   `### Fixed`/`### Changed` entry under `[Unreleased]`, tag `v1.0.x`, push the
   tag (the `release.yml` workflow publishes the release).

## Quarterly

1. Re-check every `t.me` link in README/docs by hand (lychee cannot reach them
   from CI; see `lychee.toml`).
2. Run `gitleaks git --redact` locally against the full history.
3. Re-read `SECURITY.md` design commitments against the actual repository.

## On a structural change

1. The whole book lives in README.md. If it is split or merged, run
   `check-doc-split.py` against the frozen snapshot first.
2. If anchors move, that is a major release (2.x) per the CHANGELOG policy.
   Decide before editing, not after.

## Checklist before tagging

- [ ] `python3 scripts/check-repo-contract.py . scripts/repo-contract.json`
- [ ] `python3 scripts/check-repo-contract_test.py`
- [ ] `python3 scripts/check-evidence.py && python3 scripts/check-evidence.py --self-test`
- [ ] `python3 scripts/check-claims.py --strict`
- [ ] `python3 scripts/check-templates.py && python3 scripts/check-templates.py --self-test`
- [ ] `python3 scripts/check-version.py`
- [ ] `ruff check .`
- [ ] `gitleaks git --redact`
- [ ] `CITATION.cff` version == tag
- [ ] CHANGELOG has a section for the tag
