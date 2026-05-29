# Hermes Memory Hybrid

**One-command hybrid memory upgrade for Hermes Agent** — adds semantic search (sqlite-vec embeddings) alongside existing FTS5 keyword search with relational pre-filtering.

Any Hermes agent or human can fully replicate and apply this upgrade safely using:

```bash
python replicate.py --auto-snapshot
```

This repository is both a **standalone upgrade tool** and a **native Hermes skill**.

---

## What This Project Does

Hermes agents accumulate skills, memories, and context over time. The default FTS5 full-text search works well for small systems but degrades as the knowledge base grows — agents begin to lose the ability to surface relevant memories and skills when keyword matches are imperfect.

**Hermes Memory Hybrid** solves this by introducing a **hybrid search architecture**:

- **FTS5** — Fast keyword and phrase matching (unchanged behavior for exact queries)
- **sqlite-vec** — Semantic / embedding-based similarity search
- **Relational pre-filtering** — Structured filtering by skill name, category, tags, timestamps, etc.

The result is significantly better retrieval quality while remaining fully backward compatible and completely reversible.

---

## Key Features

- Snapshot-first, production-safe upgrade process
- Full backout capability at any stage
- One-command replication (`replicate.py --auto-snapshot`)
- Installable as a native Hermes skill
- Designed to survive future Hermes core updates

---

## Quick Start

```bash
# Clone and run the full upgrade in an isolated snapshot
python replicate.py --auto-snapshot
```

See [QUICKSTART.md](QUICKSTART.md) for the fastest path and [docs/snapshot-discipline.md](docs/snapshot-discipline.md) for the safety rules.

---

## Install as a Hermes Skill

This repository is designed to be installed directly into any Hermes agent:

```bash
# One-line install
curl -sSL https://raw.githubusercontent.com/neilshermes-project/hermes-memory-hybrid/master/install.sh | bash

# Or manual clone
git clone https://github.com/neilshermes-project/hermes-memory-hybrid.git ~/.hermes/skills/hermes-memory-hybrid
```

After installation, any Hermes agent can activate the upgrade with:

```bash
python ~/.hermes/skills/hermes-memory-hybrid/replicate.py --auto-snapshot
```

The included `SKILL.md` allows future Hermes skill discovery systems to recognize and load this automatically.

---

## Long-Term Value

As Hermes systems grow over months and years, pure keyword search becomes a liability. This hybrid architecture turns growth into an advantage:

- Semantic similarity finds related skills even when keywords don't match
- Performance scales with the size of the memory store
- Historical decisions and patterns remain discoverable
- Agents stay coherent and capable as their knowledge base expands

---

## Documentation

- [QUICKSTART.md](QUICKSTART.md) — 5-minute installation guide
- [INTEGRATION.md](INTEGRATION.md) — Proposal for core Hermes integration
- [CONTRIBUTING.md](CONTRIBUTING.md) — How to contribute
- [docs/](docs/) — Snapshot discipline, promotion checklist, and technical details

---

## License

MIT

---

*Built so that any future Hermes agent can reproduce and benefit from the May 2026 memory architecture upgrade.*