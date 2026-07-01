# Hole Wizards - Setup & Running

## Installation

### Requirements

Hole Wizards requires **pygame** for graphics rendering.

```bash
cd holewizards
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Game

### Start the Game

```bash
source .venv/bin/activate  # If using venv
python3 src/main.py
```

Or use the helper script:

```bash
./run_game.sh
```

## Troubleshooting

### pygame not installed

Hole Wizards requires pygame. Install it with:

```bash
pip install pygame
```

### pygame.font Circular Import

On some systems (particularly macOS with homebrew Python 3.14), pygame.font may fail with a circular import error. This is a pygame environment issue, not a bug in Hole Wizards.

**Workaround**: The game automatically detects this and falls back to text mode, which is fully functional and just as playable.

**If you want graphical mode**: This requires a working pygame.font installation, which may need:

- Different Python version
- Different system configuration
- System-level dependencies for SDL2

## System Requirements

- **Text Mode**: Python 3.6+
- **Graphical Mode**: Python 3.6+, pygame 2.0+, SDL2

## Running from Script

Quick setup and run:

```bash
cd holewizards
bash run_game.sh
```

This script handles virtual environment setup and runs the game.
