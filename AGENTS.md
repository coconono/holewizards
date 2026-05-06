# Hole Wizards - Agent Guidelines

**Project:** Hole Wizards - An ASCII dungeon crawling RPG game in Python  
**Development Stage:** Early development  
**Key Approach:** Prompt-driven development using markdown design files

## Project Overview

Hole Wizards is a simple text-based dungeon crawling RPG where players navigate an ASCII dungeon, fight monsters, collect items, and escape. See [readme.md](readme.md) for features and [intro.msg](intro.msg) for the game narrative.

### Developer Philosophy

The developer uses AI for **code generation** (implementing game logic based on design specs) but intentionally avoids using AI for **creative content** (flavor text, monster descriptions, art direction). See [manifesto.md](manifesto.md) for the full rationale.

## Development Workflow

1. **Design Phase:** Requirements and mechanics are documented in `.md` files (e.g., `prompt_initial.md`)
2. **Implementation Phase:** AI builds Python code based on the design files
3. **Iteration:** Mistakes and learnings inform refinement of the design
4. **Content Phase:** Flavor text, descriptions, and art are human-created (not AI-generated)

## Key Files and Structure

| File/Folder | Purpose |
| --- | --- |
| `prompt_initial.md` | Core game design: UI layout, mechanics, commands, stats system |
| `readme.md` | Project overview and features |
| `manifesto.md` | Developer's philosophy on AI usage |
| `intro.msg` | Game intro text (human-written, do not auto-generate) |
| `data/` | Game data (will hold item definitions, monsters, spells—initially empty) |
| `utilities/` | Utility modules (initially empty) |

## Code Generation Guidelines

### DO

- Generate Python code implementing mechanics described in `prompt_initial.md`
- Follow the UI structure: map display (top-left), stats window (top-right), log + command interface (bottom)
- Implement command parsing and game state management
- Use clear class structures for Player, Enemy, Item, Inventory, GameState
- Ask clarifying questions if design specs are ambiguous

### DON'T

- Generate flavor text, monster names, item descriptions, or quest narratives
- Create art or visual assets
- Write the intro message or any narrative content
- Assume requirements beyond what's in the design files—ask instead

## Game Architecture Notes

### Core Components (from design)

1. **UI System:** Display map, stats window, log, command input
2. **Commands:** Parsing and execution of player commands (show stats, inventory, take/drop/equip items)
3. **Game State:** Player, enemy, inventory, chest state
4. **Stats System:** HP, Mana, XP, Level, Equipped items/spells
5. **Map System:** Track explored areas, show player (`p`), monsters (`m`), walls, doors, chests, bags

### Design References

- **UI Layout:** See "UI Design Notes" section in `prompt_initial.md`
- **Commands:** See "mechanics" → "commands" section in `prompt_initial.md`
- **Stats Pages:** Player, Enemy, Inventory, Chest Inventory pages defined in `prompt_initial.md`

## Python Environment

- **Language:** Python 3.x
- **Dependencies:** See `requirements.txt` (currently empty—add as needed)
- **No external frameworks required yet** (plain Python for initial implementation)

## Common Tasks

### Adding New Mechanics

1. Update `prompt_initial.md` with the new mechanic
2. Request code generation with reference to the specific section

### Bug Fixes

- Reference the exact command or feature behaving incorrectly
- Provide reproduction steps if available

### Refinement

- Update design specs in `.md` files when requirements change
- Use the updated specs for code regeneration

## What Agents Should Know

- This is a **learning project** where early mistakes help define the project structure
- The developer is very hands-on with design but trusts AI for implementation
- Focus on **correct implementation** of the design, not creative embellishment
- When in doubt, link to or quote the relevant design section rather than guessing
- Test commands and UI rendering match the specified layout in `prompt_initial.md`

## Next Steps After MVP

Once core gameplay is working:

1. Refine UI and QoL improvements
2. Build asset generators (weapons, armor, spells, monsters—randomized initially)
3. Prepare for graphical version (Steam release)
4. Create installer and portable distribution
