#!/bin/bash
# Build script for Linux executable
# Run this script from the project root directory on a Linux machine

set -e  # Exit on error

echo "Building Hole Wizards for Linux..."

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
echo "Building Linux executable..."
pyinstaller \
    --onefile \
    --add-data "data:data" \
    --name holewizards_linux \
    src/main.py

echo ""
echo "✓ Build complete!"
echo "Output location: dist/holewizards_linux"
echo ""
echo "Testing checklist:"
echo "1. Run on a clean Linux system without Python"
echo "2. Verify all game assets load (monsters, sprites, fonts, messages)"
echo "3. Test basic gameplay (movement, combat, inventory)"
echo "4. Make executable if needed: chmod +x dist/holewizards_linux"
