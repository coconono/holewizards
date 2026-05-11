"""Items and Spells for Hole Wizards game."""

import random


class Item:
    """Base class for items."""

    def __init__(self, name, item_type, attack_value=0, defense_value=0):
        """Initialize an item."""
        self.name = name
        self.item_type = item_type  # "weapon", "armor", "consumable"
        self.attack_value = attack_value
        self.defense_value = defense_value
        self.hp_increase = 0
        self.mana_increase = 0
        self.effects = []  # List of effects

    def get_attack_value(self):
        """Get attack value for this item."""
        if isinstance(self.attack_value, int):
            return self.attack_value
        return random.randint(self.attack_value[0], self.attack_value[1])

    def get_defense_value(self):
        """Get defense value for this item."""
        if isinstance(self.defense_value, int):
            return self.defense_value
        return random.randint(self.defense_value[0], self.defense_value[1])

    def apply_equip_effect(self, character):
        """Apply EQUIP effect to a character."""
        if self.hp_increase > 0:
            character.max_hp += self.hp_increase
            character.hp = min(character.hp + self.hp_increase, character.max_hp)
        if self.mana_increase > 0:
            character.max_mana += self.mana_increase
            character.mana = min(character.mana + self.mana_increase, character.max_mana)

    def apply_use_effect(self, character):
        """Apply USE effect to a character."""
        if self.hp_increase > 0:
            character.heal(self.hp_increase)
        if self.mana_increase > 0:
            character.restore_mana(self.mana_increase)

    def __repr__(self):
        return f"{self.name}"


class Weapon(Item):
    """A weapon item that deals damage."""

    def __init__(self, name, attack_value):
        """Initialize a weapon."""
        super().__init__(name, "weapon", attack_value=attack_value)

    def __repr__(self):
        return f"{self.name} (Weapon, ATK:{self.get_attack_value()})"


class Armor(Item):
    """An armor item that provides defense."""

    def __init__(self, name, defense_value):
        """Initialize armor."""
        super().__init__(name, "armor", defense_value=defense_value)

    def __repr__(self):
        return f"{self.name} (Armor, DEF:{self.get_defense_value()})"


class Potion(Item):
    """A consumable potion."""

    def __init__(self, name, potion_type="hp", value=0):
        """Initialize a potion."""
        super().__init__(name, "consumable")
        self.potion_type = potion_type  # "hp" or "mana"
        if potion_type == "hp":
            self.hp_increase = value if value > 0 else random.randint(2, 5)
        else:
            self.mana_increase = value if value > 0 else random.randint(2, 4)

    def __repr__(self):
        if self.potion_type == "hp":
            return f"{self.name} (+{self.hp_increase} HP)"
        else:
            return f"{self.name} (+{self.mana_increase} Mana)"


class Spell(Item):
    """A spell item with various effects."""

    def __init__(self, name, spell_level="basic"):
        """Initialize a spell."""
        super().__init__(name, "spell")
        self.spell_level = spell_level  # "basic", "advanced", "superior"
        self.num_effects = {"basic": 1, "advanced": 2, "superior": 3}[spell_level]
        self.effects = []
        self.mana_cost = random.randint(1, self.num_effects + 1)
        self._generate_effects()

    def _generate_effects(self):
        """Generate random effects for this spell."""
        effect_types = ["attack", "defend", "heal", "mana_restore"]
        selected_effects = random.sample(effect_types, min(self.num_effects, len(effect_types)))
        
        for effect_type in selected_effects:
            if effect_type == "attack":
                self.attack_value = random.randint(2, 8)
            elif effect_type == "defend":
                self.defense_value = random.randint(1, 5)
            elif effect_type == "heal":
                self.hp_increase = random.randint(2, 6)
            elif effect_type == "mana_restore":
                self.mana_increase = random.randint(1, 4)
            
            self.effects.append(effect_type)

    def __repr__(self):
        effects_str = ", ".join(self.effects)
        return f"{self.name} (Spell: {effects_str})"


class LootBag(Item):
    """A bag containing loot from a defeated enemy."""

    def __init__(self, enemy_name, items_list=None):
        """Initialize a loot bag."""
        super().__init__(f"{enemy_name}'s Loot Bag", "bag")
        self.enemy_name = enemy_name
        self.contents = items_list if items_list else []

    def __repr__(self):
        return f"{self.name} ({len(self.contents)} items)"


class StackableItem(Item):
    """A stackable item (potions, etc.) with quantity tracking."""

    def __init__(self, name, item_type, quantity=1):
        """Initialize a stackable item."""
        super().__init__(name, item_type)
        self.quantity = quantity
        self.max_quantity = 99
        self.base_name = name  # Store original name without quantity

    def add_quantity(self, amount):
        """Add to quantity, capping at max_quantity. Returns overflow."""
        self.quantity += amount
        if self.quantity > self.max_quantity:
            overflow = self.quantity - self.max_quantity
            self.quantity = self.max_quantity
            return overflow
        return 0

    def remove_quantity(self, amount):
        """Remove from quantity. Returns True if successful."""
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False

    def __repr__(self):
        return f"{self.base_name} ({self.quantity})"


# Preset items for initial inventory
def load_random_weapon_from_config():
    """Load a random weapon from weapons.cfg."""
    from configparser import ConfigParser
    from pathlib import Path
    import random
    
    # Get path to weapons.cfg
    config_file = Path(__file__).parent.parent / "data" / "weapons.cfg"
    
    if not config_file.exists():
        # Fallback to basic weapon if config doesn't exist
        return Weapon("Iron Dagger", 2)
    
    config = ConfigParser()
    config.read(config_file)
    
    weapons = []
    for section in config.sections():
        if section.startswith('weapon_'):
            weapon_name = config.get(section, 'name')
            attack_value = config.getint(section, 'attack_value')
            weapons.append(Weapon(weapon_name, attack_value))
    
    return random.choice(weapons) if weapons else Weapon("Iron Dagger", 2)


def load_random_armor_from_config():
    """Load a random armor from armor.cfg."""
    from configparser import ConfigParser
    from pathlib import Path
    import random
    
    # Get path to armor.cfg
    config_file = Path(__file__).parent.parent / "data" / "armor.cfg"
    
    if not config_file.exists():
        # Fallback to basic armor if config doesn't exist
        return Armor("Leather Armor", 1)
    
    config = ConfigParser()
    config.read(config_file)
    
    armors = []
    for section in config.sections():
        if section.startswith('armor_'):
            armor_name = config.get(section, 'name')
            defense_value = config.getint(section, 'defense_value')
            armors.append(Armor(armor_name, defense_value))
    
    return random.choice(armors) if armors else Armor("Leather Armor", 1)


def create_starting_weapon():
    """Create a random starting weapon from config or basic fallback."""
    return load_random_weapon_from_config()


def create_starting_armor():
    """Create a random starting armor from config or basic fallback."""
    return load_random_armor_from_config()


def create_starting_spell():
    """Create a basic starting spell."""
    spell = Spell("Spark", "basic")
    return spell


def create_hp_potion():
    """Create an HP potion."""
    return Potion("HP Potion", "hp", value=random.randint(3, 5))


def create_mana_potion():
    """Create a Mana potion."""
    return Potion("Mana Potion", "mana", value=random.randint(2, 4))
