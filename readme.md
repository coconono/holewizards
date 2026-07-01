# Hole Wizards

ASCII dungeon crawler RPG in Python.

Current build status: playable in graphics mode with turn-based and real-time gameplay.

## Introduction

hi yes hello. coconono the developer here. I'm learning how to do cool stuff with python and github copilot. If you see something that looks sloppy point it out. The goal here is to create a framework people can use to make their own RPG game.

There is a functioning game. It is not very good. There are still bugs. There's not a lot to do. Its sorta pretty. I'll get to all of that. I want to re-assure people that all the writing is human first(please let me use spelling and grammar checks). Same with the art. I can do real artists doing art real easy peasy.

Yes there is a manifesto but for the life of me I cannot find my beret.

## Current Feature Set

- Graphics mode (pygame window, 1400x900 layout) with ANSI-colored logs
- Real-time mode toggle (`realtime`) with WASD controls
- Turn-based command mode with command parsing and shortcuts
- Context-aware tab completion
- Procedural dungeon map with fog-of-war exploration
- Combat system: attack, suplex reposition, defend
- Enemy AI actions each turn/frame, including enemy-vs-enemy combat
- Reinforcement-weighted enemy action selection
- Inventory, equipment, consumables, and spell usage
- Loot bags from defeated enemies and chest interaction
- Stackable consumables (HP and mana potions)
- End screens for victory/defeat with combat statistics
- Config-driven data loading from `data/*.cfg`

## Quick Start

### Requirements

- Python 3.8+
- `pygame` for graphics mode

### Install

```bash
cd holewizards
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
# recommended helper script
./run_game.sh

# or run directly
python3 src/main.py
```

## Gameplay

### Objective

Survive, defeat enemy wizards, gather loot, and reach the exit tile.

### Turn-Based Commands

#### Movement

| Command | Shortcut | Action |
| --- | --- | --- |
| `move up` | `mu` | Move north |
| `move down` | `md` | Move south |
| `move left` | `ml` | Move west |
| `move right` | `mr` | Move east |
| `move x,y` | `mX,Y` | Auto-step to coordinates |

#### Combat

| Command | Shortcut | Action |
| --- | --- | --- |
| `attack [name]` | `a[name]` | Attack adjacent named enemy |
| `suplex [name]` | `s [name]` | Grapple + throw enemy if space is available |
| `defend` | - | Enter defensive stance |

#### Inventory and Interaction

| Command | Action |
| --- | --- |
| `take [item]` | Pick up item from ground/chest/loot view |
| `drop [item]` | Drop item from inventory |
| `equip [item]` | Equip weapon/armor/spell |
| `use [item]` | Consume potion or cast usable spell |

#### Info and Utility

| Command | Action |
| --- | --- |
| `show player stats` | View player stats |
| `show enemy stats` | View nearby enemy stats |
| `show player inventory` | View inventory page |
| `show loot` | Open nearby loot bag contents |
| `show [enemy] loot` | Open specific nearby loot bag |
| `show chest` | Open nearby chest contents |
| `legend` | Display map legend |
| `list commands` or `help` | Show command help |
| `realtime` | Toggle real-time mode |
| `restart` | Start a new run |
| `quit` | Exit game |

### Real-Time Controls

When real-time mode is active:

- `W A S D` move
- `Shift` suplex nearest adjacent target
- `Z` defend
- `Space` interact (opens chest and returns to turn-based mode)
- `R` return to turn-based mode

### Map Symbols

```text
p = player
m = enemy
█ = wall
╬ = closed door
─ = open door
C = chest
E = entrance
X = exit
◆ = loot bag
▪ = consumable on ground
? = unexplored tile
```

## UI Layout

Graphics mode uses a four-panel layout:

- Top-left: map
- Top-right: stats/inventory/chest/loot pages
- Bottom-left: event log
- Bottom-right: command input

Text mode renders the same information in terminal format.

## Known Limitations (Current Build)

- Save/load is not implemented yet.
- Some systems are intentionally simple (early-development balancing).
- Graphics behavior depends on local pygame/font setup.

## Animation Studio Utility

Hole Wizards includes a standalone sprite composition and timeline tool:

- Location: `utilities/animation_studio.py`
- Purpose: Build layered frames from PNG assets, collect frames into libraries, and play/save timelines

### Run Animation Studio

```bash
python3 utilities/animation_studio.py
```

Optional paths:

```bash
python3 utilities/animation_studio.py --assets-dir data/png --output-dir utilities/animation_studio_output
```

### Auto-Discovery

- On startup, the tool scans the output directory for existing `.library` files.
- If one or more libraries are found, it auto-loads the first discovered library (alphabetical order).

### Studio Save Formats

- `.frame` for a single frame
- `.library` for frame libraries
- `.timeline` for playback timelines

### Core Studio Controls

- Left panel: click an asset to select it
- Asset count is shown in the top bar and asset panel header
- Canvas: click to place layer, click/drag to move selected layer
- Transform: arrows move, `Shift+arrows` move faster, `H`/`V` flip, `PageUp`/`PageDown` reorder
- Layer ops: `Delete` remove, `I` visibility toggle, `O`/`P` opacity down/up
- Timeline: `A` add current frame as clip, `Space` play/pause, `Shift+Space` toggle loop
- Timeline selection: click timeline rows to switch displayed frame
- Timeline scrolling: mouse wheel scrolls clip list (scrollbar shown when needed)
- Save/load: `Ctrl+S` save frame + timeline, `Ctrl+L` save library, `Ctrl+T` save timeline, `Ctrl+O` load by path
- Reload assets: `Ctrl+R` rescans `data/png` (or your `--assets-dir`) without restarting

## Project Structure

```text
holewizards/
├── src/
│   ├── main.py
│   ├── game_state.py
│   ├── map_system.py
│   ├── player.py
│   ├── enemy.py
│   ├── items.py
│   ├── commands.py
│   ├── tab_completion.py
│   ├── realtime_input.py
│   ├── graphics.py
│   └── ui.py
├── data/
│   ├── monsters.cfg
│   ├── weapons.cfg
│   ├── armor.cfg
│   ├── spells.cfg
│   ├── items.cfg
│   ├── settings.cfg
│   └── messages/
├── prompts/
├── utilities/
│   ├── animation_studio.py
├── run_game.sh
└── readme.md
```

## Development Workflow

This project follows prompt-driven development:

- Design requirements are written in `.md` files first.
- Implementation follows those specs.
- Narrative/flavor content is human-authored.

See `AGENTS.md`, `manifesto.md`, and `prompts/implemented/prompt_initial.md` for project philosophy and mechanic specs.
