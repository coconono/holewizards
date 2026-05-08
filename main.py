#!/usr/bin/env python3
"""Main game loop for Hole Wizards."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from ui import UI
from commands import CommandParser


class Game:
    """Main game controller."""

    def __init__(self):
        """Initialize the game."""
        self.state = GameState()
        self.ui = UI()
        self.running = True
        self.should_show_intro = True

    def render(self):
        """Render the current game state."""
        os.system("clear" if os.name == "posix" else "cls")
        
        current_enemy = self.state.get_current_enemy()
        screen = self.ui.render_full_screen(
            self.state.player,
            current_enemy,
            self.state.map,
            self.state.current_stats_page,
            self.state.chest_items
        )
        print(screen)
        print(self.ui.render_command_prompt(), end="", flush=True)

    def process_command(self, command_string):
        """Process a player command."""
        cmd_type, args = CommandParser.parse(command_string)
        
        if cmd_type is None:
            self.ui.add_log_message("Unknown command. Type 'help' for commands.")
            return

        # Stats commands
        if cmd_type == "show_player_stats":
            self.state.current_stats_page = "player"
            self.ui.add_log_message("Showing player stats")

        elif cmd_type == "show_enemy_stats":
            enemy = self.state.get_current_enemy()
            if enemy and enemy.alive:
                self.state.current_stats_page = "enemy"
                self.ui.add_log_message(f"Showing {enemy.name}'s stats")
            else:
                self.ui.add_log_message("No enemy nearby")

        elif cmd_type == "show_player_inventory":
            self.state.current_stats_page = "player_inventory"
            self.ui.add_log_message(f"Showing inventory ({len(self.state.player.inventory)} items)")

        elif cmd_type == "show_enemy_inventory":
            enemy = self.state.get_current_enemy()
            if enemy and not enemy.alive:
                self.state.current_stats_page = "enemy_inventory"
                self.ui.add_log_message(f"Showing {enemy.name}'s inventory")
            elif enemy:
                self.ui.add_log_message("Enemy is still alive - cannot loot")
            else:
                self.ui.add_log_message("No enemy to loot")

        elif cmd_type == "show_chest_inventory":
            self.ui.add_log_message("No chest nearby (feature coming soon)")

        elif cmd_type == "list_commands":
            self.ui.clear_log()
            self.ui.add_log_message(self.ui.render_help())

        # Movement commands
        elif cmd_type == "move_up":
            if self.state.player_move(0, -1):
                self.ui.add_log_message("Moved up")
                enemy = self.state.get_current_enemy()
                if enemy and enemy.alive:
                    self.ui.add_log_message(f"You encounter {enemy.name}!")
            else:
                self.ui.add_log_message("Cannot move up - blocked")

        elif cmd_type == "move_down":
            if self.state.player_move(0, 1):
                self.ui.add_log_message("Moved down")
                enemy = self.state.get_current_enemy()
                if enemy and enemy.alive:
                    self.ui.add_log_message(f"You encounter {enemy.name}!")
            else:
                self.ui.add_log_message("Cannot move down - blocked")

        elif cmd_type == "move_left":
            if self.state.player_move(-1, 0):
                self.ui.add_log_message("Moved left")
                enemy = self.state.get_current_enemy()
                if enemy and enemy.alive:
                    self.ui.add_log_message(f"You encounter {enemy.name}!")
            else:
                self.ui.add_log_message("Cannot move left - blocked")

        elif cmd_type == "move_right":
            if self.state.player_move(1, 0):
                self.ui.add_log_message("Moved right")
                enemy = self.state.get_current_enemy()
                if enemy and enemy.alive:
                    self.ui.add_log_message(f"You encounter {enemy.name}!")
            else:
                self.ui.add_log_message("Cannot move right - blocked")

        # Combat commands
        elif cmd_type == "attack":
            success, message = self.state.player_attack()
            self.ui.add_log_message(message)
            
            if success:
                enemy = self.state.get_current_enemy()
                if enemy and enemy.alive:
                    # Enemy counterattack
                    self.state.enemy_take_turn(enemy)
                    # Simple enemy attack response
                    if self.state._is_adjacent(enemy, self.state.player):
                        damage = enemy.get_attack_damage()
                        if self.state.player.defending:
                            damage = max(1, damage - self.state.player.get_defense_value())
                            self.state.player.defending = False
                            self.ui.add_log_message(f"{enemy.name} attacks but you defend! ({damage} damage)")
                        else:
                            self.state.player.take_damage(damage)
                            self.ui.add_log_message(f"{enemy.name} counterattacks for {damage} damage!")

        elif cmd_type == "defend":
            success, message = self.state.player_defend()
            self.ui.add_log_message(message)

        # Item commands
        elif cmd_type == "take":
            if args:
                success, message = self.state.player_take_item(args)
                self.ui.add_log_message(message)
            else:
                self.ui.add_log_message("Take what?")

        elif cmd_type == "drop":
            if args:
                success, message = self.state.player_drop_item(args)
                self.ui.add_log_message(message)
            else:
                self.ui.add_log_message("Drop what?")

        elif cmd_type == "equip":
            if args:
                success, message = self.state.player_equip_item(args)
                self.ui.add_log_message(message)
            else:
                self.ui.add_log_message("Equip what?")

        elif cmd_type == "use":
            if args:
                success, message = self.state.player_use_item(args)
                self.ui.add_log_message(message)
            else:
                self.ui.add_log_message("Use what?")

    def show_intro(self):
        """Show the game intro."""
        os.system("clear" if os.name == "posix" else "cls")
        intro_text = """
╔═══════════════════════════════════════════════════════════════════════╗
║                     WELCOME TO HOLE WIZARDS                           ║
║                                                                       ║
║  You have entered the Hole! A place of undescribable terror and      ║
║  riches! You are a wizard! Cast your spells and swing your sword!    ║
║                                                                       ║
║  There are other wizards between you and the exit. They don't like   ║
║  you! Beat them up, take their stuff and ESCAPE THE HOLE!            ║
║                                                                       ║
║  Commands: move up/down/left/right, attack, defend, take [item],    ║
║           drop [item], equip [item], use [item],                     ║
║           show player stats, list commands                           ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
        """
        print(intro_text)
        input("Press Enter to begin...")

    def show_game_over(self, result):
        """Show game over screen."""
        os.system("clear" if os.name == "posix" else "cls")
        
        if result == "victory":
            victory_text = """
╔═══════════════════════════════════════════════════════════════════════╗
║                         VICTORY!                                      ║
║                                                                       ║
║  You have escaped the Hole with your life (and treasure)!            ║
║  The other wizards have fallen and their treasures are yours!        ║
║                                                                       ║
║  You emerge from the darkness into the light... a hero!              ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
            """
            print(victory_text)
        else:
            defeat_text = """
╔═══════════════════════════════════════════════════════════════════════╗
║                         DEFEAT!                                       ║
║                                                                       ║
║  You have fallen in the Hole. Your adventure has ended...            ║
║  Perhaps another wizard will be more successful.                     ║
║                                                                       ║
║  Your remains will rest in the darkness forever...                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
            """
            print(defeat_text)
        
        print("\nFinal Stats:")
        print(f"  Level: {self.state.player.level}")
        print(f"  XP: {self.state.player.xp}")
        print(f"  Items: {len(self.state.player.inventory)}")

    def run(self):
        """Run the main game loop."""
        if self.should_show_intro:
            self.show_intro()

        while self.running:
            # Check win/loss conditions
            result = self.state.check_game_over()
            if result:
                self.show_game_over(result)
                self.running = False
                break

            # Render game state
            self.render()

            # Get player input
            try:
                command = input().strip()
                if command:
                    self.process_command(command)
            except (KeyboardInterrupt, EOFError):
                print("\nThanks for playing Hole Wizards!")
                self.running = False
                break


def main():
    """Entry point for the game."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
