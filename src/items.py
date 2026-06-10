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
        self.effects = []  # List of effects (legacy)
        
        # New comprehensive effect system
        self.equip_effect = {}  # Applied when equipped
        self.use_effect = {}  # Applied when used/consumed
        self.attack_effect = {}  # Applied during attacks
        self.consumable = False  # Whether item is destroyed on use
        self.description = ""  # Flavor text

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

    def apply_equip_effect(self, character, equipping=True):
        """Apply or reverse EQUIP effect on a character.
        
        Args:
            character: The character to apply effects to
            equipping: True when equipping, False when unequipping
        """
        multiplier = 1 if equipping else -1
        
        # Handle legacy hp/mana increase (for backwards compatibility)
        if self.hp_increase != 0:
            character.max_hp += (self.hp_increase * multiplier)
            # Keep current HP in bounds
            character.hp = max(0, min(character.hp, character.max_hp))
        
        if self.mana_increase != 0:
            character.max_mana += (self.mana_increase * multiplier)
            # Keep current mana in bounds
            character.mana = max(0, min(character.mana, character.max_mana))
        
        # Handle new equip_effect format
        if self.equip_effect and isinstance(self.equip_effect, dict):
            effect_type = self.equip_effect.get('type', '')
            
            if effect_type == 'stat_mod':
                # Stat modifications
                if 'defense' in self.equip_effect:
                    character.defense_bonus = getattr(character, 'defense_bonus', 0)
                    character.defense_bonus += (self.equip_effect['defense'] * multiplier)
                if 'attack' in self.equip_effect:
                    character.attack_bonus = getattr(character, 'attack_bonus', 0)
                    character.attack_bonus += (self.equip_effect['attack'] * multiplier)
                if 'max_hp' in self.equip_effect:
                    character.max_hp += (self.equip_effect['max_hp'] * multiplier)
                    character.hp = max(0, min(character.hp, character.max_hp))
                if 'max_mana' in self.equip_effect:
                    character.max_mana += (self.equip_effect['max_mana'] * multiplier)
                    character.mana = max(0, min(character.mana, character.max_mana))
        
        return True

    def apply_use_effect(self, character, has_weapon_equipped=True):
        """Apply USE effect to a character.
        
        Args:
            character: The character to apply effects to
            has_weapon_equipped: Whether character has a weapon equipped (for conditional buffs)
        
        Returns:
            tuple: (success: bool, message: str, buff_info: dict or None)
        """
        # Handle legacy hp/mana increase (for backwards compatibility)
        hp_restored = 0
        mana_restored = 0
        
        if self.hp_increase > 0:
            hp_before = character.hp
            character.heal(self.hp_increase)
            hp_restored = character.hp - hp_before
        
        if self.mana_increase > 0:
            mana_before = character.mana
            character.restore_mana(self.mana_increase)
            mana_restored = character.mana - mana_before
        
        # Build message
        messages = []
        if hp_restored > 0:
            messages.append(f"You restore {hp_restored} HP!")
        if mana_restored > 0:
            messages.append(f"You restore {mana_restored} Mana!")
        
        # Handle new use_effect format
        buff_info = None
        if self.use_effect and isinstance(self.use_effect, dict):
            effect_type = self.use_effect.get('type', '')
            
            if effect_type == 'heal':
                hp_heal = self.use_effect.get('hp', 0)
                hp_before = character.hp
                character.heal(hp_heal)
                hp_restored = character.hp - hp_before
                if hp_restored > 0:
                    messages.append(f"You restore {hp_restored} HP!")
                elif character.hp == character.max_hp:
                    messages.append("You're already at full health!")
            
            elif effect_type == 'mana_restore':
                mana_heal = self.use_effect.get('mana', 0)
                mana_before = character.mana
                character.restore_mana(mana_heal)
                mana_restored = character.mana - mana_before
                if mana_restored > 0:
                    messages.append(f"You restore {mana_restored} Mana!")
                elif character.mana == character.max_mana:
                    messages.append("You're already at full mana!")
            
            elif effect_type == 'buff_attack':
                # Elemental attack buff
                requires_weapon = self.use_effect.get('requires_weapon', True)
                
                if requires_weapon and not has_weapon_equipped:
                    # Damage the player instead
                    damage = self.use_effect.get('damage', 10)
                    character.take_damage(damage)
                    messages.append(f"You take {damage} fire damage because you have no weapon equipped!")
                    return (True, "\n".join(messages), None)
                else:
                    # Apply buff
                    element = self.use_effect.get('element', 'fire')
                    damage = self.use_effect.get('damage', 10)
                    duration = self.use_effect.get('duration', 1)
                    
                    buff_info = {
                        'type': 'attack_buff',
                        'element': element,
                        'damage': damage,
                        'duration': duration
                    }
                    messages.append(f"Your next {duration} attack(s) will deal an additional {damage} {element} damage!")
        
        message = "\n".join(messages) if messages else "Nothing happens."
        return (True, message, buff_info)

    def apply_attack_effect(self, attacker, target):
        """Apply ATTACK effect during an attack.
        
        Args:
            attacker: The character attacking
            target: The target being attacked
        
        Returns:
            dict: Effect results with keys 'extra_damage', 'damage_type', 'status_applied', 'lifesteal'
        """
        result = {
            'extra_damage': 0,
            'damage_type': None,
            'status_applied': None,
            'lifesteal': 0
        }
        
        if not self.attack_effect or not isinstance(self.attack_effect, dict):
            return result
        
        effect_type = self.attack_effect.get('type', '')
        
        if effect_type == 'elemental':
            # Elemental damage
            result['extra_damage'] = self.attack_effect.get('damage', 0)
            result['damage_type'] = self.attack_effect.get('element', 'fire')
        
        elif effect_type == 'status':
            # Apply status effect (poison, burn, etc.)
            status_type = self.attack_effect.get('status', 'poison')
            damage_per_turn = self.attack_effect.get('damage_per_turn', 5)
            duration = self.attack_effect.get('duration', 3)
            
            result['status_applied'] = {
                'type': status_type,
                'damage': damage_per_turn,
                'duration': duration
            }
        
        elif effect_type == 'lifesteal':
            # Lifesteal effect
            result['lifesteal'] = self.attack_effect.get('amount', 5)
        
        return result
    
    def get_stats_display(self):
        """Get formatted stats for display."""
        lines = []
        lines.append(f"Item: {self.name}")
        lines.append(f"Type: {self.item_type.capitalize()}")
        lines.append(f"Attack Value: +{self.attack_value}" if self.attack_value else "Attack Value: +0")
        lines.append(f"Defend Value: +{self.defense_value}" if self.defense_value else "Defend Value: +0")
        lines.append(f"HP Increase: +{self.hp_increase}" if self.hp_increase else "HP Increase: +0")
        lines.append(f"Mana Increase: +{self.mana_increase}" if self.mana_increase else "Mana Increase: +0")
        
        # EQUIP Effect
        if self.equip_effect and self.equip_effect != {}:
            equip_desc = self._format_effect_description(self.equip_effect)
            lines.append(f"EQUIP Effect: {equip_desc}")
        else:
            lines.append("EQUIP Effect: None")
        
        # USE Effect
        if self.use_effect and self.use_effect != {}:
            use_desc = self._format_effect_description(self.use_effect)
            lines.append(f"USE Effect: {use_desc}")
        else:
            lines.append("USE Effect: None")
        
        # ATTACK Effect
        if self.attack_effect and self.attack_effect != {}:
            attack_desc = self._format_effect_description(self.attack_effect)
            lines.append(f"ATTACK Effect: {attack_desc}")
        else:
            lines.append("ATTACK Effect: None")
        
        return "\n".join(lines)
    
    def _format_effect_description(self, effect):
        """Format an effect dict into readable description."""
        if not effect or not isinstance(effect, dict):
            return "None"
        
        effect_type = effect.get('type', '')
        
        if effect_type == 'stat_mod':
            parts = []
            if 'defense' in effect:
                parts.append(f"Defense {effect['defense']:+d}")
            if 'attack' in effect:
                parts.append(f"Attack {effect['attack']:+d}")
            if 'max_hp' in effect:
                parts.append(f"Max HP {effect['max_hp']:+d}")
            if 'max_mana' in effect:
                parts.append(f"Max Mana {effect['max_mana']:+d}")
            return ", ".join(parts) if parts else "None"
        
        elif effect_type == 'heal':
            hp = effect.get('hp', 0)
            return f"Restores {hp} HP when consumed"
        
        elif effect_type == 'mana_restore':
            mana = effect.get('mana', 0)
            return f"Restores {mana} Mana when consumed"
        
        elif effect_type == 'buff_attack':
            element = effect.get('element', 'fire')
            damage = effect.get('damage', 10)
            duration = effect.get('duration', 1)
            return f"Adds +{damage} {element} damage to next {duration} attack(s)"
        
        elif effect_type == 'elemental':
            element = effect.get('element', 'fire')
            damage = effect.get('damage', 10)
            return f"Deals +{damage} {element} damage per attack"
        
        elif effect_type == 'status':
            status = effect.get('status', 'poison')
            damage = effect.get('damage_per_turn', 5)
            duration = effect.get('duration', 3)
            return f"Applies {status} ({damage} damage/turn for {duration} turns)"
        
        elif effect_type == 'lifesteal':
            amount = effect.get('amount', 5)
            return f"Heals {amount} HP on successful hit"
        
        return str(effect)

    def __repr__(self):
        return f"{self.name}"


class Weapon(Item):
    """A weapon item that deals damage."""

    def __init__(self, name, attack_value):
        """Initialize a weapon."""
        super().__init__(name, "weapon", attack_value=attack_value)
        self.consumable = False

    def __repr__(self):
        return f"{self.name} (Weapon, ATK:{self.get_attack_value()})"


class Armor(Item):
    """An armor item that provides defense."""

    def __init__(self, name, defense_value):
        """Initialize armor."""
        super().__init__(name, "armor", defense_value=defense_value)
        self.consumable = False

    def __repr__(self):
        return f"{self.name} (Armor, DEF:{self.get_defense_value()})"


class Potion(Item):
    """A consumable potion."""

    def __init__(self, name, potion_type="hp", value=0):
        """Initialize a potion."""
        super().__init__(name, "consumable")
        self.potion_type = potion_type  # "hp" or "mana"
        self.consumable = True
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
    from resource_path import get_data_path
    import random
    import json
    
    # Get path to weapons.cfg
    config_file = get_data_path('weapons.cfg')
    
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
            weapon = Weapon(weapon_name, attack_value)
            
            # Load optional new fields
            if config.has_option(section, 'description'):
                weapon.description = config.get(section, 'description')
            
            if config.has_option(section, 'attack_effect'):
                try:
                    effect_str = config.get(section, 'attack_effect')
                    if effect_str and effect_str != '{}':
                        weapon.attack_effect = json.loads(effect_str)
                except (json.JSONDecodeError, ValueError):
                    pass  # Skip malformed effects
            
            if config.has_option(section, 'equip_effect'):
                try:
                    effect_str = config.get(section, 'equip_effect')
                    if effect_str and effect_str != '{}':
                        weapon.equip_effect = json.loads(effect_str)
                except (json.JSONDecodeError, ValueError):
                    pass
            
            weapons.append(weapon)
    
    return random.choice(weapons) if weapons else Weapon("Iron Dagger", 2)


def load_random_armor_from_config():
    """Load a random armor from armor.cfg."""
    from configparser import ConfigParser
    from resource_path import get_data_path
    import random
    import json
    
    # Get path to armor.cfg
    config_file = get_data_path('armor.cfg')
    
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
            armor = Armor(armor_name, defense_value)
            
            # Load optional new fields
            if config.has_option(section, 'description'):
                armor.description = config.get(section, 'description')
            
            if config.has_option(section, 'equip_effect'):
                try:
                    effect_str = config.get(section, 'equip_effect')
                    if effect_str and effect_str != '{}':
                        armor.equip_effect = json.loads(effect_str)
                except (json.JSONDecodeError, ValueError):
                    pass  # Skip malformed effects
            
            if config.has_option(section, 'hp_increase'):
                armor.hp_increase = config.getint(section, 'hp_increase')
            
            if config.has_option(section, 'mana_increase'):
                armor.mana_increase = config.getint(section, 'mana_increase')
            
            armors.append(armor)
    
    return random.choice(armors) if armors else Armor("Leather Armor", 1)


def load_random_spell_from_config():
    """Load a random spell from spells.cfg."""
    from configparser import ConfigParser
    from resource_path import get_data_path
    import random
    
    # Get path to spells.cfg
    config_file = get_data_path('spells.cfg')
    
    if not config_file.exists():
        # Fallback to basic spell if config doesn't exist
        return Spell("Spark", "basic")
    
    config = ConfigParser()
    config.read(config_file)
    
    spells = []
    for section in config.sections():
        if section.startswith('spell_'):
            spell_name = config.get(section, 'name')
            spell_level = config.get(section, 'level', fallback='basic')
            spell = Spell(spell_name, spell_level)
            
            # Apply effects from config
            effects_str = config.get(section, 'effects', fallback='')
            effects = [e.strip() for e in effects_str.split(',') if e.strip()]
            
            for effect in effects:
                if effect == "attack":
                    spell.attack_value = config.getint(section, 'attack', fallback=0)
                elif effect == "defend":
                    spell.defense_value = config.getint(section, 'defense', fallback=0)
                elif effect == "heal":
                    spell.hp_increase = config.getint(section, 'heal', fallback=0)
                elif effect == "mana_restore":
                    spell.mana_increase = config.getint(section, 'mana_restore', fallback=0)
            
            spell.effects = effects
            spell.mana_cost = config.getint(section, 'mana_cost', fallback=1)
            spells.append(spell)
    
    return random.choice(spells) if spells else Spell("Spark", "basic")


def create_starting_weapon():
    """Create a random starting weapon from config or basic fallback."""
    return load_random_weapon_from_config()


def create_starting_armor():
    """Create a random starting armor from config or basic fallback."""
    return load_random_armor_from_config()


def create_starting_spell():
    """Create a random starting spell from config or basic fallback."""
    return load_random_spell_from_config()


def create_hp_potion():
    """Create an HP potion."""
    return Potion("HP Potion", "hp", value=random.randint(3, 5))


def create_mana_potion():
    """Create a Mana potion."""
    return Potion("Mana Potion", "mana", value=random.randint(2, 4))
