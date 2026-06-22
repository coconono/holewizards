# Real-Time Mode Design

**Purpose:** Implement an action-based real-time gameplay mode alongside the existing turn-based text interface.

**Status:** Ready for Implementation

---

## Overview

Real-time mode allows players to control their character using keyboard inputs (WASD movement) instead of typing commands. All entities (player, enemies) act simultaneously with time-based intervals. Players can toggle between real-time and turn-based modes at any time.

---

## Mechanics

### Mode Toggle

**Real-Time Mode ON:**
- Activated by typing `realtime` in the text interface
- Player uses keyboard controls (WASD + action keys)
- All entities act simultaneously based on internal timers
- Game loop runs continuously, polling for input

**Real-Time Mode OFF (Turn-Based):**
- Activated by pressing `R` key during real-time mode
- Returns to command prompt interface
- Turn-based mechanics resume
- Player types commands (e.g., `north`, `attack`, `take`)

**Implementation Details:**
- Add `realtime_mode` boolean to GameState
- Display mode indicator in UI (e.g., "[REALTIME]" or "[TURN-BASED]")
- Seamless state preservation when switching modes

---

### Game Loop System

**Real-Time Loop:**
- Continuously poll for keyboard input (non-blocking)
- Update all entity timers
- Process actions when timers expire
- Render UI after each update cycle
- Target: ~30-60 updates per second

**Implementation Details:**
- Use `curses` or `keyboard` library for input polling
- Implement action cooldowns (prevent spam)
- Track `last_action_time` per entity
- Ensure responsive input (sub-100ms latency)

---

### Player Controls (Real-Time Mode Only)

| Key | Action | Cooldown |
|-----|--------|----------|
| `W` | Move North | 0.2s |
| `A` | Move West | 0.2s |
| `S` | Move South | 0.2s |
| `D` | Move East | 0.2s |
| `Shift` | Suplex (adjacent enemy) | 1.0s |
| `Z` | Defend (reduce damage) | 0.5s |
| `Space` | Interact (chests, loot bags) | 0.3s |
| `R` | Toggle back to turn-based | Instant |

**Implementation Details:**
- Buffer inputs to prevent dropped commands
- Support simultaneous key presses (e.g., move + defend)
- Display cooldown timers in UI (optional)
- Visual feedback for successful actions (log message, highlight)

---

### Enemy Behavior

**Real-Time AI:**
- Enemies act every 0.5-1.5 seconds (varies by enemy type)
- Use existing pathfinding/decision logic
- Enemies target nearest hostile (player OR other enemies)
- Treat all non-allied entities as attack targets

**Implementation Details:**
- Each enemy has `action_timer` that counts down
- When timer reaches 0, execute action (move/attack/defend)
- Reset timer after action
- Enemies can attack each other (free-for-all combat)

---

## Object Interaction Changes

### Loot Bag Physics

**Rule:** Loot bags occupy floor tiles and can be pushed.

**Behavior:**
- When an entity moves onto a loot bag tile, the bag is pushed 1 tile in the movement direction
- If target tile is blocked (wall, chest, another entity), attempt to push to any adjacent open tile
- If no adjacent tiles are open, the loot bag is **destroyed** and contents are lost
- Loot bags cannot overlap with other objects

**Implementation Details:**
- Check for loot bags before processing movement
- Use `push_loot_bag(bag, direction)` function
- Log destruction events ("The loot bag spills and is lost!")

---

### Chest Interaction

**Rules:**
- Chests are **immovable** obstacles
- Entities cannot occupy or pass through chest tiles
- Treated as impassable terrain (like walls)

**Real-Time Interaction:**
- Press `Space` adjacent to a chest to interact
- **Automatically pauses real-time mode** (switches to turn-based)
- Opens chest inventory screen (existing text interface)
- Player uses text commands to loot items
- Type `realtime` again to resume real-time mode

**Implementation Details:**
- Check adjacent tiles for chests when `Space` is pressed
- Call `open_chest(chest)` → sets `realtime_mode = False`
- Display standard chest inventory UI
- Preserve game state during mode switch

---

## UI/Display

### Mode Indicator

```
[ REAL-TIME MODE ]  HP: 45/50  Mana: 20/30  
┌─────────────────────┐
│ #####p####     #### │  [Legend: p=Player m=Enemy c=Chest b=Bag]
│ ####m##### ... #### │
└─────────────────────┘

[Cooldowns: Move=READY  Suplex=1.2s  Defend=READY]

> (Press R to return to turn-based mode)
```

### Feedback Elements

- Action cooldowns displayed in UI
- Brief log messages for actions ("You suplex the goblin!")
- Visual highlight for interactive objects (optional)
- Damage numbers/status effects in log

---

## Data Structures

### GameState Additions

```python
class GameState:
    realtime_mode: bool = False
    last_update_time: float = 0.0
    action_cooldowns: dict[str, float] = {}  # {"move": 0.0, "suplex": 1.2, ...}
```

### Entity Additions

```python
class Entity:  # Base for Player/Enemy
    action_timer: float = 0.0
    action_interval: float = 0.5  # seconds between actions
```

---

## Edge Cases & Rules

### Mode Switching
- Switching modes does **not** end combat
- Enemy timers continue running (but don't execute until real-time resumes)
- Player can switch modes freely (no cooldown)

### Loot Bag Destruction
- Display warning: "The loot bag was crushed! Contents lost."
- Only happens if no adjacent tiles are open
- Rare in open dungeon areas, common in corridors

### Multi-Entity Collisions
- If player and enemy both move to same tile, player's move fails (enemy has priority in real-time)
- Implement collision detection before finalizing moves

### Chest Blocking
- Enemies will pathfind around chests (treat as walls)
- Player cannot suplex enemies into chests

### Combat in Real-Time
- Damage calculation uses existing combat system
- "Defend" action reduces incoming damage by 50% for 0.5s
- Suplex has cooldown to prevent spam

---

## Dependencies

- Input library: `curses` (cross-platform terminal control) or `keyboard` (Windows/Linux)
- Timer system: Use `time.time()` for tracking cooldowns
- Existing: Player, Enemy, Item, GameState classes
- Existing: Pathfinding, combat calculation functions

---

## Implementation Notes

- Start with WASD movement only, then add action keys
- Test cooldowns to ensure responsive but not overpowered gameplay
- Ensure clean mode transitions (no state corruption)
- Log all real-time actions to scrollback buffer (preserve history)
- Consider adding visual "action pending" indicator for player actions 
