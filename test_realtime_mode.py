#!/usr/bin/env python3
"""Test script for real-time mode functionality."""

import sys
sys.path.insert(0, 'src')

from game_state import GameState
from realtime_input import RealtimeInput
import time


def test_game_state_realtime():
    """Test GameState real-time mode features."""
    print("Testing GameState real-time mode...")
    
    state = GameState()
    
    # Test initial state
    assert state.realtime_mode == False, "Should start in turn-based mode"
    assert state.action_cooldowns["move"] == 0.0, "Move cooldown should start at 0"
    
    # Test mode toggle
    result = state.toggle_realtime_mode()
    assert result == True, "Should return True when entering real-time"
    assert state.realtime_mode == True, "Should be in real-time mode"
    
    result = state.toggle_realtime_mode()
    assert result == False, "Should return False when exiting real-time"
    assert state.realtime_mode == False, "Should be in turn-based mode"
    
    print("✓ GameState real-time mode toggle works")


def test_cooldowns():
    """Test action cooldown system."""
    print("Testing action cooldowns...")
    
    state = GameState()
    
    # Test cooldown setting and checking
    assert state.can_perform_action("move") == True, "Should be able to move initially"
    
    state.set_cooldown("move", 0.5)
    assert state.can_perform_action("move") == False, "Should not be able to move on cooldown"
    assert state.action_cooldowns["move"] == 0.5, "Cooldown should be 0.5s"
    
    # Test cooldown update
    state.update_cooldowns(0.3)
    assert state.action_cooldowns["move"] == 0.2, "Cooldown should decrease to 0.2s"
    assert state.can_perform_action("move") == False, "Should still be on cooldown"
    
    state.update_cooldowns(0.3)
    assert state.action_cooldowns["move"] == 0.0, "Cooldown should be 0 now"
    assert state.can_perform_action("move") == True, "Should be able to move now"
    
    print("✓ Action cooldowns work correctly")


def test_entity_timers():
    """Test entity action timers."""
    print("Testing entity timers...")
    
    state = GameState()
    
    # Check player has timer properties
    assert hasattr(state.player, 'action_timer'), "Player should have action_timer"
    assert hasattr(state.player, 'action_interval'), "Player should have action_interval"
    
    # Check enemies have timer properties
    for enemy in state.enemies:
        assert hasattr(enemy, 'action_timer'), "Enemy should have action_timer"
        assert hasattr(enemy, 'action_interval'), "Enemy should have action_interval"
        assert enemy.action_interval > 0, "Enemy action_interval should be positive"
    
    # Test timer updates
    state.player.action_timer = 1.0
    state.enemies[0].action_timer = 0.5
    
    state.update_entity_timers(0.3)
    
    assert state.player.action_timer == 0.7, "Player timer should decrease"
    assert state.enemies[0].action_timer == 0.2, "Enemy timer should decrease"
    
    print("✓ Entity timers work correctly")


def test_loot_bag_physics():
    """Test loot bag pushing mechanics."""
    print("Testing loot bag physics...")
    
    state = GameState()
    
    # Test that push_loot_bag method exists
    assert hasattr(state.map, 'push_loot_bag'), "Map should have push_loot_bag method"
    
    # Test that move_player and move_enemy accept ui parameter
    import inspect
    move_player_sig = inspect.signature(state.map.move_player)
    assert 'ui' in move_player_sig.parameters, "move_player should accept ui parameter"
    
    move_enemy_sig = inspect.signature(state.map.move_enemy)
    assert 'ui' in move_enemy_sig.parameters, "move_enemy should accept ui parameter"
    
    print("✓ Loot bag physics implemented")


def test_chest_blocking():
    """Test that chests are impassable."""
    print("Testing chest blocking...")
    
    state = GameState()
    
    # Find a chest on the map
    chest_pos = None
    for y in range(state.map.height):
        for x in range(state.map.width):
            tile = state.map.get_tile(x, y)
            if tile and tile.tile_type == "chest":
                chest_pos = (x, y)
                break
        if chest_pos:
            break
    
    if chest_pos:
        x, y = chest_pos
        # Chest tile should not be walkable
        assert not state.map.is_walkable(x, y), "Chest tiles should not be walkable"
        print(f"✓ Chests are impassable (tested at {chest_pos})")
    else:
        print("⚠ No chests found on map to test (this is okay)")


def test_realtime_input():
    """Test RealtimeInput class."""
    print("Testing RealtimeInput class...")
    
    rt_input = RealtimeInput()
    
    # Test that it initializes
    assert hasattr(rt_input, 'poll_keys'), "Should have poll_keys method"
    assert hasattr(rt_input, 'enter_realtime_mode'), "Should have enter_realtime_mode method"
    assert hasattr(rt_input, 'exit_realtime_mode'), "Should have exit_realtime_mode method"
    
    # Test that poll_keys returns a list
    keys = rt_input.poll_keys()
    assert isinstance(keys, list), "poll_keys should return a list"
    
    print("✓ RealtimeInput class works")


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("Real-Time Mode Implementation Tests")
    print("="*50 + "\n")
    
    try:
        test_game_state_realtime()
        test_cooldowns()
        test_entity_timers()
        test_loot_bag_physics()
        test_chest_blocking()
        test_realtime_input()
        
        print("\n" + "="*50)
        print("✓ ALL TESTS PASSED")
        print("="*50 + "\n")
        return 0
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
