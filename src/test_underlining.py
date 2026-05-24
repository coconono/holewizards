"""Test entity name underlining in text mode."""

from ui import UI

def test_text_underlining():
    """Test that entity names are underlined in text mode."""
    ui = UI()
    
    # Set entity names
    ui.set_entity_names("You", ["Goblin_0", "Skeleton_1", "Orc_2"])
    
    # Add messages containing entity names
    ui.add_log_message("Moved north", "movement")
    ui.add_log_message("You spot Goblin_0 nearby!", "movement")
    ui.add_log_message("Attacked Skeleton_1 for 10 damage!", "combat_dealt")
    ui.add_log_message("Orc_2 attacks you for 5 damage!", "combat_taken")
    ui.add_log_message("Defeated Goblin_0! Gained 10 XP!", "victory")
    
    # Render the log
    log_lines = ui.render_log(80)
    
    print("Text Mode Log Output (with ANSI codes):")
    print("=" * 60)
    for line in log_lines:
        print(line)
    print("=" * 60)
    print("\nIn a terminal that supports ANSI codes:")
    print("  - Entity names (You, Goblin_0, Skeleton_1, Orc_2) should be underlined")
    print("  - Messages should be color-coded by type")
    print("\nRaw ANSI codes are visible above if terminal doesn't support them.")

if __name__ == "__main__":
    test_text_underlining()
