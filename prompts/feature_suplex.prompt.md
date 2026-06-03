# Suplex Command Design

**Purpose:** A grappling attack that moves the target to the opposite side of the attacker while dealing weapon-based damage.

**Status:** Ready for Implementation

---

## Overview

The suplex command allows both players and enemies to perform a grappling maneuver that:

1. Targets an adjacent enemy/player
2. Deals damage based on the attacker's equipped weapon
3. Repositions the target to the opposite side of the attacker
4. Can be used by both players and AI enemies

This adds a tactical positioning element to combat, allowing combatants to reposition enemies (or be repositioned themselves).

---

## Mechanics

### Command Syntax

**Player Command:**

```text
suplex <target_name>
```

**Aliases:**

- `suplex <target>` (full command)
- `s <target>` (short form)

**Examples:**

- `suplex Goblin`
- `s Orc`

### Range and Targeting

**Range Requirements:**

- Target must be adjacent (within 1 tile in any direction, including diagonals)
- Target must be alive
- Target must be visible to the attacker

**Valid Targets:**

- For player: any adjacent living enemy
- For enemies: the player (if adjacent)

### Damage Calculation

**Damage Formula:**

```text
base_damage = weapon_damage (from equipped weapon)
suplex_damage = base_damage + random(0, 2)  # Slight variance
```

**Weapon Source:**

- Player: uses `player.equipped_weapon.damage` if equipped, otherwise base damage of 1
- Enemy: uses `enemy.equipped_weapon.damage` if equipped, otherwise base damage of 1

**Special Cases:**

- If no weapon equipped: base damage = 1 (bare-handed suplex)
- Critical hits: not applicable to suplex (future enhancement)

### Repositioning Mechanics

**Position Calculation:**

The target is moved to the opposite side of the attacker:

```python
attacker_pos = (ax, ay)
target_pos = (tx, ty)

# Calculate direction vector from attacker to target
dx = tx - ax
dy = ty - ay

# New position is on the opposite side
new_x = ax - dx
new_y = ay - dy
```

**Example Scenarios:**

1. **Horizontal suplex:**

   ```text
   Before:    [Player] [Enemy] [ ]
   After:     [ ] [Player] [Enemy]
   ```

2. **Vertical suplex:**

   ```text
   Before:    [Enemy]
              [Player]
              [ ]
   
   After:     [ ]
              [Player]
              [Enemy]
   ```

3. **Diagonal suplex:**

   ```text
   Before:    [Enemy] [ ]     [ ]
              [ ] [Player]    [ ]
              [ ] [ ]         [ ]
   
   After:     [ ] [ ]         [ ]
              [ ] [Player]    [ ]
              [ ] [ ]         [Enemy]
   ```

**Collision Handling:**

If the target position is not walkable (wall, another entity, out of bounds):

- The suplex still deals damage
- The target is NOT moved (suplex "failed" to reposition)
- Display message: `"Suplex hits <target> but failed to reposition! (<damage> damage)"`

If the target position is walkable:

- The suplex deals damage
- The target is moved to the new position
- Display message: `"You suplex <target> to the other side! (<damage> damage)"`

### Enemy AI Usage

**AI Decision Making:**

Enemies can use suplex when:

- Player is adjacent
- Enemy has learned suplex behavior (reinforcement learning weight)
- Random chance based on enemy's reinforcement weights

**AI Implementation:**

- Add "suplex" as an action type in enemy reinforcement learning
- Enemies will naturally learn when suplex is effective through gameplay
- No special AI logic needed beyond exposing the action

---

## UI/Display

### Command Interface

**Tab Completion:**

- `suplex <TAB>` shows list of adjacent enemies
- `s <TAB>` shows list of adjacent enemies (alias)

**Command Output Messages:**

Success (with reposition):

```text
You grab Goblin and suplex them to the other side! (5 damage)
Goblin is repositioned!
```

Success (blocked reposition):

```text
You suplex Goblin against the wall! (5 damage)
Goblin couldn't be moved!
```

Failure (out of range):

```text
Goblin is not in range for a suplex!
```

Failure (invalid target):

```text
There is no enemy named 'Goblin' nearby.
```

Enemy using suplex on player:

```text
Orc grabs you and suplexes you! (4 damage)
You are repositioned!
```

### Map Display

- Standard map tile updates as entities move
- Player position updates immediately if suplexed by enemy
- Enemy position updates immediately if suplexed by player

### Stats Display

- Damage is reflected in HP changes for target
- No special status effects or indicators needed

---

## Commands Integration

### Command Parser Updates

**Add to command list:**

- `suplex` (full command)
- `s` (alias)

**Command categories:**

- Combat commands (alongside `attack`, `defend`)

**Tab completion support:**

- Complete enemy names after `suplex` or `s`
- Use same target completion logic as `attack` command

---

## Implementation Requirements

### Files to Modify

1. **`src/commands.py`**
   - Add `handle_suplex()` method
   - Parse `suplex <target>` and `s <target>` commands
   - Validate target adjacency
   - Calculate damage and new position
   - Update entity positions via map system

2. **`src/tab_completion.py`**
   - Add "suplex" to command list in `_get_all_commands()`
   - Add "suplex" and "s" to argument completion in `_complete_argument()`
   - Use `_complete_target()` for enemy name completion

3. **`src/enemy.py`**
   - Add suplex action to enemy AI decision making
   - Add reinforcement learning weight for suplex action
   - Implement `perform_suplex()` method for enemies

4. **`src/game_state.py`**
   - No changes needed (uses existing position and damage systems)

5. **`src/map_system.py`**
   - No changes needed (uses existing `move_player()` and `move_enemy()` methods)

### Implementation Steps

1. **Add suplex command parsing**
   - Recognize "suplex" and "s" commands
   - Extract target name from command
   - Find matching adjacent enemy

2. **Implement damage calculation**
   - Get attacker's equipped weapon damage
   - Add slight random variance
   - Apply damage to target

3. **Implement repositioning logic**
   - Calculate opposite position
   - Check if position is walkable
   - Move target if possible
   - Display appropriate message

4. **Add tab completion**
   - Add commands to completion list
   - Enable target name completion

5. **Add enemy AI support**
   - Add suplex action to reinforcement learning
   - Implement enemy suplex behavior
   - Test AI usage in combat

### Testing Checklist

- [ ] Player can suplex adjacent enemies
- [ ] Short alias `s <target>` works
- [ ] Damage is based on equipped weapon
- [ ] Target moves to opposite side when possible
- [ ] Target stays in place when blocked by walls/entities
- [ ] Out of range message displays correctly
- [ ] Tab completion shows adjacent enemies
- [ ] Enemy AI can suplex the player
- [ ] Map updates correctly after repositioning
- [ ] Collision detection prevents invalid moves

---

## Future Enhancements

**Not for initial implementation:**

- Suplex chaining (suplex multiple times in a row)
- Critical suplex (extra damage + guaranteed reposition)
- Suplex through entities (push other enemies out of the way)
- Suplex into hazards (walls deal extra damage)
- Special suplex moves for different weapon types
- Suplex cooldown (prevent spamming)

---

## Notes

- This command adds tactical depth to combat positioning
- Players can use it to separate enemies or reposition themselves
- Enemies using suplex creates dynamic combat scenarios
- The mechanic is simple enough to understand but strategic to master
- Weapon-based damage makes weapon choice matter more
