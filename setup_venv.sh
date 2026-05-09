#!/bin/zsh
cd /Users/coconono/scripts/holewizards
/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pygame
echo "Virtual environment created and pygame installed"
