#!/usr/bin/env python3
"""Quick test of graphics mode with fallback rendering."""

import time
import pygame
from graphics import GraphicalUI
from game_state import GameState

print("Starting graphics mode test...")
print("Window should open for 5 seconds showing colored UI sections")
print("(Green: Map, Yellow: Stats, Cyan: Log, Orange: Command Input)\n")

try:
    ui = GraphicalUI()
    state = GameState()
    
    # Show the fallback UI for 5 seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        # Get game state
        player = state.player
        enemy = state.get_current_enemy()
        map_display = state.map.get_visible_map(player, x_distance=49, y_distance=6)
        
        # Render
        ui.render(player, enemy, map_display)
        
        # Control frame rate
        ui.tick(30)
        
        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
    
    pygame.quit()
    print("✓ Test complete!")
    print("\nYou should have seen a window with colored sections:")
    print("  - Green border = Map display area")
    print("  - Yellow border = Stats display area") 
    print("  - Cyan border = Log/messages area")
    print("  - Orange border = Command input area")
    print("\nThe UI is functioning but fonts are unavailable.")
    print("To use graphics mode with proper text, pygame.font must be fixed.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
