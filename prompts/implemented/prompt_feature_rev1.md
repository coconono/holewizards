# Feature Revisions Design

**Purpose:** Add new commands for game control and improve visibility balance.

**Status:** New

---

## Overview

This feature adds quality-of-life commands for player control (quit, restart, legend) and improves movement with the move command. Additionally, visibility ranges are adjusted for better game balance.

---

## Mechanics

### Visibility Adjustment

Player and enemy visibility ranges are updated for balanced gameplay.

**Implementation Details:**

- Player visibility range: 3 squares
- Enemy visibility range: 5 squares

---

## Player Commands

### quit

- **Effect:** Ends the game and exits the application
- **Requirements:** None
- **Outcome:** Game terminates

### restart

- **Effect:** Ends the current game and returns to the intro screen
- **Requirements:** None
- **Outcome:** Game state resets, player sees the intro message

### legend

- **Effect:** Displays a legend showing what each icon on the map represents
- **Requirements:** None
- **Outcome:** Player sees a reference table of all map symbols and their meanings

### move x,y

- **Effect:** Moves the player to the specified x,y coordinates
- **Requirements:** Must be a valid reachable position
- **Outcome:** Player moves one square at a time toward the destination; movement is interrupted if a new enemy is encountered or if a wall blocks the path

---

## Edge Cases & Rules

- If player attempts to move to an unreachable location (blocked by walls), the move command fails
- If an enemy is spotted during movement, the move is interrupted and combat state is initiated
- Legend command should display all possible map symbols currently in use

---

## Dependencies

- Affects: command parsing system, visibility system, game loop
