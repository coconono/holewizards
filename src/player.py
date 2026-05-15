"""Player class for Hole Wizards game."""


class Player:
    """Represents the player character."""

    def __init__(self, x=0, y=0):
        """Initialize a player with default stats."""
        self.hp = 10
        self.max_hp = 10
        self.mana = 5
        self.max_mana = 5
        self.xp = 0
        self.level = 1
        self.position = {"x": x, "y": y}
        self.inventory = []
        self.max_inventory_size = 20  # Maximum items player can carry
        self.equipped_weapon = None
        self.equipped_armor = None
        self.equipped_spell = None
        self.alive = True
        self.view_distance = 3
        self.defending = False

    def take_damage(self, damage):
        """Reduce HP by damage amount."""
        self.hp = max(0, self.hp - damage)
        if self.hp == 0:
            self.alive = False

    def heal(self, amount):
        """Increase HP up to max."""
        self.hp = min(self.max_hp, self.hp + amount)

    def restore_mana(self, amount):
        """Increase mana up to max."""
        self.mana = min(self.max_mana, self.mana + amount)

    def gain_xp(self, amount):
        """Gain experience and handle level ups."""
        self.xp += amount
        while self.xp >= 10:
            self.xp -= 10
            self.level_up()

    def level_up(self):
        """Increase level and stats."""
        self.level += 1
        self.max_hp += 1
        self.max_mana += 1
        self.hp = self.max_hp
        self.mana = self.max_mana

    def add_to_inventory(self, item):
        """Add an item to inventory. Returns True if successful, False if inventory is full."""
        if len(self.inventory) >= self.max_inventory_size:
            return False
        self.inventory.append(item)
        return True

    def count_items_by_type(self, item_type):
        """Count items of a specific type in inventory."""
        return sum(1 for item in self.inventory if item.item_type == item_type)

    def can_carry_item_type(self, item_type, max_count=2):
        """Check if player can carry another item of this type."""
        return self.count_items_by_type(item_type) < max_count

    def can_carry_weapon(self):
        """Check if player can carry another weapon (max 2)."""
        return self.can_carry_item_type("weapon", 2)

    def can_carry_armor(self):
        """Check if player can carry another armor (max 2)."""
        return self.can_carry_item_type("armor", 2)

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

    def find_item_in_inventory(self, item_name):
        """Find an item in inventory by name."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def move(self, dx, dy, map_obj):
        """Attempt to move player on the map."""
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
