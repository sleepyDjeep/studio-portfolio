#!/usr/bin/env python3
"""
Post-push live check for the entries a push just changed.

tools/check_live_shell.py hashes the whole payload once every four days, so a new
entry's images could go unchecked for up to 96 hours. This script closes that
window: it diffs the pushed range, keeps the entry docs that were added or
edited, waits for the deployed portfolio-data.js to list those ids (Pages builds
after CI, so the first fetches can still see the previous deploy), then fetches
each of their media and diagram files and compares the bytes with the sha256 the
committed bundle recorded. A 404, a wrong content type or differing bytes fails
the run and names the path.

    python tools/check_live_push.py --base HEAD^ --head HEAD
    python tools/check_live_push.py --ids aether-engine --timeout 120
    python tools/check_live_push.py --base "$GITHUB_EVENT_BEFORE" --head "$GITHUB_SHA"

Pushes that do not touch an entry doc exit 0 without fetching anything.

Exit codes: 0 = verified or nothing to check, 1 = missing/mismatched/never deployed.
"""

import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = PORTFOLIO_ROOT / "portfolio-data.js"
BUNDLE_PREFIX = "window.PORTFOLIO_DATA = "
DEFAULT_BASE = "https://sleepydjeep.github.io/studio-portfolio/"

CONTENT_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".wav": "audio/",
}

sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import FrontmatterError, split_document  # noqa: E402


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=str(PORTFOLIO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    ).stdout


def changed_docs(base: str, head: str) -> list[str]:
    paths = []
    for line in git("diff", "--name-status", base, head, "--", "docs").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0] in {"A", "M"} and parts[1].endswith(".md"):
            paths.append(parts[1])
    return paths


def commit_exists(ref: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
        cwd=str(PORTFOLIO_ROOT),
        capture_output=True,
    ).returncode == 0


def ensure_base(base: str) -> bool:
    """Shallow checkouts, force pushes and first pushes can lack the old commit."""
    if commit_exists(base):
        return True
    subprocess.run(
        ["git", "fetch", "--quiet", "--depth=1", "origin", base],
        cwd=str(PORTFOLIO_ROOT),
        capture_output=True,
        text=True,
    )
    return commit_exists(base)


def head_doc_changes(head: str) -> list[str]:
    """Docs touched by the head commit alone, used when there is no base to diff."""
    paths = []
    for line in git("diff-tree", "--no-commit-id", "--name-status", "-r", "--root", head, "--", "docs").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0] in {"A", "M"} and parts[1].endswith(".md"):
            paths.append(parts[1])
    return paths


def entry_from_doc(path: str, text: str) -> tuple[str, dict] | None:
    try:
        meta, _body = split_document(text, path)
    except FrontmatterError as exc:
        print(f"[entry-live] skipping unparseable doc: {exc}")
        return None
    if str(meta.get("visibility") or "").strip().lower() == "vault":
        return None
    if "vault" in Path(path).relative_to("docs").parts:
        return None
    ident = str(meta.get("id") or Path(path).stem).strip()
    media = meta.get("media") if isinstance(meta.get("media"), list) else []
    return ident, {
        "media": [str(item.get("src") or "") for item in media if isinstance(item, dict)],
        "diagram": str(meta.get("diagram") or ""),
    }


def local_bundle() -> dict:
    raw = BUNDLE_PATH.read_text(encoding="utf-8")
    index = raw.find(BUNDLE_PREFIX)
    if index == -1:
        raise SystemExit("[entry-live] portfolio-data.js has no PORTFOLIO_DATA assignment")
    return json.loads(raw[index + len(BUNDLE_PREFIX):].rstrip().rstrip(";"))


def fetch(url: str, timeout: int = 30) -> tuple[bytes, str]:
    request = urllib.request.Request(
        url, headers={"Cache-Control": "no-cache", "User-Agent": "portfolio-entry-live-check"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(), response.headers.get("Content-Type", "")


def wait_for_bundle(base_url: str, ids: set[str], timeout: float, interval: float) -> dict:
    deadline = time.time() + timeout
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        url = f"{base_url}portfolio-data.js?entry-check={int(time.time())}-{attempt}"
        try:
            raw, _ = fetch(url)
            text = raw.decode("utf-8", errors="replace")
            index = text.find(BUNDLE_PREFIX)
            bundle = json.loads(text[index + len(BUNDLE_PREFIX):].rstrip().rstrip(";")) if index >= 0 else {}
            live_ids = {str(entry.get("id")) for entry in bundle.get("entries", [])}
            missing = ids - live_ids
            if not missing:
                print(f"[entry-live] deploy lists {', '.join(sorted(ids))} (attempt {attempt}).")
                return bundle
            print(f"[entry-live] waiting for the deploy to list {', '.join(sorted(missing))}.")
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            print(f"[entry-live] bundle fetch failed ({exc}); retrying.")
        time.sleep(interval)
    raise SystemExit(f"[entry-live] {', '.join(sorted(ids))} never appeared in the deployed bundle")


def verify_assets(base_url: str, bundle: dict, ids: set[str]) -> list[str]:
    problems: list[str] = []
    for entry in bundle.get("entries", []):
        if str(entry.get("id")) not in ids:
            continue
        assets = []
        if entry.get("diagram"):
            assets.append((str(entry["diagram"]), str(entry.get("diagram_sha256") or "")))
        for item in entry.get("media", []):
            assets.append((str(item.get("src") or ""), str(item.get("sha256") or "")))
        for src, digest in assets:
            url = f"{base_url}{src}?v={digest[:12]}"
            try:
                data, content_type = fetch(url)
            except urllib.error.HTTPError as exc:
                problems.append(f"{src}: HTTP {exc.code} from the deployed site")
                continue
            except (urllib.error.URLError, TimeoutError) as exc:
                problems.append(f"{src}: {exc}")
                continue
            required = CONTENT_TYPES.get(Path(src).suffix.lower())
            if required and required not in content_type:
                problems.append(f"{src}: Content-Type {content_type!r} is not {required}")
            served = hashlib.sha256(data).hexdigest()
            if digest and served != digest:
                problems.append(f"{src}: served sha256 {served[:12]} != bundle {digest[:12]}")
        print(f"[entry-live] {entry['id']}: checked {len(assets)} asset(s).")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a just-pushed entry on the live site.")
    parser.add_argument("--base", help="commit before the push (defaults to HEAD^)")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--timeout", type=float, default=600.0, help="seconds to wait for the deploy")
    parser.add_argument("--interval", type=float, default=15.0)
    parser.add_argument("--ids", help="comma-separated ids to check, skipping the diff (for testing)")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/") + "/"
    if args.ids:
        ids = {item.strip() for item in args.ids.split(",") if item.strip()}
    else:
        base = args.base or "HEAD^"
        if ensure_base(base):
            paths = changed_docs(base, args.head)
            range_label = f"{base}..{args.head}"
        else:
            print(
                f"::notice::base commit {base} is not available (shallow clone, force push "
                f"or first push); checking only the docs changed by {args.head}"
            )
            paths = head_doc_changes(args.head)
            range_label = f"{args.head} alone"
        entries = [entry_from_doc(path, git("show", f"{args.head}:{path}")) for path in paths]
        found = {ident: detail for ident, detail in (item for item in entries if item)}
        if not found:
            print(f"[entry-live] no entry docs changed in {range_label}; nothing to check.")
            return 0
        ids = set(found)
        print(f"[entry-live] changed entries: {', '.join(sorted(ids))}.")

    bundle = wait_for_bundle(base_url, ids, args.timeout, args.interval)
    problems = verify_assets(base_url, bundle, ids)
    if problems:
        print("\n=== LIVE ENTRY CHECK FAILED ===")
        for problem in problems:
            print(f"  [X] {problem}")
        return 1
    print(f"\n[entry-live] {len(ids)} entry id(s) and their assets verified on {base_url}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
