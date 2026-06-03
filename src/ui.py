"""UI and display system for Hole Wizards game."""

# Event type to color name mapping
EVENT_TYPES = {
    'combat_dealt': 'green',
    'combat_taken': 'red',
    'healing': 'blue',
    'loot': 'yellow',
    'status': 'magenta',
    'system': 'gray',
    'movement': 'cyan',
    'victory': 'bright_green',
    'defeat': 'bright_red',
    'default': 'white'
}

# ANSI color codes for terminal rendering
ANSI_COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'blue': '\033[94m',
    'yellow': '\033[93m',
    'magenta': '\033[95m',
    'gray': '\033[90m',
    'cyan': '\033[96m',
    'bright_green': '\033[1;92m',
    'bright_red': '\033[1;91m',
    'white': '\033[97m',
    'reset': '\033[0m',
    'underline': '\033[4m',
    'underline_off': '\033[24m'
}


class UI:
    """Handles all UI display and rendering."""

    def __init__(self, map_width=100, stats_width=30):
        """Initialize the UI."""
        self.map_width = map_width
        self.stats_width = stats_width
        self.log_messages = []
        self.max_log_lines = 10
        self.current_stats_page = "player"  # Track which stats page is displayed
        self.player_name = None  # Track player name for underlining
        self.enemy_names = []  # Track enemy names for underlining

    def add_log_message(self, message, event_type="default"):
        """Add a message to the game log with optional event type for coloring.
        
        Args:
            message: The log message text
            event_type: Event category for color coding (default: "default")
        """
        # Store message with its event type
        self.log_messages.append({'text': message, 'event_type': event_type})
        if len(self.log_messages) > self.max_log_lines:
            self.log_messages.pop(0)

    def clear_log(self):
        """Clear all log messages."""
        self.log_messages = []
    
    def set_entity_names(self, player_name, enemy_names):
        """Set entity names for log message formatting.
        
        Args:
            player_name: Name of the player
            enemy_names: List of enemy names currently in the game
        """
        self.player_name = player_name
        self.enemy_names = enemy_names
    
    def _format_entity_names(self, message):
        """Apply underline formatting to entity names in a message.
        
        Args:
            message: The log message text
            
        Returns:
            Message with entity names underlined
        """
        formatted = message
        underline = ANSI_COLORS['underline']
        underline_off = ANSI_COLORS['underline_off']
        
        # Underline player name
        if self.player_name and self.player_name in formatted:
            formatted = formatted.replace(
                self.player_name,
                f"{underline}{self.player_name}{underline_off}"
            )
        
        # Underline enemy names
        for enemy_name in self.enemy_names:
            if enemy_name in formatted:
                formatted = formatted.replace(
                    enemy_name,
                    f"{underline}{enemy_name}{underline_off}"
                )
        
        return formatted

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

    def _render_inventory_list(self, items, title, show_equipped_marker=False, equipped_items=None):
        """Helper method to render inventory lists consistently."""
        lines = [
            "═" * (self.stats_width - 2),
            title.center(self.stats_width - 2),
            "═" * (self.stats_width - 2),
        ]
        
        if not items:
            lines.append("(empty)")
        else:
            for item in items:
                if show_equipped_marker and equipped_items:
                    marker = "*" if item in equipped_items else " "
                    lines.append(f"{marker} {item}")
                else:
                    lines.append(f" {item}")
        
        return lines

    def render_player_inventory(self, player):
        """Render player inventory page."""
        equipped_items = [player.equipped_weapon, player.equipped_armor, player.equipped_spell]
        return self._render_inventory_list(
            player.inventory,
            "PLAYER INVENTORY",
            show_equipped_marker=True,
            equipped_items=equipped_items
        )

    def render_enemy_inventory(self, enemy):
        """Render enemy inventory page."""
        if not enemy:
            return ["No enemy selected"]
        
        if not enemy.alive:
            return self._render_inventory_list(
                enemy.inventory,
                f"{enemy.name}'s INVENTORY"
            )
        else:
            return ["Enemy is alive - cannot loot"]

    def render_chest_inventory(self, chest_items):
        """Render chest inventory page."""
        return self._render_inventory_list(chest_items, "CHEST INVENTORY")

    def render_loot_inventory(self, loot_items, enemy_name="Unknown"):
        """Render loot inventory page."""
        return self._render_inventory_list(loot_items, f"LOOT: {enemy_name}")

    def render_stats_window(self, player, enemy, page="player", chest_items=None, loot_items=None, loot_enemy="Unknown"):
        """Render the stats window based on current page."""
        if page == "player":
            lines = self.render_player_stats(player)
        elif page == "enemy":
            lines = self.render_enemy_stats(enemy)
        elif page == "player_inventory":
            lines = self.render_player_inventory(player)
        elif page == "enemy_inventory":
            lines = self.render_enemy_inventory(enemy)
        elif page in ("chest_inventory", "chest"):
            lines = self.render_chest_inventory(chest_items or [])
        elif page == "loot":
            lines = self.render_loot_inventory(loot_items or [], loot_enemy)
        else:
            lines = self.render_player_stats(player)

        # Pad to fixed width
        padded_lines = []
        for line in lines:
            padded_lines.append(line.ljust(self.stats_width - 2))
        
        return padded_lines

    def render_log(self, width):
        """Render the game log with color coding."""
        lines = ["─" * width]
        for msg_data in self.log_messages[-self.max_log_lines:]:
            # Handle both old string format and new dict format for backward compatibility
            if isinstance(msg_data, dict):
                msg = msg_data['text']
                event_type = msg_data.get('event_type', 'default')
            else:
                msg = msg_data
                event_type = 'default'
            
            # Get color for this event type
            color_name = EVENT_TYPES.get(event_type, 'white')
            color_code = ANSI_COLORS.get(color_name, ANSI_COLORS['white'])
            reset_code = ANSI_COLORS['reset']
            
            # Format entity names (underline)
            formatted_msg = self._format_entity_names(msg)
            
            # Apply color to message
            colored_msg = f"{color_code}{formatted_msg}{reset_code}"
            
            # Wrap long messages (account for ANSI codes in length calculation)
            # Strip ANSI codes when calculating display length
            display_msg = msg  # Use original msg for length calculation
            if len(display_msg) > width - 2:
                words = display_msg.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 > width - 2:
                        lines.append(f"{color_code}{current_line}{reset_code}")
                        current_line = word
                    else:
                        current_line += " " + word if current_line else word
                if current_line:
                    lines.append(f"{color_code}{current_line}{reset_code}")
            else:
                lines.append(colored_msg)
        
        return lines[-self.max_log_lines:]

    def render_command_prompt(self):
        """Render the command prompt."""
        return "> "

    def render_full_screen(self, player, enemy, map_obj, page="player", chest_items=None, loot_items=None, loot_enemy="Unknown", game_state=None):
        """Render the complete game screen (for reference, terminal will handle actual rendering)."""
        # Calculate display distances to fill available map area optimally
        # X distance to fill map_width, Y distance to keep map compact
        x_distance = (self.map_width - 1) // 2
        y_distance = 6  # Show about 13 rows (6 above/below + center)
        
        map_display = map_obj.get_visible_map(player, x_distance=x_distance, y_distance=y_distance)
        stats_lines = self.render_stats_window(player, enemy, page, chest_items, loot_items, loot_enemy)
        
        # Build the screen
        screen_lines = []
        
        # Add real-time mode indicator if active
        if game_state and game_state.realtime_mode:
            mode_line = f"{ANSI_COLORS['bright_green']}[ REAL-TIME MODE ]{ANSI_COLORS['reset']}  "
            mode_line += f"HP: {player.hp}/{player.max_hp}  Mana: {player.mana}/{player.max_mana}"
            screen_lines.append(mode_line)
            
            # Add cooldown indicators
            cooldowns = []
            for action, cooldown in game_state.action_cooldowns.items():
                if cooldown > 0:
                    cooldowns.append(f"{action.capitalize()}={cooldown:.1f}s")
                else:
                    cooldowns.append(f"{action.capitalize()}=READY")
            
            cooldown_line = f"{ANSI_COLORS['yellow']}[Cooldowns: {' | '.join(cooldowns)}]{ANSI_COLORS['reset']}"
            screen_lines.append(cooldown_line)
            screen_lines.append("")
        
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
  show loot                  → Display loot from defeated enemies
  show chest                 → Display contents of adjacent chest
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
  use [item]                 → Use/consume one item (potions use 1 from stack)

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
  C          → Chest (closed, stand adjacent and use 'show chest')
  ╬          → Door (closed)
  ─          → Door (open)
  (space)    → Open floor (walkable)


[ITEMS]

  ◆          → Loot bag (from defeated enemies) or equipment
  ▪          → Consumable item (potions, etc.)


[EXPLORATION]

  ?          → Unexplored area (will reveal as you move)


╔═══════════════════════════════════════════════════════════════════════╗
║  Visibility: You can see 3 squares away.                             ║
║  Enemies can see 5 squares away.                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
        """
        return legend_text
    
    def render_defeat_screen(self, combat_stats, message=None):
        """Render the defeat screen with performance summary.
        
        Args:
            combat_stats: Dictionary of combat statistics
            message: Optional message to display (from defeat.msg)
        """
        killing_blow = combat_stats.get('killing_blow')
        if killing_blow:
            killer = killing_blow['attacker']
            damage = killing_blow['damage']
            death_message = f"You were slain by {killer} with a {damage} damage attack!"
        else:
            death_message = "You were defeated!"
        
        # Add custom message if provided
        message_section = ""
        if message:
            message_section = f"\n{ANSI_COLORS['white']}{message}{ANSI_COLORS['reset']}\n"
        
        screen = f"""
{ANSI_COLORS['bright_red']}╔════════════════════════════════════════════════════════════════════╗
║                  GAME OVER - DEFEATED                               ║
╚════════════════════════════════════════════════════════════════════╝{ANSI_COLORS['reset']}

{ANSI_COLORS['red']}{death_message}{ANSI_COLORS['reset']}{message_section}

{ANSI_COLORS['yellow']}Performance Summary:{ANSI_COLORS['reset']}
{ANSI_COLORS['gray']}────────────────────{ANSI_COLORS['reset']}
{ANSI_COLORS['green']}Damage Dealt:{ANSI_COLORS['reset']}      {combat_stats.get('total_damage_dealt', 0)}
{ANSI_COLORS['red']}Damage Taken:{ANSI_COLORS['reset']}      {combat_stats.get('total_damage_taken', 0)}
{ANSI_COLORS['cyan']}Monsters Defeated:{ANSI_COLORS['reset']} {combat_stats.get('monsters_defeated', 0)}
{ANSI_COLORS['blue']}Healing Used:{ANSI_COLORS['reset']}      {combat_stats.get('healing_used', 0)} HP
{ANSI_COLORS['yellow']}Items Collected:{ANSI_COLORS['reset']}  {combat_stats.get('items_collected', 0)}
{ANSI_COLORS['magenta']}Turns Survived:{ANSI_COLORS['reset']}    {combat_stats.get('turns_elapsed', 0)}
{ANSI_COLORS['gray']}Attacks Made:{ANSI_COLORS['reset']}      {combat_stats.get('attacks_made', 0)}
{ANSI_COLORS['gray']}Chests Opened:{ANSI_COLORS['reset']}     {combat_stats.get('chests_opened', 0)}

{ANSI_COLORS['gray']}[Press Enter to restart | ESC/Q to quit]{ANSI_COLORS['reset']}
"""
        return screen
    
    def render_victory_screen(self, combat_stats, message=None):
        """Render the victory screen with performance summary.
        
        Args:
            combat_stats: Dictionary of combat statistics
            message: Optional message to display (from victory.msg)
        """
        last_attack = combat_stats.get('last_attack_dealt')
        if last_attack:
            target = last_attack['target']
            damage = last_attack['damage']
            victory_message = f"You defeated {target} with a devastating {damage} damage blow!"
        else:
            victory_message = "You escaped the Hole!"
        
        # Add custom message if provided
        message_section = ""
        if message:
            message_section = f"\n{ANSI_COLORS['white']}{message}{ANSI_COLORS['reset']}\n"
        
        screen = f"""
{ANSI_COLORS['bright_green']}╔════════════════════════════════════════════════════════════════════╗
║                    VICTORY - ESCAPED!                               ║
╚════════════════════════════════════════════════════════════════════╝{ANSI_COLORS['reset']}

{ANSI_COLORS['green']}{victory_message}{ANSI_COLORS['reset']}{message_section}

{ANSI_COLORS['yellow']}Performance Summary:{ANSI_COLORS['reset']}
{ANSI_COLORS['gray']}────────────────────{ANSI_COLORS['reset']}
{ANSI_COLORS['green']}Damage Dealt:{ANSI_COLORS['reset']}      {combat_stats.get('total_damage_dealt', 0)}
{ANSI_COLORS['red']}Damage Taken:{ANSI_COLORS['reset']}      {combat_stats.get('total_damage_taken', 0)}
{ANSI_COLORS['cyan']}Monsters Defeated:{ANSI_COLORS['reset']} {combat_stats.get('monsters_defeated', 0)}
{ANSI_COLORS['blue']}Healing Used:{ANSI_COLORS['reset']}      {combat_stats.get('healing_used', 0)} HP
{ANSI_COLORS['yellow']}Items Collected:{ANSI_COLORS['reset']}  {combat_stats.get('items_collected', 0)}
{ANSI_COLORS['magenta']}Total Turns:{ANSI_COLORS['reset']}       {combat_stats.get('turns_elapsed', 0)}
{ANSI_COLORS['gray']}Attacks Made:{ANSI_COLORS['reset']}      {combat_stats.get('attacks_made', 0)}
{ANSI_COLORS['gray']}Chests Opened:{ANSI_COLORS['reset']}     {combat_stats.get('chests_opened', 0)}

{ANSI_COLORS['gray']}[Press Enter to restart | ESC/Q to quit]{ANSI_COLORS['reset']}
"""
        return screen
