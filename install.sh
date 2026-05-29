#!/bin/bash
# One-line installer for Hermes Memory Hybrid skill

set -e

SKILL_DIR="$HOME/.hermes/skills/hermes-memory-hybrid"

echo "==> Installing Hermes Memory Hybrid skill..."

if [ -d "$SKILL_DIR" ]; then
    echo "==> Updating existing installation..."
    cd "$SKILL_DIR"
    git pull --quiet
else
    echo "==> Cloning repository..."
    git clone --quiet https://github.com/neilshermes-project/hermes-memory-hybrid.git "$SKILL_DIR"
fi

echo "==> Installation complete."
echo ""
echo "You can now run:"
echo "  python $SKILL_DIR/replicate.py --auto-snapshot"
echo ""
echo "Or load as a skill with: skill_view(name='hermes-memory-hybrid')"