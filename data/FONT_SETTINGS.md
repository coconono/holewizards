# Font Configuration

## Overview

The Hole Wizards graphical display can use custom fonts. Font selection is managed through `data/settings.cfg`.

## Available Fonts

Located in `data/fonts/`:

- `2Dumb.ttf` - Fun, chunky font (default)
- `3Dumb.ttf` - Variant of 2Dumb
- `ABeeZee-Regular.otf` - Clean, readable serif font
- `20db.otf` - Decorative font

## Changing Fonts

1. Edit `data/settings.cfg`:

   ```ini
   [display]
   font = ABeeZee-Regular.otf
   ```

2. Run the game:

   ```bash
   python3 main.py
   ```

3. The new font will load automatically

## Adding Custom Fonts

1. Place TTF or OTF font files in `data/fonts/`
2. Update `settings.cfg` with the filename
3. Restart the game

## Format

- Leave blank to use system default: `font =`
- Specify font name: `font = 2Dumb.ttf`

## Troubleshooting

- **Font doesn't load**: Check filename spelling in settings.cfg
- **Game falls back to text mode**: pygame.font module may not be available
- **Font looks incorrect**: Some fonts may not render well at all sizes; try another

## Notes

- Only `.ttf` and `.otf` fonts are supported
- Fonts apply only in graphical mode (not text mode)
- If the specified font fails to load, system default is used automatically
