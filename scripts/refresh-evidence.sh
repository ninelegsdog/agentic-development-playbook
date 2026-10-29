#!/usr/bin/env bash
# Re-measure the ten public repositories and report drift against
# evidence/metrics.json. Used by the monthly refresh workflow and by hand.
#
# Usage:
#   scripts/refresh-evidence.sh                 # all ten, fail on any drift
#   scripts/refresh-evidence.sh --repo X        # one repository
#   scripts/refresh-evidence.sh --dry-run       # measure, do not fail (exit 0)
#
# Exit codes: 0 no drift (or dry-run), 1 drift detected, 2 cannot run.
set -u

REPO_FILTER=""
DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO_FILTER="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
METRICS="$ROOT/evidence/metrics.json"
WORK="${TMPDIR:-/tmp}/refresh-evidence-$$"
mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT

if ! command -v uv >/dev/null 2>&1; then
  echo "cannot run: uv is not installed" >&2
  exit 2
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "cannot run: python3 is not installed" >&2
  exit 2
fi

python3 - "$METRICS" "$REPO_FILTER" "$WORK" <<'PY'
import json, subprocess, sys, os
metrics_path, repo_filter, work = sys.argv[1], sys.argv[2], sys.argv[3]
data = json.load(open(metrics_path))
entries = data["repositories"]
if repo_filter:
    entries = [e for e in entries if e["repo"] == repo_filter]
    if not entries:
        print(f"unknown repo: {repo_filter}", file=sys.stderr)
        sys.exit(2)

drift = False
for e in entries:
    repo = e["repo"]; sha = e["sha"]
    clone = os.path.join(work, repo)
    subprocess.run(["git", "clone", "-q", f"https://github.com/ninelegsdog/{repo}", clone],
                  check=True, capture_output=True)
    subprocess.run(["git", "-C", clone, "checkout", "-q", sha], check=True, capture_output=True)
    # sync
    if repo == "botkit-core":
        subprocess.run(["uv", "sync", "--all-extras"], cwd=clone, check=True,
                       capture_output=True, timeout=300)
    else:
        subprocess.run(["uv", "sync", "--frozen", "--all-extras"], cwd=clone, check=True,
                       capture_output=True, timeout=300)
    # collect
    collect_out = subprocess.run(["uv", "run", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
                                cwd=clone, capture_output=True, text=True, timeout=300)
    collected = None
    for line in collect_out.stdout.splitlines() + collect_out.stderr.splitlines():
        import re
        m = re.search(r"(\d+) tests? collected", line)
        if m:
            collected = int(m.group(1))
    # run
    run_out = subprocess.run(["uv", "run", "pytest", "-q", "-p", "no:cacheprovider"],
                            cwd=clone, capture_output=True, text=True, timeout=600)
    passed = skipped = 0
    cov = None
    for line in (run_out.stdout + "\n" + run_out.stderr).splitlines():
        m = re.search(r"(\d+) passed", line); 
        if m: passed = int(m.group(1))
        m = re.search(r"(\d+) skipped", line)
        if m: skipped = int(m.group(1))
        m = re.search(r"Total coverage: ([0-9.]+)%", line)
        if m: cov = float(m.group(1))
    print(f"{repo} @ {sha[:7]}: collected={collected} (was {e['collected']}), "
          f"passed={passed} (was {e['passed']}), skipped={skipped} (was {e['skipped']}), "
          f"coverage={cov} (was {e['coverage']})")
    if (collected != e["collected"] or passed != e["passed"] or skipped != e["skipped"]
            or (cov is not None and abs(cov - e["coverage"]) > 0.5)):
        drift = True
        print(f"  -> DRIFT in {repo}")

sys.exit(1 if drift else 0)
PY
rc=$?
if [[ $DRY_RUN -eq 1 ]]; then
  echo "dry-run: ignoring exit code $rc"
  exit 0
fi
exit $rc
