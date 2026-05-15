"""Game state manager for Hole Wizards game."""

import random
from player import Player
from enemy import Enemy
from map_system import Map
from items import (
    create_starting_weapon,
    create_starting_armor,
    create_starting_spell,
    create_hp_potion,
    create_mana_potion,
    LootBag,
)
from pathlib import Path
import configparser


class GameState:
    """Manages the overall game state."""

    def __init__(self):
        """Initialize a new game."""
        self.player = Player()
        self.enemies = []
        self.map = Map(32, 32)
        self.current_enemy = None  # Currently viewed enemy for stats display
        self.game_over = False
        self.victory = False
        self.current_stats_page = "player"
        self.chest_items = []  # Items available in current chest
        self.loot_items = []  # Items available in current loot pile
        self.current_loot_enemy = None  # Enemy whose loot is being viewed
        self.chests = {}  # Dictionary of chest locations {(x, y): [items]}
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
        
        # Create and place chests
        self._spawn_chests()

    def _load_monsters_from_config(self):
        """Load monster definitions from data/monsters.cfg."""
        monsters = []
        
        # Try multiple possible locations for the config file
        possible_paths = [
            Path(__file__).parent.parent / "data" / "monsters.cfg",
            Path.cwd() / "data" / "monsters.cfg",
        ]
        
        config_file = None
        for path in possible_paths:
            if path.exists():
                config_file = path
                break
        
        if not config_file:
            return None  # Config file not found, use fallback
        
        config = configparser.ConfigParser()
        config.read(config_file)
        
        for section in config.sections():
            if section.startswith('monster_'):
                monster_data = {
                    'name': config.get(section, 'name', fallback='Unknown'),
                    'description': config.get(section, 'description', fallback='insert funny text here'),
                    'hp': config.getint(section, 'hp', fallback=5),
                    'max_hp': config.getint(section, 'max_hp', fallback=5),
                    'mana': config.getint(section, 'mana', fallback=1),
                    'max_mana': config.getint(section, 'max_mana', fallback=1),
                    'xp': config.getint(section, 'xp', fallback=1),
                    'level': config.getint(section, 'level', fallback=1),
                    'view_distance': config.getint(section, 'view_distance', fallback=5),
                    'reinforcement': config.get(section, 'reinforcement', fallback='5,5,5,5,5,5,5,5,5,5'),
                    'weapon': config.get(section, 'weapon', fallback=None),
                    'armor': config.get(section, 'armor', fallback=None),
                    'hp_potions': config.getint(section, 'hp_potions', fallback=0),
                    'mana_potions': config.getint(section, 'mana_potions', fallback=0),
                    'spell': config.get(section, 'spell', fallback=None),
                }
                monsters.append(monster_data)
        
        return monsters if monsters else None

    def _spawn_enemies(self):
        """Spawn enemies on the map from config file."""
        from items import StackableItem
        
        # Try to load monsters from config
        monster_data_list = self._load_monsters_from_config()
        
        if monster_data_list:
            # Use monsters from config file
            for monster_data in monster_data_list:
                enemy = Enemy(monster_data['name'])
                enemy.hp = monster_data['hp']
                enemy.max_hp = monster_data['max_hp']
                enemy.mana = monster_data['mana']
                enemy.max_mana = monster_data['max_mana']
                enemy.xp = monster_data['xp']
                enemy.level = monster_data['level']
                enemy.view_distance = monster_data['view_distance']
                
                # Parse reinforcement values
                try:
                    reinforcement_values = [int(x) for x in monster_data['reinforcement'].split(',')]
                    enemy.reinforcement = reinforcement_values
                except (ValueError, AttributeError):
                    enemy.reinforcement = [5] * 10  # Fallback
                
                # Give enemy items from config
                if monster_data.get('weapon'):
                    weapon = create_starting_weapon()  # TODO: Load specific weapon from config
                    enemy.add_to_inventory(weapon)
                    enemy.equip_weapon(weapon)
                
                if monster_data.get('armor'):
                    armor = create_starting_armor()  # TODO: Load specific armor from config
                    enemy.add_to_inventory(armor)
                    enemy.equip_armor(armor)
                
                # Add potions as stackable items
                if monster_data.get('hp_potions', 0) > 0:
                    hp_potions = StackableItem("HP Potion", "consumable", monster_data['hp_potions'])
                    enemy.add_to_inventory(hp_potions)
                
                if monster_data.get('mana_potions', 0) > 0:
                    mana_potions = StackableItem("Mana Potion", "consumable", monster_data['mana_potions'])
                    enemy.add_to_inventory(mana_potions)
                
                # Add spell
                if monster_data.get('spell'):
                    spell = create_starting_spell()  # TODO: Load specific spell from config
                    enemy.add_to_inventory(spell)
                
                self.enemies.append(enemy)
                self._place_enemy_on_map(enemy)
        else:
            # Fallback: use hardcoded enemies
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
                self._place_enemy_on_map(enemy)

    def _place_enemy_on_map(self, enemy):
        """Place an enemy on the map at a random location."""
        placed = False
        attempts = 0
        while not placed and attempts < 10:
            x = random.randint(5, self.map.width - 5)
            y = random.randint(5, self.map.height - 5)
            placed = self.map.place_enemy(enemy, x, y)
            attempts += 1

    def _spawn_chests(self):
        """Spawn chests on the map with random contents."""
        from items import StackableItem
        
        num_chests = random.randint(3, 5)
        
        for _ in range(num_chests):
            attempts = 0
            while attempts < 20:
                x = random.randint(5, self.map.width - 5)
                y = random.randint(5, self.map.height - 5)
                
                # Check if tile is walkable and not already occupied
                tile = self.map.get_tile(x, y)
                if tile and tile.tile_type not in ["wall", "door_closed", "chest"] and not tile.player and not tile.enemy:
                    # Mark tile as chest
                    tile.tile_type = "chest"
                    
                    # Generate chest contents (2-5 items)
                    chest_contents = []
                    num_items = random.randint(2, 5)
                    
                    for _ in range(num_items):
                        item_type = random.choice(["weapon", "armor", "potion_hp", "potion_mana", "spell"])
                        
                        if item_type == "weapon":
                            chest_contents.append(create_starting_weapon())
                        elif item_type == "armor":
                            chest_contents.append(create_starting_armor())
                        elif item_type == "potion_hp":
                            # Create stackable potion
                            hp_amount = random.randint(3, 5)
                            chest_contents.append(StackableItem("HP Potion", "consumable", quantity=1))
                            chest_contents[-1].hp_increase = hp_amount
                        elif item_type == "potion_mana":
                            # Create stackable potion
                            mana_amount = random.randint(2, 4)
                            chest_contents.append(StackableItem("Mana Potion", "consumable", quantity=1))
                            chest_contents[-1].mana_increase = mana_amount
                        elif item_type == "spell":
                            chest_contents.append(create_starting_spell())
                    
                    # Store chest contents
                    self.chests[(x, y)] = chest_contents
                    break
                
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
                # Check inventory space
                if len(self.player.inventory) >= self.player.max_inventory_size:
                    return False, "Inventory is full"
                
                # Check weapon/armor limits
                if item.item_type == "weapon" and not self.player.can_carry_weapon():
                    return False, "Can only carry 2 weapons max"
                if item.item_type == "armor" and not self.player.can_carry_armor():
                    return False, "Can only carry 2 armor pieces max"
                
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
            
            # For stackable items, only remove one from the stack
            if hasattr(item, 'remove_quantity'):
                if item.remove_quantity(1):
                    # If quantity reaches 0, remove the item entirely
                    if item.quantity <= 0:
                        self.player.remove_from_inventory(item)
                    return True, f"Used {item.base_name}"
            else:
                # Non-stackable consumables are removed entirely
                self.player.remove_from_inventory(item)
                return True, f"Used {item.name}"
        
        elif item.item_type == "spell":
            # Check if player has enough mana
            mana_cost = getattr(item, 'mana_cost', 1)
            if self.player.mana < mana_cost:
                return False, f"Not enough mana to cast {item.name} (costs {mana_cost}, have {self.player.mana})"
            
            # Consume mana
            self.player.mana -= mana_cost
            
            # Apply spell effects
            item.apply_use_effect(self.player)
            
            return True, f"Cast {item.name} (cost {mana_cost} mana)"
        
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
            # Collect all items from inventory (equipped items are already in inventory)
            loot_items = list(enemy.inventory)
            
            # Create loot bag
            loot_bag = LootBag(enemy.name, loot_items)
            
            # Place loot bag on map at enemy's position
            enemy_x = enemy.position["x"]
            enemy_y = enemy.position["y"]
            self.map.place_item(loot_bag, enemy_x, enemy_y)
            
            # Remove dead enemy from map and game state
            self.map.remove_enemy(enemy)
            self.enemies.remove(enemy)
            xp_gained = enemy.xp
            self.player.gain_xp(xp_gained)
            
            # Build loot message with items list
            if loot_items:
                items_str = ", ".join([str(item) for item in loot_items])
                return True, f"Defeated {enemy.name}! Gained {xp_gained} XP! Loot: {items_str}"
            else:
                return True, f"Defeated {enemy.name}! Gained {xp_gained} XP!"

    def player_attack_target(self, target_name):
        """Have the player attack a named enemy (must be adjacent)."""
        # Find enemy by name
        target_enemy = None
        for enemy in self.enemies:
            if enemy.alive and enemy.name.lower() == target_name.lower():
                target_enemy = enemy
                break
        
        if not target_enemy:
            return False, f"Enemy '{target_name}' not found"
        
        # Check if adjacent
        if not self._is_adjacent(self.player, target_enemy):
            return False, f"{target_enemy.name} is not within reach"
        
        # Attack the target
        damage = self.player.get_attack_damage()
        target_enemy.take_damage(damage)
        
        if target_enemy.alive:
            return True, f"Attacked {target_enemy.name} for {damage} damage! ({target_enemy.hp} HP remaining)"
        else:
            # Collect all items from inventory (equipped items are already in inventory)
            loot_items = list(target_enemy.inventory)
            
            # Create loot bag
            loot_bag = LootBag(target_enemy.name, loot_items)
            
            # Place loot bag on map at enemy's position
            enemy_x = target_enemy.position["x"]
            enemy_y = target_enemy.position["y"]
            self.map.place_item(loot_bag, enemy_x, enemy_y)
            
            # Remove dead enemy from map and game state
            self.map.remove_enemy(target_enemy)
            self.enemies.remove(target_enemy)
            xp_gained = target_enemy.xp
            self.player.gain_xp(xp_gained)
            
            # Build loot message with items list
            if loot_items:
                items_str = ", ".join([str(item) for item in loot_items])
                return True, f"Defeated {target_enemy.name}! Gained {xp_gained} XP! Loot: {items_str}"
            else:
                return True, f"Defeated {target_enemy.name}! Gained {xp_gained} XP!"

    def player_defend(self):
        """Have the player prepare to defend."""
        self.player.defending = True
        return True, "You assume a defensive stance"

    def show_loot(self):
        """Show loot from a dead enemy at current location or adjacent."""
        px = self.player.position["x"]
        py = self.player.position["y"]
        
        # Check current position and adjacent tiles
        loot_items = []
        loot_enemy = "Unknown"
        
        # Check current position first
        items = self.map.get_items_at(px, py)
        for item in items:
            if item.item_type == "bag" and hasattr(item, 'contents'):
                loot_items = item.contents
                loot_enemy = item.enemy_name
                break
        
        # If no loot found at current position, check adjacent tiles
        if not loot_items:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx = px + dx
                    ny = py + dy
                    items = self.map.get_items_at(nx, ny)
                    for item in items:
                        if item.item_type == "bag" and hasattr(item, 'contents'):
                            loot_items = item.contents
                            loot_enemy = item.enemy_name
                            break
                    if loot_items:
                        break
                if loot_items:
                    break
        
        self.loot_items = loot_items
        self.current_loot_enemy = loot_enemy
        self.current_stats_page = "loot"
        return bool(loot_items), "Loot found" if loot_items else "No loot here"

    def show_chest(self):
        """Show contents of an adjacent chest."""
        px = self.player.position["x"]
        py = self.player.position["y"]
        
        # Check adjacent tiles for chests
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = px + dx, py + dy
                if (nx, ny) in self.chests:
                    self.chest_items = self.chests[(nx, ny)]
                    self.current_stats_page = "chest"
                    return True, f"Opened chest at ({nx}, {ny})"
        
        return False, "No chest nearby"

    def take_loot_item(self, item_name):
        """Take an item from the current loot pile."""
        from items import StackableItem
        
        for item in self.loot_items:
            # Check item name (and base_name if it's a StackableItem)
            name_matches = item.name.lower() == item_name.lower()
            if not name_matches and hasattr(item, 'base_name'):
                name_matches = item.base_name.lower() == item_name.lower()
            
            if name_matches:
                # Check if it's a stackable item
                if isinstance(item, StackableItem):
                    # Try to add to existing stack in inventory
                    for inv_item in self.player.inventory:
                        if isinstance(inv_item, StackableItem) and inv_item.base_name == item.base_name:
                            overflow = inv_item.add_quantity(item.quantity)
                            if overflow > 0:
                                item.quantity = overflow
                                return True, f"Took {item.base_name} (now carrying {inv_item.quantity})"
                            else:
                                self.loot_items.remove(item)
                                return True, f"Took {item.base_name} (now carrying {inv_item.quantity})"
                    # No existing stack, add as new item
                    if len(self.player.inventory) >= self.player.max_inventory_size:
                        return False, "Inventory is full"
                    self.player.add_to_inventory(item)
                    self.loot_items.remove(item)
                    return True, f"Took {item.name}"
                else:
                    if len(self.player.inventory) >= self.player.max_inventory_size:
                        return False, "Inventory is full"
                    
                    # Check weapon/armor limits
                    if item.item_type == "weapon" and not self.player.can_carry_weapon():
                        return False, "Can only carry 2 weapons max"
                    if item.item_type == "armor" and not self.player.can_carry_armor():
                        return False, "Can only carry 2 armor pieces max"
                    
                    self.player.add_to_inventory(item)
                    self.loot_items.remove(item)
                    return True, f"Took {item.name}"
        
        return False, f"Item '{item_name}' not in loot"

    def take_chest_item(self, item_name):
        """Take an item from the current chest."""
        from items import StackableItem
        
        for item in self.chest_items:
            if item.name.lower() == item_name.lower() or (hasattr(item, 'base_name') and item.base_name.lower() == item_name.lower()):
                if isinstance(item, StackableItem):
                    for inv_item in self.player.inventory:
                        if isinstance(inv_item, StackableItem) and inv_item.base_name == item.base_name:
                            overflow = inv_item.add_quantity(item.quantity)
                            if overflow > 0:
                                item.quantity = overflow
                                return True, f"Took {item.base_name} (now carrying {inv_item.quantity})"
                            else:
                                self.chest_items.remove(item)
                                return True, f"Took {item.base_name} (now carrying {inv_item.quantity})"
                    if len(self.player.inventory) >= self.player.max_inventory_size:
                        return False, "Inventory is full"
                    self.player.add_to_inventory(item)
                    self.chest_items.remove(item)
                    return True, f"Took {item.name}"
                else:
                    if len(self.player.inventory) >= self.player.max_inventory_size:
                        return False, "Inventory is full"
                    
                    # Check weapon/armor limits
                    if item.item_type == "weapon" and not self.player.can_carry_weapon():
                        return False, "Can only carry 2 weapons max"
                    if item.item_type == "armor" and not self.player.can_carry_armor():
                        return False, "Can only carry 2 armor pieces max"
                    
                    self.player.add_to_inventory(item)
                    self.chest_items.remove(item)
                    return True, f"Took {item.name}"
        
        return False, f"Item '{item_name}' not in chest"

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
        
        # Reward action if enemy can see the player
        if self._can_enemy_see_player(enemy):
            enemy.reward_action_for_seeing_player()

    def _is_adjacent(self, entity1, entity2):
        """Check if two entities are adjacent (including diagonals)."""
        dx = abs(entity1.position["x"] - entity2.position["x"])
        dy = abs(entity1.position["y"] - entity2.position["y"])
        # Adjacent if both distances are <= 1 and at least one is non-zero
        return dx <= 1 and dy <= 1 and (dx != 0 or dy != 0)

    def _can_enemy_see_player(self, enemy):
        """Check if an enemy can see the player based on view distance."""
        ex = enemy.position["x"]
        ey = enemy.position["y"]
        px = self.player.position["x"]
        py = self.player.position["y"]
        
        # Calculate distance between enemy and player
        distance = abs(ex - px) + abs(ey - py)  # Manhattan distance
        
        return distance <= enemy.view_distance

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
