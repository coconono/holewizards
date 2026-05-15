#!/usr/bin/env python3
"""Generate monsters using names from names.list and save to data/monsters.cfg"""

import random
from pathlib import Path
from configparser import ConfigParser


def load_names(names_file):
    """Load names from names.list file, removing duplicates."""
    with open(names_file, 'r') as f:
        names = [line.strip() for line in f if line.strip()]
    # Remove duplicates while preserving order
    seen = set()
    unique_names = []
    for name in names:
        if name not in seen:
            unique_names.append(name)
            seen.add(name)
    return unique_names


def _load_config_items(config_file, section_prefix, item_keys):
    """Generic config loader for items (weapons, armor, spells).
    
    Args:
        config_file: Path to config file
        section_prefix: Prefix for sections (e.g., 'weapon_', 'armor_')
        item_keys: List of keys to extract from config (e.g., ['name', 'attack_value'])
    
    Returns:
        List of dictionaries with requested keys
    """
    if not Path(config_file).exists():
        return []
    
    config = ConfigParser()
    config.read(config_file)
    
    items = []
    for section in config.sections():
        if section.startswith(section_prefix):
            item = {}
            for key in item_keys:
                fallback = 0 if key != 'name' else 'Unknown'
                try:
                    value = config.get(section, key)
                    # Try to convert to int if it looks like a number
                    if key != 'name' and key != 'level':
                        item[key] = int(value)
                    else:
                        item[key] = value
                except (ValueError, Exception):
                    item[key] = fallback
            items.append(item)
    
    return items


def load_weapons(weapons_file):
    """Load weapons from weapons.cfg file."""
    return _load_config_items(weapons_file, 'weapon_', ['name', 'attack_value'])


def load_armor(armor_file):
    """Load armor from armor.cfg file."""
    return _load_config_items(armor_file, 'armor_', ['name', 'defense_value'])


def load_spells(spells_file):
    """Load spells from spells.cfg file."""
    return _load_config_items(spells_file, 'spell_', ['name', 'level'])


def generate_monster(name, weapons_list=None, armor_list=None, spells_list=None):
    """Generate a monster with randomized stats and optional random weapon/armor/potions/spells."""
    monster = {
        'name': name.capitalize(),  # Capitalize first letter
        'description': "insert funny text here",
        'hp': random.randint(5, 12),
        'mana': random.randint(1, 5),
        'xp': random.randint(1, 10),
        'level': random.randint(1, 3),
        'view_distance': 5,
        'reinforcement': [random.randint(1, 10) for _ in range(10)],  # 10 action weights (1-10)
    }
    monster['max_hp'] = monster['hp']
    monster['max_mana'] = monster['mana']
    
    # Randomly assign a weapon to about 50% of monsters
    if weapons_list and random.random() < 0.5:
        weapon = random.choice(weapons_list)
        monster['weapon'] = weapon['name']
        monster['weapon_attack'] = weapon['attack_value']
    else:
        monster['weapon'] = None
        monster['weapon_attack'] = 0
    
    # Randomly assign armor to about 50% of monsters
    if armor_list and random.random() < 0.5:
        armor = random.choice(armor_list)
        monster['armor'] = armor['name']
        monster['armor_defense'] = armor['defense_value']
    else:
        monster['armor'] = None
        monster['armor_defense'] = 0
    
    # Add random potions (0-10 each)
    monster['hp_potions'] = random.randint(0, 10)
    monster['mana_potions'] = random.randint(0, 10)
    
    # Randomly assign a spell to about 50% of monsters
    if spells_list and random.random() < 0.5:
        spell = random.choice(spells_list)
        monster['spell'] = spell['name']
    else:
        monster['spell'] = None
    
    return monster


def generate_monsters(names, count=10, weapons_list=None, armor_list=None, spells_list=None):
    """Generate a list of monsters with unique names and optional random weapons/armor/potions/spells."""
    # Ensure count doesn't exceed available unique names
    actual_count = min(count, len(names))
    selected_names = random.sample(names, actual_count)
    monsters = [generate_monster(name, weapons_list, armor_list, spells_list) for name in selected_names]
    return monsters


def save_monsters_cfg(output_file, monsters):
    """Save monsters to a config file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        for i, monster in enumerate(monsters):
            f.write(f"[monster_{i}]\n")
            f.write(f"name={monster['name']}\n")
            f.write(f"description={monster['description']}\n")
            f.write(f"hp={monster['hp']}\n")
            f.write(f"max_hp={monster['max_hp']}\n")
            f.write(f"mana={monster['mana']}\n")
            f.write(f"max_mana={monster['max_mana']}\n")
            f.write(f"xp={monster['xp']}\n")
            f.write(f"level={monster['level']}\n")
            f.write(f"view_distance={monster['view_distance']}\n")
            f.write(f"reinforcement={','.join(map(str, monster['reinforcement']))}\n")
            if monster.get('weapon'):
                f.write(f"weapon={monster['weapon']}\n")
                f.write(f"weapon_attack={monster['weapon_attack']}\n")
            if monster.get('armor'):
                f.write(f"armor={monster['armor']}\n")
                f.write(f"armor_defense={monster['armor_defense']}\n")
            if monster.get('hp_potions'):
                f.write(f"hp_potions={monster['hp_potions']}\n")
            if monster.get('mana_potions'):
                f.write(f"mana_potions={monster['mana_potions']}\n")
            if monster.get('spell'):
                f.write(f"spell={monster['spell']}\n")
            f.write("\n")
    
    print(f"✓ Generated {len(monsters)} monsters and saved to {output_file}")


if __name__ == "__main__":
    # Get paths relative to this script
    script_dir = Path(__file__).parent.parent
    names_file = script_dir / "data" / "names.list"
    weapons_file = script_dir / "data" / "weapons.cfg"
    armor_file = script_dir / "data" / "armor.cfg"
    spells_file = script_dir / "data" / "spells.cfg"
    output_file = script_dir / "data" / "monsters.cfg"
    
    # Load names, weapons, armor, and spells
    names = load_names(names_file)
    weapons = load_weapons(weapons_file)
    armors = load_armor(armor_file)
    spells = load_spells(spells_file)
    
    # Generate monsters with weapons, armor, potions, and spells
    monsters = generate_monsters(names, count=10, 
                                weapons_list=weapons if weapons else None,
                                armor_list=armors if armors else None,
                                spells_list=spells if spells else None)
    save_monsters_cfg(output_file, monsters)
    
    # Print generated monsters for verification
    print("\nGenerated monsters:")
    for i, monster in enumerate(monsters, 1):
        weapon_info = f" + {monster.get('weapon', 'None')}" if monster.get('weapon') else ""
        armor_info = f" + {monster.get('armor', 'None')}" if monster.get('armor') else ""
        potions_info = f" + Potions: HP({monster.get('hp_potions', 0)})/Mana({monster.get('mana_potions', 0)})" if (monster.get('hp_potions', 0) or monster.get('mana_potions', 0)) else ""
        spell_info = f" + {monster.get('spell', 'None')}" if monster.get('spell') else ""
        print(f"  {i}. {monster['name']} (Level {monster['level']}, HP: {monster['hp']}, XP: {monster['xp']}){weapon_info}{armor_info}{potions_info}{spell_info}")
