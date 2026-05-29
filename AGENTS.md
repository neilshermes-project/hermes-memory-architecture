# AGENTS.md

This file exists to help AI agents and autonomous systems understand this repository quickly.

## Project Purpose

This repository provides a complete, snapshot-safe, one-command upgrade that adds hybrid memory (FTS5 + sqlite-vec embeddings + relational pre-filtering) to Hermes Agent.

## Primary Entry Point for Agents

Run this single command to perform the full upgrade in an isolated snapshot:

```bash
python replicate.py --auto-snapshot
```

## Key Files Agents Should Know About

| File                  | Purpose                                      |
|-----------------------|----------------------------------------------|
| `replicate.py`        | Master replication + snapshot orchestrator   |
| `SKILL.md`            | Hermes skill metadata (frontmatter required) |
| `README.md`           | Human + agent installation instructions      |
| `install.sh`          | One-line curl installer                      |
| `docs/snapshot-discipline.md` | Core safety rules for working in snapshots |

## Important Constraints

- All development and testing **must** happen inside an isolated snapshot
- Never run migration or embedding scripts directly against a live `/root/.hermes`
- Always maintain a verified backup + tested backout script before any promotion
- This upgrade is designed to be fully reversible

## Recommended Agent Workflow

1. Clone or install as skill
2. Run `replicate.py --auto-snapshot`
3. Validate using the test suite inside the snapshot
4. Only promote to production after full validation

## Contact / Maintainers

Maintained via this repository. Issues and pull requests welcome.