# Loot & Inventory System Design

**Purpose:** Expand player inventory capacity with stackable items and implement loot drops from defeated enemies and chest discoveries.

**Status:** New

---

## Overview

Players gain an expanded inventory system with stackable potions, multiple weapons/armor slots, and spells. Defeated enemies drop their inventory and equipped items as loot. Maps spawn chests containing random valuable items that players can loot.

---

## Mechanics

### Player Inventory Expansion

Players have a fixed inventory with the following capacity:

**Implementation Details:**

- One additional weapon slot alongside equipped weapon
- One additional armor slot alongside equipped armor
- Maximum 99 HP Potions (stackable, display as "HP Potions(x)")
- Maximum 99 Mana Potions (stackable, display as "Mana Potions(x)")
- 3 spells maximum (only one equipped at a time)

### Monster Loot Drops

When monsters are defeated, they drop their inventory and equipped items as loot.

**Implementation Details:**

- Monsters carry random 0-10 HP Potions
- Monsters carry random 0-10 Mana Potions
- Monsters carry a random spell from spells.cfg
- Player accesses dropped loot with "show loot" command
- Player uses "take item" to transfer items to inventory

### Map Chests

Maps spawn 10 chests scattered throughout containing valuable items.

**Implementation Details:**

- Each chest contains random items: 0-2 weapons, 0-2 armor pieces, 0-12 HP Potions, 0-12 Mana Potions
- Player accesses chest with "show chest" command
- Player uses "take item" to transfer items to inventory

---

## UI/Display

The inventory view should display stackable items with quantity notation:

```plaintext
PLAYER INVENTORY

* Longsword (equipped)
  Broadsword
* Iron Armor (equipped)
  Leather Armor
* Fireball Spell (equipped)
  Lightning Bolt
  Heal
* HP Potions (45)
* Mana Potions (12)
```

---

## Player Commands

### show loot

- **Effect:** Display the inventory of a defeated enemy or current loot pile
- **Requirements:** Enemy must be adjacent and dead, or loot must be present at player location
- **Outcome:** Shows loot inventory page; player can "take item" to pick up items

### show chest

- **Effect:** Display contents of an adjacent chest
- **Requirements:** Chest must be adjacent to player
- **Outcome:** Shows chest inventory page; player can "take item" to loot items

### take item

- **Effect:** Move an item from loot/chest into player inventory
- **Requirements:** Item must be in current loot/chest and inventory space available
- **Outcome:** Item transferred to inventory, removed from loot/chest

---

## Data Structures

### Stackable Item

```plaintext
- Name: string (e.g., "HP Potion")
- Quantity: integer (1-99)
- Type: enum (potion, weapon, armor, spell)
```

### Loot Pile

```plaintext
- Items: list of Item/StackableItem
- Location: {x: integer, y: integer}
```

### Chest

```plaintext
- Contents: list of Item/StackableItem
- Location: {x: integer, y: integer}
- Opened: boolean
```

---

## Edge Cases & Rules

- Stackable items automatically combine (e.g., taking 5 potions when carrying 40 results in 45)
- Cannot pick up items if inventory is full
- Potions cannot be equipped, only consumed via "use" command
- Multiple spells can be carried but only one equipped for casting
- Chests are persistent once opened (items don't respawn)

---

## Implementation Tasks

- Update `monster_gen.py` to include random potions (0-10 each) and spells
- Create `spell_gen.py` to generate 20 spells and save to spells.cfg
- Implement `StackableItem` class in items.py
- Update `Inventory` class to handle stackable items and quantity display
- Add "show loot" and "show chest" command handlers to commands.py
- Update help screen to reflect new commands
- Generate and populate spells.cfg with 20 spell definitions
