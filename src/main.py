#!/usr/bin/env python3
"""Main game loop for Hole Wizards."""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from ui import UI
from commands import CommandParser
from tab_completion import TabCompletion

# Try to import pygame for graphical UI
try:
    from graphics import GraphicalUI
    import pygame
    GRAPHICS_AVAILABLE = True
except ImportError:
    GRAPHICS_AVAILABLE = False
    pygame = None


class Game:
    """Main game controller."""

    # Direction constants for movement
    DIRECTIONS = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    def __init__(self):
        """Initialize the game in graphics mode."""
        self.state = GameState()
        self.running = True
        self.quit_game = False
        
        # Initialize tab completion for graphics mode (no readline needed)
        self.tab_completion = TabCompletion(self.state, use_readline=False)
        
        # Initialize graphics UI
        if not GRAPHICS_AVAILABLE:
            raise RuntimeError("Pygame is required to run Hole Wizards. Install it with: pip install pygame")
        
        try:
            self.ui = GraphicalUI(width=1400, height=900, tab_completion=self.tab_completion)
            print("✓ Graphics mode initialized (fallback rendering available)")
        except Exception as e:
            raise RuntimeError(f"Graphics initialization failed: {e}")
        
        # Set UI reference on game state for enemy actions
        self.state.ui = self.ui

    def render(self):
        """Render the current game state."""
        # Update entity names for log formatting
        enemy_names = [enemy.name for enemy in self.state.enemies if enemy.alive]
        player_name = "You"  # Player is referred to as "You" in messages
        
        # Graphical rendering
        self.ui.set_entity_names(player_name, enemy_names)
        enemy_to_display = self.state.current_enemy if self.state.current_stats_page == "enemy" else self.state.get_current_enemy()
        # Calculate view distances based on sprite size (64x72 pixels with 72px spacing)
        # Map area is 800x400, so we can fit ~11 tiles wide x ~5.5 tiles tall
        # Use half of that to center the player (with some padding)
        map_display = self.state.map.get_visible_map(self.state.player, x_distance=5, y_distance=2)
        self.ui.render(self.state.player, enemy_to_display, map_display, self.state.current_stats_page,
                      self.state.chest_items, self.state.loot_items, self.state.current_loot_enemy or "Unknown")
        self.ui.tick()

    def process_command(self, command_string):
        """Process a player command."""
        cmd_type, args = CommandParser.parse(command_string)
        
        if cmd_type is None:
            self.ui.add_log_message("Unknown command. Type 'help' for commands.", "system")
            return

        # Stats commands
        if cmd_type == "show_player_stats":
            self.state.current_stats_page = "player"
            self.state.current_enemy = None
            self.ui.add_log_message("Showing player stats", "system")

        elif cmd_type == "show_enemy_stats":
            enemy = self.state.get_adjacent_enemy()
            if enemy:
                self.state.current_enemy = enemy
                self.state.current_stats_page = "enemy"
                self.ui.add_log_message(f"Showing {enemy.name}'s stats", "system")
            else:
                self.ui.add_log_message("No enemy nearby", "system")

        elif cmd_type == "show_player_inventory":
            self.state.current_stats_page = "player_inventory"
            self.state.current_enemy = None
            self.ui.add_log_message(f"Showing inventory ({len(self.state.player.inventory)} items)", "system")

        elif cmd_type == "show_item_stats":
            item = self.state.player.find_item_in_inventory(args)
            if item:
                stats_display = item.get_stats_display()
                self.ui.add_log_message(stats_display, "system")
            else:
                self.ui.add_log_message(f"Item '{args}' not in inventory", "system")

        elif cmd_type == "show_loot_named":
            success, message = self.state.show_loot(owner_name=args)
            self.ui.add_log_message(message, "loot")

        elif cmd_type == "show_loot":
            success, message = self.state.show_loot()
            self.ui.add_log_message(message, "loot")

        elif cmd_type == "show_chest":
            success, message = self.state.show_chest()
            self.ui.add_log_message(message, "loot")

        elif cmd_type == "list_commands":
            self.show_help()

        elif cmd_type == "legend":
            self.show_legend()

        elif cmd_type == "quit":
            self.ui.add_log_message("Thanks for playing Hole Wizards!", "system")
            self.quit_game = True
            self.running = False
            return

        elif cmd_type == "restart":
            self.ui.add_log_message("Restarting game...", "system")
            self.state = GameState()
            self.state.ui = self.ui
            self.ui = UI()
            self.running = False
            return
        
        elif cmd_type == "realtime":
            new_mode = self.state.toggle_realtime_mode()
            if new_mode:
                self.ui.add_log_message("Entering REAL-TIME MODE!", "status")
                self.ui.add_log_message("Use WASD to move, Shift to suplex, Z to defend, Space to interact, R to exit", "status")
            else:
                self.ui.add_log_message("Returning to turn-based mode", "status")

        # Movement commands
        elif cmd_type in ("move_up", "move_down", "move_left", "move_right"):
            direction_map = {
                "move_up": "up",
                "move_down": "down",
                "move_left": "left",
                "move_right": "right",
            }
            self._handle_directional_move(direction_map[cmd_type])

        elif cmd_type == "move":
            self._handle_targeted_move(args)

        # Combat commands
        elif cmd_type == "attack":
            if not args:
                # No target specified, show list of available targets
                available_targets = self._get_adjacent_enemy_names()
                if available_targets:
                    self.ui.add_log_message(f"Available targets: {', '.join(available_targets)}", "system")
                    self.ui.add_log_message("Use: attack <name> or a<name>", "system")
                else:
                    self.ui.add_log_message("No enemies in range", "system")
            else:
                # Attack specified target
                success, message = self.state.player_attack_target(args)
                # Determine event type based on success (victory if enemy defeated, combat_dealt otherwise)
                event_type = "victory" if success and "Defeated" in message else "combat_dealt"
                self.ui.add_log_message(message, event_type)
                
                if success:
                    # Monster turns after player attack
                    self._resolve_monster_turns()

        elif cmd_type == "suplex":
            if not args:
                # No target specified, show list of available targets
                available_targets = self._get_adjacent_enemy_names()
                if available_targets:
                    self.ui.add_log_message(f"Available targets: {', '.join(available_targets)}", "system")
                    self.ui.add_log_message("Use: suplex <name> or s <name>", "system")
                else:
                    self.ui.add_log_message("No enemies in range", "system")
            else:
                # Suplex specified target
                success, message = self.state.player_suplex_target(args)
                # Suplex with repositioning is a status effect, defeats are victory
                event_type = "victory" if success and "defeats" in message else ("status" if "repositioned" in message else "combat_dealt")
                self.ui.add_log_message(message, event_type)
                
                if success:
                    # Monster turns after player suplex
                    self._resolve_monster_turns()

        elif cmd_type == "defend":
            success, message = self.state.player_defend()
            self.ui.add_log_message(message, "status")
            # Monsters take turns after player defends
            self._resolve_monster_turns()

        # Item commands
        elif cmd_type == "take":
            self._handle_take_item(args)

        elif cmd_type == "drop":
            if args:
                success, message = self.state.player_drop_item(args)
                self.ui.add_log_message(message, "loot")
            else:
                self.ui.add_log_message("Drop what?", "system")

        elif cmd_type == "equip":
            if args:
                success, message = self.state.player_equip_item(args)
                self.ui.add_log_message(message, "loot")
            else:
                self.ui.add_log_message("Equip what?", "system")

        elif cmd_type == "use":
            if args:
                success, message = self.state.player_use_item(args)
                # Use items can be healing (potions) or other
                event_type = "healing" if "HP" in message or "Mana" in message or "Restored" in message else "loot"
                self.ui.add_log_message(message, event_type)
            else:
                self.ui.add_log_message("Use what?", "system")

    def _handle_directional_move(self, direction):
        """Handle movement in a cardinal direction."""
        dx, dy = self.DIRECTIONS[direction]
        
        if self.state.player_move(dx, dy):
            # Reset stats page to player view when moving away from loot/chests
            if self.state.current_stats_page in ["loot", "chest"]:
                self.state.current_stats_page = "player"
            
            self.ui.add_log_message(f"Moved {direction}", "movement")
            enemy = self.state.get_adjacent_enemy()
            if enemy and enemy.alive:
                self.ui.add_log_message(f"You spot {enemy.name} nearby!", "movement")
            # Monsters take their turns after player move
            self._resolve_monster_turns()
        else:
            self.ui.add_log_message(f"Cannot move {direction} - blocked", "movement")

    def _handle_targeted_move(self, args):
        """Handle movement to a specific coordinate with step-by-step resolution."""
        import time
        
        if not args or not isinstance(args, tuple) or len(args) != 2:
            self.ui.add_log_message("Invalid coordinates. Use: move x,y or m x,y", "system")
            return
        
        target_x, target_y = args
        
        # Keep moving until destination, blocked, or enemy encountered
        while True:
            current_x = self.state.player.position["x"]
            current_y = self.state.player.position["y"]
            
            # Check if reached destination
            if current_x == target_x and current_y == target_y:
                self.ui.add_log_message(f"Reached destination ({target_x}, {target_y})", "movement")
                self.render()  # Final render at destination
                break
            
            # Calculate next step
            dx = 0 if current_x == target_x else (1 if target_x > current_x else -1)
            dy = 0 if current_y == target_y else (1 if target_y > current_y else -1)
            
            # Try to move
            if self.state.player_move(dx, dy):
                # Reset stats page to player view when moving away from loot/chests
                if self.state.current_stats_page in ["loot", "chest"]:
                    self.state.current_stats_page = "player"
                
                # Allow monsters to move (turn-based)
                self._resolve_monster_turns()
                
                # Render after player and monsters move
                self.render()
                
                # Pause before next step
                time.sleep(0.5)
                
                # Check for adjacent enemy encounter
                enemy = self.state.get_adjacent_enemy()
                if enemy and enemy.alive:
                    self.ui.add_log_message(f"You spot {enemy.name} nearby! Movement interrupted.", "movement")
                    self.render()
                    break
            else:
                self.ui.add_log_message("Path blocked - stopped moving", "movement")
                self.render()
                break

    def _handle_take_item(self, args):
        """Handle taking an item based on current view."""
        if not args:
            self.ui.add_log_message("Take what?", "system")
            return
        
        if self.state.current_stats_page == "loot":
            success, message = self.state.take_loot_item(args)
        elif self.state.current_stats_page == "chest":
            success, message = self.state.take_chest_item(args)
        else:
            success, message = self.state.player_take_item(args)
        
        self.ui.add_log_message(message, "loot")

    def _get_adjacent_enemy_names(self):
        """Get a list of adjacent enemy names."""
        adjacent_enemies = []
        for enemy in self.state.enemies:
            if enemy.alive and self.state._is_adjacent(self.state.player, enemy):
                adjacent_enemies.append(enemy.name)
        return adjacent_enemies

    def _resolve_monster_turns(self):
        """Have all monsters take their turns."""
        for enemy in self.state.enemies:
            if not enemy.alive:
                continue
            
            # Let enemy AI choose and execute action
            self.state.enemy_take_turn(enemy)
        
        # Track turns elapsed
        self.state.combat_stats['turns_elapsed'] += 1

    def _get_message_file(self, filename):
        """Get path to a message file in data/messages/."""
        # Try multiple possible locations
        possible_paths = [
            Path(__file__).parent / "data" / "messages" / filename,
            Path(__file__).parent.parent / "data" / "messages" / filename,
            Path.cwd() / "data" / "messages" / filename,
        ]
        for path in possible_paths:
            if path.exists():
                return str(path)
        return None

    def show_intro(self):
        """Show the game intro."""
        self.ui.render_intro_screen()

    def show_help(self):
        """Display the help screen."""
        help_text = UI().render_help()
        self.ui.full_screen_text = help_text
        self.ui.showing_full_screen = "help"

    def show_legend(self):
        """Display the legend screen."""
        legend_text = UI().render_legend()
        self.ui.full_screen_text = legend_text
        self.ui.showing_full_screen = "legend"

    def show_game_over(self, result):
        """Show game over screen with performance statistics."""
        # Load the appropriate message file
        message = None
        message_file = "victory.msg" if result == "victory" else "defeat.msg"
        message_path = self._get_message_file(message_file)
        if message_path:
            try:
                with open(message_path, 'r') as f:
                    message = f.read().strip()
            except:
                pass
        
        # Graphics mode - render defeat/victory screen with stats
        if result == "victory":
            self.ui.render_victory_screen(self.state.combat_stats, message)
        else:
            self.ui.render_defeat_screen(self.state.combat_stats, message)
        
        # Wait for user input: Enter/Space to restart, ESC/Q to quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        waiting = False
                        return "quit"
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        waiting = False
                        return "restart"
            self.ui.clock.tick(30)
        
        return "restart"
    
    def _run_realtime_frame(self):
        """Run a single frame of real-time mode."""
        import time
        
        # Initialize time tracking
        if not hasattr(self, 'last_realtime_update'):
            self.last_realtime_update = time.time()
        
        # Calculate delta time
        current_time = time.time()
        delta_time = current_time - self.last_realtime_update
        self.last_realtime_update = current_time
        
        # Update cooldowns
        self.state.update_cooldowns(delta_time)
        self.state.update_entity_timers(delta_time)
        
        # Graphics mode: use pygame key states for held keys
        import pygame
        
        # Process pygame events for quit and action keys
        action_keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                # Map action keys (non-movement)
                if event.key == pygame.K_z:
                    action_keys.append('z')
                elif event.key == pygame.K_r:
                    action_keys.append('r')
                elif event.key == pygame.K_SPACE:
                    action_keys.append(' ')
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    action_keys.append('S')
        
        # Check held keys for movement (supports diagonal)
        pressed = pygame.key.get_pressed()
        dx, dy = 0, 0
        if pressed[pygame.K_w]:
            dy -= 1
        if pressed[pygame.K_s]:
            dy += 1
        if pressed[pygame.K_a]:
            dx -= 1
        if pressed[pygame.K_d]:
            dx += 1
        
        # Process movement if any direction pressed
        if (dx != 0 or dy != 0) and self.state.can_perform_action("move"):
            if self.state.player_move(dx, dy):
                # Reset stats page to player view when moving away from loot/chests
                if self.state.current_stats_page in ["loot", "chest"]:
                    self.state.current_stats_page = "player"
                
                # Build direction name for log
                direction_parts = []
                if dy < 0:
                    direction_parts.append("north")
                elif dy > 0:
                    direction_parts.append("south")
                if dx < 0:
                    direction_parts.append("west")
                elif dx > 0:
                    direction_parts.append("east")
                
                direction_name = "-".join(direction_parts)
                self.ui.add_log_message(f"Moved {direction_name}", "movement")
                self.state.set_cooldown("move", 0.2)
                
                # Check for adjacent enemies
                enemy = self.state.get_adjacent_enemy()
                if enemy and enemy.alive:
                    self.ui.add_log_message(f"You spot {enemy.name} nearby!", "movement")
            else:
                self.ui.add_log_message("Cannot move - blocked", "movement")
        
        # Process action keys
        for key in action_keys:
            self._handle_realtime_action_key(key)
        
        # Process enemy actions in real-time
        for enemy in self.state.enemies:
            if enemy.alive and enemy.action_timer <= 0:
                self.state.enemy_take_turn(enemy)
                enemy.action_timer = enemy.action_interval
        
        # Render
        self.render()
        
        # Frame rate limiting (~30 FPS) using pygame clock
        self.ui.clock.tick(30)
    
    def _handle_realtime_key(self, key):
        """Handle a single keypress in real-time mode."""
        # Movement keys (WASD)
        if key in ['w', 'a', 's', 'd'] and self.state.can_perform_action("move"):
            direction_map = {
                'w': (0, -1),  # Up
                's': (0, 1),   # Down
                'a': (-1, 0),  # Left
                'd': (1, 0),   # Right
            }
            dx, dy = direction_map[key]
            
            if self.state.player_move(dx, dy):
                # Reset stats page to player view when moving away from loot/chests
                if self.state.current_stats_page in ["loot", "chest"]:
                    self.state.current_stats_page = "player"
                
                direction_names = {'w': 'north', 's': 'south', 'a': 'west', 'd': 'east'}
                self.ui.add_log_message(f"Moved {direction_names[key]}", "movement")
                self.state.set_cooldown("move", 0.2)
                
                # Check for adjacent enemies
                enemy = self.state.get_adjacent_enemy()
                if enemy and enemy.alive:
                    self.ui.add_log_message(f"You spot {enemy.name} nearby!", "movement")
            else:
                self.ui.add_log_message("Cannot move - blocked", "movement")
        
        # Suplex (Shift key - will show as different character)
        elif key in ['S'] and self.state.can_perform_action("suplex"):  # Capital S for shift+s
            # Get adjacent enemy
            enemy = self.state.get_adjacent_enemy()
            if enemy:
                success, message = self.state.player_suplex_target(enemy.name)
                event_type = "victory" if success and "defeats" in message else ("status" if "repositioned" in message else "combat_dealt")
                self.ui.add_log_message(message, event_type)
                self.state.set_cooldown("suplex", 1.0)
            else:
                self.ui.add_log_message("No enemy to suplex", "system")
        
        # Defend (Z key)
        elif key == 'z' and self.state.can_perform_action("defend"):
            success, message = self.state.player_defend()
            self.ui.add_log_message(message, "status")
            self.state.set_cooldown("defend", 0.5)
        
        # Interact (Space key)
        elif key == ' ' and self.state.can_perform_action("interact"):
            # Check for adjacent chest
            px, py = self.state.player.position["x"], self.state.player.position["y"]
            chest_found = False
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                check_x, check_y = px + dx, py + dy
                if self.state.map.is_valid_position(check_x, check_y):
                    tile = self.state.map.get_tile(check_x, check_y)
                    if tile and tile.tile_type == "chest":
                        # Open chest and exit real-time mode
                        success, message = self.state.show_chest()
                        self.ui.add_log_message(message, "loot")
                        if success:
                            self.state.toggle_realtime_mode()
                            self.ui.add_log_message("Chest opened - returning to turn-based mode", "status")
                        chest_found = True
                        break
            
            if not chest_found:
                self.ui.add_log_message("Nothing to interact with", "system")
            
            self.state.set_cooldown("interact", 0.3)
        
        # Toggle back to turn-based mode (R key)
        elif key == 'r':
            self.state.toggle_realtime_mode()
            self.ui.add_log_message("Returning to turn-based mode", "status")
    
    def _handle_realtime_action_key(self, key):
        """Handle action keys in real-time mode (non-movement).
        
        This is used in graphics mode where movement is handled separately via key states.
        
        Args:
            key: Action key character ('z', 'r', ' ', 'S')
        """
        # Suplex (Shift key)
        if key == 'S' and self.state.can_perform_action("suplex"):
            # Get adjacent enemy
            enemy = self.state.get_adjacent_enemy()
            if enemy:
                success, message = self.state.player_suplex_target(enemy.name)
                event_type = "victory" if success and "defeats" in message else ("status" if "repositioned" in message else "combat_dealt")
                self.ui.add_log_message(message, event_type)
                self.state.set_cooldown("suplex", 1.0)
            else:
                self.ui.add_log_message("No enemy to suplex", "system")
        
        # Defend (Z key)
        elif key == 'z' and self.state.can_perform_action("defend"):
            success, message = self.state.player_defend()
            self.ui.add_log_message(message, "status")
            self.state.set_cooldown("defend", 0.5)
        
        # Interact (Space key)
        elif key == ' ' and self.state.can_perform_action("interact"):
            # Check for adjacent chest
            px, py = self.state.player.position["x"], self.state.player.position["y"]
            chest_found = False
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                check_x, check_y = px + dx, py + dy
                if self.state.map.is_valid_position(check_x, check_y):
                    tile = self.state.map.get_tile(check_x, check_y)
                    if tile and tile.tile_type == "chest":
                        # Open chest and exit real-time mode
                        success, message = self.state.show_chest()
                        self.ui.add_log_message(message, "loot")
                        if success:
                            self.state.toggle_realtime_mode()
                            self.ui.add_log_message("Chest opened - returning to turn-based mode", "status")
                        chest_found = True
                        break
            
            if not chest_found:
                self.ui.add_log_message("Nothing to interact with", "system")
            
            self.state.set_cooldown("interact", 0.3)
        
        # Toggle back to turn-based mode (R key)
        elif key == 'r':
            self.state.toggle_realtime_mode()
            self.ui.add_log_message("Returning to turn-based mode", "status")

    def run(self):
        """Run the main game loop."""
        import time
        
        self.show_intro()

        while self.running:
            # Check win/loss conditions
            result = self.state.check_game_over()
            if result:
                game_over_result = self.show_game_over(result)
                # If user quit from game over screen, exit without restarting
                if game_over_result == "quit":
                    self.quit_game = True
                self.running = False
                break

            # Handle real-time mode or turn-based mode
            if self.state.realtime_mode:
                self._run_realtime_frame()
            else:
                # Render game state
                self.render()

                # Get player input (graphics mode with tab completion)
                # Update game state in tab completion for context-aware completions
                if self.tab_completion:
                    self.tab_completion.set_game_state(self.state)
                
                command = self.ui.handle_events()
                if command == "quit":
                    self.quit_game = True
                    self.running = False
                elif command:
                    self.process_command(command)


def main():
    """Entry point for the game."""
    try:
        while True:
            game = Game()
            game.run()
            
            # Exit if player quit
            if game.quit_game:
                break
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
