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


# Preset items for initial inventory
def create_starting_weapon():
    """Create a basic starting weapon."""
    return Weapon("Iron Dagger", 2)


def create_starting_armor():
    """Create a basic starting armor."""
    return Armor("Leather Armor", 1)


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
