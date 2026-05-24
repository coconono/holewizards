"""Test combat statistics tracking."""

from game_state import GameState

def test_combat_stats():
    """Verify combat stats are tracked correctly."""
    state = GameState()
    
    print("Initial combat stats:")
    for key, value in state.combat_stats.items():
        print(f"  {key}: {value}")
    
    print("\n✓ Combat stats dictionary initialized successfully")
    print(f"✓ Tracking {len(state.combat_stats)} different statistics")
    
    # Verify all expected keys exist
    expected_keys = [
        'total_damage_dealt', 'total_damage_taken', 'monsters_defeated',
        'healing_used', 'items_collected', 'turns_elapsed', 'attacks_made',
        'attacks_received', 'chests_opened', 'spells_cast', 'last_attack_dealt',
        'last_attack_taken', 'killing_blow'
    ]
    
    for key in expected_keys:
        assert key in state.combat_stats, f"Missing key: {key}"
    
    print(f"\n✓ All {len(expected_keys)} expected stat keys present")

if __name__ == "__main__":
    test_combat_stats()
