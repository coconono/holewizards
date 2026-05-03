# Hole Wizards

**Language:** Python

## Goal

Create a simple ASCII graphical dungeon crawling role playing game. It will have:

- A text interface for the user to enter commands and receive feedback
- A map that shows what the player has explored
- A statistics window that will show useful information

---

## UI Design Notes

### Top Left Corner: Map

- Icon `p` for the player
- Icon `m` for the monster
- Green lines for walls
- Red line for door
- Yellow square for chest
- Cyan square for bag

### Bottom Half: Text Log & Command Interface

- See section on commands
- user enters commands, game updates and prints results

### Top Right Corner: Stats (Multiple Pages)

#### Player Stats Page

- Player HP
- Player Mana
- Player XP
- Player Level
- Equipped Spell

#### Enemy Stats Page

- Enemy Name
- Enemy HP
- Enemy Mana
- Enemy XP
- Enemy Level
- Equipped Spell

#### Player Inventory Page

- lists all items in inventory

#### Enemy Inventory Page

- lists all items inventory
- can only be search if dead (enemy HP = 0)

#### Chest Inventory Page

---

## mechanics

### commands

show player stats

- displays the player stats page

show enemy stats

- displayes the enemy stats page

show player inventory

- displays the player inventory

show enemy inventory

- displays enemy inventory

show chest inventory

- show inventory of the chest(if it exists)

take "item"

- pick up the item and put it in inventory
- also applies to spells

drop "item"

- remove item and place it bag behind player
- also applies to spells

equip "item"

- mark the item with a "*" and apply its EQUIP effect
- also applies to spells
- only 1 weapon, 1 armor, and 1 spell can be equipped

use "item"

- remove the item and apply its USE effect
- also applies to spells

attack

- if no item equipped attack damage is 1
- if item is equipped use the item's attack damage
- if item has an ATTACK effect apply that.

defend

- if no item equipped, or item does not have a defend value, reduce incoming attack damage by 1
- if item is equipped  

list commands

- shows the list of commands with a short description

### statistics

HP

- integer
- if 0, set Alive to 0, greater than 0, Alive value 1
- gets subtracted by damage
- some items will increase HP

Alive

- boolean
- value 0 is dead, value 1 is alive
- if player value is 0, game over
- player value is 1, they can still enter commands
- if enemy value 0, they can be looted

Mana

- integer
- minimum value 0
- if a spell's mana cost exceeds the value of mana, it cannot be used

XP

- player XP starts at 0
- monsters will get a randomized amount of XP between 1 and 10
- killing a monster will add that monster's XP value to the players

Level

- every 10 XP increases the level by 1
- increasing the level will also increase HP by 1 and Mana by 1

Damage

- default value is 1, modified by items, spells

Position

- x,y value on the map

View distance

- number of squares the player or enemy can see
- vision for the player is represented by the amount of map revealed
- default is 1

### items

HP potions

- increases HP by a random amount when used
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

decrease HP

- can be a USE, PASSIVE, EQUIP effect

increase Mana

- can be a USE, PASSIVE, EQUIP effect

decrease Mana

- can be a USE, PASSIVE, EQUIP effect

increase attack

- can be a USE, PASSIVE, EQUIP effect

decrease attack

- can be a USE, PASSIVE, EQUIP effect

increase view distance

- can be a USE, PASSIVE, EQUIP effect

decrease view distance

- can be a USE, PASSIVE, EQUIP effect

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
- initialize list of spells
  - generate a number of spells, for each one pick random effects
- initialize player stats
- write player stats to file charsheet.cfg
- initialize the map
- write the map to file map.map
- intialize monsters
  - assign a weapon, armor and spell
  - assign a location on the map (update the map.map file)
  - assign a name(no duplicates)
  - write entries to monsters.cfg
- give the player a starting spell, weapon and armor
  - update charsheet.cfg
- place the player on the map
  - update the map.map
- print the introductory message(from file intro.msg)
