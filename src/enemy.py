"""Enemy class for Hole Wizards game."""

import random


class Enemy:
    """Represents an enemy character."""

    def __init__(self, name, x=0, y=0):
        """Initialize an enemy with randomized stats."""
        self.name = name
        self.hp = random.randint(5, 12)
        self.max_hp = self.hp
        self.mana = random.randint(1, 5)
        self.max_mana = self.mana
        self.xp = random.randint(1, 10)
        self.level = random.randint(1, 3)
        self.position = {"x": x, "y": y}
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.equipped_spell = None
        self.alive = True
        self.view_distance = 10  # Increased from 5 to 10
        self.reinforcement = [random.randint(1, 10) for _ in range(10)]  # Weights for 10 different actions (1-10)
        self.last_action = None
        self.defending = False
        self.last_direction = None  # Track last movement direction to avoid immediately backtracking

    def take_damage(self, damage):
        """Reduce HP by damage amount."""
        self.hp = max(0, self.hp - damage)
        if self.hp == 0:
            self.alive = False
        # Decrease reinforcement for last action when taking damage
        if self.last_action is not None:
            self.reinforcement[self.last_action] = max(1, self.reinforcement[self.last_action] - 1)

    def heal(self, amount):
        """Increase HP up to max."""
        self.hp = min(self.max_hp, self.hp + amount)
        # Increase reinforcement for last action when healing
        if self.last_action is not None:
            self.reinforcement[self.last_action] = min(10, self.reinforcement[self.last_action] + 1)

    def reward_action_for_seeing_player(self):
        """Increase reinforcement for last action when player is in view."""
        if self.last_action is not None:
            self.reinforcement[self.last_action] = min(10, self.reinforcement[self.last_action] + 1)

    def restore_mana(self, amount):
        """Increase mana up to max."""
        self.mana = min(self.max_mana, self.mana + amount)

    def add_to_inventory(self, item):
        """Add an item to inventory."""
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        """Remove an item from inventory."""
        if item not in self.inventory:
            return False
        self.inventory.remove(item)
        # Unequip if this item was equipped
        if self.equipped_weapon == item:
            self.equipped_weapon = None
        if self.equipped_armor == item:
            self.equipped_armor = None
        if self.equipped_spell == item:
            self.equipped_spell = None
        return True

    def _equip_item(self, item, slot):
        """Generic equip method. Slot can be 'weapon', 'armor', or 'spell'."""
        if item not in self.inventory:
            return False
        setattr(self, f"equipped_{slot}", item)
        return True

    def equip_weapon(self, weapon):
        """Equip a weapon."""
        return self._equip_item(weapon, "weapon")

    def equip_armor(self, armor):
        """Equip armor."""
        return self._equip_item(armor, "armor")

    def equip_spell(self, spell):
        """Equip a spell."""
        return self._equip_item(spell, "spell")

    def get_attack_damage(self):
        """Calculate total attack damage."""
        damage = 1  # Base damage
        if self.equipped_weapon:
            damage = self.equipped_weapon.get_attack_value()
        return damage

    def get_defense_value(self):
        """Calculate total defense value."""
        defense = 1  # Base defense reduction
        if self.equipped_armor:
            defense = self.equipped_armor.get_defense_value()
        return defense

    def choose_action(self):
        """Choose next action based on reinforcement weights."""
        # Actions: 0-3 = movement, 4 = attack, 5 = defend, 6-9 = reserved
        total_weight = sum(self.reinforcement)
        choice = random.randint(0, total_weight - 1)
        
        current = 0
        for i, weight in enumerate(self.reinforcement):
            current += weight
            if choice < current:
                self.last_action = i
                return i
        
        self.last_action = 0
        return 0

    def record_damage_dealt(self, damage):
        """Record that this enemy dealt damage (for reinforcement)."""
        if self.last_action is not None:
            self.reinforcement[self.last_action] = min(10, self.reinforcement[self.last_action] + 2)

    def find_item_in_inventory(self, item_name):
        """Find an item in inventory by name."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def move(self, dx, dy, map_obj):
        """Attempt to move enemy on the map."""
        # Use the map's move_enemy method to update both position dict and tile state
        return map_obj.move_enemy(self, dx, dy)

    def get_visible_tiles(self, map_obj):
        """Get list of visible tiles based on view distance."""
        visible = []
        for dx in range(-self.view_distance, self.view_distance + 1):
            for dy in range(-self.view_distance, self.view_distance + 1):
                x = self.position["x"] + dx
                y = self.position["y"] + dy
                if map_obj.is_valid_position(x, y):
                    visible.append((x, y))
        return visible

    def get_distance_to(self, target_pos):
        """Calculate Manhattan distance to target position."""
        dx = abs(self.position["x"] - target_pos["x"])
        dy = abs(self.position["y"] - target_pos["y"])
        return dx + dy

    def can_see_target(self, target_pos):
        """Check if target is within view distance."""
        return self.get_distance_to(target_pos) <= self.view_distance

    def get_move_towards_target(self, target_pos, map_obj):
        """Calculate a single step towards target. Returns (dx, dy) or None if can't move."""
        current_x = self.position["x"]
        current_y = self.position["y"]
        target_x = target_pos["x"]
        target_y = target_pos["y"]
        
        # Prefer moving horizontally or vertically (Manhattan distance)
        dx = 0 if current_x == target_x else (1 if target_x > current_x else -1)
        dy = 0 if current_y == target_y else (1 if target_y > current_y else -1)
        
        # If both directions are equally good, randomly choose one
        if dx != 0 and dy != 0 and random.choice([True, False]):
            dy = 0
        
        # Try preferred direction
        new_x = current_x + dx
        new_y = current_y + dy
        if map_obj.is_walkable(new_x, new_y):
            return (dx, dy)
        
        # If preferred fails, try only horizontal
        if dx != 0:
            new_x = current_x + dx
            if map_obj.is_walkable(new_x, current_y):
                return (dx, 0)
        
        # Try only vertical
        if dy != 0:
            new_y = current_y + dy
            if map_obj.is_walkable(current_x, new_y):
                return (0, dy)
        
        return None

    def get_random_move_direction(self, map_obj):
        """Get a random valid move direction, avoiding the direction just moved from."""
        # Possible movement directions
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        # Remove the direction we just came from
        if self.last_direction:
            reverse = (-self.last_direction[0], -self.last_direction[1])
            directions = [d for d in directions if d != reverse]
        
        # Shuffle and try to move
        random.shuffle(directions)
        current_x = self.position["x"]
        current_y = self.position["y"]
        
        for dx, dy in directions:
            new_x = current_x + dx
            new_y = current_y + dy
            if map_obj.is_walkable(new_x, new_y):
                return (dx, dy)
        
        return None
