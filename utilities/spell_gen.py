#!/usr/bin/env python3
"""Generate spells and save to data/spells.cfg"""

import random
from pathlib import Path


def generate_spell(name, spell_level="basic"):
    """Generate a spell with random effects."""
    num_effects = {"basic": 1, "advanced": 2, "superior": 3}[spell_level]
    
    spell = {
        'name': name,
        'level': spell_level,
        'mana_cost': random.randint(1, num_effects + 2),
        'effects': [],
        'attack': 0,
        'defense': 0,
        'heal': 0,
        'mana_restore': 0,
    }
    
    # Generate random effects
    effect_types = ["attack", "defend", "heal", "mana_restore"]
    selected_effects = random.sample(effect_types, min(num_effects, len(effect_types)))
    
    for effect_type in selected_effects:
        spell['effects'].append(effect_type)
        if effect_type == "attack":
            spell['attack'] = random.randint(2, 8)
        elif effect_type == "defend":
            spell['defense'] = random.randint(1, 5)
        elif effect_type == "heal":
            spell['heal'] = random.randint(2, 6)
        elif effect_type == "mana_restore":
            spell['mana_restore'] = random.randint(1, 4)
    
    return spell


def generate_spells(count=20):
    """Generate a list of unique spells."""
    spell_names = [
        "Fireball", "Ice Spike", "Lightning Bolt", "Heal", "Mana Shield",
        "Dark Curse", "Holy Light", "Meteor Storm", "Teleport", "Time Warp",
        "Confusion", "Petrify", "Regenerate", "Force Push", "Summon",
        "Inferno", "Blizzard", "Thunder", "Blessing", "Annihilation"
    ]
    
    # Randomize levels
    spells = []
    spell_levels = ["basic", "basic", "basic", "basic", "basic",
                   "advanced", "advanced", "advanced", "advanced",
                   "superior", "superior", "superior"]
    
    levels = spell_levels + [random.choice(["basic", "advanced", "superior"]) 
                            for _ in range(count - len(spell_levels))]
    random.shuffle(levels)
    
    for i in range(min(count, len(spell_names))):
        spells.append(generate_spell(spell_names[i], levels[i]))
    
    return spells


def save_spells_cfg(output_file, spells):
    """Save spells to a config file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        for i, spell in enumerate(spells):
            f.write(f"[spell_{i}]\n")
            f.write(f"name={spell['name']}\n")
            f.write(f"level={spell['level']}\n")
            f.write(f"mana_cost={spell['mana_cost']}\n")
            f.write(f"effects={','.join(spell['effects'])}\n")
            if spell['attack'] > 0:
                f.write(f"attack={spell['attack']}\n")
            if spell['defense'] > 0:
                f.write(f"defense={spell['defense']}\n")
            if spell['heal'] > 0:
                f.write(f"heal={spell['heal']}\n")
            if spell['mana_restore'] > 0:
                f.write(f"mana_restore={spell['mana_restore']}\n")
            f.write("\n")
    
    print(f"✓ Generated {len(spells)} spells and saved to {output_file}")


if __name__ == "__main__":
    script_dir = Path(__file__).parent.parent
    output_file = script_dir / "data" / "spells.cfg"
    
    spells = generate_spells(count=20)
    save_spells_cfg(output_file, spells)
    
    print("\nGenerated spells:")
    for i, spell in enumerate(spells, 1):
        effects_str = ", ".join(spell['effects'])
        print(f"  {i}. {spell['name']} ({spell['level']}, Mana: {spell['mana_cost']}, Effects: {effects_str})")
