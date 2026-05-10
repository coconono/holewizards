"""Graphical UI for Hole Wizards using pygame."""

import pygame
import os
import sys
import warnings
from configparser import ConfigParser
from pathlib import Path

# Suppress pygame.font circular import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='pygame.font')

# Try PIL/Pillow as a font rendering alternative
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Try to use pygame.freetype for text rendering (bypasses pygame.font issues)
try:
    import pygame.freetype
    FREETYPE_AVAILABLE = True
except (ImportError, RuntimeError) as e:
    FREETYPE_AVAILABLE = False

# Simple text-based character rendering using ASCII art patterns
# Each character is defined as a list of strings (5x5 grid)
SIMPLE_FONT = {
    'A': ['*****', '*   *', '*****', '*   *', '*   *'],
    'B': ['**** ', '*   *', '****,', '*   *', '**** '],
    'C': [' ****', '*    ', '*    ', '*    ', ' ****'],
    'D': ['**** ', '*   *', '*   *', '*   *', '**** '],
    'E': ['*****', '*    ', '****,', '*    ', '*****'],
    'F': ['*****', '*    ', '****,', '*    ', '*    '],
    'G': [' ****', '*    ', '*  **', '*   *', ' ****'],
    'H': ['*   *', '*   *', '*****', '*   *', '*   *'],
    'I': ['*****', '  *  ', '  *  ', '  *  ', '*****'],
    'J': ['  ***', '    *', '    *', '*   *', ' *** '],
    'K': ['*   *', '*  * ', '**   ', '*  * ', '*   *'],
    'L': ['*    ', '*    ', '*    ', '*    ', '*****'],
    'M': ['*   *', '** **', '* * *', '*   *', '*   *'],
    'N': ['*   *', '**  *', '* * *', '*  **', '*   *'],
    'O': [' *** ', '*   *', '*   *', '*   *', ' *** '],
    'P': ['**** ', '*   *', '****,', '*    ', '*    '],
    'Q': [' *** ', '*   *', '*   *', '*  * ', ' ** *'],
    'R': ['**** ', '*   *', '****,', '*  * ', '*   *'],
    'S': [' ****', '*    ', ' *** ', '    *', '*** '],
    'T': ['*****', '  *  ', '  *  ', '  *  ', '  *  '],
    'U': ['*   *', '*   *', '*   *', '*   *', ' *** '],
    'V': ['*   *', '*   *', '*   *', ' * * ', '  *  '],
    'W': ['*   *', '*   *', '* * *', '* * *', ' * * '],
    'X': ['*   *', ' * * ', '  *  ', ' * * ', '*   *'],
    'Y': ['*   *', ' * * ', '  *  ', '  *  ', '  *  '],
    'Z': ['*****', '   * ', '  *  ', ' *   ', '*****'],
    'a': [' *** ', '    *', ' ****', '*   *', ' *** '],
    'b': ['*    ', '*    ', '* ** ', '*   *', '* ** '],
    'c': [' *** ', '*    ', '*    ', '*    ', ' *** '],
    'd': ['    *', '    *', ' ****', '*   *', ' ****'],
    'e': [' *** ', '*   *', '**** ', '*    ', ' *** '],
    'f': ['  ** ', ' *   ', '***  ', ' *   ', ' *   '],
    'g': [' ****', '*   *', ' ****', '    *', ' *** '],
    'h': ['*    ', '*    ', '* ** ', '*   *', '*   *'],
    'i': ['  *  ', '     ', '  *  ', '  *  ', '  *  '],
    'j': ['   * ', '     ', '   * ', '   * ', ' *   '],
    'k': ['*    ', '*  * ', '**   ', '*  * ', '*   *'],
    'l': ['  *  ', '  *  ', '  *  ', '  *  ', '  *  '],
    'm': ['      ', ' ** * ', '*   *', '*   *', '*   *'],
    'n': ['      ', ' **** ', '*   *', '*   *', '*   *'],
    'o': ['      ', ' *** ', '*   *', '*   *', ' *** '],
    'p': ['      ', ' **** ', '*   *', ' **** ', '*    '],
    'q': ['      ', ' **** ', '*   *', ' **** ', '    *'],
    'r': ['      ', ' **** ', '*    ', '*    ', '*    '],
    's': ['      ', ' *** ', '*    ', '    *', ' *** '],
    't': ['  *  ', ' *** ', '  *  ', '  *  ', '  ** '],
    'u': ['      ', '*   *', '*   *', '*   *', ' *** '],
    'v': ['      ', '*   *', '*   *', ' * * ', '  *  '],
    'w': ['      ', '*   *', '* * *', '* * *', ' * * '],
    'x': ['      ', '*   *', ' * * ', '  *  ', ' * * '],
    'y': ['      ', '*   *', ' ****', '    *', ' *** '],
    'z': ['      ', '**** ', '   * ', '  *  ', '**** '],
    '0': [' *** ', '*   *', '*  **', '** *', ' *** '],
    '1': ['  *  ', ' **  ', '  *  ', '  *  ', ' *** '],
    '2': [' *** ', '*   *', '   * ', '  *  ', '**** '],
    '3': [' *** ', '*   *', '  ** ', '    *', ' *** '],
    '4': ['   * ', '  ** ', ' * * ', '**** ', '   * '],
    '5': ['**** ', '*    ', ' *** ', '    *', ' *** '],
    '6': [' *** ', '*    ', '* ** ', '*   *', ' *** '],
    '7': ['**** ', '    *', '   * ', '  *  ', ' *   '],
    '8': [' *** ', '*   *', ' *** ', '*   *', ' *** '],
    '9': [' *** ', '*   *', ' ****', '    *', ' *** '],
    ' ': ['     ', '     ', '     ', '     ', '     '],
    '.': ['     ', '     ', '     ', '  *  ', '  *  '],
    ':': ['     ', '  *  ', '     ', '  *  ', '     '],
    ',': ['     ', '     ', '     ', '  *  ', ' *   '],
    '!': ['  *  ', '  *  ', '  *  ', '     ', '  *  '],
    '?': [' *** ', '*   *', '   * ', '     ', '  *  '],
    '+': ['     ', '  *  ', ' *** ', '  *  ', '     '],
    '-': ['     ', '     ', '**** ', '     ', '     '],
    '=': ['     ', '**** ', '     ', '**** ', '     '],
    '/': ['    *', '   * ', '  *  ', ' *   ', '*    '],
    '\\': ['*    ', ' *   ', '  *  ', '   * ', '    *'],
    '*': ['  *  ', ' *** ', ' *** ', '  *  ', '     '],
    '"': [' * * ', ' * * ', '     ', '     ', '     '],
    "'": ['  *  ', '  *  ', '     ', '     ', '     '],
    '(': ['   * ', '  * ', '  * ', '  * ', '   * '],
    ')': [' *   ', '  *  ', '  *  ', '  *  ', ' *   '],
    '[': ['  ** ', '  *  ', '  *  ', '  *  ', '  ** '],
    ']': [' **  ', '  *  ', '  *  ', '  *  ', ' **  '],
    '<': ['    *', '   * ', '  *  ', '   * ', '    *'],
    '>': ['*    ', ' *   ', '  *  ', ' *   ', '*    '],
    '_': ['     ', '     ', '     ', '     ', '*****'],
}


class GraphicalUI:
    """Handles graphical rendering using pygame."""

    def __init__(self, width=1400, height=900):
        """Initialize the graphical UI."""
        # Suppress warnings during initialization
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning)
            
            # Initialize pygame
            pygame.init()
        
        # Create the main display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Hole Wizards")
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        
        # Initialize colors and layout BEFORE fonts
        self._init_colors_and_layout()
        
        # Initialize font renderer type
        self.font_renderer = 'bitmap'  # Default fallback
        
        # Initialize fonts (may fail gracefully)
        self.fonts = self._init_fonts()
        
        # Store font references
        self.font_tiny = self.fonts.get('tiny')
        self.font_small = self.fonts.get('small')
        self.font_normal = self.fonts.get('normal')
        self.font_title = self.fonts.get('title')
        self.font_large = self.fonts.get('large')

    def _init_fonts(self):
        """Initialize fonts from data/fonts folder based on settings.cfg."""
        fonts = {
            'tiny': None,
            'small': None,
            'normal': None,
            'title': None,
            'large': None,
        }
        
        # Get font path from settings
        font_path = self._get_font_path()
        
        # Try PIL/Pillow first (most reliable for custom fonts)
        if PIL_AVAILABLE:
            if font_path and os.path.exists(font_path):
                try:
                    fonts['tiny'] = ImageFont.truetype(font_path, size=9)
                    fonts['small'] = ImageFont.truetype(font_path, size=12)
                    fonts['normal'] = ImageFont.truetype(font_path, size=16)
                    fonts['title'] = ImageFont.truetype(font_path, size=22)
                    fonts['large'] = ImageFont.truetype(font_path, size=28)
                    self.font_renderer = 'PIL'
                    return fonts
                except Exception:
                    pass
            
            # Try system fonts with PIL
            try:
                fonts['small'] = ImageFont.load_default()
                fonts['normal'] = ImageFont.load_default()
                fonts['title'] = ImageFont.load_default()
                fonts['large'] = ImageFont.load_default()
                self.font_renderer = 'PIL'
                return fonts
            except Exception:
                pass
        
        # Try pygame font (may fail due to circular imports)
        try:
            from pygame.font import Font as PygameFont
            if font_path and os.path.exists(font_path):
                fonts['tiny'] = PygameFont(font_path, 9)
                fonts['small'] = PygameFont(font_path, 12)
                fonts['normal'] = PygameFont(font_path, 16)
                fonts['title'] = PygameFont(font_path, 22)
                fonts['large'] = PygameFont(font_path, 28)
            else:
                fonts['tiny'] = PygameFont(None, 9)
                fonts['small'] = PygameFont(None, 12)
                fonts['normal'] = PygameFont(None, 16)
                fonts['title'] = PygameFont(None, 22)
                fonts['large'] = PygameFont(None, 28)
            self.font_renderer = 'pygame'
            return fonts
        except Exception:
            pass
        
        # If all fails, fonts stay None and we'll use fallback rendering
        self.font_renderer = 'bitmap'
        return fonts
    
    def _get_font_path(self):
        """Load font path from settings.cfg or return None for default."""
        try:
            # Get project root (parent of src directory)
            project_root = os.path.dirname(os.path.dirname(__file__))
            settings_path = os.path.join(project_root, 'data', 'settings.cfg')
            
            if not os.path.exists(settings_path):
                return None
            
            config = ConfigParser()
            config.read(settings_path)
            
            if config.has_option('display', 'font'):
                font_name = config.get('display', 'font').strip()
                
                if not font_name:  # Empty string means use default
                    return None
                
                # Construct path to font file
                font_path = os.path.join(project_root, 'data', 'fonts', font_name)
                return font_path
        except Exception as e:
            pass
        
        return None
        
    def _init_colors_and_layout(self):
        """Initialize colors and layout constants."""
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.DARK_GRAY = (40, 40, 40)
        self.LIGHT_GRAY = (220, 220, 220)
        self.DARK_GREEN = (0, 120, 0)
        self.BRIGHT_GREEN = (100, 255, 100)
        self.RED = (255, 80, 80)
        self.YELLOW = (255, 255, 100)
        self.CYAN = (100, 255, 255)
        self.MAGENTA = (255, 100, 255)
        self.ORANGE = (255, 200, 100)
        
        # Layout constants
        self.map_x = 20
        self.map_y = 20
        self.map_width = 800
        self.map_height = 400
        self.stats_x = 840
        self.stats_y = 20
        self.stats_width = 540
        self.stats_height = 400
        self.log_x = 20
        self.log_y = 440
        self.log_width = 1360
        self.log_height = 420
        
        self.command_input = ""
        self.log_messages = []
        self.max_log_lines = 15
        self.showing_full_screen = None  # "help", "legend", or None
        self.full_screen_text = None  # Text to display for help/legend

    def add_log_message(self, message):
        """Add a message to the game log."""
        self.log_messages.append(message)
        if len(self.log_messages) > self.max_log_lines:
            self.log_messages.pop(0)

    def clear_log(self):
        """Clear all log messages."""
        self.log_messages = []

    def render_text(self, text, font, color):
        """Safely render text, handling different font types (pygame, PIL, None)."""
        if font is None:
            return None
        
        try:
            # Handle PIL fonts
            if PIL_AVAILABLE and hasattr(font, 'getbbox'):
                # This is a PIL font - render using PIL
                # Get approximate text size
                bbox = font.getbbox(text)
                width = bbox[2] - bbox[0] + 2
                height = bbox[3] - bbox[1] + 2
                
                # Create PIL image with transparent background
                pil_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(pil_img)
                draw.text((0, 0), text, font=font, fill=color + (255,))  # Add alpha channel
                
                # Convert PIL image to pygame surface
                pil_str = pil_img.tobytes()
                surf = pygame.image.fromstring(pil_str, pil_img.size, "RGBA")
                return surf
            
            # Handle pygame.freetype.Font
            elif FREETYPE_AVAILABLE and isinstance(font, pygame.freetype.Font):
                surface, rect = font.render(text, fgcolor=color)
                return surface
            
            # Handle pygame.font.Font
            elif hasattr(font, 'render'):
                return font.render(text, True, color)
            else:
                return None
        except Exception:
            return None
    
    def render_bitmap_text(self, text, scale=1, color=(255, 255, 255)):
        """Render text to a surface using simple ASCII art font."""
        if not text:
            return None
        
        pixel_size = 4 * scale
        char_width = (5 * pixel_size) + 2
        char_height = (5 * pixel_size) + 2
        surface_width = len(text) * char_width
        surface_height = char_height
        
        # Create transparent surface
        surf = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        
        # Draw each character
        for i, char in enumerate(text):
            char_x = i * char_width
            
            if char in SIMPLE_FONT:
                pattern = SIMPLE_FONT[char]
                for row_idx, row in enumerate(pattern):
                    for col_idx, pixel in enumerate(row):
                        if pixel == '*':
                            px = char_x + (col_idx * pixel_size)
                            py = row_idx * pixel_size
                            pygame.draw.rect(surf, color, (px, py, pixel_size, pixel_size))
        
        return surf

    def draw_simple_text(self, text, x, y, color, scale=1.0):
        """Draw text using simple ASCII art font renderer."""
        if not text:
            return
        
        pixel_size = int(3 * scale)  # Size of each pixel block
        if pixel_size < 1:
            pixel_size = 1
        char_width = int((5 * pixel_size) + 2)
        char_height = int((5 * pixel_size) + 2)
        
        for i, char in enumerate(text[:100]):
            char_x = x + (i * char_width)
            
            # Skip if off-screen
            if char_x > self.width - 20:
                break
            
            # Get character pattern
            if char in SIMPLE_FONT:
                pattern = SIMPLE_FONT[char]
                # Each row in the pattern
                for row_idx, row in enumerate(pattern):
                    for col_idx, pixel in enumerate(row):
                        if pixel == '*':  # Draw filled pixel
                            px = char_x + (col_idx * pixel_size)
                            py = y + (row_idx * pixel_size)
                            if pixel_size > 1:
                                pygame.draw.rect(self.screen, color, (px, py, pixel_size, pixel_size))
                            else:
                                self.screen.set_at((px, py), color)
            else:
                # Draw placeholder box for unknown character
                pygame.draw.rect(self.screen, color, (char_x, y, char_width - 2, char_height - 2), 1)
    
    def draw_fallback_ui(self):
        """Draw complete UI structure using only rectangles when fonts unavailable."""
        # Map area
        pygame.draw.rect(self.screen, self.DARK_GRAY,
                        (self.map_x, self.map_y, self.map_width, self.map_height))
        pygame.draw.rect(self.screen, self.BRIGHT_GREEN,
                        (self.map_x, self.map_y, self.map_width, self.map_height), 3)
        # Map label box
        pygame.draw.rect(self.screen, self.DARK_GREEN,
                        (self.map_x + 10, self.map_y - 25, 80, 20), 0)
        pygame.draw.rect(self.screen, self.BRIGHT_GREEN,
                        (self.map_x + 10, self.map_y - 25, 80, 20), 2)
        # Grid lines in map
        for i in range(0, self.map_height, 30):
            pygame.draw.line(self.screen, self.DARK_GREEN,
                           (self.map_x + 10, self.map_y + i + 20),
                           (self.map_x + 200, self.map_y + i + 20), 1)
        
        # Stats area
        pygame.draw.rect(self.screen, self.DARK_GRAY,
                        (self.stats_x, self.stats_y, self.stats_width, self.stats_height))
        pygame.draw.rect(self.screen, self.YELLOW,
                        (self.stats_x, self.stats_y, self.stats_width, self.stats_height), 3)
        # Stats label box
        pygame.draw.rect(self.screen, self.RED,
                        (self.stats_x + 10, self.stats_y - 25, 80, 20), 0)
        pygame.draw.rect(self.screen, self.YELLOW,
                        (self.stats_x + 10, self.stats_y - 25, 80, 20), 2)
        # Stat bars in stats area
        for i in range(0, 6):
            bar_y = self.stats_y + 50 + i * 50
            pygame.draw.line(self.screen, self.RED,
                           (self.stats_x + 10, bar_y),
                           (self.stats_x + 200, bar_y), 1)
        
        # Log area
        pygame.draw.rect(self.screen, self.DARK_GRAY,
                        (self.log_x, self.log_y, self.log_width, self.log_height))
        pygame.draw.rect(self.screen, self.CYAN,
                        (self.log_x, self.log_y, self.log_width, self.log_height), 3)
        # Log label box
        pygame.draw.rect(self.screen, self.DARK_GREEN,
                        (self.log_x + 10, self.log_y - 25, 80, 20), 0)
        pygame.draw.rect(self.screen, self.CYAN,
                        (self.log_x + 10, self.log_y - 25, 80, 20), 2)
        # Log lines in log area
        for i in range(0, 10):
            pygame.draw.line(self.screen, self.DARK_GREEN,
                           (self.log_x + 10, self.log_y + 10 + i * 35),
                           (self.log_x + 800, self.log_y + 10 + i * 35), 1)
        
        # Command input area
        pygame.draw.line(self.screen, self.LIGHT_GRAY,
                        (self.log_x, self.log_y + self.log_height + 10),
                        (self.log_x + self.log_width, self.log_y + self.log_height + 10), 2)
        pygame.draw.rect(self.screen, self.DARK_GRAY,
                        (self.log_x, self.log_y + self.log_height + 15, self.log_width, 40))
        pygame.draw.rect(self.screen, self.ORANGE,
                        (self.log_x, self.log_y + self.log_height + 15, self.log_width, 40), 2)
        # Cursor indicator
        pygame.draw.line(self.screen, self.ORANGE,
                        (self.log_x + 15, self.log_y + self.log_height + 25),
                        (self.log_x + 15, self.log_y + self.log_height + 45), 2)

    def draw_fallback_status(self):
        """Draw status message when fonts are unavailable."""
        # Draw status bar at bottom
        pygame.draw.rect(self.screen, (20, 20, 20), (0, self.height - 50, self.width, 50))
        pygame.draw.line(self.screen, self.LIGHT_GRAY, (0, self.height - 50), (self.width, self.height - 50), 2)
        
        # Status indicators (using colored dots)
        # "HOLE WIZARDS" indicator (top left corner)
        pygame.draw.circle(self.screen, self.BRIGHT_GREEN, (50, 50), 10)
        pygame.draw.circle(self.screen, self.BRIGHT_GREEN, (50, 50), 5)
        
        # Mode indicator (top right corner)
        pygame.draw.circle(self.screen, self.YELLOW, (self.width - 50, 50), 8)
        pygame.draw.circle(self.screen, self.YELLOW, (self.width - 50, 50), 4)

    def handle_events(self):
        """Handle pygame events. Returns command or None."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if self.showing_full_screen:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.showing_full_screen = None
                else:
                    if event.key == pygame.K_RETURN:
                        command = self.command_input.strip()
                        self.command_input = ""
                        if command:
                            return command
                    elif event.key == pygame.K_BACKSPACE:
                        self.command_input = self.command_input[:-1]
                    elif event.unicode.isprintable():
                        self.command_input += event.unicode
        
        return None

    def render_map_display(self, map_display):
        """Render the map in the map area."""
        # Background
        pygame.draw.rect(self.screen, self.DARK_GRAY, 
                        (self.map_x, self.map_y, self.map_width, self.map_height))
        pygame.draw.rect(self.screen, self.WHITE,
                        (self.map_x, self.map_y, self.map_width, self.map_height), 2)
        
        # Map title
        if self.font_normal:
            title = self.render_text("MAP", self.font_normal, self.WHITE)
            if title:
                self.screen.blit(title, (self.map_x + 10, self.map_y - 25))
        else:
            self.draw_simple_text("MAP", self.map_x + 10, self.map_y - 25, self.WHITE, scale=0.6)
        
        # Map content - calculate max lines to fill entire window
        lines = map_display.split("\n")
        line_height = 24  # Pixels per line (22 char height + 2 padding)
        available_height = self.map_height - 20  # Account for padding
        max_lines = available_height // line_height
        
        # Calculate character width for alignment
        pixel_size = 4
        char_width = (5 * pixel_size) + 2
        available_width = self.map_width - 20  # Account for padding
        max_chars_per_line = available_width // char_width
        
        # Find the maximum line length
        max_line_length = max(len(line) for line in lines) if lines else 0
        
        y_offset = self.map_y + 10
        for line in lines[:max_lines]:
            # Right-align if the map is at the right edge (shorter line than max possible)
            if max_line_length < max_chars_per_line:
                # Calculate padding to right-align
                padding = max_chars_per_line - len(line)
                x_offset = self.map_x + 10 + (padding * char_width)
            else:
                # Left-align normally
                x_offset = self.map_x + 10
            
            # Render the map line with special character handling
            self.render_map_line(line, x_offset, y_offset)
            y_offset += line_height

    def render_map_line(self, line, x_pos, y_pos):
        """Render a single line of the map, handling special characters."""
        # Special tile characters that need visual rendering
        special_chars = {
            '█': self.DARK_GRAY,  # Wall - gray
            '◆': self.YELLOW,     # Item/bag - yellow
            '▪': self.YELLOW,     # Consumable - yellow
            '╬': self.CYAN,       # Closed door - cyan
            '─': self.BRIGHT_GREEN,  # Open door - green
            'E': self.ORANGE,     # Entrance - orange
            'X': self.MAGENTA,    # Exit - magenta
            'p': self.BRIGHT_GREEN,  # Player - bright green
            'm': self.RED,        # Monster - red
            '?': self.LIGHT_GRAY, # Unknown - gray
        }
        
        # Characters that should display their letter inside the box
        chars_with_labels = {'E', 'X'}
        
        x_offset = x_pos
        for char in line:
            if char in special_chars:
                # Render special character as a colored box/shape
                color = special_chars[char]
                # Draw a filled square for the character
                pygame.draw.rect(self.screen, color, 
                               (x_offset, y_pos, 16, 18))
                # Draw border
                pygame.draw.rect(self.screen, self.WHITE, 
                               (x_offset, y_pos, 16, 18), 1)
                
                # Draw letter inside the box for E and X
                if char in chars_with_labels and self.font_small:
                    text = self.render_text(char, self.font_small, self.WHITE)
                    if text:
                        # Center the text inside the box
                        text_x = x_offset + (16 - text.get_width()) // 2
                        text_y = y_pos + (18 - text.get_height()) // 2
                        self.screen.blit(text, (text_x, text_y))
            else:
                # Render normal character with the font
                if self.font_small:
                    text = self.render_text(char, self.font_small, self.BRIGHT_GREEN)
                    if text:
                        self.screen.blit(text, (x_offset, y_pos))
                else:
                    # Fallback: don't render
                    pass
            
            x_offset += 18  # Move to next character position

    def render_stats_display(self, player, enemy, page="player"):
        """Render stats in the stats area."""
        # Background
        pygame.draw.rect(self.screen, self.DARK_GRAY,
                        (self.stats_x, self.stats_y, self.stats_width, self.stats_height))
        pygame.draw.rect(self.screen, self.WHITE,
                        (self.stats_x, self.stats_y, self.stats_width, self.stats_height), 2)
        
        # Stats title
        if self.font_normal:
            title = self.render_text("STATS", self.font_normal, self.WHITE)
            if title:
                self.screen.blit(title, (self.stats_x + 10, self.stats_y - 25))
        else:
            self.draw_simple_text("STATS", self.stats_x + 10, self.stats_y - 25, self.WHITE, scale=0.6)
        
        # Stats content
        y_offset = self.stats_y + 10
        
        if page == "player" and player:
            stats_text = [
                f"Player: Level {player.level}",
                f"HP: {player.hp}/{player.max_hp}",
                f"Mana: {player.mana}/{player.max_mana}",
                f"XP: {player.xp}/10",
                f"Pos: ({player.position['x']}, {player.position['y']})",
                "",
                f"Equipped Weapon: {player.equipped_weapon or 'None'}",
                f"Equipped Armor: {player.equipped_armor or 'None'}",
                f"Equipped Spell: {player.equipped_spell or 'None'}",
            ]
            
            for line in stats_text:
                if line:
                    color = self.YELLOW if "HP" in line else self.LIGHT_GRAY
                    if self.font_normal:
                        text = self.render_text(line, self.font_normal, color)
                        if text:
                            self.screen.blit(text, (self.stats_x + 10, y_offset))
                    else:
                        self.draw_simple_text(line, self.stats_x + 10, y_offset, color, scale=0.7)
                y_offset += 16
        
        elif page == "enemy" and enemy:
            stats_text = [
                f"Enemy: {enemy.name}",
                f"Level: {enemy.level}",
                f"HP: {enemy.hp}/{enemy.max_hp}",
                f"Mana: {enemy.mana}/{enemy.max_mana}",
                f"Pos: ({enemy.position['x']}, {enemy.position['y']})",
            ]
            
            for line in stats_text:
                color = self.RED if "HP" in line else self.LIGHT_GRAY
                if self.font_normal:
                    text = self.render_text(line, self.font_normal, color)
                    if text:
                        self.screen.blit(text, (self.stats_x + 10, y_offset))
                else:
                    self.draw_simple_text(line, self.stats_x + 10, y_offset, color, scale=0.7)
                y_offset += 16

    def render_log_display(self):
        """Render the game log."""
        # Background
        pygame.draw.rect(self.screen, self.DARK_GRAY,
                        (self.log_x, self.log_y, self.log_width, self.log_height))
        pygame.draw.rect(self.screen, self.WHITE,
                        (self.log_x, self.log_y, self.log_width, self.log_height), 2)
        
        # Log title
        if self.font_normal:
            title = self.render_text("LOG", self.font_normal, self.WHITE)
            if title:
                self.screen.blit(title, (self.log_x + 10, self.log_y - 25))
        else:
            self.draw_simple_text("LOG", self.log_x + 10, self.log_y - 25, self.WHITE, scale=0.6)
        
        # Log messages
        y_offset = self.log_y + 10
        for message in self.log_messages[-self.max_log_lines:]:
            lines = self.wrap_text(message, 150)
            for line in lines:
                if self.font_small:
                    text = self.render_text(line, self.font_small, self.LIGHT_GRAY)
                    if text:
                        self.screen.blit(text, (self.log_x + 10, y_offset))
                else:
                    self.draw_simple_text(line, self.log_x + 10, y_offset, self.LIGHT_GRAY)
                y_offset += 22

    def render_command_input(self):
        """Render the command input area."""
        # Background
        pygame.draw.line(self.screen, self.LIGHT_GRAY,
                        (self.log_x, self.log_y + self.log_height + 10),
                        (self.log_x + self.log_width, self.log_y + self.log_height + 10), 2)
        
        # Prompt and input
        if self.font_normal:
            prompt = self.render_text("> ", self.font_normal, self.CYAN)
            if prompt:
                self.screen.blit(prompt, (self.log_x + 10, self.log_y + self.log_height + 20))
            
            input_text = self.render_text(self.command_input, self.font_normal, self.WHITE)
            if input_text:
                self.screen.blit(input_text, (self.log_x + 40, self.log_y + self.log_height + 20))
        else:
            self.draw_simple_text("> " + self.command_input, self.log_x + 10, self.log_y + self.log_height + 20, self.CYAN)

    def render_help_screen(self, help_text):
        """Render a full-screen help/legend display."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(30)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Help box
        box_width = 1000
        box_height = 700
        box_x = (self.width - box_width) // 2
        box_y = (self.height - box_height) // 2
        
        pygame.draw.rect(self.screen, self.DARK_GRAY, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, self.BRIGHT_GREEN, (box_x, box_y, box_width, box_height), 3)
        
        # Special characters mapping for legend display
        special_chars = {
            '█': self.DARK_GRAY,      # Wall - gray
            '◆': self.YELLOW,         # Item - yellow
            '▪': self.YELLOW,         # Consumable - yellow
            '╬': self.CYAN,           # Closed door - cyan
            '─': self.BRIGHT_GREEN,   # Open door - green
            '?': self.LIGHT_GRAY,     # Unknown - gray (white box)
        }
        
        # Text using small font - readable and compact
        y_offset = box_y + 20
        line_height = 16
        
        for line in help_text.split("\n"):
            if line.strip():
                # Render line with special character handling
                self._render_legend_line(line, box_x + 20, y_offset, special_chars)
            y_offset += line_height
        
        # Instructions using normal font
        if self.font_normal:
            instr = self.render_text("Press Enter or ESC to close", self.font_normal, self.YELLOW)
            if instr:
                self.screen.blit(instr, (box_x + 20, box_y + box_height - 30))
        else:
            self.draw_simple_text("Press Enter or ESC to close", box_x + 20, box_y + box_height - 30, self.YELLOW)

    def _render_legend_line(self, line, x_pos, y_pos, special_chars):
        """Render a line from legend, handling special characters as colored boxes."""
        x_offset = x_pos
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if char in special_chars:
                # Draw colored box for special character
                color = special_chars[char]
                pygame.draw.rect(self.screen, color, (x_offset, y_pos, 14, 14))
                pygame.draw.rect(self.screen, self.WHITE, (x_offset, y_pos, 14, 14), 1)
                x_offset += 16
                i += 1
            elif char == ' ':
                x_offset += 8
                i += 1
            else:
                # Render normal text - find the next special character or end
                text_chunk = ""
                while i < len(line) and line[i] not in special_chars and line[i] != ' ':
                    text_chunk += line[i]
                    i += 1
                
                if text_chunk:
                    if self.font_small:
                        text = self.render_text(text_chunk, self.font_small, self.LIGHT_GRAY)
                        if text:
                            self.screen.blit(text, (x_offset, y_pos))
                            x_offset += text.get_width() + 2
                    else:
                        self.draw_simple_text(text_chunk, x_offset, y_pos, self.LIGHT_GRAY, scale=0.7)
                        x_offset += len(text_chunk) * 8

    def _get_message_file(self, filename):
        """Get path to a message file in data/messages/."""
        # Try multiple possible locations
        possible_paths = [
            Path(__file__).parent / "data" / "messages" / filename,
            Path(__file__).parent.parent / "data" / "messages" / filename,
            Path.cwd() / "data" / "messages" / filename,
        ]
        for path in possible_paths:
            if path.exists():
                return str(path)
        return None

    def render_intro_screen(self):
        """Render the intro screen."""
        self.screen.fill(self.BLACK)
        
        # Title - use title font if available
        if self.font_title:
            title = self.render_text("HOLE WIZARDS", self.font_title, self.BRIGHT_GREEN)
            if title:
                self.screen.blit(title, (self.width // 2 - 150, 50))
        else:
            self.draw_simple_text("HOLE WIZARDS", self.width // 2 - 150, 50, self.BRIGHT_GREEN)
        
        # Load intro text from file
        intro_lines = []
        intro_msg_path = self._get_message_file("intro.msg")
        if intro_msg_path:
            try:
                with open(intro_msg_path, 'r') as f:
                    intro_lines = f.read().strip().split("\n")
            except:
                pass
        
        # Fallback intro text if file not found
        if not intro_lines:
            intro_lines = [
                "You have entered the Hole!",
                "A place of terror and riches!",
                "You are a wizard!",
                "",
                "Other wizards block your exit.",
                "Beat them up, take their stuff!",
                "ESCAPE THE HOLE!",
                "",
                "Controls:",
                "move up/down/left/right",
                "attack, defend",
                "take/drop/equip/use",
                "show player",
                "quit, restart",
            ]
        
        y_offset = 150
        for line in intro_lines:
            if line:
                # Use normal font if available, otherwise fallback to simple text
                if self.font_normal:
                    text_surface = self.render_text(line, self.font_normal, self.LIGHT_GRAY)
                    if text_surface:
                        self.screen.blit(text_surface, (100, y_offset))
                    else:
                        self.draw_simple_text(line, 100, y_offset, self.LIGHT_GRAY)
                else:
                    self.draw_simple_text(line, 100, y_offset, self.LIGHT_GRAY)
            y_offset += 30
        
        # Instructions - use normal font if available
        if self.font_normal:
            instr = self.render_text("Press Enter to begin...", self.font_normal, self.YELLOW)
            if instr:
                self.screen.blit(instr, (self.width // 2 - 200, self.height - 80))
            else:
                self.draw_simple_text("Press Enter to begin...", self.width // 2 - 200, self.height - 80, self.YELLOW)
        else:
            self.draw_simple_text("Press Enter to begin...", self.width // 2 - 200, self.height - 80, self.YELLOW)
        
        pygame.display.flip()
        
        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
        
        return True

    def render_victory_screen(self):
        """Render the victory screen."""
        self.screen.fill(self.BLACK)
        
        # Title - use title font if available
        if self.font_title:
            title = self.render_text("VICTORY!", self.font_title, self.BRIGHT_GREEN)
            if title:
                self.screen.blit(title, (self.width // 2 - 120, 50))
        else:
            self.draw_simple_text("VICTORY!", self.width // 2 - 120, 50, self.BRIGHT_GREEN)
        
        # Load and display victory message
        victory_msg = None
        victory_msg_path = self._get_message_file("victory.msg")
        if victory_msg_path:
            try:
                with open(victory_msg_path, 'r') as f:
                    victory_msg = f.read().strip()
            except:
                pass
        
        if not victory_msg:
            victory_msg = "You have escaped the Hole with your life!\nThe other wizards have fallen and their treasures are yours!"
        
        # Display message - use normal font if available
        y_offset = 150
        for line in victory_msg.split("\n"):
            if line.strip():
                if self.font_normal:
                    text_surface = self.render_text(line, self.font_normal, self.LIGHT_GRAY)
                    if text_surface:
                        self.screen.blit(text_surface, (100, y_offset))
                    else:
                        self.draw_simple_text(line, 100, y_offset, self.LIGHT_GRAY, scale=0.8)
                else:
                    self.draw_simple_text(line, 100, y_offset, self.LIGHT_GRAY, scale=0.8)
            y_offset += 40
        
        # Instructions - use normal font if available
        if self.font_normal:
            instr = self.render_text("Press Enter to continue... Q/ESC to quit", self.font_normal, self.YELLOW)
            if instr:
                self.screen.blit(instr, (self.width // 2 - 350, self.height - 80))
            else:
                self.draw_simple_text("Press Enter to continue... Q/ESC to quit", self.width // 2 - 350, self.height - 80, self.YELLOW)
        else:
            self.draw_simple_text("Press Enter to continue... Q/ESC to quit", self.width // 2 - 350, self.height - 80, self.YELLOW)
        
        pygame.display.flip()
        
        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return "quit"
        
        return "continue"

    def render_defeat_screen(self):
        """Render the defeat screen."""
        self.screen.fill(self.BLACK)
        
        # Title - use title font if available
        if self.font_title:
            title = self.render_text("DEFEAT!", self.font_title, self.RED)
            if title:
                self.screen.blit(title, (self.width // 2 - 120, 50))
        else:
            self.draw_simple_text("DEFEAT!", self.width // 2 - 120, 50, self.RED)
        
        # Load and display defeat message
        defeat_msg = None
        defeat_msg_path = self._get_message_file("defeat.msg")
        if defeat_msg_path:
            try:
                with open(defeat_msg_path, 'r') as f:
                    defeat_msg = f.read().strip()
            except:
                pass
        
        if not defeat_msg:
            defeat_msg = "You have fallen in the Hole.\nYour adventure has ended..."
        
        # Display message - use normal font if available
        y_offset = 150
        for line in defeat_msg.split("\n"):
            if line.strip():
                if self.font_normal:
                    text_surface = self.render_text(line, self.font_normal, self.LIGHT_GRAY)
                    if text_surface:
                        self.screen.blit(text_surface, (100, y_offset))
                    else:
                        self.draw_simple_text(line, 100, y_offset, self.LIGHT_GRAY, scale=0.8)
                else:
                    self.draw_simple_text(line, 100, y_offset, self.LIGHT_GRAY, scale=0.8)
            y_offset += 40
        
        # Instructions - use normal font if available
        if self.font_normal:
            instr = self.render_text("Press Enter to continue... Q/ESC to quit", self.font_normal, self.YELLOW)
            if instr:
                self.screen.blit(instr, (self.width // 2 - 350, self.height - 80))
            else:
                self.draw_simple_text("Press Enter to continue... Q/ESC to quit", self.width // 2 - 350, self.height - 80, self.YELLOW)
        else:
            self.draw_simple_text("Press Enter to continue... Q/ESC to quit", self.width // 2 - 350, self.height - 80, self.YELLOW)
        
        pygame.display.flip()
        
        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return "quit"
        
        return "continue"

    def render(self, player, enemy, map_display, page="player"):
        """Render the complete game screen."""
        self.screen.fill(self.BLACK)
        
        # Always render game content
        # Check if showing full screen
        if self.showing_full_screen in ["help", "legend"]:
            # Render help or legend screen
            if self.full_screen_text:
                self.render_help_screen(self.full_screen_text)
        else:
            # Normal game view - always render content
            self.render_map_display(map_display)
            self.render_stats_display(player, enemy, page)
            self.render_log_display()
            self.render_command_input()
        
        pygame.display.flip()

    def wrap_text(self, text, max_length):
        """Wrap text to fit within max length."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 > max_length:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line += " " + word if current_line else word
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def get_fps(self):
        """Get current FPS."""
        return self.clock.get_fps()

    def tick(self, fps=60):
        """Update clock and maintain FPS."""
        self.clock.tick(fps)

    def quit(self):
        """Quit pygame."""
        pygame.quit()
