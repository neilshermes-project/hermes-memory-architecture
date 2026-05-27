#!/usr/bin/env python3
"""
Hermes Memory Architecture - Embedding Population Script

Generates sentence-transformer embeddings for all rows in memory_store.
Run after migrate_schema.py.
"""

import sqlite3
import argparse
import sys
from datetime import datetime

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError:
    print("ERROR: Please install: pip install sentence-transformers numpy", file=sys.stderr)
    sys.exit(1)


def populate(db_path: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    dim = model.get_sentence_embedding_dimension()
    print(f"Embedding dimension: {dim}")

    con = sqlite3.connect(db_path)
    rows = con.execute("SELECT id, content FROM memory_store WHERE embedding IS NULL").fetchall()
    print(f"Found {len(rows)} rows without embeddings")

    updated = 0
    for row_id, content in rows:
        if not content or len(content.strip()) == 0:
            continue
        emb = model.encode(content, normalize_embeddings=True)
        blob = emb.astype(np.float32).tobytes()
        con.execute("UPDATE memory_store SET embedding = ? WHERE id = ?", (blob, row_id))
        updated += 1
        if updated % 50 == 0:
            con.commit()
            print(f"  ... {updated} embeddings generated")

    con.commit()
    print(f"[OK] Populated {updated} embeddings")
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    args = parser.parse_args()
    populate(args.db, args.model)