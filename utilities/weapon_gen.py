#!/usr/bin/env python3
"""Generate weapons and save to data/weapons.cfg"""

import random
import json
from pathlib import Path


# Weapon name templates
WEAPON_ADJECTIVES = [
    "Iron", "Steel", "Bronze", "Silver", "Golden", "Cursed", "Holy", "Enchanted",
    "Ancient", "Rusty", "Sharp", "Dull", "Flaming", "Frozen", "Poisoned", "Blessed"
]

WEAPON_TYPES = [
    "Sword", "Axe", "Mace", "Spear", "Dagger", "Hammer", "Flail", "Bow",
    "Staff", "Halberd", "Broadsword", "Shortsword", "Cleaver", "Pike", "Saber", "Club"
]


def generate_weapon_name():
    """Generate a random weapon name."""
    adjective = random.choice(WEAPON_ADJECTIVES)
    weapon_type = random.choice(WEAPON_TYPES)
    return f"{adjective} {weapon_type}"


def generate_attack_effect(weapon_name):
    """Generate an attack effect based on weapon name."""
    name_lower = weapon_name.lower()
    
    # Elemental weapons
    if 'flaming' in name_lower or 'fire' in name_lower:
        return {"type": "elemental", "element": "fire", "damage": random.randint(5, 10)}
    elif 'frozen' in name_lower or 'ice' in name_lower:
        return {"type": "elemental", "element": "ice", "damage": random.randint(5, 10)}
    elif 'lightning' in name_lower or 'thunder' in name_lower:
        return {"type": "elemental", "element": "lightning", "damage": random.randint(5, 10)}
    
    # Status effect weapons
    elif 'poisoned' in name_lower or 'poison' in name_lower:
        return {"type": "status", "status": "poison", "damage_per_turn": random.randint(3, 7), "duration": 3}
    elif 'cursed' in name_lower or 'dark' in name_lower:
        return {"type": "status", "status": "curse", "damage_per_turn": random.randint(2, 5), "duration": 4}
    
    # Lifesteal weapons
    elif 'vampire' in name_lower or 'blood' in name_lower:
        return {"type": "lifesteal", "amount": random.randint(3, 7)}
    
    # 30% chance for special weapons to have effects anyway
    elif random.random() < 0.3:
        effect_type = random.choice(['elemental', 'status', 'lifesteal'])
        if effect_type == 'elemental':
            element = random.choice(['fire', 'ice', 'lightning'])
            return {"type": "elemental", "element": element, "damage": random.randint(3, 8)}
        elif effect_type == 'status':
            status = random.choice(['poison', 'burn'])
            return {"type": "status", "status": status, "damage_per_turn": random.randint(2, 5), "duration": 3}
        else:
            return {"type": "lifesteal", "amount": random.randint(2, 5)}
    
    return {}


def generate_weapon():
    """Generate a random weapon with stats and effects."""
    name = generate_weapon_name()
    weapon = {
        'name': name,
        'attack_value': random.randint(3, 12),
        'attack_effect': generate_attack_effect(name),
        'equip_effect': {},
        'description': ''  # Placeholder for human-written descriptions
    }
    return weapon


def generate_weapons(count=20):
    """Generate a list of unique weapons."""
    weapons = []
    used_names = set()
    
    # Keep generating until we have the requested count of unique weapons
    while len(weapons) < count:
        weapon = generate_weapon()
        if weapon['name'] not in used_names:
            weapons.append(weapon)
            used_names.add(weapon['name'])
    
    return weapons


def save_weapons_cfg(output_file, weapons):
    """Save weapons to a config file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        for i, weapon in enumerate(weapons):
            f.write(f"[weapon_{i}]\n")
            f.write(f"name={weapon['name']}\n")
            f.write(f"attack_value={weapon['attack_value']}\n")
            f.write(f"attack_effect={json.dumps(weapon['attack_effect'])}\n")
            f.write(f"equip_effect={json.dumps(weapon['equip_effect'])}\n")
            if weapon['description']:
                f.write(f"description={weapon['description']}\n")
            f.write("\n")
    
    print(f"✓ Generated {len(weapons)} weapons and saved to {output_file}")


if __name__ == "__main__":
    # Get paths relative to this script
    script_dir = Path(__file__).parent.parent
    output_file = script_dir / "data" / "weapons.cfg"
    
    # Generate weapons
    weapons = generate_weapons(count=20)
    save_weapons_cfg(output_file, weapons)
    
    # Print generated weapons for verification
    print("\nGenerated weapons:")
    for i, weapon in enumerate(weapons, 1):
        effect_desc = ""
        if weapon['attack_effect']:
            effect_type = weapon['attack_effect'].get('type', '')
            if effect_type == 'elemental':
                elem = weapon['attack_effect'].get('element')
                dmg = weapon['attack_effect'].get('damage')
                effect_desc = f" [+{dmg} {elem}]"
            elif effect_type == 'status':
                status = weapon['attack_effect'].get('status')
                effect_desc = f" [{status}]"
            elif effect_type == 'lifesteal':
                amt = weapon['attack_effect'].get('amount')
                effect_desc = f" [lifesteal {amt}]"
        print(f"  {i}. {weapon['name']} (ATK:{weapon['attack_value']}){effect_desc}")
