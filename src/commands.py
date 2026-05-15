"""Command parser for Hole Wizards game."""

import re


class CommandParser:
    """Parses and validates player commands."""

    # Command patterns
    COMMANDS = {
        "show_player_stats": r"^show\s+player\s+stats$",
        "show_enemy_stats": r"^show\s+enemy\s+stats$",
        "show_player_inventory": r"^show\s+player\s+inventory$",
        "show_loot": r"^show\s+loot$",
        "show_chest": r"^show\s+chest$",
        "list_commands": r"^list\s+commands$|^help$",
        "legend": r"^legend$",
        "quit": r"^quit$",
        "restart": r"^restart$",
        "take": r"^take\s+['\"]?(.+?)['\"]?$",
        "drop": r"^drop\s+['\"]?(.+?)['\"]?$",
        "equip": r"^equip\s+['\"]?(.+?)['\"]?$",
        "use": r"^use\s+['\"]?(.+?)['\"]?$",
        # Attack patterns: must handle "attack", "attack name", "a", "aname"
        "attack": r"^attack(?:\s+(.+?))?$|^a(.*)$",
        "defend": r"^defend$",
        # Movement patterns: shortcuts first for priority matching
        "move_up": r"^mu$|^move\s+up$",
        "move_down": r"^md$|^move\s+down$",
        "move_left": r"^ml$|^move\s+left$",
        "move_right": r"^mr$|^move\s+right$",
        "move": r"^m(\d+)[,\s]+(\d+)$|^move\s+(\d+)[,\s]+(\d+)$",
    }

    @staticmethod
    def parse(command_string):
        """Parse a command string and return (command_type, args)."""
        command_string = command_string.strip().lower()
        
        for cmd_type, pattern in CommandParser.COMMANDS.items():
            match = re.match(pattern, command_string)
            if match:
                if match.groups():
                    if cmd_type == "move" and len(match.groups()) >= 2:
                        # Handle both m6,9 and move 6,9 patterns
                        x = int(match.group(1) or match.group(3))
                        y = int(match.group(2) or match.group(4))
                        return (cmd_type, (x, y))
                    elif cmd_type == "attack":
                        # Attack can be "attack", "attack name", "a", or "aname"
                        # Group 1 is from "attack ..." pattern (optional, can be None)
                        # Group 2 is from "a..." pattern (required in that branch)
                        target = match.group(1) or match.group(2)
                        if target:
                            return (cmd_type, target.strip())
                        else:
                            return (cmd_type, None)  # No target specified
                    else:
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
  legend                 - Show map legend
  quit                   - Quit the game
  restart                - Restart the game

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
