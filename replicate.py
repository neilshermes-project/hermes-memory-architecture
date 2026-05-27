#!/usr/bin/env python3
"""
Hermes Memory Architecture - Master Replication Script

This is the single entry point for any agent or human to fully replicate
the Hermes hybrid memory architecture upgrade.

Usage (recommended):

    python replicate.py --auto-snapshot

It will:
1. Verify / install all dependencies
2. Create a timestamped snapshot
3. Run schema migration + embedding population
4. Provide next steps
"""
import argparse
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_PACKAGES = ["sentence-transformers", "numpy", "sqlite-vec"]

def check_python_version():
    if sys.version_info < (3, 9):
        print("[FAIL] Python 3.9+ required")
        sys.exit(1)
    print(f"[OK] Python {sys.version.split()[0]}")

def ensure_venv(snapshot_dir: Path) -> Path:
    venv_dir = snapshot_dir / "venv"
    if not venv_dir.exists():
        print(f"[INFO] Creating venv at {venv_dir}")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    return venv_dir

def install_requirements(venv_python: Path):
    print("[INFO] Installing dependencies...")
    subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
    for pkg in REQUIRED_PACKAGES:
        subprocess.check_call([str(venv_python), "-m", "pip", "install", pkg])
        print(f"  [OK] {pkg}")

def create_snapshot(base_dir: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot = base_dir / f"hermes-snapshot-{ts}"
    snapshot.mkdir(parents=True, exist_ok=True)
    return snapshot

def backup_state_db(source: Path, dest: Path):
    con = sqlite3.connect(str(source))
    con.execute("PRAGMA wal_checkpoint(FULL)")
    backup = sqlite3.connect(str(dest))
    con.backup(backup)
    backup.close()
    con.close()

def copy_supporting_files(source: Path, dest: Path):
    for item in ["memories", "skills", "config.yaml", ".env"]:
        src = source / item
        if src.exists():
            if src.is_dir():
                if (dest / item).exists():
                    shutil.rmtree(dest / item)
                shutil.copytree(src, dest / item)
            else:
                shutil.copy2(src, dest / item)

def run_script(venv_python: Path, script_name: str, db_path: Path):
    script = Path(__file__).parent / "scripts" / script_name
    cmd = [str(venv_python), str(script), "--db", str(db_path)]
    subprocess.check_call(cmd)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-snapshot", action="store_true")
    parser.add_argument("--snapshot-dir", type=Path)
    parser.add_argument("--production-dir", type=Path, default=Path("/root/.hermes"))
    args = parser.parse_args()

    print("=== Hermes Memory Architecture Replication ===\n")
    check_python_version()

    if args.auto_snapshot:
        base = Path("/mnt/hermesdata/snapshots")
        base.mkdir(parents=True, exist_ok=True)
        snapshot = create_snapshot(base)
    elif args.snapshot_dir:
        snapshot = args.snapshot_dir
    else:
        print("[ERROR] Use --auto-snapshot or --snapshot-dir")
        sys.exit(1)

    prod_db = args.production_dir / "state.db"
    snap_db = snapshot / "state.db"
    if not snap_db.exists():
        backup_state_db(prod_db, snap_db)
        copy_supporting_files(args.production_dir, snapshot)

    venv = ensure_venv(snapshot)
    venv_python = venv / "bin" / "python"
    install_requirements(venv_python)

    run_script(venv_python, "migrate_schema.py", snap_db)
    run_script(venv_python, "populate_embeddings.py", snap_db)

    print("\n=== Replication Complete ===")
    print(f"Snapshot ready at: {snapshot}")
    print("Next: source {}/venv/bin/activate".format(snapshot))

if __name__ == "__main__":
    main()