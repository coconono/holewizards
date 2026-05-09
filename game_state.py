"""Game state manager for Hole Wizards game."""

from player import Player
from enemy import Enemy
from map_system import Map
from items import (
    create_starting_weapon,
    create_starting_armor,
    create_starting_spell,
    create_hp_potion,
    create_mana_potion,
)


class GameState:
    """Manages the overall game state."""

    def __init__(self):
        """Initialize a new game."""
        self.player = Player()
        self.enemies = []
        self.map = Map(32, 32)
        self.current_enemy = None
        self.game_over = False
        self.victory = False
        self.current_stats_page = "player"
        self.chest_items = []  # Items available in current chest
        self._initialize_game()

    def _initialize_game(self):
        """Set up the initial game state."""
        # Give player starting items
        weapon = create_starting_weapon()
        armor = create_starting_armor()
        spell = create_starting_spell()
        
        self.player.add_to_inventory(weapon)
        self.player.add_to_inventory(armor)
        self.player.add_to_inventory(spell)
        
        self.player.equip_weapon(weapon)
        self.player.equip_armor(armor)
        self.player.equip_spell(spell)
        
        # Add some potions
        self.player.add_to_inventory(create_hp_potion())
        self.player.add_to_inventory(create_mana_potion())
        
        # Place player on map
        self.map.place_player(self.player)
        
        # Create and place enemies
        self._spawn_enemies()

    def _spawn_enemies(self):
        """Spawn enemies on the map."""
        enemy_names = ["Goblin", "Skeleton", "Orc", "Troll", "Wraith"]
        num_enemies = 3
        
        for i in range(num_enemies):
            name = enemy_names[i % len(enemy_names)] + f"_{i}"
            enemy = Enemy(name)
            
            # Give enemy random items
            if i % 2 == 0:
                weapon = create_starting_weapon()
                enemy.add_to_inventory(weapon)
                enemy.equip_weapon(weapon)
            
            if i % 3 == 0:
                armor = create_starting_armor()
                enemy.add_to_inventory(armor)
                enemy.equip_armor(armor)
            
            self.enemies.append(enemy)
            
            # Place on map (avoid player start position)
            placed = False
            attempts = 0
            while not placed and attempts < 10:
                import random
                x = random.randint(5, self.map.width - 5)
                y = random.randint(5, self.map.height - 5)
                placed = self.map.place_enemy(enemy, x, y)
                attempts += 1

    def get_current_enemy(self):
        """Get the enemy at the player's location."""
        px = self.player.position["x"]
        py = self.player.position["y"]
        tile = self.map.get_tile(px, py)
        if tile and tile.enemy:
            return tile.enemy
        return None

    def get_adjacent_enemy(self):
        """Get an adjacent enemy (within melee range)."""
        px = self.player.position["x"]
        py = self.player.position["y"]
        
        # Check all adjacent tiles (8 directions)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip current position
                
                nx = px + dx
                ny = py + dy
                tile = self.map.get_tile(nx, ny)
                if tile and tile.enemy and tile.enemy.alive:
                    return tile.enemy
        
        return None

    def player_move(self, dx, dy):
        """Move the player on the map."""
        return self.map.move_player(self.player, dx, dy)

    def player_take_item(self, item_name):
        """Have the player take an item from the current location."""
        px = self.player.position["x"]
        py = self.player.position["y"]
        items = self.map.get_items_at(px, py)
        
        for item in items:
            if item.name.lower() == item_name.lower():
                self.player.add_to_inventory(item)
                self.map.remove_item_at(item, px, py)
                return True, f"Took {item.name}"
        
        return False, f"Item '{item_name}' not found"

    def player_drop_item(self, item_name):
        """Have the player drop an item."""
        item = self.player.find_item_in_inventory(item_name)
        if not item:
            return False, f"Item '{item_name}' not in inventory"
        
        self.player.remove_from_inventory(item)
        px = self.player.position["x"]
        py = self.player.position["y"]
        self.map.place_item(item, px, py)
        return True, f"Dropped {item.name}"

    def player_equip_item(self, item_name):
        """Have the player equip an item."""
        item = self.player.find_item_in_inventory(item_name)
        if not item:
            return False, f"Item '{item_name}' not in inventory"
        
        if item.item_type == "weapon":
            self.player.equip_weapon(item)
            return True, f"Equipped {item.name} as weapon"
        elif item.item_type == "armor":
            self.player.equip_armor(item)
            return True, f"Equipped {item.name} as armor"
        elif item.item_type == "spell":
            self.player.equip_spell(item)
            return True, f"Equipped {item.name} as spell"
        
        return False, "Cannot equip this item"

    def player_use_item(self, item_name):
        """Have the player use an item."""
        item = self.player.find_item_in_inventory(item_name)
        if not item:
            return False, f"Item '{item_name}' not in inventory"
        
        if item.item_type == "consumable":
            item.apply_use_effect(self.player)
            self.player.remove_from_inventory(item)
            return True, f"Used {item.name}"
        
        return False, "Cannot use this item"

    def player_attack(self):
        """Have the player attack an adjacent enemy."""
        enemy = self.get_adjacent_enemy()
        if not enemy:
            return False, "No enemy in range"
        
        if not enemy.alive:
            return False, "Enemy is already dead"
        
        damage = self.player.get_attack_damage()
        enemy.take_damage(damage)
        
        if enemy.alive:
            return True, f"Attacked {enemy.name} for {damage} damage! ({enemy.hp} HP remaining)"
        else:
            # Remove dead enemy from map
            self.map.remove_enemy(enemy)
            xp_gained = enemy.xp
            self.player.gain_xp(xp_gained)
            return True, f"Defeated {enemy.name}! Gained {xp_gained} XP!"

    def player_defend(self):
        """Have the player prepare to defend."""
        self.player.defending = True
        return True, "You assume a defensive stance"

    def enemy_take_turn(self, enemy):
        """Have an enemy take a turn."""
        # Implement basic enemy AI
        action = enemy.choose_action()
        
        if action == 0:  # Move up
            self.map.move_enemy(enemy, 0, -1)
            enemy.last_action = 0
        elif action == 1:  # Move down
            self.map.move_enemy(enemy, 0, 1)
            enemy.last_action = 1
        elif action == 2:  # Move left
            self.map.move_enemy(enemy, -1, 0)
            enemy.last_action = 2
        elif action == 3:  # Move right
            self.map.move_enemy(enemy, 1, 0)
            enemy.last_action = 3
        elif action == 4:  # Attack
            if self._is_adjacent(enemy, self.player):
                damage = enemy.get_attack_damage()
                if self.player.defending:
                    damage = max(1, damage - self.player.get_defense_value())
                    self.player.defending = False
                self.player.take_damage(damage)
                enemy.record_damage_dealt(damage)
                enemy.last_action = 4
        elif action == 5:  # Defend
            enemy.defending = True
            enemy.last_action = 5

    def _is_adjacent(self, entity1, entity2):
        """Check if two entities are adjacent."""
        dx = abs(entity1.position["x"] - entity2.position["x"])
        dy = abs(entity1.position["y"] - entity2.position["y"])
        return dx + dy == 1

    def check_game_over(self):
        """Check win/loss conditions."""
        if not self.player.alive:
            self.game_over = True
            return "defeat"
        
        if self.map.check_win_condition(self.player):
            self.game_over = True
            return "victory"
        
        return None

    def get_game_status(self):
        """Get a summary of the game status."""
        status = {
            "player_hp": self.player.hp,
            "player_level": self.player.level,
            "player_position": self.player.position,
            "current_enemy": self.get_current_enemy(),
            "enemies_alive": sum(1 for e in self.enemies if e.alive),
            "game_over": self.game_over,
        }
        return status
