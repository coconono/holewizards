# Design Prompt Template

Use this template when creating new feature or mechanics design files for Hole Wizards.

## File Naming

- `prompt_initial.md` - Core game (existing)
- `prompt_FEATURE.md` - Feature-specific design (new designs use this pattern)
- Examples: `prompt_combat.md`, `prompt_inventory_system.md`, `prompt_spells.md`

---

## Template

```markdown
# [Feature Name] Design

**Purpose:** One sentence describing what this feature does or solves.

**Status:** New / In Progress / Ready for Implementation

---

## Overview

Brief description of the feature and how it fits into the game.

---

## Mechanics

### [Mechanic 1 Name]

Description of what this mechanic does.

**Implementation Details:**
- Detail 1
- Detail 2
- Detail 3

### [Mechanic 2 Name]

[Repeat above format for each mechanic]

---

## UI/Display

How this feature appears to the player (if visual).

### Example Layout

```

[ASCII representation or description]

```

---

## Player Commands

List of new or modified commands the player can use:

### command_name

- **Effect:** What happens when the player uses this command
- **Requirements:** Any conditions that must be met
- **Outcome:** What the player sees or experiences

---

## Data Structures

Any new data types, classes, or state needed:

### Class/Structure Name

```

- Property 1: type
- Property 2: type
- Method/Action: description

```

---

## Edge Cases & Rules

List any special rules, constraints, or edge cases:

- Rule 1
- Rule 2
- What happens if [scenario]?

---

## Dependencies

Features or systems this depends on:
- Feature A
- Feature B

---

## Notes

Implementation hints, gotchas, or design rationale.
```

---

## Usage Guidelines

1. **Be Specific:** The more detailed the design, the better the implementation
2. **Reference Existing Files:** Link to `prompt_initial.md` or other design files when relevant
3. **Use Examples:** ASCII mockups or concrete examples help clarify intent
4. **List Edge Cases:** Prevent implementation surprises by addressing "what if" scenarios upfront
5. **Keep It Actionable:** Every section should guide implementation, not leave questions

---

## Example: Combat System

See this template applied to a hypothetical combat system:

```markdown
# Combat System Design

**Purpose:** Define how player and enemy combat works.

**Status:** Ready for Implementation

---

## Overview

Combat is turn-based. Player acts first, then enemies respond.

---

## Mechanics

### Player Turn

Description of player actions during combat.

**Implementation Details:**
- Player can attack, cast spell, or defend
- Actions consume AP (action points)
- Combat ends when player or enemy HP ≤ 0

### Enemy Turn

Description of enemy AI behavior.

**Implementation Details:**
- Enemy AI selects random action
- Damage calculation uses Level + Equipment bonuses
- Enemy flees if HP falls below 20%

---

## Player Commands

### attack enemy

- **Effect:** Player deals damage to enemy
- **Requirements:** Player must be in combat
- **Outcome:** Enemy HP decreases, combat continues

### cast [spell_name]

- **Effect:** Player casts spell at enemy
- **Requirements:** Player has mana, spell is equipped
- **Outcome:** Spell effect applied, mana consumed

---

## Edge Cases & Rules

- What if player and enemy reach 0 HP simultaneously? → Enemy dies, player is critically wounded (1 HP)
- What if enemy has no valid actions? → Enemy defends
- Can player flee? → Not yet (future feature)
```

---

## When to Create a New Prompt File

Create a new `prompt_*.md` file when:

- Adding a major new system (combat, magic, crafting, etc.)
- Significantly expanding an existing system
- Need to document complex mechanics before implementation
- Want to iterate on design before writing code

For small tweaks to existing features, update the relevant existing file instead.
