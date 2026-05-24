"""Visual test of graphics mode colors - creates a pygame window showing all color types."""

import pygame
from graphics import GraphicalUI
import time

def main():
    """Display all log message colors in a pygame window."""
    pygame.init()
    
    # Create graphics UI
    ui = GraphicalUI(width=1400, height=900, tab_completion=None)
    
    # Set entity names for highlighting
    ui.set_entity_names("You", ["Goblin_0", "Skeleton_1", "Orc_2"])
    
    # Add test messages with all event types and entity names
    ui.add_log_message("=== TESTING LOG COLORS & ENTITY HIGHLIGHTING ===", "default")
    ui.add_log_message("", "default")
    ui.add_log_message("GREEN: You attack Goblin_0 for 15 damage!", "combat_dealt")
    ui.add_log_message("RED: Skeleton_1 hits you for 8 damage!", "combat_taken")
    ui.add_log_message("BLUE: You restored 20 HP with potion", "healing")
    ui.add_log_message("YELLOW: Found Iron Sword from Orc_2", "loot")
    ui.add_log_message("MAGENTA: Goblin_0 repositions you!", "status")
    ui.add_log_message("GRAY: Unknown command", "system")
    ui.add_log_message("CYAN: You moved north", "movement")
    ui.add_log_message("BRIGHT GREEN: Victory! You defeated Skeleton_1!", "victory")
    ui.add_log_message("BRIGHT RED: Orc_2 defeats you!", "defeat")
    ui.add_log_message("", "default")
    ui.add_log_message("Entity names (You, Goblin_0, Skeleton_1, Orc_2) have YELLOW backgrounds!", "default")
    ui.add_log_message("Press ESC or close window to exit", "system")
    
    # Display the window
    print("\nShowing color + entity highlighting test window...")
    print("Each log message should be a different color.")
    print("Entity names (You, Goblin_0, Skeleton_1, Orc_2) should have YELLOW backgrounds.")
    print("Press ESC or close the window to exit.\n")
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Render just the log display
        ui.screen.fill((20, 20, 20))  # Dark background
        ui.render_log_display()
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    print("✓ Test complete")

if __name__ == "__main__":
    main()
