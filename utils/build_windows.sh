#!/bin/bash
# Build script for Windows executable
# Run this script from the project root directory on a Windows machine

set -e  # Exit on error

echo "Building Hole Wizards for Windows..."

# Check if running from project root
if [ ! -f "src/main.py" ]; then
    echo "Error: This script must be run from the project root directory"
    exit 1
fi

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Error: PyInstaller is not installed"
    echo "Install it with: pip install pyinstaller"
    exit 1
fi

# Clean previous build artifacts
echo "Cleaning previous build artifacts..."
rm -rf build/ dist/ *.spec

# Create dist directory if it doesn't exist
mkdir -p dist

# Build the executable
echo "Building Windows executable..."
pyinstaller \
    --onefile \
    --add-data "data;data" \
    --name holewizards_windows \
    src/main.py

echo ""
echo "✓ Build complete!"
echo "Output location: dist/holewizards_windows.exe"
echo ""
echo "Testing checklist:"
echo "1. Run on a clean Windows system without Python"
echo "2. Verify all game assets load (monsters, sprites, fonts, messages)"
echo "3. Test basic gameplay (movement, combat, inventory)"
