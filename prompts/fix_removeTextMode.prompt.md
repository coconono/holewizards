# Remove Text Mode - Graphics Only

**Purpose:** Eliminate text-based UI mode from the codebase and establish graphics mode as the sole rendering system.

**Status:** Ready for Implementation

---

## Overview

The game currently supports both text mode and graphics mode via command-line arguments and conditional rendering logic. This creates technical debt and maintenance burden. By removing text mode entirely, we simplify the codebase, reduce branching logic, and establish graphics as the primary and only rendering system.

---

## Scope of Changes

### Code Cleanup Targets

1. **Command-line Arguments**
   - Remove `--text-mode` or similar flags from argument parser
   - Remove `--graphics-mode` flag (graphics should be default/only)
   - Keep only essential arguments (debug, verbose, etc.)

2. **Conditional Rendering Logic**
   - Remove all `if mode == 'text'` or similar conditional checks
   - Remove all `if mode == 'graphics'` conditions (always true now)
   - Eliminate render mode switching logic

3. **Main Game Loop**
   - Consolidate to graphics-only input/rendering path
   - Remove text mode input handling (if separate)
   - Keep only graphics-mode frame updates

4. **UI Module**
   - Remove text-only rendering functions
   - Remove mode detection/switching code
   - Keep graphics rendering pipeline intact

5. **Documentation & Instructions**
   - Update `readme.md` to remove text mode mentions
   - Update `SETUP.md` to remove text mode setup steps
   - Update any help text or usage instructions
   - Verify all comments referencing text mode are removed or updated

### Files to Review/Modify

- `src/main.py` - Remove mode argument parsing and conditional logic
- `src/ui.py` - Remove text rendering code paths
- `src/graphics.py` - Ensure graphics rendering is unconditional
- `src/game_state.py` - Remove any mode-related state
- `readme.md` - Remove text mode documentation
- `SETUP.md` - Remove text mode setup instructions
- `run_game.sh` - Remove text mode launch options
- Any build/deployment scripts - Remove text mode references

---

## Implementation Details

### Step 1: Remove Command-Line Argument Parsing
- Delete argument parser entries for `--text-mode` and `--graphics-mode`
- Test that the game launches without mode arguments
- Ensure any remaining legitimate arguments still work

### Step 2: Remove Conditional Mode Logic
- Identify all instances of mode checking (grep for "text_mode", "graphics_mode", "mode ==", etc.)
- Remove conditional branches that execute text-only code
- Remove conditional branches that execute graphics-only code (keep the body)
- Ensure game flow remains logically correct

### Step 3: Consolidate Input/Rendering
- Remove text-mode input handling if it differs from graphics input
- Keep graphics-mode input pipeline only
- Verify main loop calls only graphics rendering

### Step 4: Clean Up UI Module
- Remove text-rendering functions (if any)
- Remove mode-detection utilities
- Simplify any mode-switching logic to direct graphics calls

### Step 5: Update Documentation
- Edit `readme.md` to remove text mode mentions
- Edit `SETUP.md` to remove text mode instructions
- Update `run_game.sh` to remove text mode launch option
- Search codebase comments for "text mode" references and update

### Step 6: Verify Graphics is Functional
- Launch game and confirm graphics display works
- Test all UI screens (player stats, inventory, etc.)
- Confirm no residual text-mode behavior

---

## Success Criteria

- [ ] No command-line arguments reference text/graphics mode
- [ ] No conditional mode-checking code remains in codebase
- [ ] Game launches and runs in graphics mode only
- [ ] All documentation updated to reflect graphics-only operation
- [ ] No "text mode" or "graphics mode" references in comments or strings
- [ ] All UI screens display correctly in graphics
- [ ] No floating imports or unused mode-related imports

---

## Testing Checklist

1. Launch game without any arguments - graphics should display
2. Test all UI screens (player, enemy, inventory, chest stats)
3. Test movement and combat - should work in graphics
4. Test all player commands - should work in graphics
5. Verify error messages and logs display correctly
6. Check build scripts still work (`run_game.sh`, Windows/Linux builds)