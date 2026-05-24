"""Test defeat/victory screen rendering."""

from ui import UI

def test_defeat_screen():
    """Test defeat screen rendering."""
    ui = UI()
    
    # Mock combat stats
    combat_stats = {
        'total_damage_dealt': 125,
        'total_damage_taken': 85,
        'monsters_defeated': 3,
        'healing_used': 45,
        'items_collected': 12,
        'turns_elapsed': 87,
        'attacks_made': 35,
        'chests_opened': 2,
        'killing_blow': {
            'attacker': 'Goblin_0',
            'target': 'You',
            'damage': 12
        }
    }
    
    # Test with message
    test_message = "you lost, try again"
    screen = ui.render_defeat_screen(combat_stats, message=test_message)
    print(screen)
    print("\n" + "="*70)
    print("✓ Defeat screen with message rendered successfully")

def test_victory_screen():
    """Test victory screen rendering."""
    ui = UI()
    
    # Mock combat stats
    combat_stats = {
        'total_damage_dealt': 342,
        'total_damage_taken': 156,
        'monsters_defeated': 8,
        'healing_used': 78,
        'items_collected': 24,
        'turns_elapsed': 213,
        'attacks_made': 89,
        'chests_opened': 5,
        'last_attack_dealt': {
            'attacker': 'You',
            'target': 'Orc_2',
            'damage': 18
        }
    }
    
    # Test with message
    test_message = "you win\n\ndon't you feel relieved?"
    screen = ui.render_victory_screen(combat_stats, message=test_message)
    print(screen)
    print("\n" + "="*70)
    print("✓ Victory screen with message rendered successfully")

if __name__ == "__main__":
    print("TESTING DEFEAT SCREEN:")
    print("="*70)
    test_defeat_screen()
    
    print("\n\nTESTING VICTORY SCREEN:")
    print("="*70)
    test_victory_screen()
