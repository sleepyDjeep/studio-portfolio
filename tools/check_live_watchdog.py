#!/usr/bin/env python3
"""
Morning watchdog: fail when the daily live check has not succeeded.

GitHub documents that a scheduled run can be delayed for hours and that queued
runs can be dropped, and a run that never happens leaves no red row behind. This
looks for a successful run of the live workflow created since 08:00 local time
(08:00 America/Chicago by default) and exits non-zero when the morning passed
with nothing to show, so a silent morning becomes a failed run with an issue.

    python tools/check_live_watchdog.py
    python tools/check_live_watchdog.py --since 2026-11-25T14:00:00Z
    python tools/check_live_watchdog.py --repo owner/name --workflow other.yml

Set GH_TOKEN (or GITHUB_TOKEN) to use the GitHub Actions token; the runs list is
public for a public repository, so a token is optional when calling by hand.

Exit codes: 0 = a successful run exists in the window, 1 = none, 2 = could not check.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python without zoneinfo
    ZoneInfo = None

DEFAULT_REPO = "sleepydjeep/studio-portfolio"
DEFAULT_WORKFLOW = "portfolio-live-freshness.yml"
DEFAULT_TIMEZONE = "America/Chicago"
DEFAULT_HOUR = 8
API_ROOT = "https://api.github.com"

# A transient API error should not look like a missed morning.
RETRY_ATTEMPTS = 3
RETRY_BASE_DELAY = 2.0


def annotate(message: str) -> None:
    """Surface the failure as an annotation when running inside GitHub Actions."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::error::{message}")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def window_start(since: str | None, zone: str, hour: int) -> datetime:
    if since:
        return parse_time(since)
    if ZoneInfo is None:
        raise SystemExit("[watchdog] zoneinfo is unavailable; pass --since as an ISO timestamp")
    local = datetime.now(ZoneInfo(zone))
    return local.replace(hour=hour, minute=0, second=0, microsecond=0).astimezone(timezone.utc)


def list_runs(repo: str, workflow: str) -> list[dict]:
    url = (
        f"{API_ROOT}/repos/{urllib.parse.quote(repo, safe='/')}"
        f"/actions/workflows/{urllib.parse.quote(workflow, safe='')}/runs?per_page=100"
    )
    headers = {
        "User-Agent": "studio-portfolio-watchdog",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    last_error = ""
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
            runs = payload.get("workflow_runs")
            if not isinstance(runs, list):
                raise ValueError("response has no workflow_runs list")
            return runs
        except urllib.error.HTTPError as exc:
            if exc.code < 500 and exc.code != 429:
                raise RuntimeError(f"HTTP {exc.code} from the runs API")
            last_error = f"HTTP {exc.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as exc:
            last_error = str(exc)

        if attempt < RETRY_ATTEMPTS:
            delay = RETRY_BASE_DELAY * 2 ** (attempt - 1)
            print(f"[watchdog] runs API failed ({last_error}); retrying in {delay:.0f}s", file=sys.stderr)
            time.sleep(delay)

    raise RuntimeError(f"runs API unreachable after {RETRY_ATTEMPTS} attempts: {last_error}")


def describe(run: dict) -> str:
    return (
        f"{run.get('created_at')} {run.get('status')}/{run.get('conclusion') or 'pending'} "
        f"{run.get('event')} {run.get('html_url')}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail when the daily live check has not succeeded.")
    parser.add_argument("--repo", default=DEFAULT_REPO, help=f"owner/name (default: {DEFAULT_REPO})")
    parser.add_argument("--workflow", default=DEFAULT_WORKFLOW, help=f"workflow file name (default: {DEFAULT_WORKFLOW})")
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE, help=f"IANA zone for the window (default: {DEFAULT_TIMEZONE})")
    parser.add_argument("--hour", type=int, default=DEFAULT_HOUR, help=f"local hour the window opens (default: {DEFAULT_HOUR})")
    parser.add_argument("--since", help="ISO timestamp to use instead of today's window, for testing")
    args = parser.parse_args()

    since = window_start(args.since, args.timezone, args.hour)
    now = datetime.now(timezone.utc)
    window_label = since.strftime("%Y-%m-%d %H:%M UTC")

    if now < since:
        print(f"[watchdog] window opens at {window_label}; nothing to check yet")
        return 0

    try:
        runs = list_runs(args.repo, args.workflow)
    except RuntimeError as exc:
        print(f"[watchdog] could not check {args.repo} {args.workflow}: {exc}", file=sys.stderr)
        return 2

    recent = [run for run in runs if parse_time(run["created_at"]) >= since]
    winners = [run for run in recent if run.get("conclusion") == "success"]

    if winners:
        best = winners[0]
        print(f"[watchdog] live check succeeded at {best.get('created_at')}: {best.get('html_url')}")
        return 0

    print(f"=== NO SUCCESSFUL LIVE CHECK SINCE {window_label} ===")
    print(f"window: {window_label} -> {now.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"runs of {args.workflow} created in the window: {len(recent)}")
    for run in recent[:5]:
        print(f"  [run] {describe(run)}")
    if runs:
        print(f"newest run of the workflow: {describe(runs[0])}")
    else:
        print("the workflow has no runs at all")
    print()
    print("GitHub can delay a scheduled run by hours or drop it entirely, and a dropped run")
    print("leaves nothing to notice. A morning with no successful run is a missing check, not")
    print("a pass: open the workflow dispatch and run it by hand, then look at what failed.")

    annotate(f"No successful live atlas run since {window_label}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
