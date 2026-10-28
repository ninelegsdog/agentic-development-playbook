# Security Policy

## Reporting a vulnerability

**Do not open a public issue.**

Use GitHub's private vulnerability reporting at
<https://github.com/ninelegsdog/agentic-development-playbook/security/advisories/new>.
Include what the issue is, what an attacker gains, and the commit or version it
affects.

You should get an acknowledgement within a few days. Confirmed issues are fixed
on `main` and cut in a patch release; the reporter is credited unless they prefer
otherwise.

## Scope

This repository publishes a document and the small Python checks that guard it.
The security surface is therefore small and specific.

In scope:

- **The contract checker** (`scripts/check-repo-contract.py`) — it reads
  repository files and is executed by CI. A path traversal, a crash on hostile
  input, or a check that silently passes is a security-relevant defect, because
  a green gate that did not run is worse than a red one.
- **The CI workflows** — permissions, action pinning, and anything that could
  let a pull request execute code with a write-scoped token.
- **Secrets and personal data in the repository** — a token in the history, a
  real customer identifier, a public IP or an internal hostname in an example.
- **Supply chain** — a compromised action or dependency used by CI.

Out of scope:

- The nine Telegram bots, `botkit-core`, `botkit-monitoring`, `botkit-farm` and
  the templates. Each has its own repository and its own policy; report there.
- Findings that require an attacker who already has write access to this
  repository.
- GitHub itself, and vulnerabilities in the actions used here — report those
  upstream, though a note here is welcome if the pin needs to move.

## Design commitments

These are properties this repository holds itself to. A change that breaks one
is a security change and needs review.

1. **No secret ever enters git.** There is no `.env` here and no runtime secret.
   CI scans the full history, not just the tip, because a secret removed in a
   later commit is still in the history.
2. **CI actions are pinned by commit SHA**, not by a mutable tag. A tag can be
   moved under a repository that has already trusted it.
3. **CI tokens are read-only.** The workflow declares `permissions: contents:
   read` and does not use `pull_request_target`, so a pull request from a fork
   cannot execute with a write token.
4. **Examples use reserved data.** Documentation examples use addresses from
   the reserved ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) and
   phone numbers from the reserved block (`+7 (999) 000-00-00`). A real hostname
   or IP in an example is a defect, even if it looks harmless.
5. **A gate that cannot fail is not a gate.** Every rule in the checker has a
   negative test, and CI runs those tests alongside the checker.

## Supported versions

The document is versioned by git tag; the current release is listed in
[CHANGELOG.md](CHANGELOG.md). Security fixes land on `main` and are cut from
there as a patch release. There is no long-term-support branch.
