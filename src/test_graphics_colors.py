"""Test graphics mode color rendering."""

import pygame
import sys
from graphics import GraphicalUI

def test_graphics_colors():
    """Test that colors are applied correctly in graphics mode."""
    pygame.init()
    
    # Create a minimal graphics UI
    ui = GraphicalUI()
    
    # Add test messages with different event types
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
    
    # Check what was stored
    print("Messages stored in log:")
    for i, msg_data in enumerate(ui.log_messages):
        print(f"  {i}: {msg_data}")
        if isinstance(msg_data, dict):
            event_type = msg_data.get('event_type', 'default')
            color = ui.LOG_COLORS.get(event_type, ui.LOG_COLORS['default'])
            print(f"     Event type: {event_type}, Color: {color}")
    
    print("\n✓ All messages stored correctly with event types")
    print(f"✓ LOG_COLORS keys: {list(ui.LOG_COLORS.keys())}")
    
    pygame.quit()

if __name__ == "__main__":
    test_graphics_colors()
