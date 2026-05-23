# building binary executables for Windows, MacOS, and Linux

## Overview

Create three OS-native build scripts: each script is intended to run only on its corresponding OS (Windows script on Windows, macOS script on macOS, Linux script on Linux). PyInstaller does not reliably cross-compile across operating systems.

Each script should be executed from the project root directory.

## Prerequisites

- Python 3.8+
- PyInstaller installed: `pip install pyinstaller`
- All scripts must be run from project root directory
- update requirements.txt to include pyinstaller if not already included
- update gitignore to exclude build artifacts: `build/`, `dist/`, and `*.spec` files

## Common Build Requirements

Place each script in the project-root relative path `utils/` (not an absolute path). Name them: build_windows.sh, build_macos.sh, and build_linux.sh.

All scripts must:
- Use `src/main.py` as the entry point
- Include game assets with `--add-data` flag:
  - Windows: `--add-data "data;data"`
  - macOS/Linux: `--add-data "data:data"`
- Clean build artifacts before building: `rm -rf build/ dist/ *.spec`
- Create `dist/` directory if it doesn't exist
- Bundle Python dependencies with PyInstaller (system-provided OS libraries may still be required)

Target architectures: Windows x86_64, macOS native (arm64 or x86_64 depending on build machine), Linux x86_64.

Note: macOS builds target the native architecture only due to Pillow library constraints. Universal2 builds are not supported.

Output requirements:
- Use PyInstaller `--onefile` for Windows and Linux to produce single executable binaries
- For macOS, produce a `.app` bundle using `--windowed --name holewizards_macos` (application bundle, not a single file)
- All outputs go in the project-root relative `dist/` directory

## windows

Script to build a single-file binary executable for Windows using pyinstaller.

Place script at: `utils/build_windows.sh`

Output location: `dist/holewizards_windows.exe`

Requirements:
- Clean artifacts: `rm -rf build/ dist/ *.spec`
- Use PyInstaller with `--onefile` flag
- Include data folder: `--add-data "data;data"` (Windows uses semicolon)
- Target architecture: x86_64
- Entry point: `src/main.py`

## macos

Script to build a macOS application bundle using pyinstaller.

Place script at: `utils/build_macos.sh`

Output location: `dist/holewizards_macos.app` (application bundle directory structure, not a single file)

Requirements:
- Clean artifacts: `rm -rf build/ dist/ *.spec`
- Use PyInstaller with `--windowed --name holewizards_macos` flags
- Include data folder: `--add-data "data:data"` (macOS uses colon)
- Target architecture: native (arm64 on Apple Silicon, x86_64 on Intel)
- Entry point: `src/main.py`
- Note: `.app` bundle is a directory structure containing the executable and resources
- Universal2 builds not supported due to Pillow library binary constraints

## linux

Script to build a single-file binary executable for Linux using pyinstaller.

Place script at: `utils/build_linux.sh`

Output location: `dist/holewizards_linux`

Requirements:
- Clean artifacts: `rm -rf build/ dist/ *.spec`
- Use PyInstaller with `--onefile` flag
- Include data folder: `--add-data "data:data"` (Linux uses colon)
- Target architecture: x86_64
- Entry point: `src/main.py`

## Testing the Builds

After building, verify each executable:
1. Run on a clean system without Python installed
2. Verify all game assets load correctly:
   - 100 monsters from `data/monsters.cfg`
   - Weapons, armor, spells from config files
   - PNG sprites from `data/png/`
   - Fonts from `data/fonts/`
   - Message files (intro, victory, defeat)
3. Test basic gameplay (movement, combat, inventory)
4. Check console for errors about missing files or dependencies
