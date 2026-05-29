# fix up issues with loot

loot bags should have a unique name, based on who dropped them. EG Alice's loot bag, Bob's loot bag, etc. This will allow the user to specifically target a loot bag for pickup

this will allow the user to specifically target a loot bag for pickup EG:

'show Alice loot' will show the loot bag that Alice dropped, and allowing the user to pick items out of them

loot bags shouldn't stack on top of each other, they should be spread out a little bit so you can see them and target them

---

## Implementation Plan

### 1. Loot Bag Data Structure Enhancement
**File:** `src/items.py`
- Add `owner_name` attribute to loot bag class/structure
- Store the name of the enemy who dropped the bag
- Update loot bag creation to accept and store owner name
- Update display name to show as "{Owner}'s loot bag"

### 2. Enemy Death and Loot Creation
**File:** `src/enemy.py`
- When enemy is defeated, pass enemy name to loot bag creation
- Ensure enemy name is available for display (check if enemies have readable names)

### 3. Map Position Management
**File:** `src/map_system.py`
- Implement loot bag spread logic to prevent stacking
- When placing a new loot bag at a position:
  - Check if position is occupied by another loot bag
  - If yes, find nearest adjacent free tile (cardinal or diagonal)
  - Place bag in first available adjacent position
  - Maximum search radius: 2-3 tiles to keep bags nearby
- Add method: `find_adjacent_free_tile(x, y, max_radius=2)`

### 4. Command Parsing Enhancement
**File:** `src/commands.py`
- Update `show` command to accept owner name as a filter
- Parse patterns like:
  - `show Alice loot` → filter to loot bags owned by "Alice"
  - `show loot` → show all loot bags (existing behavior)
- Update `take` command similarly to target specific bags:
  - `take sword from Alice` → take from Alice's bag
  - `take all from Alice` → take all from Alice's bag

### 5. Game State Management
**File:** `src/game_state.py`
- Store multiple loot bags with unique identifiers
- Track loot bags by position and owner name
- Update methods to filter by owner name when needed
- Ensure loot bag removal when empty

### 6. UI Display Updates
**File:** `src/ui.py`
- Update loot bag display to show owner names
- Update map legend if needed (loot bags still show as 'b' but with owner info in stats)
- Ensure stat window shows proper loot bag name when player is on bag tile

### 7. Tab Completion Support
**File:** `src/tab_completion.py`
- Add enemy names to completion suggestions for loot-related commands
- Suggest owner names when typing `show [TAB]` or `take ... from [TAB]`

---

## Testing Checklist
- [ ] Defeat multiple enemies in same area, verify bags have unique names
- [ ] Verify bags don't stack (spread to adjacent tiles)
- [ ] Test `show Alice loot` targeting specific bag
- [ ] Test `show loot` showing all bags
- [ ] Test `take item from Alice` targeting specific bag
- [ ] Test bag removal when emptied
- [ ] Verify map display shows multiple bags correctly
- [ ] Test tab completion suggests enemy names

---

## Edge Cases to Consider
1. What if all adjacent tiles are blocked? (walls, enemies, etc.)
   - Fall back to placing on same tile? Log warning?
2. What if two enemies have the same name?
   - Add numerical suffix: "Alice's loot bag (1)", "Alice's loot bag (2)"
3. Maximum number of loot bags in one area?
   - Consider despawning oldest bags if limit reached