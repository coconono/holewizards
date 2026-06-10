#!/usr/bin/env python3
"""Generate consumable items and save to data/items.cfg"""

import json
from pathlib import Path


def generate_items():
    """Generate consumable items (potions, scrolls, etc.)."""
    items = []
    
    # Health Potions
    items.append({
        'id': 'health_potion_small',
        'name': 'Small Health Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 10,
        'mana_increase': 0,
        'equip_effect': {},
        'use_effect': {"type": "heal", "hp": 10},
        'attack_effect': {},
        'consumable': True,
        'description': 'A small red vial that restores health.'
    })
    
    items.append({
        'id': 'health_potion',
        'name': 'Health Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 20,
        'mana_increase': 0,
        'equip_effect': {},
        'use_effect': {"type": "heal", "hp": 20},
        'attack_effect': {},
        'consumable': True,
        'description': 'A red vial that restores health.'
    })
    
    items.append({
        'id': 'health_potion_large',
        'name': 'Large Health Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 50,
        'mana_increase': 0,
        'equip_effect': {},
        'use_effect': {"type": "heal", "hp": 50},
        'attack_effect': {},
        'consumable': True,
        'description': 'A large red vial that restores significant health.'
    })
    
    # Mana Potions
    items.append({
        'id': 'mana_potion_small',
        'name': 'Small Mana Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 0,
        'mana_increase': 10,
        'equip_effect': {},
        'use_effect': {"type": "mana_restore", "mana": 10},
        'attack_effect': {},
        'consumable': True,
        'description': 'A small blue vial that restores mana.'
    })
    
    items.append({
        'id': 'mana_potion',
        'name': 'Mana Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 0,
        'mana_increase': 20,
        'equip_effect': {},
        'use_effect': {"type": "mana_restore", "mana": 20},
        'attack_effect': {},
        'consumable': True,
        'description': 'A blue vial that restores mana.'
    })
    
    items.append({
        'id': 'mana_potion_large',
        'name': 'Large Mana Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 0,
        'mana_increase': 50,
        'equip_effect': {},
        'use_effect': {"type": "mana_restore", "mana": 50},
        'attack_effect': {},
        'consumable': True,
        'description': 'A large blue vial that restores significant mana.'
    })
    
    # Elemental Buff Potions
    items.append({
        'id': 'fire_potion',
        'name': 'Fire Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 0,
        'mana_increase': 0,
        'equip_effect': {},
        'use_effect': {"type": "buff_attack", "element": "fire", "damage": 10, "duration": 1, "requires_weapon": True},
        'attack_effect': {},
        'consumable': True,
        'description': 'Imbues your weapon with fire for one attack.'
    })
    
    items.append({
        'id': 'ice_potion',
        'name': 'Ice Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 0,
        'mana_increase': 0,
        'equip_effect': {},
        'use_effect': {"type": "buff_attack", "element": "ice", "damage": 10, "duration": 1, "requires_weapon": True},
        'attack_effect': {},
        'consumable': True,
        'description': 'Imbues your weapon with ice for one attack.'
    })
    
    items.append({
        'id': 'lightning_potion',
        'name': 'Lightning Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 0,
        'mana_increase': 0,
        'equip_effect': {},
        'use_effect': {"type": "buff_attack", "element": "lightning", "damage": 12, "duration": 1, "requires_weapon": True},
        'attack_effect': {},
        'consumable': True,
        'description': 'Imbues your weapon with lightning for one attack.'
    })
    
    # Stat Boost Potions
    items.append({
        'id': 'strength_potion',
        'name': 'Strength Potion',
        'type': 'consumable',
        'attack_value': 0,
        'defend_value': 0,
        'hp_increase': 0,
        'mana_increase': 0,
        'equip_effect': {},
        'use_effect': {"type": "buff_attack", "element": "physical", "damage": 5, "duration": 3, "requires_weapon": False},
        'attack_effect': {},
        'consumable': True,
        'description': 'Temporarily increases attack power for 3 attacks.'
    })
    
    return items


def save_items_cfg(output_file, items):
    """Save items to a config file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        for item in items:
            f.write(f"[{item['id']}]\n")
            f.write(f"name={item['name']}\n")
            f.write(f"type={item['type']}\n")
            f.write(f"attack_value={item['attack_value']}\n")
            f.write(f"defend_value={item['defend_value']}\n")
            f.write(f"hp_increase={item['hp_increase']}\n")
            f.write(f"mana_increase={item['mana_increase']}\n")
            f.write(f"equip_effect={json.dumps(item['equip_effect'])}\n")
            f.write(f"use_effect={json.dumps(item['use_effect'])}\n")
            f.write(f"attack_effect={json.dumps(item['attack_effect'])}\n")
            f.write(f"consumable={item['consumable']}\n")
            if item['description']:
                f.write(f"description={item['description']}\n")
            f.write("\n")
    
    print(f"✓ Generated {len(items)} consumable items and saved to {output_file}")


if __name__ == "__main__":
    # Get paths relative to this script
    script_dir = Path(__file__).parent.parent
    output_file = script_dir / "data" / "items.cfg"
    
    # Generate items
    items = generate_items()
    save_items_cfg(output_file, items)
    
    # Print generated items for verification
    print("\nGenerated items:")
    for i, item in enumerate(items, 1):
        effect_desc = ""
        use_effect = item['use_effect']
        if use_effect:
            effect_type = use_effect.get('type', '')
            if effect_type == 'heal':
                effect_desc = f" [+{use_effect.get('hp')} HP]"
            elif effect_type == 'mana_restore':
                effect_desc = f" [+{use_effect.get('mana')} Mana]"
            elif effect_type == 'buff_attack':
                elem = use_effect.get('element')
                dmg = use_effect.get('damage')
                dur = use_effect.get('duration')
                effect_desc = f" [+{dmg} {elem} x{dur}]"
        print(f"  {i}. {item['name']}{effect_desc}")
