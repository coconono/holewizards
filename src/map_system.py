"""Map system for Hole Wizards game."""

import random


class MapTile:
    """Represents a single tile on the map."""

    TILE_TYPES = {
        "wall": "█",
        "door_closed": "╬",
        "door_open": "─",
        "open": " ",
        "entrance": "E",
        "exit": "X",
        "chest": "C",
        "bag": "◆",
    }

    def __init__(self, tile_type="open"):
        """Initialize a map tile."""
        self.tile_type = tile_type
        self.player = None
        self.enemy = None
        self.items = []  # List of items on this tile
        self.explored = False

    def is_walkable(self):
        """Check if this tile can be walked on."""
        # Chests are immovable obstacles
        if self.tile_type in ["wall", "door_closed", "chest"]:
            return False
        return True

    def can_hold_entity(self):
        """Check if this tile can hold a player or enemy."""
        return self.is_walkable()

    def get_display_char(self):
        """Get the character to display for this tile."""
        if self.player:
            return "p"
        if self.enemy:
            return "m"
        if self.items:
            if self.items[0].item_type == "consumable":
                return "▪"
            return "◆"
        return self.TILE_TYPES.get(self.tile_type, " ")

    def __repr__(self):
        return f"Tile({self.tile_type})"


class Map:
    """Represents the game map."""

    def __init__(self, width=32, height=32):
        """Initialize a map."""
        self.width = width
        self.height = height
        self.tiles = [[MapTile("open") for _ in range(width)] for _ in range(height)]
        self.player_view = set()  # Tiles the player has explored
        self._generate_map()

    def _generate_map(self):
        """Generate a basic map layout."""
        # Add walls around the edges
        for x in range(self.width):
            self.tiles[0][x].tile_type = "wall"
            self.tiles[self.height - 1][x].tile_type = "wall"
        
        for y in range(self.height):
            self.tiles[y][0].tile_type = "wall"
            self.tiles[y][self.width - 1].tile_type = "wall"

        # Add some random walls
        for _ in range(20):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            self.tiles[y][x].tile_type = "wall"

        # Add entrance (player start)
        self.tiles[2][2].tile_type = "entrance"
        
        # Add exit
        exit_x = self.width - 3
        exit_y = self.height - 3
        self.tiles[exit_y][exit_x].tile_type = "exit"
        
        # Add exit to initial player view so it's always visible
        self.player_view.add((exit_x, exit_y))

    def is_valid_position(self, x, y):
        """Check if position is within map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x, y):
        """Check if a position is walkable."""
        if not self.is_valid_position(x, y):
            return False
        tile = self.tiles[y][x]
        return tile.is_walkable() and tile.player is None and tile.enemy is None

    def get_tile(self, x, y):
        """Get tile at position."""
        if self.is_valid_position(x, y):
            return self.tiles[y][x]
        return None

    def place_player(self, player):
        """Place player on the map at entrance."""
        player.position["x"] = 2
        player.position["y"] = 2
        self.tiles[2][2].player = player
        
        # Add all tiles within view distance to player_view
        view_distance = player.view_distance
        for y in range(max(0, 2 - view_distance), min(self.height, 2 + view_distance + 1)):
            for x in range(max(0, 2 - view_distance), min(self.width, 2 + view_distance + 1)):
                self.player_view.add((x, y))

    def place_enemy(self, enemy, x, y):
        """Place an enemy on the map."""
        if self.is_walkable(x, y):
            self.tiles[y][x].enemy = enemy
            enemy.position["x"] = x
            enemy.position["y"] = y
            return True
        return False

    def remove_enemy(self, enemy):
        """Remove an enemy from the map."""
        x = enemy.position["x"]
        y = enemy.position["y"]
        if self.is_valid_position(x, y):
            tile = self.tiles[y][x]
            if tile.enemy == enemy:
                tile.enemy = None
                return True
        return False

    def move_player(self, player, dx, dy, ui=None):
        """Move player on the map.
        
        Args:
            player: Player object
            dx, dy: Direction to move
            ui: UI object for logging (optional)
        """
        old_x = player.position["x"]
        old_y = player.position["y"]
        new_x = old_x + dx
        new_y = old_y + dy

        if self.is_valid_position(new_x, new_y):
            # Push loot bags if present at target position
            self.push_loot_bag(new_x, new_y, dx, dy, ui)
            
            # Check if walkable AND no collision with enemies
            if self.is_walkable(new_x, new_y):
                # Remove player from old position
                self.tiles[old_y][old_x].player = None
                
                # Add player to new position
                self.tiles[new_y][new_x].player = player
                player.position["x"] = new_x
                player.position["y"] = new_y
                
                # Add all tiles within view distance to player_view
                view_distance = player.view_distance
                for y in range(max(0, new_y - view_distance), min(self.height, new_y + view_distance + 1)):
                    for x in range(max(0, new_x - view_distance), min(self.width, new_x + view_distance + 1)):
                        self.player_view.add((x, y))
                
                return True
        return False

    def move_enemy(self, enemy, dx, dy, ui=None):
        """Move an enemy on the map.
        
        Args:
            enemy: Enemy object
            dx, dy: Direction to move
            ui: UI object for logging (optional)
        """
        old_x = enemy.position["x"]
        old_y = enemy.position["y"]
        new_x = old_x + dx
        new_y = old_y + dy

        if self.is_valid_position(new_x, new_y):
            # Push loot bags if present at target position
            self.push_loot_bag(new_x, new_y, dx, dy, ui)
            
            # Check if walkable AND no collision with player or other enemies
            if self.is_walkable(new_x, new_y):
                # Remove enemy from old position
                self.tiles[old_y][old_x].enemy = None
                
                # Add enemy to new position
                self.tiles[new_y][new_x].enemy = enemy
                enemy.position["x"] = new_x
                enemy.position["y"] = new_y
                
                return True
        return False

    def find_adjacent_free_tile(self, x, y, max_radius=2):
        """Find the nearest free tile adjacent to (x, y).
        
        Args:
            x, y: Starting position
            max_radius: Maximum search radius
        
        Returns:
            (x, y) tuple of free tile, or None if none found
        """
        # Check if starting position is free
        if self.is_valid_position(x, y):
            tile = self.tiles[y][x]
            if tile.is_walkable() and not tile.items:
                return (x, y)
        
        # Search in expanding circles
        for radius in range(1, max_radius + 1):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    # Only check tiles at the current radius (outer ring)
                    if abs(dx) != radius and abs(dy) != radius:
                        continue
                    
                    nx, ny = x + dx, y + dy
                    if self.is_valid_position(nx, ny):
                        tile = self.tiles[ny][nx]
                        if tile.is_walkable() and not tile.items:
                            return (nx, ny)
        
        return None

    def place_item(self, item, x, y, spread_loot=False):
        """Place an item on the map.
        
        Args:
            item: The item to place
            x, y: The target position
            spread_loot: If True and position has loot bags, find adjacent tile
        
        Returns:
            True if item was placed successfully, False otherwise
        """
        if not self.is_valid_position(x, y):
            return False
        
        # Check if we should spread loot bags
        if spread_loot and item.item_type == "bag":
            tile = self.tiles[y][x]
            # Check if there's already a loot bag at this position
            has_loot_bag = any(i.item_type == "bag" for i in tile.items)
            
            if has_loot_bag:
                # Find adjacent free tile
                free_tile = self.find_adjacent_free_tile(x, y)
                if free_tile:
                    x, y = free_tile
                # If no free tile found, place on same tile anyway
        
        self.tiles[y][x].items.append(item)
        return True
    
    def push_loot_bag(self, x, y, dx, dy, ui=None):
        """Push loot bags at a position in a direction.
        
        Args:
            x, y: Position with loot bags
            dx, dy: Direction to push
            ui: UI object for logging messages (optional)
        
        Returns:
            bool: True if bags were pushed/destroyed, False if no bags
        """
        if not self.is_valid_position(x, y):
            return False
        
        tile = self.tiles[y][x]
        loot_bags = [item for item in tile.items if item.item_type == "bag"]
        
        if not loot_bags:
            return False
        
        # Try to push in the direction of movement
        target_x, target_y = x + dx, y + dy
        
        # Check if target position is valid and walkable
        if self.is_valid_position(target_x, target_y):
            target_tile = self.tiles[target_y][target_x]
            if target_tile.is_walkable() and not target_tile.player and not target_tile.enemy:
                # Push bags to target position
                for bag in loot_bags:
                    tile.items.remove(bag)
                    target_tile.items.append(bag)
                if ui:
                    ui.add_log_message("Loot bag pushed", "movement")
                return True
        
        # If target is blocked, try to find any adjacent open tile
        for check_dx in [-1, 0, 1]:
            for check_dy in [-1, 0, 1]:
                if check_dx == 0 and check_dy == 0:
                    continue
                
                alt_x, alt_y = x + check_dx, y + check_dy
                if self.is_valid_position(alt_x, alt_y):
                    alt_tile = self.tiles[alt_y][alt_x]
                    if alt_tile.is_walkable() and not alt_tile.player and not alt_tile.enemy:
                        # Push bags to alternate position
                        for bag in loot_bags:
                            tile.items.remove(bag)
                            alt_tile.items.append(bag)
                        if ui:
                            ui.add_log_message("Loot bag pushed aside", "movement")
                        return True
        
        # No available tiles - destroy the loot bags
        for bag in loot_bags:
            tile.items.remove(bag)
        if ui:
            ui.add_log_message("The loot bag was crushed! Contents lost.", "loot")
        return True

    def get_items_at(self, x, y):
        """Get items at a position."""
        if self.is_valid_position(x, y):
            return self.tiles[y][x].items
        return []

    def remove_item_at(self, item, x, y):
        """Remove an item from the map."""
        if self.is_valid_position(x, y):
            if item in self.tiles[y][x].items:
                self.tiles[y][x].items.remove(item)
                return True
        return False

    def check_win_condition(self, player):
        """Check if player reached the exit."""
        return (player.position["x"], player.position["y"]) == (self.width - 3, self.height - 3)

    def get_visible_map(self, player, x_distance=None, y_distance=None):
        """Get a string representation of the map from the player's perspective.
        
        Args:
            player: The player object
            x_distance: How far horizontally to display (if None, defaults to view_distance * 3)
            y_distance: How far vertically to display (if None, defaults to view_distance)
        """
        output = []
        
        # Use different display distances for X and Y (wider than tall)
        if x_distance is None:
            x_distance = max(20, player.view_distance * 3)
        if y_distance is None:
            y_distance = max(8, player.view_distance * 2)
        
        px = player.position["x"]
        py = player.position["y"]
        
        exit_pos = (self.width - 3, self.height - 3)
        entrance_pos = (2, 2)
        
        # Determine display bounds, expanding to include important tiles if explored
        min_x = max(0, px - x_distance)
        max_x = min(self.width, px + x_distance + 1)
        min_y = max(0, py - y_distance)
        max_y = min(self.height, py + y_distance + 1)
        
        # Expand bounds to include exit and entrance if explored
        if exit_pos in self.player_view:
            min_x = min(min_x, exit_pos[0])
            max_x = max(max_x, exit_pos[0] + 1)
            min_y = min(min_y, exit_pos[1])
            max_y = max(max_y, exit_pos[1] + 1)

        for y in range(min_y, max_y):
            row = []
            for x in range(min_x, max_x):
                if (x, y) in self.player_view or (x, y) == (px, py):
                    row.append(self.tiles[y][x].get_display_char())
                else:
                    row.append("?")
            output.append("".join(row))

        return "\n".join(output)

    def get_full_map(self):
        """Get a string representation of the entire map (for debugging)."""
        output = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.tiles[y][x].get_display_char())
            output.append("".join(row))
        return "\n".join(output)
