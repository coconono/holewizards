# improving the game logging pane

The game logging panel helps the player understand the game's events (e.g., where monsters are). To enhance its functionality, we will implement the following features:

## Current Implementation Overview

**Logging System Location:**
- Text UI: `src/ui.py` - `add_log_message()`, `render_log()` methods
- Graphics UI: `src/graphics.py` - `add_log_message()`, `render_log_display()` methods

**Current State:**
- Messages stored as plain strings in `self.log_messages` list (FIFO queue, max 10 lines)
- No categorization, metadata, or color coding
- Text mode: plain print statements, no ANSI codes
- Graphics mode: all messages rendered in LIGHT_GRAY (200, 200, 200)
- No combat statistics tracking in GameState

**Message Types Currently Generated:**
- Movement: "Moved up", "Cannot move down - blocked", "You spot Goblin_0 nearby!"
- Combat: "Attacked Skeleton_1 for 5 damage!", "Goblin_0 attacks you for 3 damage!"
- Inventory: "Took Iron Sword", "Equipped Fireball as spell"
- System: "Showing player stats", "Unknown command"
- Loot: "Opened chest at (12, 15)", "Loot found"

## Step 1: Color styling for log messages

**Acceptance criteria:**
- Define a fixed color map for all log event types: player damage dealt=green, player damage taken=red, healing=blue, loot=yellow, status effects=magenta, system messages=gray
- Add unit tests verifying color assignment to message types
- Colors render correctly in the logging pane
- Provide complete mapping table for every log event category with default fallback color for unknown events

**Implementation:** Colorize the following event types: all combat actions, healing, status effects, item pickups, and boss/quest events. Style precedence: base line color by event type, then apply underlining to names without changing the base color. Leave all other messages in default color.

## Step 2: Underline formatting for entity names
**Acceptance criteria:**
- Player and enemy names are underlined in all log messages
- Formatting rules applied consistently across log entries
- Add tests for name detection and formatting

**Implementation:** Underline player and enemy names to make them stand out in the log.

## Step 3: Defeat screen with performance summary
**Acceptance criteria:**
- Defeat screen displays on player defeat
- Shows total damage dealt, monsters defeated, and other performance metrics
- Highlights the attack that killed the player
- Add tests for screen trigger and data display

**Implementation:** When the player is defeated, display a defeat screen with a summary of the player's performance (e.g., total damage dealt, monsters defeated), and highlight what attack killed the player.

## Step 4: Victory screen with performance summary
**Acceptance criteria:**
- Victory screen displays when player wins
- Shows total damage dealt, monsters defeated, and other performance metrics
- Highlights the final attack that defeated the last monster
- Add tests for screen trigger and data display

**Implementation:** When the player wins, display a victory screen with a summary of the player's performance (e.g., total damage dealt, monsters defeated), and highlight the final attack that defeated the last monster.

---

## Technical Implementation Details

### Integration Points

**Files to Modify:**

1. **`src/ui.py`** (Text Mode)
   - Modify `add_log_message(message)` → `add_log_message(message, event_type="default")`
   - Update `render_log()` to process ANSI escape codes
   - Add color constant definitions
   - Implement name underlining logic

2. **`src/graphics.py`** (Graphics Mode)
   - Modify `add_log_message(message)` → `add_log_message(message, event_type="default")`
   - Update `render_log_display()` to use different colors per event type
   - Update color palette to include event type colors
   - Implement name underlining (or use bold/italic as visual alternative)

3. **`src/game_state.py`** (Statistics Tracking)
   - Add `combat_stats` dictionary to GameState.__init__()
   - Track: total_damage_dealt, total_damage_taken, monsters_defeated, healing_used, items_collected, turns_elapsed
   - Update combat methods to increment statistics
   - Add defeat/victory screen display methods

4. **`src/main.py`** (Message Generation)
   - Update all log calls to include event_type parameter
   - Example: `ui.add_log_message("Attacked enemy for 5 damage", "combat_dealt")`

### Message Event Types

**Complete Event Type Mapping:**

```python
EVENT_TYPES = {
    'combat_dealt': 'green',      # Player deals damage
    'combat_taken': 'red',        # Player takes damage
    'healing': 'blue',            # HP/Mana restoration
    'loot': 'yellow',             # Item pickup, chest opening
    'status': 'magenta',          # Status effects, buffs/debuffs
    'system': 'gray',             # UI messages, commands
    'movement': 'cyan',           # Room transitions, movement
    'victory': 'bright_green',    # Victory/level up messages
    'defeat': 'bright_red',       # Defeat/death messages
    'default': 'white'            # Fallback for unspecified
}
```

### ANSI Color Codes (Text Mode)

**Color Constant Definitions:**
```python
# Add to ui.py
ANSI_COLORS = {
    'green': '\033[92m',          # Bright green
    'red': '\033[91m',            # Bright red
    'blue': '\033[94m',           # Bright blue
    'yellow': '\033[93m',         # Bright yellow
    'magenta': '\033[95m',        # Bright magenta
    'gray': '\033[90m',           # Dim gray
    'cyan': '\033[96m',           # Bright cyan
    'bright_green': '\033[1;92m', # Bold bright green
    'bright_red': '\033[1;91m',   # Bold bright red
    'white': '\033[97m',          # Bright white
    'reset': '\033[0m',           # Reset all formatting
    'underline': '\033[4m',       # Underline text
    'underline_off': '\033[24m'   # Remove underline
}
```

**Terminal Compatibility:**
- Modern terminals (macOS Terminal, iTerm2, Linux terminals): Full ANSI support
- Windows: PowerShell 5.1+ and Windows Terminal support ANSI; Command Prompt requires `colorama` library
- Fallback: If ANSI not supported, strip codes and render plain text

### RGB Colors (Graphics Mode)

**Color Tuple Definitions:**
```python
# Add to graphics.py color palette
LOG_COLORS = {
    'combat_dealt': (0, 255, 0),       # Green
    'combat_taken': (255, 0, 0),       # Red
    'healing': (100, 150, 255),        # Blue
    'loot': (255, 255, 0),             # Yellow
    'status': (255, 0, 255),           # Magenta
    'system': (150, 150, 150),         # Gray
    'movement': (0, 255, 255),         # Cyan
    'victory': (150, 255, 150),        # Bright green
    'defeat': (255, 100, 100),         # Bright red
    'default': (200, 200, 200)         # Light gray (current)
}
```

### Entity Name Detection & Underlining

**Detection Strategy:**
1. Extract player name from `game_state.player.name`
2. Extract enemy names from `game_state.enemies` list (e.g., "Goblin_0", "Skeleton_1")
3. Search message string for exact name matches
4. Apply underline formatting around matched names

**Text Mode Implementation:**
```python
def format_entity_names(message, player_name, enemy_names):
    """Apply underline formatting to player and enemy names."""
    # Underline player name
    if player_name in message:
        message = message.replace(
            player_name,
            f"{ANSI_COLORS['underline']}{player_name}{ANSI_COLORS['underline_off']}"
        )
    
    # Underline enemy names
    for enemy_name in enemy_names:
        if enemy_name in message:
            message = message.replace(
                enemy_name,
                f"{ANSI_COLORS['underline']}{enemy_name}{ANSI_COLORS['underline_off']}"
            )
    
    return message
```

**Graphics Mode Implementation:**
- Option 1: Use bold font weight for entity names
- Option 2: Use different font style (italic)
- Option 3: Render with slight background highlight
- Recommendation: Bold text (most readable in pygame)

### Statistics Tracking

**GameState Class Modifications:**

```python
class GameState:
    def __init__(self, ...):
        # ... existing init code ...
        
        # Add combat statistics tracking
        self.combat_stats = {
            'total_damage_dealt': 0,
            'total_damage_taken': 0,
            'monsters_defeated': 0,
            'healing_used': 0,
            'items_collected': 0,
            'turns_elapsed': 0,
            'attacks_made': 0,
            'attacks_received': 0,
            'chests_opened': 0,
            'spells_cast': 0,
            'last_attack_dealt': None,  # {"attacker": name, "target": name, "damage": X}
            'last_attack_taken': None,  # {"attacker": name, "target": name, "damage": X}
            'killing_blow': None        # Same format as last_attack
        }
```

**Stat Tracking Points:**
- Increment `total_damage_dealt` when player attacks (game_state.py attack logic)
- Increment `total_damage_taken` when player takes damage (game_state.py enemy attack logic)
- Increment `monsters_defeated` when enemy.alive becomes False
- Increment `healing_used` when player uses HP potion or healing spell
- Increment `items_collected` in take_item() method
- Increment `turns_elapsed` in main game loop
- Store `killing_blow` when player HP reaches 0 (for defeat screen)
- Store `last_attack_dealt` when enemy dies (for victory screen)

### Defeat/Victory Screen Display

**Defeat Screen Format:**
```
================================
       GAME OVER - DEFEATED
================================

You were slain by Goblin_0 with a 12 damage attack!

Performance Summary:
--------------------
Damage Dealt:      125
Damage Taken:      85
Monsters Defeated: 3
Healing Used:      45 HP
Items Collected:   12
Turns Survived:    87

[Press Enter to exit]
```

**Victory Screen Format:**
```
================================
        VICTORY - ESCAPED!
================================

You defeated Orc_2 with a devastating 18 damage blow!

Performance Summary:
--------------------
Damage Dealt:      342
Damage Taken:      156
Monsters Defeated: 8
Healing Used:      78 HP
Items Collected:   24
Total Turns:       213

[Press Enter to exit]
```

**Implementation:**
- Create `display_defeat_screen(ui, combat_stats)` function
- Create `display_victory_screen(ui, combat_stats)` function
- Call from main game loop when `game_state.game_over` or `game_state.victory` is True
- Wait for Enter key before exiting

### API Changes Summary

**Before (Current):**
```python
ui.add_log_message("Attacked enemy for 5 damage")
```

**After (New):**
```python
ui.add_log_message("Attacked enemy for 5 damage", event_type="combat_dealt")
```

**Backward Compatibility:**
- Default `event_type="default"` ensures old code still works
- All existing calls render in default white/light gray
- New calls with event_type get color coding

### Testing Requirements

**Unit Tests to Add:**

1. **Color Assignment Tests:**
   - Verify each event_type maps to correct color
   - Test fallback to default for unknown event types
   - Validate ANSI code generation (text mode)
   - Validate RGB tuple selection (graphics mode)

2. **Name Formatting Tests:**
   - Test player name detection and underlining
   - Test enemy name detection and underlining
   - Test multiple names in same message
   - Test names that partially overlap (e.g., "Bob" vs "Bobby")

3. **Statistics Tracking Tests:**
   - Verify damage counters increment correctly
   - Test monster defeat counter
   - Test healing tracking
   - Verify last_attack capture

4. **Screen Display Tests:**
   - Test defeat screen displays on player death
   - Test victory screen displays on escape
   - Verify stats displayed correctly
   - Test killing blow highlight rendering

### Implementation Order

**Recommended Progression:**

1. **Phase 1: Color System Foundation**
   - Add EVENT_TYPES mapping
   - Add ANSI_COLORS constants (ui.py)
   - Add LOG_COLORS constants (graphics.py)
   - Modify add_log_message() signature to accept event_type
   - Update render methods to apply colors (no entity formatting yet)

2. **Phase 2: Message Categorization**
   - Update all add_log_message() calls in game_state.py to include event_type
   - Update all add_log_message() calls in main.py to include event_type
   - Test color rendering in both text and graphics modes

3. **Phase 3: Entity Name Formatting**
   - Implement name detection logic
   - Add underline/bold formatting
   - Test in both UI modes

4. **Phase 4: Statistics Tracking**
   - Add combat_stats to GameState
   - Implement stat tracking in combat methods
   - Test stat accumulation

5. **Phase 5: End Game Screens**
   - Create defeat screen display function
   - Create victory screen display function
   - Integrate with game loop
   - Test screen triggers and display