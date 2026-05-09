#!/usr/bin/env python3
"""Test graphics rendering with continuous display."""

import pygame
import time
from graphics import GraphicalUI
from game_state import GameState

print("Graphics Display Test")
print("=" * 60)
print("Opening window for 10 seconds...")
print("The window should display:")
print("  - Green bordered area (top-left) = Map")
print("  - Yellow bordered area (top-right) = Stats")
print("  - Cyan bordered area (bottom) = Log")
print("  - Orange bordered area (input) = Command Input")
print("\nPress Ctrl+C to close or wait 10 seconds")
print("=" * 60)

try:
    # Create UI and game state
    ui = GraphicalUI()
    state = GameState()
    
    print("\n✓ Graphics window opened")
    print(f"✓ Using fallback rendering: {ui.font_normal is None}")
    
    # Keep rendering for 10 seconds
    start_time = time.time()
    frame_count = 0
    
    while time.time() - start_time < 10:
        # Get game state
        player = state.player
        enemy = state.get_current_enemy()
        map_display = state.map.get_visible_map(player, x_distance=49, y_distance=6)
        
        # Render
        ui.render(player, enemy, map_display)
        frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\n✓ Window closed by user")
                pygame.quit()
                exit(0)
        
        # Maintain frame rate
        ui.tick(30)
    
    # Cleanup
    pygame.quit()
    print(f"\n✓ Test complete")
    print(f"✓ Rendered {frame_count} frames")
    print(f"✓ Graphics system working correctly")
    
except KeyboardInterrupt:
    print("\n✓ Test interrupted by user")
    pygame.quit()
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
