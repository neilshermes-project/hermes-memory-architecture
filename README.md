# Hermes Memory Architecture Upgrade

A complete, production-safe system for upgrading Hermes Agent's memory from simple FTS5 to a hybrid FTS5 + vector embedding + relational pre-filtering architecture.

This repository contains the full design specification, all migration and population code, backout scripts, and the exact repeatable process so that any person or agent can replicate the upgrade.

---

## Goals

- Move from pure FTS5 full-text search to **hybrid search** (FTS5 + `sqlite-vec` cosine similarity)
- Add **relational pre-filtering** using structured fields (skill, category, timestamp, tags)
- Create clean central tables: `memory_store` and `skills_store`
- Enable high-quality semantic retrieval while keeping the safety and speed of keyword search
- Provide a **snapshot-first, fully reversible** upgrade path that survives future Hermes updates
- Allow clean rollback at any stage

---

## Core Principles (Non-Negotiable)

1. **Snapshot-first development** — All work happens inside an isolated snapshot. Production is never touched until validation is complete.
2. **Never run code directly against `/root/.hermes`** during development.
3. **Always maintain a verified backup + tested backout script** before any promotion.
4. **Quality over cheapest models** — Use capable models (DeepSeek Coder, Qwen2.5-Coder-32B/72B) even if slightly more expensive.
5. **Orchestrator stays Grok** — The main architect model remains Grok; execution is delegated.

---

## Repository Structure

```
hermes-memory-architecture/
├── README.md                          # This file (complete design + replication guide)
├── scripts/
│   ├── migrate_schema.py              # Creates hybrid schema inside snapshot
│   ├── populate_embeddings.py         # Generates embeddings for existing memories
│   ├── populate_real_data.py          # Imports real user data (optional)
│   ├── backout_v2.py                  # Full rollback script
│   └── backup_production.sh           # Safe production backup helper
├── docs/
│   ├── snapshot-discipline.md
│   └── promotion-checklist.md
└── skills/                            # Original skill definitions (reference)
    └── ...
```

---

## Prerequisites

- Hermes running on Linux
- Access to `/mnt/hermesdata/` (or large storage volume)
- Root/sudo access
- Python 3.10+
- The dedicated `neilshermes-project` GitHub identity (or your own)

---

## Step-by-Step Replication Process

### 1. Create an Isolated Snapshot

```bash
mkdir -p /mnt/hermesdata/snapshots
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_DIR="/mnt/hermesdata/snapshots/hermes-snapshot-$TIMESTAMP"
mkdir -p "$SNAPSHOT_DIR"

# Full WAL checkpoint + backup of state.db
python3 -c "
import sqlite3
source = '/root/.hermes/state.db'
dest = '$SNAPSHOT_DIR/state.db'
con = sqlite3.connect(source)
con.execute('PRAGMA wal_checkpoint(FULL)')
backup = sqlite3.connect(dest)
con.backup(backup)
backup.close()
con.close()
"

# Copy supporting data (never modify originals)
cp -r /root/.hermes/memories "$SNAPSHOT_DIR/"
cp -r /root/.hermes/skills "$SNAPSHOT_DIR/"
cp /root/.hermes/config.yaml "$SNAPSHOT_DIR/"
cp /root/.hermes/.env "$SNAPSHOT_DIR/"
```

### 2. Prepare Snapshot Environment

```bash
python3 -m venv "$SNAPSHOT_DIR/venv"
source "$SNAPSHOT_DIR/venv/bin/activate"
pip install sqlite-vec numpy sentence-transformers
```

### 3. Apply Schema Migration

Run inside the snapshot:

```bash
python scripts/migrate_schema.py --db "$SNAPSHOT_DIR/state.db"
```

This script:
- Creates `memory_store` and `skills_store` tables
- Adds `embedding` column (using `sqlite-vec`)
- Preserves all existing FTS5 tables for backward compatibility
- Adds relational columns (`skill`, `category`, `tags_json`, `created_at`)

### 4. Populate Embeddings

```bash
python scripts/populate_embeddings.py \
    --db "$SNAPSHOT_DIR/state.db" \
    --model "sentence-transformers/all-MiniLM-L6-v2"
```

This generates 384-dimensional embeddings for every memory row.

### 5. (Optional) Populate Real User Data

If you have exported real memories, run:

```bash
python scripts/populate_real_data.py --db "$SNAPSHOT_DIR/state.db" --source /path/to/export.json
```

### 6. Test Thoroughly

- Run full test suite inside the snapshot
- Validate hybrid search returns correct results
- Test the backout script

### 7. Production Promotion (When Ready)

See `docs/promotion-checklist.md` for the exact safe promotion sequence, including:

- Stopping `hermes-gateway.service`
- Final backup
- Atomic swap of `state.db`
- Restart + health check
- 7-day retention of the snapshot

---

## Backout / Rollback

A complete rollback script is provided:

```bash
python scripts/backout_v2.py --snapshot "$SNAPSHOT_DIR" --production /root/.hermes
```

This restores the original `state.db` and supporting files.

---

## Future Hermes Updates

When Hermes itself is upgraded in the future:

1. Create a **new** snapshot from the latest production backup
2. Copy the `scripts/` and `docs/` folders from this repo into the new snapshot
3. Re-run `migrate_schema.py` + `populate_embeddings.py`
4. Re-validate
5. Promote only after full validation

This design survives Hermes core updates.

---

## Important Safety Rules

- Never develop against the live `/root/.hermes/state.db`
- Always stop the gateway service before schema changes on production
- Keep the most recent snapshot for at least 7 days after promotion
- Maintain at least one known-good backup before every promotion step
- Use the dedicated GitHub identity for any autonomous commits

---

## License

MIT

---

## Credits

Designed and validated in May 2026 as part of the Hermes memory architecture upgrade project.