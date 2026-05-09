"""UI and display system for Hole Wizards game."""


class UI:
    """Handles all UI display and rendering."""

    def __init__(self, map_width=100, stats_width=30):
        """Initialize the UI."""
        self.map_width = map_width
        self.stats_width = stats_width
        self.log_messages = []
        self.max_log_lines = 10
        self.current_stats_page = "player"  # Track which stats page is displayed

    def add_log_message(self, message):
        """Add a message to the game log."""
        self.log_messages.append(message)
        if len(self.log_messages) > self.max_log_lines:
            self.log_messages.pop(0)

    def clear_log(self):
        """Clear all log messages."""
        self.log_messages = []

    def render_player_stats(self, player):
        """Render player stats page."""
        lines = [
            "═" * (self.stats_width - 2),
            "PLAYER STATS".center(self.stats_width - 2),
            "═" * (self.stats_width - 2),
            f"HP:     {player.hp}/{player.max_hp}",
            f"Mana:   {player.mana}/{player.max_mana}",
            f"XP:     {player.xp}/10",
            f"Level:  {player.level}",
            f"Equipped Spell: {player.equipped_spell or 'None'}",
            "",
            "Position: ({}, {})".format(player.position["x"], player.position["y"]),
        ]
        return lines

    def render_enemy_stats(self, enemy):
        """Render enemy stats page."""
        if not enemy:
            return ["No enemy in sight"]
        
        lines = [
            "═" * (self.stats_width - 2),
            "ENEMY STATS".center(self.stats_width - 2),
            "═" * (self.stats_width - 2),
            f"Name:   {enemy.name}",
            f"HP:     {enemy.hp}/{enemy.max_hp}",
            f"Mana:   {enemy.mana}/{enemy.max_mana}",
            f"XP:     {enemy.xp}",
            f"Level:  {enemy.level}",
            f"Equipped Spell: {enemy.equipped_spell or 'None'}",
            "",
            "Position: ({}, {})".format(enemy.position["x"], enemy.position["y"]),
        ]
        return lines

    def render_player_inventory(self, player):
        """Render player inventory page."""
        lines = [
            "═" * (self.stats_width - 2),
            "PLAYER INVENTORY".center(self.stats_width - 2),
            "═" * (self.stats_width - 2),
        ]
        
        if not player.inventory:
            lines.append("(empty)")
        else:
            for item in player.inventory:
                marker = "*" if (item == player.equipped_weapon or 
                               item == player.equipped_armor or 
                               item == player.equipped_spell) else " "
                lines.append(f"{marker} {item}")
        
        return lines

    def render_enemy_inventory(self, enemy):
        """Render enemy inventory page."""
        if not enemy:
            return ["No enemy selected"]
        
        if not enemy.alive:
            lines = [
                "═" * (self.stats_width - 2),
                f"{enemy.name}'s INVENTORY".center(self.stats_width - 2),
                "═" * (self.stats_width - 2),
            ]
            
            if not enemy.inventory:
                lines.append("(empty)")
            else:
                for item in enemy.inventory:
                    lines.append(f" {item}")
            
            return lines
        else:
            return ["Enemy is alive - cannot loot"]

    def render_chest_inventory(self, chest_items):
        """Render chest inventory page."""
        lines = [
            "═" * (self.stats_width - 2),
            "CHEST INVENTORY".center(self.stats_width - 2),
            "═" * (self.stats_width - 2),
        ]
        
        if not chest_items:
            lines.append("(empty)")
        else:
            for item in chest_items:
                lines.append(f" {item}")
        
        return lines

    def render_stats_window(self, player, enemy, page="player", chest_items=None):
        """Render the stats window based on current page."""
        if page == "player":
            lines = self.render_player_stats(player)
        elif page == "enemy":
            lines = self.render_enemy_stats(enemy)
        elif page == "player_inventory":
            lines = self.render_player_inventory(player)
        elif page == "enemy_inventory":
            lines = self.render_enemy_inventory(enemy)
        elif page == "chest_inventory":
            lines = self.render_chest_inventory(chest_items or [])
        else:
            lines = self.render_player_stats(player)

        # Pad to fixed width
        padded_lines = []
        for line in lines:
            padded_lines.append(line.ljust(self.stats_width - 2))
        
        return padded_lines

    def render_log(self, width):
        """Render the game log."""
        lines = ["─" * width]
        for msg in self.log_messages[-self.max_log_lines:]:
            # Wrap long messages
            if len(msg) > width - 2:
                words = msg.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 > width - 2:
                        lines.append(current_line)
                        current_line = word
                    else:
                        current_line += " " + word if current_line else word
                if current_line:
                    lines.append(current_line)
            else:
                lines.append(msg)
        
        return lines[-self.max_log_lines:]

    def render_command_prompt(self):
        """Render the command prompt."""
        return "> "

    def render_full_screen(self, player, enemy, map_obj, page="player", chest_items=None):
        """Render the complete game screen (for reference, terminal will handle actual rendering)."""
        # Calculate display distances to fill available map area optimally
        # X distance to fill map_width, Y distance to keep map compact
        x_distance = (self.map_width - 1) // 2
        y_distance = 6  # Show about 13 rows (6 above/below + center)
        
        map_display = map_obj.get_visible_map(player, x_distance=x_distance, y_distance=y_distance)
        stats_lines = self.render_stats_window(player, enemy, page, chest_items)
        
        # Build the screen
        screen_lines = []
        
        # Top section: map (left) and stats (right)
        map_lines = map_display.split("\n")
        
        max_map_height = max(len(map_lines), len(stats_lines))
        
        for i in range(max_map_height):
            map_line = map_lines[i] if i < len(map_lines) else ""
            map_line = map_line.ljust(self.map_width)
            
            stats_line = stats_lines[i] if i < len(stats_lines) else ""
            
            screen_lines.append(map_line + " " + stats_line)
        
        # Log section
        screen_lines.append("")
        log_lines = self.render_log(self.map_width + 1 + self.stats_width)
        screen_lines.extend(log_lines)
        
        return "\n".join(screen_lines)

    def render_help(self):
        """Render help/command list."""
        help_text = """
╔═══════════════════════════════════════════════════════════════════════╗
║                     AVAILABLE COMMANDS                               ║
╚═══════════════════════════════════════════════════════════════════════╝

[INFORMATION]

  show player stats          → Display your character stats
  show enemy stats           → Display enemy stats
  show player inventory      → Display your inventory
  show enemy inventory       → Display enemy inventory (if dead)
  show chest inventory       → Display chest contents
  legend                     → Show map legend
  list commands              → Show this help

[MOVEMENT]

  move up | move down        → Move vertically
  move left | move right     → Move horizontally
  move x,y                   → Move toward coordinates (auto-path)

[COMBAT]

  attack                     → Attack an adjacent enemy
  defend                     → Reduce next incoming damage

[INVENTORY & ITEMS]

  take [item]                → Pick up an item
  drop [item]                → Drop an item
  equip [item]               → Equip an item/spell
  use [item]                 → Use/consume an item

[CONTROL]

  quit                       → Exit the game
  restart                    → Start a new game

╔═══════════════════════════════════════════════════════════════════════╗
║  GOAL: Find the exit (X) in the dungeon and escape alive!            ║
╚═══════════════════════════════════════════════════════════════════════╝
        """
        return help_text

    def render_legend(self):
        """Render map legend."""
        legend_text = """
╔═══════════════════════════════════════════════════════════════════════╗
║                          MAP LEGEND                                   ║
╚═══════════════════════════════════════════════════════════════════════╝

[CHARACTERS]

  p          → Player (you)
  m          → Monster/Enemy
  E          → Entrance (start location)
  X          → Exit (goal - escape here!)


[TERRAIN]

  █          → Wall (impassable, blocks movement)
  ╬          → Door (closed)
  ─          → Door (open)
  (space)    → Open floor (walkable)


[ITEMS]

  ◆          → Item/Bag (equipment, weapons, armor)
  ▪          → Consumable item (potions, etc.)


[EXPLORATION]

  ?          → Unexplored area (will reveal as you move)


╔═══════════════════════════════════════════════════════════════════════╗
║  Visibility: You can see 3 squares away.                             ║
║  Enemies can see 5 squares away.                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
        """
        return legend_text
