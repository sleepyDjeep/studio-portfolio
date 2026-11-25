#!/usr/bin/env python3
"""
One command for the whole portfolio update routine.

    python tools/update_portfolio.py

Steps run in order and the first failure stops the run:
  1. tools/build_portfolio.py        rebuilds portfolio-data.js from docs/ + assets/
  2. tools/verify_portfolio.py       the five coverage, completeness, asset, prose and privacy gates
  3. tools/check_bundle_freshness.py proves the committed payload matches a clean rebuild
  4. tools/backup_manifest.py        snapshots data/master_manifest.json outside the repo, once
                                     the gates have passed, so a broken state is never backed up

Gate 1 of the verifier reads the local LanceDB and conversation SQLite databases.
Machines without them (CI, a fresh clone) pass --no-verify and still get steps 1 and 3.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent

# (human label, script in tools/, needs the local databases)
STEPS = (
    ("Rebuild portfolio-data.js from docs/ + assets/", "build_portfolio.py", False),
    ("Verify the five portfolio gates", "verify_portfolio.py", True),
    ("Prove the committed bundle matches a clean rebuild", "check_bundle_freshness.py", False),
    ("Snapshot the private manifest outside the repo", "backup_manifest.py", False),
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild, verify and prove the portfolio bundle.")
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="skip the five-gate verifier (it needs the local LanceDB and conversation databases)",
    )
    args = parser.parse_args()

    steps = [step for step in STEPS if not (args.no_verify and step[2])]
    started = time.perf_counter()

    for index, (label, script, _needs_databases) in enumerate(steps, start=1):
        print(f"\n[{index}/{len(steps)}] {label}")
        step_started = time.perf_counter()
        result = subprocess.run(
            [sys.executable, str(PORTFOLIO_ROOT / "tools" / script)],
            cwd=str(PORTFOLIO_ROOT),
        )
        if result.returncode != 0:
            print(f"\n[FAIL] {script} exited {result.returncode}; stopping here.")
            return result.returncode
        print(f"[done] {script} in {time.perf_counter() - step_started:.1f}s")

    elapsed = time.perf_counter() - started
    print(f"\n[OK] portfolio-data.js rebuilt, verified and current ({elapsed:.1f}s total)")
    print("Commit it with: git add portfolio-data.js && git commit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
