# png graphics

graphical update to the game window. these will replace the ascii character art being used

## file location

/data/png

## file replaces the tile

spr_chest.png replaces chest (character: C)
spr_enterportal.png replaces enter (character: E)
spr_exitportal.png replaces exit (character: X)
spr_floortile.png replaces floor (character: space)
spr_loot.png replaces loot (character: ◆)
spr_walltile.png replaces wall (character: █)
spr_wizardenemy.png replaces enemy (character: m)
spr_wizardplayer.png replaces player (character: p)

## layering

floor tile is the lowest, all other tiles displayed will cover this
next is enter and exit portals
next is chest, loot
next is player, enemy
wall tile is the highest, it will cover all the other tiles

## Implementation Plan

### Approach

Replace the current colored-box tile rendering in `src/graphics.py` with PNG sprite rendering. Sprites should be loaded once during initialization, cached in memory, and scaled to the current tile size (16×18 pixels). Implement the layering system so sprites composite properly (floor → portals → items → entities → walls). Fallback to colored box rendering if sprites fail to load.

### Implementation Steps

1. **Add sprite loading system to GraphicalUI.**init**()**
   - Load PNG sprites from `data/png/` using `pygame.image.load()`
   - Scale each sprite to 16×18 pixels using `pygame.transform.scale()`
   - Store scaled sprites in a dictionary: `self.sprites = {}`
   - Map sprite filenames to tile characters (e.g., 'spr_wizardplayer.png' → 'p')
   - Handle missing sprite files gracefully (log warning, sprite stays None)
   - Store project root path as `self.project_root` to avoid repeated path calculations

2. **Create character-to-sprite mapping**
   - Add a `SPRITE_MAP` constant at module level mapping characters to sprite filenames:

     ```python
     SPRITE_MAP = {
         'C': 'spr_chest.png',
         'E': 'spr_enterportal.png',
         'X': 'spr_exitportal.png',
         ' ': 'spr_floortile.png',
         '◆': 'spr_loot.png',
         '█': 'spr_walltile.png',
         'm': 'spr_wizardenemy.png',
         'p': 'spr_wizardplayer.png',
     }
     ```

3. **Implement layered sprite rendering in render_map_line()**
   - For each tile position, render sprites in layering order:
     1. Floor tile (spr_floortile.png) - always render first as base
     2. Portals (enter/exit) if character is E or X
     3. Chests and loot if character is C or ◆
     4. Player and enemies if character is p or m
     5. Walls (top layer) if character is █
   - Use `screen.blit(sprite, (x_offset, y_pos))` to draw sprites
   - Maintain the same x_offset advancement (18 pixels per tile)

4. **Update render_map_line() to replace rectangle drawing**
   - Location: `src/graphics.py` lines 546-596
   - Replace the `pygame.draw.rect()` calls with sprite blitting
   - Keep the white border rendering for tiles without sprites
   - Preserve letter labels (E, X, C) if needed for clarity

5. **Add error handling and fallback**
   - If sprite dict is empty (all loads failed), use current box rendering
   - If a specific sprite is None, render that tile with the old colored box method
   - Add console warning once during initialization if sprites fail to load
   - Don't crash the game if sprites are missing

### Character-to-Sprite Reference

| Character | Tile Type | Sprite File | Current Color |
| ----------- | ----------- | ------------- | --------------- |
| `█` | Wall | spr_walltile.png | Dark Gray |
| `◆` | Loot/Bag | spr_loot.png | Yellow |
| `╬` | Closed Door | (no sprite yet) | Cyan |
| `─` | Open Door | (no sprite yet) | Bright Green |
| `E` | Entrance Portal | spr_enterportal.png | Orange |
| `X` | Exit Portal | spr_exitportal.png | Magenta |
| `C` | Chest | spr_chest.png | Gold |
| `p` | Player | spr_wizardplayer.png | Bright Green |
| `m` | Enemy | spr_wizardenemy.png | Red |
| ` ` | Floor/Open | spr_floortile.png | (background) |

### Technical Details

- **Tile size**: 16 pixels wide × 18 pixels tall (hardcoded in current rendering)
- **Sprite scaling**: All sprites should be scaled to 16×18 regardless of original size
- **Current rendering location**: `src/graphics.py`, function `render_map_line()` lines 546-596
- **Map data flow**: `map_system.py` → string of characters → `graphics.py` → visual rendering
- **No caching exists**: Sprites will be the first cached visual assets in the rendering system

### Verification Checklist

1. Run the game: `python3 main.py` or `./run_game.sh`
2. Verify sprites display for all tile types
3. Test layering: walk near walls to verify walls occlude player/enemies
4. Test fallback: rename a sprite file temporarily to check colored box fallback works
5. Check console for sprite loading warnings
6. Verify no performance degradation (should be faster than box rendering)

### Design Decisions

- **Sprite scaling**: Scale to 16×18 pixels to match current tile size
- **Layering approach**: Composite per-tile (floor → portals → items → entities → walls)
- **Floor rendering**: Render floor tile under ALL tiles for visual consistency
- **Fallback strategy**: Graceful degradation per-tile if sprite is missing
- **Scope**: Only map tile rendering; stats/log/input remain text-based
- **Excluded**: No sprite animations, no tile size configuration, no sprite sheets
