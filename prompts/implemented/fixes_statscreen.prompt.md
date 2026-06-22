# Fix: Auto-Reset Stats Page on Movement

**Status:** ✅ Implemented  
**Priority:** Medium  
**Files Affected:** `src/main.py`

---

## Problem Description

When a player views a loot bag or chest inventory (setting `state.current_stats_page` to `"loot"` or `"chest"`), the stats panel remains stuck on that view even after the player moves away. This creates several issues:

1. **UI Confusion:** Player sees "Loot Bag" or "Chest" inventory but doesn't realize they've moved away
2. **Real-Time Mode Issues:** In real-time mode, the player may not notice they're still viewing a stale inventory page while moving
3. **Stale Data:** The displayed inventory no longer corresponds to the player's current location

### Current Behavior

- `state.show_loot()` sets `current_stats_page = "loot"`
- `state.show_chest()` sets `current_stats_page = "chest"`
- Player moves via `_handle_directional_move()` or `_handle_targeted_move()`
- **Stats page remains on "loot" or "chest"** (BUG)

### Expected Behavior

When the player moves, the stats page should automatically reset to `"player"` to show the player's own stats.

---

## Implementation Plan

### Solution 1: Reset in Movement Handler (Recommended)

**Location:** `src/main.py` in `_handle_directional_move()` and `_handle_targeted_move()`

After a successful move, add:
```python
# Reset stats page to player view when moving
if self.state.current_stats_page in ["loot", "chest"]:
    self.state.current_stats_page = "player"
```

**Where to add:**
- In `_handle_directional_move()`: Right after `if self.state.player_move(dx, dy):` (line ~283)
- In `_handle_targeted_move()`: Inside the movement loop after successful `player_move()` (line ~315)

### Solution 2: Reset in GameState.player_move() (Alternative)

**Location:** `src/game_state.py` in `player_move()` method

Add the reset logic directly in the core movement function (around line 296):
```python
def player_move(self, dx, dy):
    """Move the player on the map."""
    ui = getattr(self, 'ui', None)
    result = self.map.move_player(self.player, dx, dy, ui)
    
    # Reset stats page when moving away from loot/chests
    if result and self.current_stats_page in ["loot", "chest"]:
        self.current_stats_page = "player"
    
    return result
```

**Pros:** Centralized - handles all movement types automatically  
**Cons:** Mixes movement logic with UI state

---

## Additional Enhancements (Optional)

### 1. Visual Indicators

The loot/chest inventory pages already have headers in the UI. Could be made more prominent if needed.

### 2. Map Highlighting

Add visual highlighting to the map tile containing the viewed loot/chest (future enhancement).

---

## Testing Checklist

- [ ] View a loot bag, then move north/south/east/west - stats page resets to player
- [ ] Open a chest, then move away - stats page resets to player  
- [ ] In real-time mode, view loot/chest then move - stats page resets correctly
- [ ] Targeted move command (m x,y) while viewing loot - stats page resets
- [ ] Stats page remains on "enemy" when moving (should NOT reset - enemies can be adjacent)
- [ ] Stats page remains on "player_inventory" when moving (should NOT reset - inventory follows player)

---

## Recommendation

**Use Solution 1** (add reset in movement handlers in `main.py`). This keeps the UI state management in the main game loop where other stats page switches happen (like viewing enemy stats).

---

## Implementation Summary

**Date:** 2026-06-07  
**Solution Used:** Solution 1 (movement handlers in `main.py`)

Added stats page reset logic in all movement locations:

1. **`_handle_directional_move()`** (line ~281) - Turn-based directional movement
2. **`_handle_targeted_move()`** (line ~317) - Turn-based coordinate movement
3. **Real-time mode graphics movement** (line ~572) - Real-time WASD movement (graphics mode)
4. **Real-time mode text movement** (line ~641) - Real-time WASD movement (text mode)

All movement handlers now check if `current_stats_page` is `"loot"` or `"chest"` and automatically reset it to `"player"` after a successful move. This ensures players always see their own stats when moving away from loot bags or chests.