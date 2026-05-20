# Tab Completion Feature

**Feature:** Command and context-aware tab completion for player command entry  
**Status:** Design (ready for implementation)  
**Referenced By:** Player command input system in UI

---

## Overview

When the player is typing a command at the prompt, pressing TAB will:
1. Complete partial command names to their full form
2. Complete item names based on context (inventory, loot, etc.)
3. Cycle through matching options if multiple completions exist
4. Provide visual feedback showing available completions

---

## Behavior

### Tab Completion Rules

#### Rule 1: Command Completion
- If the player types a partial command (e.g., `sh`), TAB will complete it to the first matching command
- Matching is case-insensitive and prefix-based
- If multiple commands match, cycling through TAB shows each option in sequence
- Example: `sh` → `show player stats` (first match) → `show enemy stats` (next match) → `show player inventory` (next match)

#### Rule 2: Item/Argument Completion
- After typing a complete command that takes an argument (e.g., `take`, `drop`, `equip`, `use`), TAB completes item names
- Item completions are context-aware:
  - **`take [item]`**: Complete from items in current loot/bag on ground
  - **`drop [item]`**: Complete from items in player inventory
  - **`equip [item]`**: Complete from items in player inventory that are equippable
  - **`use [item]`**: Complete from items in player inventory that are usable
  - **`attack [target]`**: Complete from enemy names in game (if exists)
- Matching is case-insensitive and prefix-based
- If multiple items match, cycling through TAB shows each option

#### Rule 3: Movement Completion
- Movement commands have shorthand forms:
  - `move up` → `mu`
  - `move down` → `md`
  - `move left` → `ml`
  - `move right` → `mr`
  - `move X,Y` → `mX,Y` (e.g., `m5,3`)
- TAB may offer both full and shorthand forms when completing movement commands

#### Rule 4: No Completion for Coordinates
- The `move X,Y` command takes numeric coordinates; TAB does not attempt completion for these

---

## Command Groups for Completion

### Always Available (All Contexts)

```
show player stats
show enemy stats
show player inventory
show loot
show chest
list commands
help
legend
quit
restart
move up / mu
move down / md
move left / ml
move right / mr
defend
```

### Context-Dependent (If Applicable)

```
take [item from ground]
drop [item from inventory]
equip [equippable item from inventory]
use [usable item from inventory]
attack [target name]
```

---

## Implementation Details

### Data Sources for Completion

1. **Command List**: Static list from `CommandParser.COMMANDS` keys
2. **Inventory Items**: From `player.inventory` (list of Item objects)
3. **Loot/Bags on Ground**: From `game_state.ground_items` at current position
4. **Enemy Info**: From `game_state.current_enemy` (if exists)
5. **Chest Contents**: From targeted chest in `game_state` (if exists)

### Integration Points

- **Input Handler**: The command input prompt (bottom of UI) should hook TAB key
- **Completion Engine**: New module `TabCompletion` that takes partial input and game state, returns matching options
- **Cycling Logic**: Track current completion index to cycle through matches on repeated TAB presses
- **Reset Logic**: Clear cycling index when the user types any non-TAB key

### Input State Management

- **Current Input**: The text the player has typed so far
- **Completion Index**: Which match to show (0 = first, 1 = second, etc.; resets on new TAB session)
- **Match Cache**: Store the list of matches to avoid recalculating on every TAB press within a session
- **Cursor Position**: Track where the player is typing to enable mid-line completion (optional enhancement)

---

## User Experience

### Example Session 1: Command Completion

```
> sh[TAB]
> show player stats[TAB]
> show enemy stats[TAB]
> show player inventory
```

### Example Session 2: Item Completion

```
> take [TAB]
> take iron sword[TAB]
> take iron axe
```

### Example Session 3: Drop with Inventory Item

```
> drop [TAB]
> drop healing potion[TAB]
> drop iron sword
```

---

## Edge Cases

1. **No Matches**: If TAB is pressed and no completions exist, the input remains unchanged and no visual feedback is given (or a brief message like "No matches").
2. **Single Match**: If only one match exists, complete it immediately.
3. **Exact Match**: If the user has typed an exact command or item name, TAB may show the next available option or do nothing (TBD by developer).
4. **Case Sensitivity**: Completion matching is case-insensitive, but the displayed/completed text should use the canonical case (e.g., "Show Player Stats" or "show player stats" as defined in the game).
5. **Quoted Items**: Items with spaces may be typed with quotes (e.g., `take "iron sword"`); completion should handle both quoted and unquoted forms.

---

## Testing Checklist

- [ ] TAB completes partial command names
- [ ] TAB cycles through multiple matching commands
- [ ] TAB completes item names from inventory for `drop`, `equip`, `use`
- [ ] TAB completes item names from ground for `take`
- [ ] TAB completes enemy/target names for `attack`
- [ ] Non-TAB key input resets completion cycle
- [ ] No completions available results in graceful handling
- [ ] Case-insensitive matching works correctly
- [ ] Quoted item names are handled correctly