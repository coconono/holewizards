"""Tab completion system for Hole Wizards game."""

import readline
from commands import CommandParser


class TabCompletion:
    """Handles tab completion for game commands and arguments."""

    def __init__(self, game_state=None, use_readline=True):
        """Initialize tab completion system.
        
        Args:
            game_state: The GameState object for context-aware completions
            use_readline: Whether to use readline integration. False for graphics mode.
        """
        self.game_state = game_state
        self.completion_matches = []
        self.completion_index = 0
        self.last_partial = ""
        self.completion_query = ""  # The query that generated current completion_matches
        self.use_readline = use_readline
        
        # Configure readline only if requested (graphics mode uses different completion)
        if use_readline:
            readline.set_completer(self.complete)
            # Allow tab completion
            readline.parse_and_bind("tab: complete")

    def set_game_state(self, game_state):
        """Update the game state reference (for dynamic context)."""
        self.game_state = game_state

    def complete(self, text, state):
        """Readline completer function.
        
        This is called by readline. Returns one match per call.
        Args:
            text: The text being completed
            state: The match number (0 for first match, 1 for second, etc.)
        
        Returns:
            A completion string or None when matches are exhausted
        """
        if state == 0:
            # First time - get all matches
            self.completion_matches = self.get_completions(text)
            self.completion_index = 0
        
        # Return the next match if available
        if self.completion_index < len(self.completion_matches):
            result = self.completion_matches[self.completion_index]
            self.completion_index += 1
            return result
        else:
            return None

    def get_completions(self, partial_input):
        """Get all possible completions for partial input.
        
        Args:
            partial_input: The partial command or argument the user typed
        
        Returns:
            A list of matching completion strings
        """
        if not partial_input:
            return []
        
        # First, try to match commands (including multi-word commands)
        all_commands = self._get_all_commands()
        # Add dynamic commands for nearby loot bags
        dynamic_commands = self._get_dynamic_loot_commands()
        all_commands.extend(dynamic_commands)
        
        partial_lower = partial_input.lower()
        
        # Check if input matches any command prefix
        command_matches = []
        for cmd in all_commands:
            if cmd.lower().startswith(partial_lower):
                command_matches.append(cmd + " ")
        
        # If we have command matches, return them
        if command_matches:
            return sorted(command_matches)
        
        # No command matches - check if we're completing arguments
        # Find the longest matching command in the input
        matched_command = None
        for cmd in sorted(all_commands, key=len, reverse=True):
            if partial_input.lower().startswith(cmd.lower() + " "):
                matched_command = cmd
                break
        
        # If we found a complete command, complete its arguments
        if matched_command:
            # Extract the argument part
            arg_start = len(matched_command) + 1  # +1 for the space
            arg_part = partial_input[arg_start:]
            arg_completions = self._complete_argument(matched_command, arg_part.split(), partial_input)
            
            # Prepend the command to each argument completion
            full_completions = [matched_command + " " + arg for arg in arg_completions]
            return full_completions
        
        return []

    def _complete_command(self, partial_command):
        """Complete a partial command name.
        
        Args:
            partial_command: The partial command text
        
        Returns:
            List of matching commands (full command + space for continuation)
        """
        matches = []
        partial_lower = partial_command.lower()
        
        # Get all command names
        all_commands = self._get_all_commands()
        
        for cmd in all_commands:
            if cmd.lower().startswith(partial_lower):
                matches.append(cmd + " ")
        
        return sorted(matches)

    def _complete_argument(self, command_name, tokens, full_input):
        """Complete arguments based on the command context.
        
        Args:
            command_name: The command being used
            tokens: Tokens after the command
            full_input: The full input string so far
        
        Returns:
            List of matching argument completions
        """
        # Determine which argument we're completing
        partial_arg = tokens[-1].lower() if tokens else ""
        
        # Special handling for "show" command with item stats
        if command_name == "show":
            return self._complete_show_command(tokens, full_input)
        
        # Get argument completions based on command
        if command_name in ("take",):
            return self._complete_item_from_ground(partial_arg)
        elif command_name in ("drop", "equip", "use"):
            return self._complete_inventory_item(command_name, partial_arg)
        elif command_name in ("attack", "a", "suplex", "s"):
            return self._complete_target(partial_arg)
        
        return []

    def _complete_show_command(self, tokens, full_input):
        """Complete 'show' command arguments (including 'show [item] stats').
        
        Args:
            tokens: Tokens after 'show'
            full_input: The full input string
        
        Returns:
            List of matching completions
        """
        if not tokens:
            # Just "show " - suggest all show subcommands
            return ["player", "enemy", "loot", "chest"]
        
        # Check if completing "show X stats" pattern
        if len(tokens) >= 2 and tokens[-1].lower() == "stats":
            # Already have "stats", nothing more to complete
            return []
        
        # Check if last token could be an item name or part of one
        # Reconstruct the potential item name from tokens (excluding "stats" if present)
        if tokens[-1].lower() == "stats":
            item_tokens = tokens[:-1]
        else:
            item_tokens = tokens
        
        # Join tokens to form potential item name (handle multi-word items)
        potential_item = " ".join(item_tokens).strip().strip('"')
        
        # Try to match against inventory items
        if not self.game_state:
            return []
        
        matches = []
        partial_lower = potential_item.lower()
        
        # Get all inventory items
        for item in self.game_state.player.inventory:
            item_name = item.name
            item_name_lower = item_name.lower()
            
            if item_name_lower.startswith(partial_lower):
                # If item name has spaces, quote it
                if " " in item_name:
                    item_display = f'"{item_name}" stats'
                else:
                    item_display = f'{item_name} stats'
                matches.append(item_display)
            elif partial_lower in item_name_lower:
                # Partial match in the middle - still suggest it
                if " " in item_name:
                    item_display = f'"{item_name}" stats'
                else:
                    item_display = f'{item_name} stats'
                matches.append(item_display)
        
        # Also suggest standard show commands if they match
        standard_options = ["player stats", "enemy stats", "player inventory", "loot", "chest"]
        for option in standard_options:
            if option.lower().startswith(partial_lower):
                matches.append(option)
        
        return sorted(set(matches))

    def _get_all_commands(self):
        """Get all available commands from CommandParser.
        
        Returns:
            List of command strings (e.g., ["show player stats", "move up", ...])
        """
        commands = [
            "show",  # Base command for dynamic completion
            "show player stats",
            "show enemy stats",
            "show player inventory",
            "show loot",
            "show chest",
            "list commands",
            "help",
            "legend",
            "quit",
            "restart",
            "realtime",
            "move up",
            "move down",
            "move left",
            "move right",
            "defend",
            "take",
            "drop",
            "equip",
            "use",
            "attack",
            "suplex",
        ]
        return commands

    def _get_dynamic_loot_commands(self):
        """Get dynamic commands for nearby loot bags.
        
        Returns:
            List of dynamic command strings like "show Alice loot"
        """
        if not self.game_state:
            return []
        
        commands = []
        
        # Get loot bags nearby (current position and adjacent)
        px = self.game_state.player.position["x"]
        py = self.game_state.player.position["y"]
        
        loot_owners = set()
        
        # Check current position
        for item in self.game_state.map.get_items_at(px, py):
            if item.item_type == "bag" and hasattr(item, 'enemy_name'):
                loot_owners.add(item.enemy_name)
        
        # Check adjacent tiles
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = px + dx, py + dy
                for item in self.game_state.map.get_items_at(nx, ny):
                    if item.item_type == "bag" and hasattr(item, 'enemy_name'):
                        loot_owners.add(item.enemy_name)
        
        # Generate "show [owner] loot" commands
        for owner in loot_owners:
            commands.append(f"show {owner} loot")
        
        return commands

    def _complete_item_from_ground(self, partial_item):
        """Complete item names from ground/loot context.
        
        Args:
            partial_item: Partial item name
        
        Returns:
            List of matching item names
        """
        if not self.game_state:
            return []
        
        items = []
        
        # Get items from ground at player position
        player_pos = (self.game_state.player.position["x"], self.game_state.player.position["y"])
        
        # Add loot items if viewing loot
        if self.game_state.current_stats_page == "loot":
            items.extend(self.game_state.loot_items)
        
        # Add chest items if viewing chest
        if self.game_state.current_stats_page == "chest":
            items.extend(self.game_state.chest_items)
        
        # Get matching items
        matches = []
        partial_lower = partial_item.lower()
        
        for item in items:
            item_name = str(item.name).lower() if hasattr(item, 'name') else str(item).lower()
            if item_name.startswith(partial_lower):
                # Quote item names with spaces
                item_display = f'"{item.name}"' if " " in item.name else item.name
                if item_display not in matches:
                    matches.append(item_display)
        
        return sorted(set(matches))

    def _complete_inventory_item(self, command_name, partial_item):
        """Complete item names from player inventory.
        
        Args:
            command_name: The command being used (drop, equip, use)
            partial_item: Partial item name
        
        Returns:
            List of matching item names
        """
        if not self.game_state:
            return []
        
        items = self.game_state.player.inventory
        matches = []
        partial_lower = partial_item.lower()
        
        # Filter by command type if needed
        if command_name == "equip":
            # Only show equippable items (weapons, armor, spells)
            items = [i for i in items if i.item_type in ("weapon", "armor", "spell")]
        elif command_name == "use":
            # Only show consumable items
            items = [i for i in items if i.item_type == "consumable"]
        
        # Get matching items
        for item in items:
            item_name = str(item.name).lower() if hasattr(item, 'name') else str(item).lower()
            if item_name.startswith(partial_lower):
                # Quote item names with spaces
                item_display = f'"{item.name}"' if " " in item.name else item.name
                if item_display not in matches:
                    matches.append(item_display)
        
        return sorted(set(matches))

    def _complete_target(self, partial_target):
        """Complete target names (for attack command).
        
        Args:
            partial_target: Partial target name
        
        Returns:
            List of matching target names
        """
        if not self.game_state:
            return []
        
        matches = []
        partial_lower = partial_target.lower()
        
        # Get adjacent enemies
        for enemy in self.game_state.enemies:
            if enemy.alive:
                # Check if adjacent
                enemy_pos = (enemy.position["x"], enemy.position["y"])
                player_pos = (self.game_state.player.position["x"], self.game_state.player.position["y"])
                
                dx = abs(enemy_pos[0] - player_pos[0])
                dy = abs(enemy_pos[1] - player_pos[1])
                
                if dx <= 1 and dy <= 1 and (dx > 0 or dy > 0):
                    enemy_name = enemy.name.lower()
                    if enemy_name.startswith(partial_lower):
                        if enemy.name not in matches:
                            matches.append(enemy.name)
        
        return sorted(set(matches))

    def enable(self):
        """Enable tab completion in readline."""
        if self.use_readline:
            readline.set_completer(self.complete)

    def disable(self):
        """Disable tab completion in readline."""
        if self.use_readline:
            readline.set_completer(None)

    def complete_input(self, current_input):
        """Complete input for graphics mode (non-readline).
        
        This method is used by graphics mode to get the next completion
        when TAB is pressed.
        
        Args:
            current_input: The current command input string
        
        Returns:
            Tuple (completed_input, is_cycling) where:
            - completed_input: The completed command/argument
            - is_cycling: True if there are more matches to cycle through
        """
        # Check if we're cycling through previous matches
        # But if the current input ends with a space and matches a completion,
        # we might be transitioning to argument completion, so get new completions
        is_from_previous_cycle = (self.completion_matches and 
                                  current_input in self.completion_matches and
                                  current_input != self.completion_query)
        
        # If the previous match ended with a space, try getting new completions
        # (might be transitioning from command to arguments)
        if is_from_previous_cycle and current_input.endswith(" "):
            new_completions = self.get_completions(current_input)
            # If we get different completions, use them (not cycling, new context)
            if new_completions and new_completions != self.completion_matches:
                self.completion_query = current_input
                self.completion_matches = new_completions
                self.completion_index = 0
                is_from_previous_cycle = False
        
        # If not cycling or no matches, get new completions
        if not is_from_previous_cycle:
            if current_input != self.completion_query:  # Avoid redundant call
                self.completion_query = current_input
                self.completion_matches = self.get_completions(current_input)
                self.completion_index = 0
        
        # Return next match if available
        if self.completion_matches:
            match = self.completion_matches[self.completion_index]
            self.completion_index = (self.completion_index + 1) % len(self.completion_matches)
            return (match, len(self.completion_matches) > 1)
        else:
            # No matches - return input unchanged
            return (current_input, False)

    def reset_completion_cycle(self):
        """Reset completion cycling for next session."""
        self.completion_index = 0
        self.completion_matches = []
        self.last_partial = ""
        self.completion_query = ""
