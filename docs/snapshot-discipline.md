# Snapshot Discipline

## Core Rule
All significant memory / knowledge base work must be done in an isolated snapshot.

## Why
- Protects production from experimental schema changes, embedding population, and index work.
- Allows clean rollback if something goes wrong.
- Enables repeatable application after future Hermes upgrades.

## Snapshot Structure
- Location: `/mnt/hermesdata/snapshots/hermes-snapshot-YYYYMMDD_HHMMSS/`
- Must contain its own `state.db`, `memories/`, `skills/`, venv, and scripts.
- Production paths must never be referenced from inside the snapshot.

## Lifecycle
1. Create snapshot from fresh production backup.
2. Work exclusively inside it.
3. Test thoroughly (including backout).
4. Delete only after promotion or when no longer needed.