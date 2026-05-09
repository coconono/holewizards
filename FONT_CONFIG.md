# Font Configuration Guide

## Quick Start

Change fonts in your Hole Wizards game:

```bash
# Interactive mode - choose from list
python3 utilities/font_manager.py

# Direct mode - set specific font
python3 utilities/font_manager.py ABeeZee-Regular.otf
```

## System Overview

### Settings File

- **Location**: `data/settings.cfg`
- **Section**: `[display]`
- **Option**: `font`

### Font Storage

- **Location**: `data/fonts/`
- **Supported formats**: `.ttf` and `.otf`
- **Available fonts**:
  - `20db.otf` - Decorative/stylized font
  - `2Dumb.ttf` - Fun, chunky font (default)
  - `3Dumb.ttf` - Variant of 2Dumb
  - `ABeeZee-Regular.otf` - Clean, readable serif

## Usage Methods

### Method 1: Font Manager Utility

**Interactive menu:**

```bash
python3 utilities/font_manager.py
```

Options:

- Enter font number (1-4) to select
- Press `d` for system default
- Press `q` to quit

**Command line:**

```bash
python3 utilities/font_manager.py 2Dumb.ttf
python3 utilities/font_manager.py ABeeZee-Regular.otf
```

### Method 2: Direct Edit

Edit `data/settings.cfg`:

```ini
[display]
font = ABeeZee-Regular.otf
```

Leave empty for system default:

```ini
[display]
font = 
```

### Method 3: Programmatic

From Python code:

```python
from utilities.font_manager import set_font
set_font('ABeeZee-Regular.otf')
```

## Adding Custom Fonts

1. Place `.ttf` or `.otf` file in `data/fonts/`
2. Set it in settings:

   ```bash
   python3 utilities/font_manager.py your_font.ttf
   ```

3. Run game - font loads automatically

## How It Works

1. **Game startup**: Graphics module reads `data/settings.cfg`
2. **Font loading**: System attempts to load font from `data/fonts/` folder
3. **Fallback**: If font fails to load, uses system default
4. **Text mode**: Font settings only apply to graphical mode (text mode uses terminal)

## Troubleshooting

| Issue | Solution |
| ------- | ---------- |
| Font not loading | Check filename in `data/settings.cfg` matches exactly |
| Game uses text mode | pygame.font module unavailable (automatic fallback) |
| Font looks wrong | Some fonts don't render well; try another |
| Font file not found | Ensure `.ttf`/`.otf` file is in `data/fonts/` |

## Technical Details

**Configuration Loading** (`graphics.py`):

```python
def _get_font_path(self):
    """Load font path from settings.cfg"""
    # Reads [display] section
    # Returns path to font file
```

**Font Path Resolution**:

- Settings value is filename only (e.g., `2Dumb.ttf`)
- Graphics module resolves to full path: `data/fonts/2Dumb.ttf`
- Supports both `.ttf` and `.otf` formats

## Default Configuration

When `data/settings.cfg` is created or reset:

```ini
[display]
font = 2Dumb.ttf

[gameplay]
difficulty = normal
```

The fun, chunky `2Dumb.ttf` is the default for visual appeal.
