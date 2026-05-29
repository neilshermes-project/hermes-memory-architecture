---
name: hermes-memory-hybrid
description: "One-command hybrid memory upgrade for Hermes (FTS5 + sqlite-vec embeddings + relational pre-filtering). Snapshot-safe and fully reproducible."
category: hermes
version: 1.0
author: neilshermes-project
tags: [memory, embeddings, sqlite-vec, upgrade, snapshot]
---

# Hermes Memory Hybrid

This skill allows any Hermes agent to install and run a complete hybrid memory architecture upgrade with a single command.

## Installation

```bash
git clone https://github.com/neilshermes-project/hermes-memory-hybrid.git ~/.hermes/skills/hermes-memory-hybrid
```

Or use the built-in installer:

```bash
curl -sSL https://raw.githubusercontent.com/neilshermes-project/hermes-memory-hybrid/master/install.sh | bash
```

## Activation

After installation, agents can run:

```bash
python ~/.hermes/skills/hermes-memory-hybrid/replicate.py --auto-snapshot
```

## What it does

- Creates a fully isolated snapshot
- Installs all required dependencies
- Migrates to hybrid FTS5 + vector search
- Populates embeddings
- Provides full backout capability

## See Also

- [README.md](README.md)
- [QUICKSTART.md](QUICKSTART.md)
- [INTEGRATION.md](INTEGRATION.md)