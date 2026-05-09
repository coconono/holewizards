#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"
source .venv/bin/activate

# Compile Python files if not already compiled
echo "Checking Python files..."
python3 -m py_compile src/main.py src/graphics.py main.py graphics.py 2>/dev/null

# Run the game
python3 src/main.py "$@" 2>&1
