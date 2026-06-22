# Enemy AI Tuning - Aggressive Combat Behavior

**Purpose:** Increase enemy aggression and enable enemy-to-enemy combat through enhanced suplex behavior.

**Status:** Ready for Implementation

---

## Overview

This tuning pass enhances enemy AI to create more dynamic and unpredictable combat scenarios by:

1. Increasing enemy preference for suplex attacks (especially against the player)
2. Enabling enemies to suplex other enemies (enemy-to-enemy combat)
3. Improving combat log messages to reflect these new behaviors

This makes combat more tactical and chaotic, as enemies become threats to each other as well as the player.

---

## Mechanics

### Enhanced Suplex Priority

**Current Behavior:**
- Enemies use reinforcement learning to choose actions
- Action 6 (suplex) has equal weight to other actions initially
- Enemies only learn to suplex through trial and error

**New Behavior:**
- Increase initial reinforcement weight for action 6 (suplex)
- Enemies should prefer suplex when adjacent to any valid target
- Suplex becomes a "signature move" that enemies use frequently

**Implementation:**
- Increase initial suplex weight in `Enemy.__init__()` from base weight to higher value
- Example: If base actions start at weight 1, suplex could start at weight 3-5
- This makes enemies naturally gravitate toward suplex without removing learning

### Enemy-to-Enemy Suplex

**Current Behavior:**
- Enemies can only suplex the player
- Action 6 only checks for `self._is_adjacent(enemy, self.player)`
- Enemies ignore other enemies for suplex purposes

**New Behavior:**
- Enemies can suplex adjacent enemies (not just the player)
- When choosing action 6, enemy should:
  1. Check for adjacent player first (priority target)
  2. If no adjacent player, check for adjacent enemies
  3. Randomly select one valid target and suplex them

**Target Selection Logic:**
```python
# Priority: Player first, then any adjacent enemy
valid_targets = []

# Check for player
if self._is_adjacent(enemy, self.player):
    valid_targets.append(self.player)

# Check for other enemies
for other_enemy in self.enemies:
    if other_enemy != enemy and other_enemy.alive:
        if self._is_adjacent(enemy, other_enemy):
            valid_targets.append(other_enemy)

# Select random target
if valid_targets:
    target = random.choice(valid_targets)
    # Perform suplex on target
```

**Collision Handling:**
- Enemy-on-enemy suplex uses same mechanics as player suplex
- Calculate opposite position relative to attacker
- Check if destination is walkable
- Move target if possible, or keep in place if blocked

### Combat Log Messages

**Player as Target:**
```text
Goblin grabs you and suplexes you! (4 damage)
You are repositioned!
```

**Enemy as Target (NEW):**
```text
Goblin grabs Orc and suplexes them! (3 damage)
Orc is repositioned!
```

**Blocked Reposition (Player):**
```text
Goblin suplexes you against the wall! (4 damage)
```

**Blocked Reposition (Enemy on Enemy - NEW):**
```text
Goblin suplexes Orc against the wall! (3 damage)
```

**Enemy Defeated by Suplex (NEW):**
```text
Goblin's suplex defeats Orc!
```

---

## Implementation Requirements

### Files to Modify

1. **`src/enemy.py`**
   - Increase initial reinforcement weight for action 6 (suplex)
   - Modify in `__init__()` method where `self.reinforcement` is initialized

2. **`src/game_state.py`**
   - Modify `enemy_take_turn()` method, action 6 handler
   - Add enemy-to-enemy suplex logic
   - Expand target selection to include other enemies
   - Add new log messages for enemy-to-enemy combat
   - Handle enemy death from suplex

### Implementation Steps

1. **Increase suplex weight**
   - Locate `Enemy.__init__()` in `src/enemy.py`
   - Find `self.reinforcement = [...]` initialization
   - Increase weight at index 6 (suplex) to 3-5x base weight

2. **Add enemy-to-enemy targeting**
   - Locate action 6 handler in `game_state.py`'s `enemy_take_turn()`
   - Replace single player check with multi-target selection
   - Build list of valid targets (player + adjacent enemies)
   - Randomly select one target

3. **Implement enemy-on-enemy suplex**
   - Create separate logic paths for player target vs enemy target
   - For enemy targets:
     - Calculate damage using attacker's weapon
     - Apply damage to target enemy
     - Calculate opposite position
     - Attempt to reposition target enemy
     - Display appropriate log message
     - Handle enemy death if HP reaches 0

4. **Add combat log messages**
   - Add `self.ui.add_log_message()` calls for all enemy-to-enemy actions
   - Format messages to clearly show attacker and target
   - Include damage values and repositioning status

5. **Handle defeated enemies**
   - Check if target enemy's HP <= 0 after suplex
   - Remove dead enemy from map and game state
   - Create loot bag at enemy's position
   - Display defeat message

### Testing Checklist

- [ ] Enemies prefer suplex over other actions
- [ ] Enemies can suplex the player (existing functionality)
- [ ] Enemies can suplex other adjacent enemies
- [ ] Log shows enemy-to-enemy suplex messages
- [ ] Enemy-to-enemy suplex deals weapon-based damage
- [ ] Target enemy is repositioned when possible
- [ ] Target enemy stays in place when blocked
- [ ] Enemy death from suplex creates loot
- [ ] Combat feels more chaotic and dynamic
- [ ] No infinite loops or AI deadlocks

---

## Balance Considerations

### Suplex Weight Tuning

**Conservative (Weight 3):**
- Enemies use suplex ~30% of the time when adjacent
- Still allows for attacks and defensive plays
- Recommended starting point

**Moderate (Weight 5):**
- Enemies use suplex ~50% of the time when adjacent
- Creates very aggressive combat
- May make positioning critical

**Aggressive (Weight 7+):**
- Enemies almost always suplex when possible
- Extremely chaotic combat
- May be frustrating for players

**Recommendation:** Start with weight 3, test gameplay, then adjust based on feel.

### Enemy-to-Enemy Combat Impact

**Positive Effects:**
- Creates opportunities for player to avoid damage
- Enemies can weaken each other
- More dynamic and unpredictable encounters
- Adds tactical depth (positioning matters more)

**Potential Issues:**
- Enemies might kill each other too easily
- Player might exploit enemy infighting
- Combat could become too random

**Mitigation:** Enemies should still prioritize player when both player and enemy are adjacent (as designed in implementation).

---

## Future Enhancements

**Not for initial implementation:**

- Faction system (some enemies team up)
- Enemy alliances (never suplex allies)
- Suplex chains (enemy suplexes another into player)
- Special enemy types with higher/lower suplex preference
- Player skill to influence enemy targeting
- Visual indicators for enemy aggression levels

---

## Notes

- This tuning makes combat more unpredictable and chaotic
- Player benefits from enemy infighting but must adapt to repositioning
- Reinforcement learning will still adjust weights based on success
- Enemy-to-enemy combat adds strategic positioning elements
- Log messages are critical for player understanding of what happened

