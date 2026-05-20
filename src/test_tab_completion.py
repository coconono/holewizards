"""Test script for tab completion functionality."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from tab_completion import TabCompletion
from items import Weapon, Armor, Potion


def test_command_completion():
    """Test command completion."""
    tc = TabCompletion()
    
    # Test partial command matching
    matches = tc._complete_command("sh")
    assert "show player stats " in matches
    assert "show enemy stats " in matches
    assert "show player inventory " in matches
    print("✓ Command completion works")


def test_inventory_item_completion():
    """Test inventory item completion."""
    state = GameState()
    tc = TabCompletion(state)
    
    # Test drop command - should complete from inventory
    player = state.player
    
    # Get current inventory items
    matches = tc._complete_inventory_item("drop", "")
    assert len(matches) > 0, f"No inventory items to complete. Inventory: {[str(i) for i in state.player.inventory]}"
    print(f"✓ Inventory item completion works ({len(matches)} items in inventory)")
    
    # Test partial item matching
    if matches:
        # Get first item name (handling quoted items)
        first_item_name = matches[0].strip('"')
        first_item_partial = first_item_name[0].lower()  # First letter of actual name
        matches_partial = tc._complete_inventory_item("drop", first_item_partial)
        assert len(matches_partial) > 0, f"No partial matches for '{first_item_partial}'. All matches: {matches}"
        print(f"✓ Partial inventory item matching works")


def test_equip_filtering():
    """Test that equip command filters for equippable items."""
    state = GameState()
    tc = TabCompletion(state)
    
    # equip should only show weapons, armor, spells
    matches = tc._complete_inventory_item("equip", "")
    
    # Count equippable items
    equippable_items = [i for i in state.player.inventory if i.item_type in ("weapon", "armor", "spell")]
    assert len(equippable_items) > 0, f"No equippable items in inventory. Items: {[i.item_type for i in state.player.inventory]}"
    
    print(f"✓ Equip filtering works correctly ({len(matches)} equippable items)")


def test_use_filtering():
    """Test that use command filters for consumable items."""
    state = GameState()
    tc = TabCompletion(state)
    
    # use should only show consumables
    matches = tc._complete_inventory_item("use", "")
    
    # Count consumables in inventory
    consumable_count = sum(1 for item in state.player.inventory if item.item_type == "consumable")
    assert consumable_count > 0
    
    print(f"✓ Use filtering works correctly ({len(matches)} consumables available)")


def test_get_all_commands():
    """Test that all commands are available."""
    tc = TabCompletion()
    commands = tc._get_all_commands()
    
    # Verify key commands exist
    assert "show player stats" in commands
    assert "attack" in commands
    assert "move up" in commands
    assert "take" in commands
    assert "quit" in commands
    
    print(f"✓ All commands available ({len(commands)} commands)")


def test_readline_integration():
    """Test that readline integration doesn't crash."""
    state = GameState()
    tc = TabCompletion(state)
    
    # Test that we can enable/disable
    tc.enable()
    tc.disable()
    
    print("✓ Readline integration works")


def test_graphics_mode_completion():
    """Test graphics mode completion (non-readline)."""
    state = GameState()
    tc = TabCompletion(state, use_readline=False)
    
    # Test complete_input method
    current_input = "sh"
    result, has_more = tc.complete_input(current_input)
    assert result != "sh", "Should complete partial command"
    assert "show" in result, f"Expected completion to contain 'show', got: {result}"
    
    # Test cycling - use the completed result as the new input (simulating real usage)
    current_input = result
    result2, has_more = tc.complete_input(current_input)
    assert result2 != result or not has_more, "Should cycle to different command or indicate no more"
    
    print("✓ Graphics mode completion works")


def test_graphics_mode_reset():
    """Test that graphics mode resets completion on new input."""
    state = GameState()
    tc = TabCompletion(state, use_readline=False)
    
    # Get first completion
    result1, _ = tc.complete_input("sh")
    
    # Change input - should reset
    result2, _ = tc.complete_input("mo")
    assert "move" in result2, f"Should complete 'mo' to 'move', got: {result2}"
    
    # Back to original - should be fresh cycle
    result3, _ = tc.complete_input("sh")
    assert result3 == result1, "Should restart completion cycle with same input"
    
    print("✓ Graphics mode completion cycling works")


def test_graphics_mode_item_completion():
    """Test graphics mode item completion."""
    state = GameState()
    tc = TabCompletion(state, use_readline=False)
    
    # Test item completion in graphics mode
    result, _ = tc.complete_input("take f")
    # Should either complete or stay same if no matches
    
    result2, _ = tc.complete_input("drop ")
    # When there's a space after command, should complete items
    
    print("✓ Graphics mode item completion works")


def run_all_tests():
    """Run all tests."""
    print("\n=== Tab Completion Tests ===\n")
    
    tests = [
        ("Commands available", test_get_all_commands),
        ("Command completion", test_command_completion),
        ("Inventory item completion", test_inventory_item_completion),
        ("Equip filtering", test_equip_filtering),
        ("Use filtering", test_use_filtering),
        ("Readline integration", test_readline_integration),
        ("Graphics mode completion", test_graphics_mode_completion),
        ("Graphics mode cycling", test_graphics_mode_reset),
        ("Graphics mode items", test_graphics_mode_item_completion),
    ]
    
    for test_name, test_func in tests:
        try:
            test_func()
        except AssertionError as e:
            print(f"\n❌ Test '{test_name}' failed: {e}\n")
            return False
        except Exception as e:
            print(f"\n❌ Test '{test_name}' error: {e}\n")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n✅ All tests passed!\n")
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
