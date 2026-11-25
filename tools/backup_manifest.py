#!/usr/bin/env python3
"""
Off-repo snapshots of data/master_manifest.json.

That file is the only copy of the reconciliation state Gate 1 measures against,
and data/ is gitignored, so losing it loses the ability to prove coverage at all.
This script copies it to a private folder outside the repository (OneDrive by
default, so a snapshot also leaves the machine), keeps the last 30 snapshots,
records every sha256 in backup_index.json, and can put one back.

    python tools/backup_manifest.py                       take a snapshot
    python tools/backup_manifest.py --list                show what is stored
    python tools/backup_manifest.py --verify              compare the newest snapshot with the live file
    python tools/backup_manifest.py --restore latest
    python tools/backup_manifest.py --restore master_manifest_20261125T053000Z.json

Destination order: --dest, PORTFOLIO_BACKUP_DIR, <home>\\OneDrive\\Backups\\
studio-portfolio, then <home>\\StudioPortfolioBackups. A destination inside the
repository is refused: this data must never be committed or deployed.

Exit codes: 0 = done, 1 = refused or failed.
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PORTFOLIO_ROOT / "data" / "master_manifest.json"
INDEX_NAME = "backup_index.json"
KEEP_SNAPSHOTS = 30
CHUNK = 1024 * 1024


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def summarise(meta: dict) -> dict:
    reconciliation = meta.get("reconciliation") or {}
    return {
        "entries": len(meta.get("entries") or []),
        "memories": reconciliation.get("wave0_memory_count"),
        "conversations": reconciliation.get("wave0_top_conversation_count"),
    }


def resolve_destination(explicit: str | None) -> Path:
    if explicit:
        destination = Path(explicit).expanduser()
    elif os.environ.get("PORTFOLIO_BACKUP_DIR"):
        destination = Path(os.environ["PORTFOLIO_BACKUP_DIR"]).expanduser()
    elif (Path.home() / "OneDrive").is_dir():
        destination = Path.home() / "OneDrive" / "Backups" / "studio-portfolio"
    else:
        destination = Path.home() / "StudioPortfolioBackups"

    destination = destination.resolve()
    root = PORTFOLIO_ROOT.resolve()
    if destination == root or root in destination.parents:
        raise SystemExit(
            f"[backup] refusing destination inside the repository: {destination}\n"
            "         data/ is gitignored on purpose; back the manifest up outside the repo."
        )
    return destination


def read_index(destination: Path) -> dict:
    index_path = destination / INDEX_NAME
    if not index_path.exists():
        return {"destination": str(destination), "snapshots": []}
    try:
        return json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise SystemExit(f"[backup] {index_path} is not valid JSON; fix or move it before continuing.")


def write_index(destination: Path, index: dict) -> None:
    index["destination"] = str(destination)
    index["updated_at"] = datetime.now(timezone.utc).isoformat()
    payload = json.dumps(index, indent=2) + "\n"
    scratch = destination / f"{INDEX_NAME}.tmp"
    scratch.write_text(payload, encoding="utf-8")
    os.replace(scratch, destination / INDEX_NAME)


def unique_name(destination: Path, stamp: str, kind: str) -> str:
    prefix = "master_manifest" if kind == "snapshot" else "pre-restore"
    candidate = f"{prefix}_{stamp}.json"
    suffix = 2
    while (destination / candidate).exists():
        candidate = f"{prefix}_{stamp}-{suffix}.json"
        suffix += 1
    return candidate


def take_snapshot(destination: Path, kind: str = "snapshot") -> dict:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"[backup] nothing to snapshot: {MANIFEST_PATH} does not exist on this machine.")

    destination.mkdir(parents=True, exist_ok=True)
    index = read_index(destination)
    source_sha = sha256_file(MANIFEST_PATH)

    # A routine rebuild should not spend a retention slot on bytes already stored.
    if kind == "snapshot" and index["snapshots"]:
        newest = index["snapshots"][-1]
        if newest["sha256"] == source_sha and (destination / newest["file"]).exists():
            print(f"[backup] unchanged since {newest['file']} (sha256 {source_sha[:12]}); no new snapshot written")
            return newest

    name = unique_name(destination, now_stamp(), kind)

    target = destination / name
    scratch = destination / f"{name}.tmp"
    scratch.write_bytes(MANIFEST_PATH.read_bytes())
    os.replace(scratch, target)

    # Never trust the copy until it has been read back and hashed.
    copied_sha = sha256_file(target)
    if copied_sha != source_sha:
        target.unlink(missing_ok=True)
        raise SystemExit(
            f"[backup] copy does not match the source (source {source_sha[:12]}, copy {copied_sha[:12]}); "
            "snapshot discarded."
        )

    entry = {
        "file": name,
        "taken_at": datetime.now(timezone.utc).isoformat(),
        "sha256": copied_sha,
        "bytes": target.stat().st_size,
        "kind": kind,
        **summarise(json.loads(target.read_text(encoding="utf-8"))),
    }
    index["snapshots"].append(entry)

    # Retention: drop the oldest files, never the one just written.
    while len(index["snapshots"]) > KEEP_SNAPSHOTS:
        oldest = index["snapshots"].pop(0)
        if oldest["file"] != name:
            (destination / oldest["file"]).unlink(missing_ok=True)

    write_index(destination, index)
    print(
        f"[backup] {MANIFEST_PATH.name} -> {target} "
        f"({entry['bytes']} bytes, sha256 {copied_sha[:12]}, {entry['entries']} entries, "
        f"{entry['memories']} memories / {entry['conversations']} conversations)"
    )
    print(f"[backup] {len(index['snapshots'])} snapshot(s) kept in {destination}")
    return entry


def show_list(destination: Path) -> int:
    index = read_index(destination)
    snapshots = index.get("snapshots") or []
    print(f"[backup] destination: {destination}")
    if not snapshots:
        print("[backup] no snapshots yet; run: python tools/backup_manifest.py")
        return 1
    for entry in snapshots:
        print(
            f"  {entry['taken_at'][:19]}  {entry['kind']:<11} {entry['file']}  "
            f"{entry['bytes']:>7} bytes  {entry['entries']} entries  sha256 {entry['sha256'][:12]}"
        )
    return 0


def verify(destination: Path) -> int:
    index = read_index(destination)
    snapshots = index.get("snapshots") or []
    if not snapshots:
        print("[backup] nothing to verify: no snapshots recorded.")
        return 1

    newest = snapshots[-1]
    stored = destination / newest["file"]
    if not stored.exists():
        print(f"[backup] newest snapshot is missing on disk: {stored}")
        return 1

    stored_sha = sha256_file(stored)
    if stored_sha != newest["sha256"]:
        print(f"[backup] newest snapshot is corrupt (index {newest['sha256'][:12]}, file {stored_sha[:12]})")
        return 1

    if not MANIFEST_PATH.exists():
        print(f"[backup] newest snapshot {newest['file']} is intact, but the live manifest is gone.")
        print("[backup] restore it with: python tools/backup_manifest.py --restore latest")
        return 0

    live_sha = sha256_file(MANIFEST_PATH)
    if live_sha == stored_sha:
        print(f"[backup] OK: newest snapshot {newest['file']} matches the live manifest "
              f"(sha256 {live_sha[:12]})")
        return 0

    print(f"[backup] the live manifest has changed since the newest snapshot "
          f"(live {live_sha[:12]}, backup {stored_sha[:12]}); take a new snapshot.")
    return 0


def restore(destination: Path, which: str) -> int:
    index = read_index(destination)
    snapshots = index.get("snapshots") or []
    if not snapshots:
        print(f"[backup] nothing to restore in {destination}")
        return 1

    if which == "latest":
        entry = snapshots[-1]
    else:
        matches = [s for s in snapshots if s["file"] == which]
        if not matches:
            matches = [s for s in snapshots if s["sha256"].startswith(which)]
        if len(matches) != 1:
            print(f"[backup] '{which}' matched {len(matches)} snapshots; use --list to pick one.")
            return 1
        entry = matches[0]

    stored = destination / entry["file"]
    if not stored.exists():
        print(f"[backup] snapshot file is missing: {stored}")
        return 1

    data = stored.read_bytes()
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        print(f"[backup] refusing to restore {entry['file']}: contents do not match the recorded sha256.")
        return 1

    if MANIFEST_PATH.exists():
        take_snapshot(destination, kind="pre-restore")
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    scratch = MANIFEST_PATH.with_suffix(".json.restore-tmp")
    scratch.write_bytes(data)
    os.replace(scratch, MANIFEST_PATH)

    meta = json.loads(data.decode("utf-8"))
    counts = summarise(meta)
    print(
        f"[restore] data/master_manifest.json <- {entry['file']} "
        f"(sha256 {entry['sha256'][:12]}, {counts['entries']} entries, "
        f"{counts['memories']} memories / {counts['conversations']} conversations)"
    )
    print("[restore] next: python tools/verify_portfolio.py   (Gate 1 re-checks coverage against the live databases)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot or restore the private master manifest, off-repo.")
    parser.add_argument("--dest", help="backup directory (default: a OneDrive folder outside the repo)")
    parser.add_argument("--list", action="store_true", help="show stored snapshots")
    parser.add_argument("--verify", action="store_true", help="compare the newest snapshot with the live manifest")
    parser.add_argument("--restore", metavar="LATEST|FILE", help="restore a snapshot into data/master_manifest.json")
    args = parser.parse_args()

    destination = resolve_destination(args.dest)

    if args.list:
        return show_list(destination)
    if args.verify:
        return verify(destination)
    if args.restore:
        return restore(destination, args.restore)
    take_snapshot(destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
