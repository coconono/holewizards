#!/bin/bash
cd /Users/coconono/scripts/holewizards
source .venv/bin/activate
python3 main.py "$@" 2>&1
