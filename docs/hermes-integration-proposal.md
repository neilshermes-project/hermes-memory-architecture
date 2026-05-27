# Hermes Memory Architecture – Integration Proposal (Detailed)

**Goal**: Make the hybrid memory system a first-class, optional component of future Hermes releases.

## Current State (v1.0)

- Fully working replication via `replicate.py --auto-snapshot`
- Schema migration, embedding, and rollback scripts included
- Zero personal data – completely portable

## Benefits of Upstream Integration

1. Users can run `hermes memory upgrade` instead of manual steps
2. Embedding model can be declared as an optional dependency
3. Future Hermes releases can ship with the improved schema by default
4. Community improvements are centralized

## Technical Integration Outline

### 1. Configuration

```yaml
memory:
  hybrid_search: true          # enables sqlite-vec + embeddings
  embedding_model: all-MiniLM-L6-v2
```

### 2. New Tables (added only when enabled)

- `memory_store`
- `skills_store`
- `memory_fts` (virtual)

### 3. CLI Commands (proposed)

- `hermes memory snapshot create`
- `hermes memory upgrade`
- `hermes memory backout`

### 4. Dependency Management

Make `sentence-transformers` and `sqlite-vec` optional (lazy import).

## Risks & Mitigations

- Model download size → Document clearly, make optional
- Performance on low-end hardware → Keep FTS5 path always available

## Roadmap Suggestion

- v1.1: Add `hermes memory` subcommands (reference this repo)
- v1.2: Include schema + scripts in core distribution (optional)
- v2.0: Consider making hybrid search the default for new installs

This work reduces long-term maintenance cost for the Hermes project while giving users a high-quality, safe upgrade path today.