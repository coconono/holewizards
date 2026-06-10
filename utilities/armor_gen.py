#!/usr/bin/env python3
"""Generate armor and save to data/armor.cfg"""

import random
import json
from pathlib import Path


# Armor name templates
ARMOR_ADJECTIVES = [
    "Iron", "Steel", "Bronze", "Silver", "Golden", "Cursed", "Holy", "Enchanted",
    "Ancient", "Leather", "Reinforced", "Heavy", "Light", "Blessed", "Shadowy", "Crystal"
]

ARMOR_TYPES = [
    "Armor", "Plate", "Mail", "Robes", "Leather", "Chainmail", "Breastplate", "Helm",
    "Gauntlets", "Boots", "Chestplate", "Leggings", "Cuirass", "Hauberk", "Jerkin", "Coat"
]


def generate_armor_name():
    """Generate a random armor name."""
    adjective = random.choice(ARMOR_ADJECTIVES)
    armor_type = random.choice(ARMOR_TYPES)
    return f"{adjective} {armor_type}"


def generate_equip_effect(armor_name, defense_value):
    """Generate an equip effect based on armor name and stats."""
    name_lower = armor_name.lower()
    effect = {"type": "stat_mod"}
    
    # Heavy armor: high defense, low HP
    if 'heavy' in name_lower or 'plate' in name_lower or 'iron' in name_lower:
        if defense_value >= 7:
            effect['max_hp'] = random.randint(-5, -2)
            effect['defense'] = random.randint(1, 3)
        return effect
    
    # Light armor: balanced or mana bonus
    elif 'light' in name_lower or 'leather' in name_lower:
        if random.random() < 0.5:
            effect['max_mana'] = random.randint(2, 5)
        return effect
    
    # Magic robes: high mana, low defense
    elif 'robes' in name_lower or 'enchanted' in name_lower or 'crystal' in name_lower:
        effect['max_mana'] = random.randint(5, 10)
        effect['defense'] = random.randint(-2, 0)
        return effect
    
    # Blessed/Holy: HP bonus
    elif 'blessed' in name_lower or 'holy' in name_lower:
        effect['max_hp'] = random.randint(3, 7)
        return effect
    
    # 20% chance for other armor to have minor effects
    elif random.random() < 0.2:
        bonus_type = random.choice(['hp', 'mana', 'defense'])
        if bonus_type == 'hp':
            effect['max_hp'] = random.randint(1, 3)
        elif bonus_type == 'mana':
            effect['max_mana'] = random.randint(1, 3)
        else:
            effect['defense'] = random.randint(1, 2)
        return effect
    
    return {}


def generate_armor():
    """Generate a random armor with stats and effects."""
    name = generate_armor_name()
    defense_value = random.randint(2, 10)
    armor = {
        'name': name,
        'defense_value': defense_value,
        'equip_effect': generate_equip_effect(name, defense_value),
        'hp_increase': 0,
        'mana_increase': 0,
        'description': ''  # Placeholder for human-written descriptions
    }
    return armor


def generate_armors(count=20):
    """Generate a list of unique armor pieces."""
    armors = []
    used_names = set()
    
    # Keep generating until we have the requested count of unique armor
    while len(armors) < count:
        armor = generate_armor()
        if armor['name'] not in used_names:
            armors.append(armor)
            used_names.add(armor['name'])
    
    return armors


def save_armors_cfg(output_file, armors):
    """Save armor to a config file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        for i, armor in enumerate(armors):
            f.write(f"[armor_{i}]\n")
            f.write(f"name={armor['name']}\n")
            f.write(f"defense_value={armor['defense_value']}\n")
            f.write(f"equip_effect={json.dumps(armor['equip_effect'])}\n")
            f.write(f"hp_increase={armor['hp_increase']}\n")
            f.write(f"mana_increase={armor['mana_increase']}\n")
            if armor['description']:
                f.write(f"description={armor['description']}\n")
            f.write("\n")
    
    print(f"✓ Generated {len(armors)} armor pieces and saved to {output_file}")


if __name__ == "__main__":
    # Get paths relative to this script
    script_dir = Path(__file__).parent.parent
    output_file = script_dir / "data" / "armor.cfg"
    
    # Generate armor
    armors = generate_armors(count=20)
    save_armors_cfg(output_file, armors)
    
    # Print generated armor for verification
    print("\nGenerated armor:")
    for i, armor in enumerate(armors, 1):
        effect_desc = ""
        if armor['equip_effect'] and armor['equip_effect'] != {"type": "stat_mod"}:
            effects = []
            effect = armor['equip_effect']
            if 'max_hp' in effect:
                effects.append(f"HP{effect['max_hp']:+d}")
            if 'max_mana' in effect:
                effects.append(f"Mana{effect['max_mana']:+d}")
            if 'defense' in effect and effect['defense'] != 0:
                effects.append(f"DEF{effect['defense']:+d}")
            if effects:
                effect_desc = f" [{', '.join(effects)}]"
        print(f"  {i}. {armor['name']} (DEF:{armor['defense_value']}){effect_desc}")
