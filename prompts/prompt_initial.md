# Core Game Design

**Purpose:** Create a simple ASCII graphical dungeon crawling RPG where players explore a map, fight monsters, collect items, and escape.

**Status:** Ready for Implementation

---

## Overview

Hole Wizards is a text-based dungeon crawling game with:

- A text interface for player commands and game feedback
- An ASCII map showing explored areas and entities (player, monsters, walls, doors, chests, bags)
- A statistics window with multiple pages (player, enemy, inventory, chest)
- Turn-based combat and item/spell management system

---

## UI/Display

### Map Layout (Top Left)

- Icon `p` for the player
- Icon `m` for monsters
- Green lines for walls
- Red lines for doors
- Yellow squares for chests
- Cyan squares for bags

### Stats Window (Top Right - Multiple Pages)

**Player Stats Page:**

- Player HP
- Player Mana
- Player XP
- Player Level
- Equipped Spell

**Enemy Stats Page:**

- Enemy Name
- Enemy HP
- Enemy Mana
- Enemy XP
- Enemy Level
- Equipped Spell

**Player Inventory Page:**

- Lists all items in inventory

**Enemy Inventory Page:**

- Lists all items in enemy inventory
- Only accessible when enemy HP = 0 (dead)

**Chest Inventory Page:**

- Lists items in targeted chest

### Log & Command Interface (Bottom Half)

- Displays game messages and action results
- Player enters commands; game updates and prints results

---

## Mechanics

### Information & UI Commands

#### show player stats

- **Effect:** Display the player stats page
- **Requirements:** None
- **Outcome:** Player stats page shown in stats window

#### show enemy stats

- **Effect:** Display the enemy stats page
- **Requirements:** An enemy must exist in the game
- **Outcome:** Enemy stats page shown in stats window

#### show player inventory

- **Effect:** Display the player's inventory page
- **Requirements:** None
- **Outcome:** Player inventory page shown in stats window

#### show enemy inventory

- **Effect:** Display the enemy's inventory page
- **Requirements:** Enemy must be dead (HP = 0)
- **Outcome:** Enemy inventory page shown in stats window

#### show chest inventory

- **Effect:** Display the chest's inventory page
- **Requirements:** A chest must exist
- **Outcome:** Chest inventory page shown in stats window

#### list commands

- **Effect:** Show all available commands with descriptions
- **Requirements:** None
- **Outcome:** Command list displayed in log

### Item & Spell Management

#### take "item"

- **Effect:** Pick up an item and add it to player inventory
- **Requirements:** Item must be on the ground
- **Outcome:** Item moved to inventory, item removed from map

#### drop "item"

- **Effect:** Remove item from inventory and place it in a bag on the ground at player's location
- **Requirements:** Item must be in inventory
- **Outcome:** Item placed in bag at current position

#### equip "item"

- **Effect:** Mark item as equipped and apply its EQUIP effect
- **Requirements:** Item must be in inventory
- **Outcome:** Item marked with "*", equipped slot filled, item effect applied
- **Note:** Only 1 weapon, 1 armor, and 1 spell can be equipped simultaneously

#### use "item"

- **Effect:** Remove item from inventory and apply its USE effect
- **Requirements:** Item must be in inventory
- **Outcome:** Item consumed/applied, effect triggered

### Combat Commands

#### attack

- **Effect:** Deal damage to enemy
- **Requirements:** An enemy must be present
- **Outcome:** Damage dealt based on equipped weapon or default (1 damage if unarmed), enemy HP reduced
- **Mechanics:**
  - If no weapon equipped: damage = 1
  - If weapon equipped: damage = weapon's attack value
  - If weapon has ATTACK effect: apply that effect

#### defend

- **Effect:** Reduce incoming damage on the next enemy action
- **Requirements:** None (can always defend)
- **Outcome:** Next incoming damage reduced by 1
- **Mechanics:**
  - If no armor equipped or no defend value: reduce damage by 1
  - If armor equipped: reduce damage by armor's defend value

### Movement Commands

#### move up

- **Effect:** Move player up on the map
- **Mechanics:** Increase Y coordinate by 1

#### move down

- **Effect:** Move player down on the map
- **Mechanics:** Decrease Y coordinate by 1

#### move left

- **Effect:** Move player left on the map
- **Mechanics:** Decrease X coordinate by 1

#### move right

- **Effect:** Move player right on the map
- **Mechanics:** Increase X coordinate by 1

---

## Data Structures

### Player

```
- HP: integer (starts at 10)
- Mana: integer (starts at 5)
- XP: integer (starts at 0)
- Level: integer (starts at 1)
- Position: {x, y}
- Inventory: array of Items
- Equipped Weapon: Item or null
- Equipped Armor: Item or null
- Equipped Spell: Spell or null
- Alive: boolean (true = alive, false = dead)
- View Distance: integer (default 1, affects map visibility)
```

### Enemy

```
- Name: string
- HP: integer
- Mana: integer
- XP: integer (random 1-10, awarded when defeated)
- Level: integer
- Position: {x, y}
- Inventory: array of Items
- Equipped Weapon: Item or null
- Equipped Armor: Item or null
- Equipped Spell: Spell or null
- Alive: boolean
- View Distance: integer
- Reinforcement: array of integers (1-10) - AI action weights
```

### Item

```
- Name: string
- Type: string (weapon, armor, consumable, etc.)
- Attack Value: integer (if weapon)
- Defend Value: integer (if armor)
- HP Increase: integer (for potions or equipment)
- Mana Increase: integer (for certain items)
- EQUIP Effect: function (applied when equipped)
- USE Effect: function (applied when used/consumed)
- ATTACK Effect: function (applied when using this item to attack)
```

### Map

```
- Width: integer
- Height: integer
- Tiles: 2D array
  - Each tile contains: terrain type, entities (player, enemies, items, walls, doors, chests)
- Player View: tracks explored areas visible to player
```

---

## Statistics System

### HP (Hit Points)

- Integer value
- When HP reaches 0: Alive = false (entity is dead)
- Reduced by damage taken
- Some items increase HP permanently
- Default player start: 10

### Mana

- Integer value (minimum 0)
- Required to cast spells
- If spell's mana cost exceeds current mana: spell cannot be used
- Default player start: 5

### XP (Experience Points)

- Player XP starts at 0
- Monsters grant randomized XP (1-10) when defeated
- Defeating a monster adds that monster's XP to player total

### Level

- Increases by 1 for every 10 XP gained
- Increasing level grants: +1 HP, +1 Mana
- Player starts at Level 1

### Position

- Stored as {x, y} coordinates on the map
- Updated by movement commands

### View Distance

- Number of squares visible from current position
- Default: 1
- Affects map revealed to player

### Alive (Status)

- Boolean: true (alive) or false (dead)
- Player: If Alive = false, game over
- Enemy: If Alive = false, can be looted; reinforcement array no longer used

### Reinforcement (Enemy Only)

- Array of integers (1-10) representing weights for each possible action
- Decreases by 1 for the last-used action when enemy takes damage
- Increases by 1 for the last-used action when enemy heals
- Increases by 2 for the last-used action when enemy deals damage
- Movement actions never decrease below 3 (prevents enemies from getting stuck)

---

## Edge Cases & Rules

- **Simultaneous Death:** If player and enemy reach 0 HP at the same time, enemy dies and player becomes critically wounded (set to 1 HP)
- **Empty Inventory:** Player can always equip items if inventory is not empty
- **Movement Boundaries:** Movement off the map edge should either wrap, block, or reveal new areas (to be specified)
- **Multiple Items:** Only one weapon, one armor, and one spell can be equipped at a time
- **Dead Enemies:** Only dead enemies can be looted; alive enemies cannot have their inventory accessed
- **Equipment Conflicts:** Equipping a new item of the same type unequips the previous one
- **Inventory Full:** Behavior if inventory reaches max capacity (to be specified)

---

## Dependencies

- **Map System:** Required for tracking player position, enemies, items, terrain
- **Combat System:** Player vs Enemy damage calculation and turn management
- **Item System:** Defines item properties and effects

---

## Notes

- **Language:** Python
- **UI Rendering:** Implement using clear text-based layout (no external UI framework required yet)
- **Turn System:** Combat should be turn-based (player acts first, then enemies respond)
- **Expandability:** Design should allow for future additions of spells, more complex items, and varied enemy types
- discarded after use

Mana potions

- increases mana by a random amount when used
- discarded after use

Weapons

- has an ATTACK effect
- must be equipped to use

Armor

- has a DEFEND effect

### spells

spells are items with randomized effects.

effects are activated passively, using them or equipping them

if a spell with an ATTACK effect is equipped and the user(player or monster attacks), it will trigger the ATTACK effect

if a spell with a DEFEND effect is eqipped and the user(player or monster) is attacked, it will trigger the DEFEND effect

basic spells will have 1 effect

advanced will have 2 effects

superior spells will have 3 effects

PASSIVE effects

- applied when the spell enters inventory

EQUIP effects

- applied when equipped

USE effects

- applied when used

ATTACK effects

- triggered when using the attack command and equipped
- damages the opponent for a random amount
- the amount can be fixed or variable (changes each attack)
- range between 1 and 10

DEFEND effects

- triggered when equipped and attacked
- reduces the amount of incoming damage by a fixed(randomized) amount
- range between 1 and 10

### effects

increase HP

- can be a USE, PASSIVE, EQUIP effect
- armor or spell

decrease HP

- can be a USE, PASSIVE, EQUIP effect
- weapon, armor, spell

increase Mana

- can be a USE, PASSIVE, EQUIP effect
- armor or spell

decrease Mana

- can be a USE, PASSIVE, EQUIP effect
- weapon armor or spell

increase attack

- can be a USE, PASSIVE, EQUIP effect
- weapon armor or spell

decrease attack

- can be a USE, PASSIVE, EQUIP effect
- weapon armor or spell

increase view distance

- can be a USE, PASSIVE, EQUIP effect
- weapon armor or spell

decrease view distance

- can be a USE, PASSIVE, EQUIP effect
- armor or spell

range

- increases range (random number 1 to 10) of attacks or spells
- can be a USE PASSIVE, EQUIP, DEFEND effect

### monsters

### map

256x256 squares
a square can be a wall, a door, or open

wall

- can only contain a wall(doors, players, items, enemies no allowed)

door

- 2 states: open and closed
- if closed, nothing else can exist on square
- if open players, items, enemies can exist on square
- must have a wall on either side

open

- players, items, enemies can exist on square

outside squares are all walls

- except for 2 squares, one will be the entrance(player start), other is exit(player wins)

---

## gameplay logic

### Program structure

- initialize list of weapons
  - each weapon will have a name and ATTACK effect
  - write these values to weapons.cfg
- initialize list of armors
  - each armor will have a name and a DEFEND effect
  - write these values to armor.cfg
- initialize list of spells
  - generate a number of spells, for each one pick random effects
  - write these values to spells.cfg
- initialize player stats
- write player stats to file charsheet.cfg
- initialize the map
- write the map to file map.map
- update the map section of the screen
- update the stats section of the screen
- intialize monsters
  - assign a weapon, armor and spell
  - assign a location on the map (update the map.map file)
  - assign a name(no duplicates)
  - assign random states (1-10)
  - assign a reinforcement stat
  - write entries to monsters.cfg
- give the player a starting spell, weapon and armor
  - update charsheet.cfg
- place the player on the map
  - update the map portion of the screen
  - update the map.map
- print the introductory message(from file intro.msg)
- player enters command
  - update position on map.map and in charsheet.cfg
  - redraw the map based on the player's view distance stat
- each other monster enters in commands at random using their reinforcement stat to weight decisions
- loop back to waiting for player input
- continue until player lands on the exit square or player HP=0
- if player lands on exit print the victory message victory.msg
- if player HP=0 print the defeat message defeat.msg
- end the program

### project structure

- use any relavant python modules, maintain a requirement.txt
- use kivy for the graphical window
- create a python virtual environment to work in
- update gitignore to include relavent entries
- update readme.md with install instructions
- store game files in data folder
- use the utilities folder additional scripts
- name generator script
  - names for players and monsters
  - stored in names.names
- item generator script
- armor generator script
- weapon generator script
- spell generator script
- map component script
  - generates different iterations of door and wall arrangements
- random map script
  - uses the components to assemble a map in the file map.map
