#!/usr/bin/env python3
"""Generate monsters using names from names.list and save to data/monsters.cfg"""

import random
from pathlib import Path


def load_names(names_file):
    """Load names from names.list file."""
    with open(names_file, 'r') as f:
        names = [line.strip() for line in f if line.strip()]
    return names


def generate_monster(name):
    """Generate a monster with randomized stats."""
    monster = {
        'name': name,
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
    return monster


def generate_monsters(names, count=10):
    """Generate a list of monsters."""
    selected_names = random.sample(names, min(count, len(names)))
    monsters = [generate_monster(name) for name in selected_names]
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
            f.write("\n")
    
    print(f"✓ Generated {len(monsters)} monsters and saved to {output_file}")


if __name__ == "__main__":
    # Get paths relative to this script
    script_dir = Path(__file__).parent.parent
    names_file = script_dir / "data" / "names.list"
    output_file = script_dir / "data" / "monsters.cfg"
    
    # Load names and generate monsters
    names = load_names(names_file)
    monsters = generate_monsters(names, count=10)
    save_monsters_cfg(output_file, monsters)
    
    # Print generated monsters for verification
    print("\nGenerated monsters:")
    for i, monster in enumerate(monsters, 1):
        print(f"  {i}. {monster['name']} (Level {monster['level']}, HP: {monster['hp']}, XP: {monster['xp']})")
