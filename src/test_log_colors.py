"""Test script for log message color coding."""

from ui import UI, EVENT_TYPES, ANSI_COLORS

def test_text_mode_colors():
    """Test color coding in text mode."""
    print("Testing Text Mode Color System")
    print("=" * 50)
    
    ui = UI()
    
    # Test each event type
    test_messages = [
        ("Player attacks for 10 damage!", "combat_dealt"),
        ("Enemy hits you for 5 damage!", "combat_taken"),
        ("Restored 15 HP", "healing"),
        ("Found Iron Sword", "loot"),
        ("You are poisoned!", "status"),
        ("Unknown command", "system"),
        ("Moved north", "movement"),
        ("Victory! You escaped!", "victory"),
        ("You died!", "defeat"),
        ("Regular message", "default"),
    ]
    
    for message, event_type in test_messages:
        ui.add_log_message(message, event_type)
    
    # Render and display
    log_lines = ui.render_log(80)
    print("\nRendered Log Messages:")
    print("-" * 50)
    for line in log_lines:
        print(line)
    
    print("\n" + "=" * 50)
    print("✓ Text mode color test complete!")
    print(f"✓ Tested {len(EVENT_TYPES)} event types")
    print("\nNote: Colors should be visible in your terminal.")
    print("If you don't see colors, your terminal may not support ANSI codes.")

def test_backward_compatibility():
    """Test that old code without event_type still works."""
    print("\n\nTesting Backward Compatibility")
    print("=" * 50)
    
    ui = UI()
    
    # Old-style calls (no event_type)
    ui.add_log_message("Old message 1")
    ui.add_log_message("Old message 2")
    
    # New-style calls
    ui.add_log_message("New colored message", "combat_dealt")
    
    log_lines = ui.render_log(80)
    print("\nMixed old/new messages:")
    print("-" * 50)
    for line in log_lines:
        print(line)
    
    print("\n✓ Backward compatibility test passed!")

if __name__ == "__main__":
    test_text_mode_colors()
    test_backward_compatibility()
    
    print("\n\nColor Reference:")
    print("=" * 50)
    for event_type, color_name in EVENT_TYPES.items():
        color_code = ANSI_COLORS.get(color_name, '')
        reset = ANSI_COLORS['reset']
        print(f"{color_code}{event_type:15} -> {color_name}{reset}")
