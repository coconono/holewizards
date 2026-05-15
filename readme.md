# Hole Wizards

A simple ASCII graphical dungeon crawling role-playing game written in Python. Navigate a procedural dungeon, defeat enemies, collect treasure, and escape the Hole!

## introduction

hi yes hello. coconono the developer here. I'm learning how to do cool stuff with python and github copilot. If you see something that looks sloppy point it out. The goal here is to create a framework people can use to make their own RPG game.

There is a functioning game. It is not very good. There are still bugs. There's not a lot to do. Its not pretty. I'll get to all of that. I want to re-assure people that all the writing is human first(please let me use spelling and grammar checks). Same with the art. I can do real artists doing art real easy peasy.

Yes there is a manifesto but for the life of me I cannot find my beret.

## Features

- **Graphics Mode** - 1400x900 pixel window with custom ASCII art font rendering
- **Text Mode** - Traditional terminal-based interface (`--text` flag)
- **Dynamic Map Display** - Shows explored areas, auto-aligns to screen edges
- **Stats System** - Track HP, Mana, XP, Level with multiple display pages
- **Combat System** - Attack and defend mechanics with randomized damage
- **Inventory Management** - Pick up, drop, and equip items
- **Victory/Defeat Screens** - Game-over messages with final stats
- **Procedural Generation** - Weapons, armor, spells, and monsters with random stats

## Quick Start

### Prerequisites

- Python 3.8+
- pygame 2.6.1

### Installation

```bash
# Clone or navigate to the repository
cd holewizards

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Game

#### **Option 1: Using the run_game.sh script (recommended)**

```bash
# Make the script executable (first time only)
chmod +x run_game.sh

# Run the game
./run_game.sh
```

The script automatically activates the virtual environment and launches the game in graphics mode.

#### **Option 2: Direct Python execution**

```bash
# Activate virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Graphics mode (default)
python3 main.py

# Text mode (terminal only)
python3 main.py --text
```

## Gameplay

### Objective

Escape the Hole! Defeat enemy wizards, collect their treasure, find the exit, and survive.

### Controls

#### Movement
| Command | Shortcut | Action |
| --- | --- | --- |
| `move up` | `mu` | Move up |
| `move down` | `md` | Move down |
| `move left` | `ml` | Move left |
| `move right` | `mr` | Move right |
| `move x,y` | `mx,y` | Move to coordinates (turn-based, step-by-step with pauses) |

#### Combat
| Command | Shortcut | Action |
| --- | --- | --- |
| `attack [name]` | `a[name]` | Attack named adjacent enemy (shows targets if no name given) |
| `defend` | - | Prepare to defend this turn |

#### Items
| Command | Shortcut | Action |
| --- | --- | --- |
| `take [item]` | - | Pick up item |
| `drop [item]` | - | Drop item from inventory |
| `equip [item]` | - | Equip weapon/armor/spell |
| `use [item]` | - | Use consumable item |

#### Stats & Info
| Command | Shortcut | Action |
| --- | --- | --- |
| `show player stats` | - | View player stats |
| `show enemy stats` | - | View current enemy stats |
| `show player inventory` | - | List your items |
| `show chest` | - | Show chest contents |
| `show loot` | - | Show loot from defeated enemy |
| `legend` | - | Show map symbols |
| `list commands` / `help` | - | Show all commands |

#### Game
| Command | Shortcut | Action |
| --- | --- | --- |
| `quit` | - | Exit game |
| `restart` | - | Start new game |

### Map Symbols

```text
p = Player
m = Monster
w = Wall
. = Floor
d = Door
c = Chest
e = Exit
? = Unexplored
```

### Game Mechanics

- **Stats Pages**: Cycle through Player, Enemy, Inventory, and Chest contents
- **Leveling**: Defeat enemies to gain XP; reach 10 XP to level up
- **Combat**: Both player and enemy have HP, Mana, and damage calculations
- **Items**: Weapons, armor, and spells with randomized attributes
- **Treasure**: Collect items from defeated enemies and chests

## UI Overview

### Graphics Mode (1400x900 window)

- **Top-Left (Green)**: MAP area - Shows explored dungeon layout
- **Top-Right (Yellow)**: STATS area - Player/Enemy information
- **Bottom-Left (Cyan)**: LOG area - Game messages and history
- **Bottom-Right (Orange)**: INPUT area - Command entry field

### Text Mode

- Traditional terminal interface
- All commands entered via keyboard
- Messages displayed in scrolling log

## Project Structure

```text
holewizards/
├── main.py              # Game controller and loop
├── game_state.py        # Game state and logic
├── graphics.py          # Pygame graphics rendering
├── map_system.py        # Dungeon map generation
├── player.py            # Player class and methods
├── enemy.py             # Enemy class and AI
├── items.py             # Item definitions
├── commands.py          # Command parser
├── ui.py                # Text UI (legacy)
├── data/
│   ├── messages/        # Victory/defeat screens
│   ├── weapons.cfg      # Weapon definitions
│   ├── armor.cfg        # Armor definitions
│   ├── spells.cfg       # Spell definitions
│   ├── monsters.cfg     # Monster templates
│   └── settings.cfg     # Game configuration
├── prompts/
│   ├── prompt_initial.md    # Core game design
│   ├── prompt_feature_rev1.md
│   └── PROMPT_TEMPLATE.md
├── utilities/           # Asset generators
└── readme.md            # This file
```

## Troubleshooting

### Graphics window doesn't appear

- Ensure pygame is installed: `pip install pygame`
- Check that your display supports graphics mode
- Try text mode: `python3 main.py --text`

### Text not displaying in graphics window

- This is normal! The custom bitmap font is rendering
- Commands work normally - type and press Enter
- Text will display once typed

### Commands not responding

- Make sure the window is focused (active)
- Commands must end with Enter key
- Check command syntax in `help` menu

### Game crashes on startup

- Verify Python 3.8+ is installed
- Reinstall dependencies: `pip install --upgrade -r requirements.txt`
- Check terminal for error messages

## Development Notes

This project uses **prompt-driven development**:

- All game mechanics are defined in `.md` design files first
- Code implements exactly what's specified in the prompts
- See [AGENTS.md](AGENTS.md) for developer philosophy

### Key Design Files

- [prompt_initial.md](prompts/prompt_initial.md) - Core game mechanics
- [AGENTS.md](AGENTS.md) - Development approach and guidelines
- [manifesto.md](manifesto.md) - Why prompt-driven development

## Future Enhancements

- [ ] Graphical tileset rendering
- [ ] Sound and music
- [ ] Advanced AI for enemies
- [ ] Procedural level variety
- [ ] Save/load game state
- [ ] Steam release preparation
- [ ] Mobile port

## License

If you want to do business, hit me up
If you want to use it to do something cool, hit me up

If you don't do these things I will think rude thoughts about you. Do you really want to find out if I'm a psychic weapon forgotten in the insanity of the Cold War or a guy with a keyboard?
