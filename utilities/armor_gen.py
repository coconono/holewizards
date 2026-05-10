#!/usr/bin/env python3
"""Generate armor and save to data/armor.cfg"""

import random
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


def generate_armor():
    """Generate a random armor with stats."""
    armor = {
        'name': generate_armor_name(),
        'defense_value': random.randint(2, 10),
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
        print(f"  {i}. {armor['name']} (DEF:{armor['defense_value']})")
