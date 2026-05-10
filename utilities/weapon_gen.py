#!/usr/bin/env python3
"""Generate weapons and save to data/weapons.cfg"""

import random
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


def generate_weapon():
    """Generate a random weapon with stats."""
    weapon = {
        'name': generate_weapon_name(),
        'attack_value': random.randint(3, 12),
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
        print(f"  {i}. {weapon['name']} (ATK:{weapon['attack_value']})")
