# Integration Proposal: Hermes Memory Architecture

**Status**: Draft  
**Target**: Future Hermes Agent releases  
**Created**: May 2026

## Summary

This repository provides a complete, snapshot-safe hybrid memory system (FTS5 + sqlite-vec embeddings + relational pre-filtering) that can be optionally integrated into Hermes Agent.

## Why Integrate?

- Dramatically improves retrieval quality while preserving keyword search
- Enables semantic search across memories and skills
- Designed from day one to be safe and reversible
- Reduces future memory upgrade effort for both users and developers

## Proposed Integration Points

1. **Optional feature flag** in `config.yaml`
2. **Core tables** (`memory_store`, `skills_store`) moved into Hermes core
3. **Embedding service** (optional, behind feature flag)
4. **Promotion scripts** included or referenced in Hermes CLI

## Backward Compatibility

- Existing FTS5 tables remain untouched
- Old searches continue to work
- Upgrade is fully reversible via `backout_v2.py`

## Recommended Approach

1. Add this repo as a git submodule or reference in Hermes
2. Expose `hermes memory upgrade` command that uses `replicate.py`
3. Include embedding model as an optional dependency

## Benefits to Core Hermes

- Reduces maintenance burden for memory upgrades
- Provides a tested, documented upgrade path
- Allows the community to contribute improvements in one place

## Next Steps

- [ ] Hermes maintainers review this proposal
- [ ] Decide on optional vs default behavior
- [ ] Align release timeline with Hermes roadmap

## Contact / Maintainers

Maintained by the Hermes community via this repository.