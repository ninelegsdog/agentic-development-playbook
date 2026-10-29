# Changelog

All notable changes to this document are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html): a correction that
changes what a reader would believe is a patch, a new section is a minor
release, and a restructure that moves anchors is a major one.

## [Unreleased]

### Added
- `templates/` with five reusable templates (`AGENTS.md`, `spec.md`, `handoff.md`,
  `review-checklist.md`, `secrets-checklist.md`) and `templates/README.md`.
- `scripts/check-templates.py` with `--self-test` (4 mutations caught).
- Version badge in README.

### Changed
- README sections 4, 5 and 9 now link to `templates/` instead of inlining the
  full blocks.

The first tagged release. It corrects claims that were published before this date
and replaces the governance files that had been copied from a bot repository. The
author's methodology text and its structure are unchanged except where a claim
was wrong.

### Added

- `evidence/metrics.json` — the measured state of the ten public repositories at
  named commits, with the command that produced each number. The README now
  quotes this file rather than numbers typed into prose.
- `evidence/raw/` — the tail of each pytest run, so the summary can be checked
  without re-running the suite.
- `scripts/check-evidence.py` — fails CI when a number in the README stops
  matching `evidence/metrics.json`, with `--self-test` proving each rule can fire.
- `evidence/README.md` — what each field means and how to re-measure it.
- `CITATION.cff`, so the document can be cited by version.
- Negative tests for the two validator defects fixed below: a fenced heading is
  not an anchor, and a clone is identified by its remote rather than its folder
  name.

### Fixed

- **Coverage claim.** The document said measured coverage was "about 32%" and
  that `pytest` exits non-zero because of the coverage gate. That figure is an
  artefact of `pytest --collect-only`, which imports modules but runs no tests.
  At the publication commits, eight of nine bots measure 72.7–92.9%; at current
  `main`, nine of nine pass their gates at 71.7–92.2%. The section now states
  what was measured, how, and what the 32% actually was.
- **Test counts.** "≈1038 tests in nine bots + 59 in `botkit-core`" replaced with
  the measured 1,537 collected, 1,499 passed, 38 skipped, dated and with SHAs.
- **Contents.** 18 of 31 anchors pointed at headings inside code fences, which
  GitHub does not render. The table of contents is rebuilt against rendered
  headings.
- **`check-repo-contract.py` counted fenced headings as anchors**, which is why
  the broken Contents block passed the gate. Fenced blocks are stripped before
  headings are extracted.
- **`check-repo-contract.py` identified the repository by folder name**, so
  `git clone … playbook` was rejected as an unknown repository. It now resolves
  the remote first and falls back to the folder name.
- **"12 containers"** in the infrastructure paragraph: `botkit-monitoring`
  composes 10 services.

### Changed

- `CONTRIBUTING.md` and `SECURITY.md` rewritten for a documentation repository.
  The previous versions were copied from a Telegram bot and instructed the
  reader to run `uv sync`, `pre-commit` and `pytest` against files that do not
  exist here, and described a webhook, an admin panel and a container that this
  repository does not have.
- Issue forms and the pull-request template now ask about claims and evidence
  rather than bot handlers and migrations.
- CI now runs the validator's negative tests, the evidence check and a secret
  scan over the full history, not only the validator against the working tree.

### Removed

- Claims that this repository's CI publishes an SBOM, scans with Trivy and
  validates a k6 load script. None of those ran here; the sentence described the
  bots' pipeline. A secret scan was the one part worth keeping, and it now runs
  here for real.
