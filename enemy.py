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
        self.view_distance = 5
        self.reinforcement = [5] * 10  # Weights for 10 different actions
        self.last_action = None
        self.defending = False

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

    def restore_mana(self, amount):
        """Increase mana up to max."""
        self.mana = min(self.max_mana, self.mana + amount)

    def add_to_inventory(self, item):
        """Add an item to inventory."""
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        """Remove an item from inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            if self.equipped_weapon == item:
                self.equipped_weapon = None
            if self.equipped_armor == item:
                self.equipped_armor = None
            if self.equipped_spell == item:
                self.equipped_spell = None
            return True
        return False

    def equip_weapon(self, weapon):
        """Equip a weapon."""
        if weapon not in self.inventory:
            return False
        self.equipped_weapon = weapon
        return True

    def equip_armor(self, armor):
        """Equip armor."""
        if armor not in self.inventory:
            return False
        self.equipped_armor = armor
        return True

    def equip_spell(self, spell):
        """Equip a spell."""
        if spell not in self.inventory:
            return False
        self.equipped_spell = spell
        return True

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
        new_x = self.position["x"] + dx
        new_y = self.position["y"] + dy
        
        # Check bounds
        if map_obj.is_walkable(new_x, new_y):
            self.position["x"] = new_x
            self.position["y"] = new_y
            return True
        return False

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
