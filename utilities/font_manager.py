#!/usr/bin/env python3
"""Utility to manage Hole Wizards font settings."""

import os
import sys
from configparser import ConfigParser
from pathlib import Path


def get_available_fonts():
    """List all available fonts in data/fonts/ folder."""
    # Get the project root (parent of utilities folder)
    project_root = Path(__file__).parent.parent
    fonts_dir = project_root / 'data' / 'fonts'
    if not fonts_dir.exists():
        return []
    
    fonts = []
    for ext in ['*.ttf', '*.otf', '*.TTF', '*.OTF']:
        fonts.extend([f.name for f in fonts_dir.glob(ext)])
    
    return sorted(fonts)


def get_current_font():
    """Get currently configured font from settings.cfg."""
    project_root = Path(__file__).parent.parent
    settings_path = project_root / 'data' / 'settings.cfg'
    
    if not settings_path.exists():
        return None
    
    try:
        config = ConfigParser()
        config.read(settings_path)
        if config.has_option('display', 'font'):
            return config.get('display', 'font').strip()
    except Exception as e:
        print(f"Error reading settings: {e}")
    
    return None


def set_font(font_name):
    """Set the font in settings.cfg."""
    project_root = Path(__file__).parent.parent
    settings_path = project_root / 'data' / 'settings.cfg'
    
    if not settings_path.exists():
        print(f"Error: {settings_path} not found")
        return False
    
    try:
        config = ConfigParser()
        config.read(settings_path)
        
        if not config.has_section('display'):
            config.add_section('display')
        
        config.set('display', 'font', font_name)
        
        with open(settings_path, 'w') as f:
            config.write(f)
        
        print(f"✓ Font set to: {font_name}")
        return True
    except Exception as e:
        print(f"Error setting font: {e}")
        return False


def main():
    """Main CLI interface."""
    fonts = get_available_fonts()
    current_font = get_current_font()
    
    if not fonts:
        print("No fonts found in data/fonts/")
        return
    
    print("\n" + "="*60)
    print("HOLE WIZARDS - Font Manager")
    print("="*60)
    
    print(f"\nCurrent font: {current_font or 'system default'}")
    
    print("\nAvailable fonts:")
    for i, font in enumerate(fonts, 1):
        marker = " ←" if font == current_font else ""
        print(f"  {i}. {font}{marker}")
    
    if len(sys.argv) > 1:
        # Non-interactive mode: set font directly
        font_name = sys.argv[1]
        if font_name in fonts:
            set_font(font_name)
        else:
            print(f"Error: Font '{font_name}' not found")
            print(f"Available fonts: {', '.join(fonts)}")
        return
    
    # Interactive mode
    while True:
        print("\nOptions:")
        print("  q  - Quit")
        print("  d  - Use system default")
        print("  1-{:d}  - Choose font".format(len(fonts)))
        
        choice = input("\nSelect option: ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 'd':
            set_font('')
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(fonts):
                    set_font(fonts[idx])
                else:
                    print("Invalid selection")
            except ValueError:
                print("Invalid input")
    
    print("\nGoodbye!")


if __name__ == '__main__':
    main()
