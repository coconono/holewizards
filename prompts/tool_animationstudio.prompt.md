# Animation Studio Tool Design

Purpose: Define a pygame-based utility for building sprite compositions and timeline animations from PNG assets.

Status: Ready for Implementation

## Overview

Animation Studio is a standalone utility under utilities that allows a user to:

1. Load PNG assets from a folder
2. Arrange assets in a 2D canvas
3. Save arrangements as named frames
4. Organize frames into a named library
5. Build and preview named timelines from library frames
6. Save and load all artifacts from disk

This tool is editor-side content tooling and does not change game runtime mechanics.

## Scope

### In Scope (MVP)

- Desktop window built with pygame
- Mouse-based placement and selection
- Keyboard shortcuts for editing
- Per-layer transform controls:
	- Position x/y
	- Flip horizontal
	- Flip vertical
	- Draw order (z-index)
	- Visibility toggle
	- Opacity 0-255
- Frame save/load to .frame files
- Frame library save/load to .library files
- Timeline save/load to .timeline files
- Timeline playback with FPS control

### Out of Scope (MVP)

- Rotation and scaling
- Onion skinning
- Skeletal animation
- Video export or GIF export
- Undo/redo history beyond single-step revert

## Utility Location and Entrypoint

- File path: utilities/animation_studio.py
- Start command: python3 utilities/animation_studio.py
- Optional argument: --assets-dir data/png

## Data Model

### AssetReference

- id: string (stable UUID)
- file_path: string (relative path)
- source_width: int
- source_height: int

### LayerInstance

- layer_id: string (stable UUID)
- asset_id: string
- x: int
- y: int
- z_index: int
- flip_x: bool
- flip_y: bool
- visible: bool
- opacity: int (0-255)

### Frame

- name: string (unique within library)
- canvas_width: int
- canvas_height: int
- background_rgba: [int, int, int, int]
- layers: list[LayerInstance]

### FrameLibrary

- name: string
- version: string (start at 1)
- assets: list[AssetReference]
- frames: list[Frame]

### TimelineClip

- frame_name: string (must exist in library)
- duration_ms: int (minimum 16)

### Timeline

- name: string
- library_name: string
- fps_override: int or null
- loop: bool
- clips: list[TimelineClip]

## File Formats

All files are UTF-8 JSON with deterministic key order.

### .frame

- Contains one Frame object
- Includes version field

### .library

- Contains one FrameLibrary object
- Includes version field

### .timeline

- Contains one Timeline object
- Includes version field

### Validation Rules

- Names cannot be empty
- Duplicate frame names are rejected
- Timeline clips referencing missing frame names are rejected
- Missing asset files during load are flagged and skipped, not fatal

## UI Layout

- Left panel: asset browser
- Center panel: canvas viewport
- Right panel: selected layer inspector
- Bottom panel: timeline editor and playback controls
- Top status bar: current file, dirty state, active mode

## Interaction Model

### Selection and Placement

- Click asset in left panel to arm placement mode
- Click canvas to place a new layer instance
- Click existing layer to select it

### Transform Controls

- Drag selected layer to move
- Arrow keys nudge by 1 pixel
- Shift + arrow keys nudge by 10 pixels
- H toggles flip_x
- V toggles flip_y
- PageUp brings layer forward (+1 z-index)
- PageDown sends layer backward (-1 z-index)
- Delete removes selected layer

### File Operations

- Ctrl+N new frame
- Ctrl+S save frame
- Ctrl+L save library
- Ctrl+O load file chooser for frame/library/timeline

### Timeline Operations

- Add selected frame to timeline with default duration 100 ms
- Edit clip duration in bottom panel
- Space toggles play/pause
- Shift+Space toggles loop mode
- FPS selector supports: 12, 24, 30, 60

## Runtime Behavior

- Canvas draw order is ascending z-index
- Hidden layers are not drawn
- Opacity applies per layer at render time
- Playback advances by clip duration, not fixed frame count
- If fps_override is set, playback uses that cadence for redraw but still honors clip duration boundaries

## Persistence and Paths

- Save outputs to a user-selected folder (default utilities/animation_studio_output)
- Persist relative asset paths against chosen assets root
- On load, resolve relative paths from file location first, then from assets root

## Error Handling

- Invalid JSON: show modal with parse error line/column
- Schema mismatch: show list of invalid fields
- Missing PNG file: show warning and placeholder checkerboard sprite
- Save failure: show file path and OS error reason

## Testing Requirements

### Unit Tests

- Serialization round-trip for Frame, FrameLibrary, Timeline
- Validation rejects duplicate frame names
- Validation rejects timeline clips with missing frame references
- Layer sort order and visibility behavior

### Integration Tests

- Load assets, place layers, save frame, reload frame
- Save library, create timeline from frames, save timeline, reload timeline
- Playback respects clip duration and loop setting

## Acceptance Criteria

1. User can load PNGs and place multiple layers on canvas.
2. User can move, flip, reorder, hide, and delete layers.
3. User can save and reload a frame without data loss.
4. User can save and reload a frame library with multiple frames.
5. User can build, save, load, and play a timeline from library frames.
6. Tool handles missing assets without crashing.
7. All tests listed above pass locally.

## Implementation Notes

- Use pygame only for MVP UI.
- Keep rendering and persistence logic in separate modules for testability.
- Start with fixed canvas size 800x450 for MVP.
- Keep schema version fields for future migrations.
