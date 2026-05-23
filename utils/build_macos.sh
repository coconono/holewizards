#!/bin/bash
# Build script for macOS application bundle
# Run this script from the project root directory on a macOS machine

set -e  # Exit on error

echo "Building Hole Wizards for macOS..."

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

# Build the application bundle
echo "Building macOS application bundle..."
pyinstaller \
    --windowed \
    --name holewizards_macos \
    --add-data "data:data" \
    src/main.py

echo ""
echo "✓ Build complete!"
echo "Output location: dist/holewizards_macos.app"
echo "Note: .app is a directory structure (application bundle), not a single file"
echo ""
echo "Testing checklist:"
echo "1. Run on a clean macOS system without Python"
echo "2. Verify all game assets load (monsters, sprites, fonts, messages)"
echo "3. Test basic gameplay (movement, combat, inventory)"
echo "4. Double-click holewizards_macos.app to launch"
