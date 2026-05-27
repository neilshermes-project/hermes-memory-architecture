#!/usr/bin/env python3
"""
Hermes Memory Architecture - Schema Migration Script

Creates the hybrid FTS5 + sqlite-vec schema inside an isolated snapshot.
Safe to run multiple times (idempotent).
"""

import sqlite3
import argparse
import sys


def migrate(db_path: str):
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys = ON;")

    # Enable sqlite-vec extension if available
    try:
        con.enable_load_extension(True)
        con.load_extension("sqlite_vec")
        print("[OK] sqlite-vec extension loaded")
    except Exception as e:
        print(f"[WARN] Could not load sqlite-vec: {e}")
        print("       Continuing with FTS5 only for now.")

    # Create central memory_store table
    con.execute("""
        CREATE TABLE IF NOT EXISTS memory_store (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            skill TEXT,
            category TEXT,
            tags_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            embedding BLOB,                    -- 384-dim float32 from sentence-transformers
            source_table TEXT,                 -- original FTS5 table name for traceability
            source_id INTEGER
        )
    """)

    # Create skills_store table
    con.execute("""
        CREATE TABLE IF NOT EXISTS skills_store (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            category TEXT,
            embedding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create virtual FTS5 table if not exists (kept for keyword search)
    con.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
            content,
            skill,
            category,
            content='memory_store',
            content_rowid='id'
        )
    """)

    con.commit()
    print(f"[OK] Schema migration completed on {db_path}")
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True, help="Path to snapshot state.db")
    args = parser.parse_args()

    try:
        migrate(args.db)
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}", file=sys.stderr)
        sys.exit(1)