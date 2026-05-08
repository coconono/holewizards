"""Command parser for Hole Wizards game."""

import re


class CommandParser:
    """Parses and validates player commands."""

    # Command patterns
    COMMANDS = {
        "show_player_stats": r"^show\s+player\s+stats$",
        "show_enemy_stats": r"^show\s+enemy\s+stats$",
        "show_player_inventory": r"^show\s+player\s+inventory$",
        "show_enemy_inventory": r"^show\s+enemy\s+inventory$",
        "show_chest_inventory": r"^show\s+chest\s+inventory$",
        "list_commands": r"^list\s+commands$|^help$",
        "take": r"^take\s+['\"]?(.+?)['\"]?$",
        "drop": r"^drop\s+['\"]?(.+?)['\"]?$",
        "equip": r"^equip\s+['\"]?(.+?)['\"]?$",
        "use": r"^use\s+['\"]?(.+?)['\"]?$",
        "attack": r"^attack$",
        "defend": r"^defend$",
        "move_up": r"^move\s+up$",
        "move_down": r"^move\s+down$",
        "move_left": r"^move\s+left$",
        "move_right": r"^move\s+right$",
    }

    @staticmethod
    def parse(command_string):
        """Parse a command string and return (command_type, args)."""
        command_string = command_string.strip().lower()
        
        for cmd_type, pattern in CommandParser.COMMANDS.items():
            match = re.match(pattern, command_string)
            if match:
                if match.groups():
                    return (cmd_type, match.group(1).strip())
                else:
                    return (cmd_type, None)
        
        return (None, None)

    @staticmethod
    def is_valid_command(command_string):
        """Check if a command is valid."""
        cmd_type, _ = CommandParser.parse(command_string)
        return cmd_type is not None

    @staticmethod
    def get_command_help():
        """Get help text for commands."""
        return """
Available Commands:

STATS & INFO:
  show player stats      - Show your stats
  show enemy stats       - Show enemy stats
  show player inventory  - Show your items
  show enemy inventory   - Show enemy's items (if dead)
  show chest inventory   - Show chest contents
  list commands / help   - Show this help

MOVEMENT:
  move up    - Move up
  move down  - Move down
  move left  - Move left
  move right - Move right

COMBAT:
  attack     - Attack the enemy
  defend     - Prepare to defend

ITEMS:
  take [item]    - Pick up an item
  drop [item]    - Drop an item
  equip [item]   - Equip an item
  use [item]     - Use/consume an item
        """
