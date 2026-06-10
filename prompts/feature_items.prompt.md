# Item System Design

**Purpose:** Implement comprehensive item properties with EQUIP, USE, and ATTACK effects for weapons, armor, and consumables.

**Status:** Ready for Implementation

---

## Overview

The item system defines how all equipment, weapons, and consumables work in Hole Wizards. Items have multiple effect types (EQUIP, USE, ATTACK) that modify player stats, apply status effects, or trigger special behaviors. This system integrates with both turn-based and real-time gameplay modes.

---

## Data Structures

### Item Class

All items must have the following properties:

```
- name: string (unique identifier)
- type: string (weapon, armor, consumable, quest, etc.)
- attack_value: int (base attack bonus, 0 if not a weapon)
- defend_value: int (base defense bonus, 0 if not armor)
- hp_increase: int (stat modification on equip or use)
- mana_increase: int (stat modification on equip or use)
- equip_effect: dict or callable (applied when equipped)
- use_effect: dict or callable (applied when consumed/used)
- attack_effect: dict or callable (applied during attacks)
- consumable: bool (True if item is destroyed on use)
- description: string (flavor text, human-written)
```

**Implementation Details:**
- Effects are stored as dicts with keys: `type`, `value`, `duration`, `message`
- Effect types: `heal`, `damage`, `buff_attack`, `buff_defense`, `status_poison`, `status_burn`, `lifesteal`
- Consumables are removed from inventory after use
- Non-consumables (e.g., weapons) remain in inventory when used

---

## Mechanics

### EQUIP Effect

Applied when the item is equipped (weapons, armor, accessories).

**Implementation Details:**
- Modifies player's base stats (HP, Mana, Attack, Defense)
- Changes persist until item is unequipped
- Can have positive or negative modifiers
  - Example: Heavy armor (+10 defense, -5 max HP)
  - Example: Magic ring (+15 max mana, +0 defense)
- When equipping, calculate: `player.stat += item.stat_modifier`
- When unequipping, reverse: `player.stat -= item.stat_modifier`
- Display stat changes in log and update UI immediately
- Cannot exceed max stat caps (HP ≤ max_hp, Mana ≤ max_mana)

**Example Log Output:**
```
> You equip Heavy Plate Armor.
> Defense +10, Max HP -5.
```

---

### USE Effect

Applied when the item is used or consumed (potions, scrolls, buff items).

**Implementation Details:**
- Instant effects: Restore HP/Mana, apply temporary buffs
- Timed effects: Apply buff that lasts for N turns or N seconds (real-time mode)
- Conditional effects: Some items require conditions (e.g., weapon must be equipped)
- Consumables are destroyed after use
- Display effect in log with confirmation

**Effect Categories:**

1. **Healing/Restoration**
   - Restores HP or Mana immediately
   - Example: Health Potion restores 20 HP
   ```
   > You use a Health Potion.
   > You restore 20 HP!
   ```

2. **Temporary Buffs**
   - Adds elemental damage to next attack(s)
   - Example: Fire Potion adds +10 fire damage to next attack
   ```
   > You use a Fire Potion.
   > Your next attack will deal an additional 10 fire damage!
   ```

3. **Conditional Effects**
   - **Rule:** Elemental buff potions require a weapon equipped
   - If no weapon equipped → damage the player instead
   ```
   > You use a Fire Potion.
   > You take 10 fire damage because you have no weapon equipped!
   ```

**Implementation Details:**
- Track active buffs in `player.active_buffs[]` list
- Each buff has: `effect_type`, `value`, `remaining_turns` or `expiry_time`
- Decrement buff counters each turn (turn-based) or on timer (real-time)
- Remove expired buffs automatically

---

### ATTACK Effect

Applied when using this item to attack (weapons only).

**Implementation Details:**
- Triggers automatically when attacking with this weapon equipped
- Can deal additional damage (elemental, type-based)
- Can apply status effects (poison, burn, freeze)
- Can heal the player (lifesteal)
- Cannot stack with suplex command (suplex ignores ATTACK effects)

**Effect Categories:**

1. **Elemental Damage**
   - Adds extra damage of a specific type
   - Example: Fire Sword deals +10 fire damage per attack
   ```
   > You attack the goblin with your Fire Sword.
   > You deal 15 physical damage and 10 fire damage!
   ```

2. **Status Effects (Damage Over Time)**
   - Applies poison, burn, or other DOT status
   - Enemy takes damage each turn for N turns
   - Example: Poison Dagger applies poison (5 damage/turn for 3 turns)
   ```
   > You attack the goblin with your Poison Dagger.
   > You deal 10 physical damage and apply poison!
   > The goblin will take 5 poison damage each turn for the next 3 turns.
   ```
   - Example: Burn Staff applies burn (4 damage/turn for 3 turns)
   ```
   > You attack the goblin with your Burn Staff.
   > You deal 8 physical damage and apply burn!
   > The goblin will take 4 burn damage each turn for the next 3 turns.
   ```

3. **Lifesteal**
   - Heals player for a percentage or flat amount of damage dealt
   - Example: Vampire Sword heals 5 HP per successful hit
   ```
   > You attack the goblin with your Vampire Sword.
   > You deal 12 physical damage and absorb 5 HP!
   ```

**Implementation Details:**
- Status effects stored in `enemy.status_effects[]` list
- Each status has: `effect_type`, `damage_per_turn`, `remaining_turns`
- Process status effects at start of each turn (turn-based) or on timer (real-time)
- Display status damage in log before enemy's turn
- Remove status when turns reach 0

---

### Suplex Interaction

**Rule:** Suplex command ignores all ATTACK effects.

**Implementation Details:**
- Suplex deals damage based on player's base attack stat only
- Item ATTACK effects (elemental damage, status, lifesteal) do NOT apply
- Player can still have weapon equipped, but its effects are inactive during suplex
- Display message clarifying this

**Example:**
```
> You suplex the goblin!
> You deal 20 physical damage.
> (Fire Sword's ATTACK effect does not apply to suplex)
```

---

## Player Commands

### show [item_name] stats

Displays detailed information about an item in the inventory or equipped.

- **Effect:** Shows item properties and all effect descriptions
- **Requirements:** Item must be in inventory or equipped
- **Outcome:** Formatted stat display in log

**Example Output:**
```
> show "Health Potion" stats

Item: Health Potion
Type: Consumable
HP Increase: +20
Mana Increase: +0
EQUIP Effect: None
USE Effect: Restores 20 HP when consumed
ATTACK Effect: None
```

**Example Output (Weapon):**
```
> show "Fire Sword" stats

Item: Fire Sword
Type: Weapon
Attack Value: +15
Defend Value: +0
HP Increase: +0
Mana Increase: +0
EQUIP Effect: None
USE Effect: None
ATTACK Effect: Deals +10 fire damage per attack
```

**Implementation Details:**
- Parse item name from command (handle quotes if present)
- Look up item in `player.inventory` or `player.equipped_items`
- Format output with consistent spacing and labels
- Show "None" for unused effect slots
- Display human-readable effect descriptions (not raw data)

---

### use [item_name]

Uses or consumes an item from inventory.

- **Effect:** Triggers USE effect, removes item if consumable
- **Requirements:** Item must be in inventory
- **Outcome:** USE effect applied, log displays results

**Implementation Details:**
- Check if item exists in inventory
- Validate any conditional requirements (e.g., weapon for elemental potions)
- Apply USE effect (heal, buff, etc.)
- Remove item from inventory if `consumable == True`
- Update UI (HP/Mana bars, inventory count)
- Log all changes with clear messages

---

### equip [item_name]

Equips a weapon, armor, or accessory.

- **Effect:** Adds item to equipped slot, triggers EQUIP effect
- **Requirements:** Item must be equippable (not consumable)
- **Outcome:** EQUIP effect applied, stats updated

**Implementation Details:**
- Check item type to determine slot (weapon, armor, accessory)
- Unequip existing item in that slot (if any)
- Apply EQUIP effect stat modifiers
- Update `player.equipped_items[slot]` reference
- Display stat changes in log

---

### unequip [item_name]

Removes an equipped item.

- **Effect:** Reverses EQUIP effect, returns item to inventory
- **Requirements:** Item must currently be equipped
- **Outcome:** EQUIP effect reversed, stats updated

**Implementation Details:**
- Reverse EQUIP effect stat modifiers
- Remove from `player.equipped_items[slot]`
- Item remains in inventory (not destroyed)
- Update UI and log

---

## Configuration Files

### armor.cfg

Update to include new fields:

```
[ARMOR_NAME]
name = Heavy Plate Armor
type = armor
attack_value = 0
defend_value = 10
hp_increase = -5
mana_increase = 0
equip_effect = {"type": "stat_mod", "defense": 10, "max_hp": -5}
use_effect = {}
attack_effect = {}
description = Thick iron plates that slow you down.
```

---

### weapons.cfg

Update to include new fields:

```
[WEAPON_NAME]
name = Fire Sword
type = weapon
attack_value = 15
defend_value = 0
hp_increase = 0
mana_increase = 0
equip_effect = {}
use_effect = {}
attack_effect = {"type": "elemental", "element": "fire", "damage": 10}
description = A blade wreathed in flames.
```

---

### items.cfg (NEW FILE)

Create this file for consumables and miscellaneous items:

```
[HEALTH_POTION]
name = Health Potion
type = consumable
attack_value = 0
defend_value = 0
hp_increase = 20
mana_increase = 0
equip_effect = {}
use_effect = {"type": "heal", "hp": 20}
attack_effect = {}
consumable = True
description = A red vial that restores health.

[FIRE_POTION]
name = Fire Potion
type = consumable
attack_value = 0
defend_value = 0
hp_increase = 0
mana_increase = 0
equip_effect = {}
use_effect = {"type": "buff_attack", "element": "fire", "damage": 10, "duration": 1, "requires_weapon": True}
attack_effect = {}
consumable = True
description = Imbues your weapon with fire for one attack.
```

---

## Edge Cases & Rules

### Effect Stacking
- **Rule:** Multiple EQUIP effects stack additively
  - Equipping Fire Sword (+15 attack) and Strength Ring (+5 attack) = +20 total attack
- **Rule:** USE buffs do NOT stack with themselves
  - Using two Fire Potions in a row does not give +20 fire damage, only refreshes duration

### Stat Boundaries
- **Rule:** HP and Mana cannot exceed maximum values
  - If max_hp = 50 and current_hp = 45, healing potion (+20) only restores to 50, not 65
- **Rule:** Stats cannot drop below 0
  - If unequipping armor would drop defense below 0, set to 0

### Status Effect Conflicts
- **Rule:** Only one instance of each status type per enemy
  - Applying poison while enemy is already poisoned refreshes the duration and damage (overwrites)
  - Example: Poison (5 dmg/turn, 2 turns left) + new poison (5 dmg/turn, 3 turns) = (5 dmg/turn, 3 turns left)

### Consumable Edge Case
- **Rule:** If item is consumed but USE effect fails (e.g., already at max HP), item is still consumed
  - Display message: "You use a Health Potion, but you're already at full health!"

### Real-Time Mode Compatibility
- **Rule:** All item commands must work in both turn-based and real-time modes
- **Turn-Based:** Commands typed as text (existing behavior)
- **Real-Time:** Pauses game when opening inventory screen (like chest interaction)
  - Player types commands, then resumes real-time mode

### Item Not Found
- **Rule:** If player tries to use/show/equip an item not in inventory, display error
  - "You don't have [item_name] in your inventory."

---

## Dependencies

Features or systems this depends on:
- **Player stats system** (HP, Mana, Attack, Defense tracking)
- **Inventory system** (storing items, equipped slots)
- **Combat system** (attack command, damage calculation)
- **Status effect tracking** (poison, burn, buffs)
- **Real-time mode** (pausing for inventory interaction)
- **Game logging** (displaying effect messages)

---

## Generator Script Updates

### utilities/item_gen.py

Update or create script to generate `items.cfg` with:
- Health potions (varying restoration amounts: 10, 20, 50)
- Mana potions (varying restoration amounts: 10, 20, 50)
- Elemental buff potions (Fire, Ice, Lightning)
- Stat boost potions (temporary attack/defense buffs)

### utilities/weapon_gen.py

Update to include:
- `attack_effect` field in generated weapons
- Status effect weapons (poison daggers, burn staffs)
- Elemental damage weapons (fire swords, ice hammers)
- Lifesteal weapons (vampire blades)

### utilities/armor_gen.py

Update to include:
- `equip_effect` field with stat tradeoffs
- Heavy armor (high defense, low HP)
- Light armor (balanced stats)
- Magic robes (high mana, low defense)

---

## Notes

### Implementation Priority

1. Update Item class with new properties
2. Implement EQUIP effect logic (stat modifiers)
3. Implement USE effect logic (healing, buffs)
4. Implement ATTACK effect logic (elemental damage, status)
5. Add `show [item] stats` command
6. Update config parsers to read new fields
7. Update generator scripts
8. Test all edge cases and interactions

### Human-Written Content

**DO NOT auto-generate:**
- Item descriptions (flavor text)
- Item names (creative content)

**OK to auto-generate:**
- Stats, values, and effect properties
- Config file structure
- Code logic and calculations

