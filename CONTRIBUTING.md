# Contributing to the Agentic Development Playbook

This repository is a document, not a service. There is no runtime, no container
and no test suite to run against a bot — the artifact is the text and the claims
inside it. A change here is a change to what a reader will believe, so the bar is
evidence, not style.

## What a change has to carry

Every factual claim in the document — a test count, a coverage number, a service
count, a deployment status — must be:

1. **Dated.** The date the number was measured, not the date it was written.
2. **Reproducible.** The command that produces it, and the commit it was run at.
3. **Level-tagged.** See [Evidence levels](#evidence-levels) below. A number
   copied from a dashboard is not the same kind of fact as a number produced by
   a command in the repository.

If you cannot reproduce a number, say so in the text. "Not verified" is an
acceptable statement; an unverified number presented as measured is not.

### Evidence levels

| Level | Meaning | Example |
|---|---|---|
| **E1** | Reproducible from a public repository with one command | `pytest` output at a named commit |
| **E2** | Observed on a running system, with a link to the run | a green deploy workflow |
| **E3** | Self-reported by the author or a vendor, not independently checked | a hosting panel's uptime figure |
| **E4** | Planned or intended, not yet true | "will be added in v1.1" |

Mark E3 and E4 inline. Unmarked statements are E1 or E2.

## Local checks

The local gate is the repository contract checker. It is standard-library Python
and needs nothing installed beyond Python 3.12.

```bash
python3 scripts/check-repo-contract.py . scripts/repo-contract.json
python3 scripts/check-repo-contract_test.py
python3 scripts/check-evidence.py
python3 scripts/check-evidence.py --self-test
```

All four must exit `0`. The negative tests are not optional: they prove the
checks can fail. A validator that has only ever returned green has been
exercised, not tested.

If you change a rule in a checker, add the negative test that makes the rule
fail first. The pull request should show the test red before the fix and green
after it.

## Editing rules

- **The body is Russian; the front page is English.** The Russian text is the
  author's own writing and is not machine-translated. An English summary at the
  top is a summary, not a translation, and must say so.
- **`docs/en/` is an outline, not a translation.** Each file states plainly that
  the Russian text is the canon and links to it. Machine translation of a whole
  chapter is not allowed.
- **Headings inside code fences are not anchors.** If you add a table-of-contents
  entry, point it at a rendered heading. The checker now enforces this; before
  it did, 18 of 31 anchors in this README were dead.
- **No internal hostnames, public IPs, customer identifiers or real personal
  data** in examples. Use reserved values (`192.0.2.10`, `+7 (999) 000-00-00`).
- **One concern per pull request.** A factual correction and a restructuring are
  two pull requests.
- **Conventional Commits** for the subject: `docs:`, `fix:`, `ci:`, `chore:`.
- **Update `CHANGELOG.md`** under `[Unreleased]` when the change is visible to a
  reader.

## Pull request rules

Use the pull-request template. It asks for the command you ran and its output;
"the checker is green" without the output is not evidence, because a checker can
be green about a rule that never ran.

For a factual correction, include:

- the old claim and where it appears;
- the measurement that contradicts it, with the command and the commit;
- the new wording.

## AI-assisted contributions

Fine, and expected — the document is about this way of working. Two conditions:

1. Say which parts were agent-generated.
2. The agent must have run the checks above, in this repository, and the output
   belongs in the pull request. "The agent says it passes" is not evidence.

## Reporting a problem with a claim

Open a bug report. Name the claim, the section, and what you measured instead.
A claim that cannot be reproduced is a bug in the document, not a difference of
opinion.

## Security

Do not open a public issue for a security problem. See [SECURITY.md](SECURITY.md).

## Code of conduct

Be straightforward and assume good faith. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
