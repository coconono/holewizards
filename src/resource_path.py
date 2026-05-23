"""Utility for getting resource paths that work in both development and PyInstaller bundles."""

import sys
import os
from pathlib import Path


def get_resource_path(relative_path=""):
    """Get absolute path to resource, works for dev and for PyInstaller bundles.
    
    Args:
        relative_path: Path relative to project root (e.g., "data/monsters.cfg")
    
    Returns:
        Absolute path to the resource
    """
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if getattr(sys, '_MEIPASS', None):
        base_path = Path(sys._MEIPASS)
    else:
        # Running in development mode
        base_path = Path(__file__).parent.parent
    
    if relative_path:
        return base_path / relative_path
    return base_path


def get_data_path(data_relative_path):
    """Get path to file in data directory.
    
    Args:
        data_relative_path: Path relative to data/ folder (e.g., "monsters.cfg" or "png/spr_chest.png")
    
    Returns:
        Absolute path to the data file
    """
    return get_resource_path("data") / data_relative_path
