# Hole Wizards - Setup & Running

## Installation

### Option 1: Using Virtual Environment (Recommended)

```bash
cd holewizards
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Option 2: System Python with Text Mode

If you don't want to use a virtual environment, you can run text mode without any dependencies:

```bash
python3 main.py --text
```

## Running the Game

### Automatic Mode (Recommended)

The game will automatically detect available dependencies and choose the best UI:

```bash
source .venv/bin/activate  # If using venv
python3 main.py
```

- If pygame is installed and fonts work, runs graphical mode
- If pygame.font fails (known issue), automatically falls back to text mode
- If pygame is not installed, runs text mode

### Text Mode (Always Available)

Force text-only mode:

```bash
python3 main.py --text
```

## Known Issues

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
