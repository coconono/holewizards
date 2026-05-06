# GitHub Copilot Instructions for Hole Wizards

**Key Principle:** This project uses prompt-driven development. All game mechanics are defined in `.md` design files **before** code generation.

## Code Generation Rule

When implementing features:
1. **Always reference `prompt_initial.md`** (or other design files) for requirements
2. **Build exactly what's specified**, no creative embellishment
3. **Ask for clarification** if specs are ambiguous

## Hard Boundaries

❌ **Do NOT:**
- Auto-generate flavor text, monster names, or item descriptions
- Create narrative content (those are human-written)
- Assume features beyond what's documented in `.md` files

✅ **DO:**
- Implement mechanics from `prompt_initial.md`
- Follow the UI structure: map (top-left), stats (top-right), log (bottom)
- Use clean class structures (Player, Enemy, Item, GameState, etc.)

## File Structure

- `prompt_initial.md` → Core game design & mechanics
- `prompt_*.md` → Feature-specific design files (create as needed)
- `AGENTS.md` → Full developer philosophy & guidelines
- `manifesto.md` → Why this approach is used

## For New Features

1. Update the relevant `prompt_*.md` file with requirements
2. Request code implementation referencing that file
3. Mistakes help refine the design—iterate on the `.md` before re-implementing
