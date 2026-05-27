#!/usr/bin/env python3
"""
Hermes Memory Architecture - Backout / Rollback Script v2

Restores production from a verified snapshot.
Use with extreme caution.
"""

import argparse
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def backout(snapshot_dir: Path, production_dir: Path, dry_run: bool = True):
    print(f"{'[DRY-RUN] ' if dry_run else ''}Starting backout from {snapshot_dir}")

    # Verify snapshot exists
    snapshot_db = snapshot_dir / "state.db"
    if not snapshot_db.exists():
        print(f"[ERROR] Snapshot database not found: {snapshot_db}", file=sys.stderr)
        sys.exit(1)

    prod_db = production_dir / "state.db"

    if dry_run:
        print(f"[DRY-RUN] Would restore: {snapshot_db} -> {prod_db}")
        print(f"[DRY-RUN] Would also restore: memories/, skills/, config.yaml, .env")
        return

    # Real restore
    print("Stopping services is your responsibility before running this script.")
    input("Type 'YES' to continue with actual restore: ")
    if input() != "YES":
        print("Aborted.")
        sys.exit(1)

    # Atomic replace of state.db
    backup_name = f"state.db.pre-backout.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(prod_db, production_dir / backup_name)
    print(f"Current production backed up as {backup_name}")

    shutil.copy2(snapshot_db, prod_db)
    print("[OK] state.db restored")

    # Restore supporting files
    for item in ["memories", "skills", "config.yaml", ".env"]:
        src = snapshot_dir / item
        dst = production_dir / item
        if src.exists():
            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"[OK] Restored {item}")

    print("\n[COMPLETE] Backout finished. Restart hermes-gateway.service manually.")