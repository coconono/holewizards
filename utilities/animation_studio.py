#!/usr/bin/env python3
"""PNG Animation Studio utility.

MVP tool for arranging PNG assets into frames, grouping frames into a library,
and building timeline playback clips.
"""

from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


SCHEMA_VERSION = "1"
DEFAULT_CANVAS_SIZE = (800, 450)
FPS_CHOICES = [12, 24, 30, 60]

# 5x7 bitmap fallback font for environments where pygame text modules are unavailable.
BITMAP_FONT_5X7 = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "10001", "11001", "10101", "10011", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "00100", "00100"],
    ":": ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "/": ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
    "|": ["00100", "00100", "00100", "00100", "00100", "00100", "00100"],
    "[": ["01110", "01000", "01000", "01000", "01000", "01000", "01110"],
    "]": ["01110", "00010", "00010", "00010", "00010", "00010", "01110"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    ",": ["00000", "00000", "00000", "00000", "00100", "00100", "01000"],
    "=": ["00000", "11111", "00000", "11111", "00000", "00000", "00000"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
}


def _new_id() -> str:
    return str(uuid.uuid4())


def _asset_id_from_path(relative_path: str) -> str:
    """Create stable asset IDs so saved layer references remain valid."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"holewizards-asset:{relative_path}"))


def discover_library_files(output_dir: Path) -> List[Path]:
    """Return discovered .library files in deterministic order."""
    if not output_dir.exists():
        return []
    return sorted(output_dir.glob("*.library"), key=lambda path: path.name.lower())


@dataclass
class AssetReference:
    id: str
    file_path: str
    source_width: int
    source_height: int


@dataclass
class LayerInstance:
    layer_id: str
    asset_id: str
    x: int
    y: int
    z_index: int
    flip_x: bool = False
    flip_y: bool = False
    visible: bool = True
    opacity: int = 255


@dataclass
class Frame:
    name: str
    canvas_width: int = DEFAULT_CANVAS_SIZE[0]
    canvas_height: int = DEFAULT_CANVAS_SIZE[1]
    background_rgba: List[int] = field(default_factory=lambda: [20, 20, 20, 255])
    layers: List[LayerInstance] = field(default_factory=list)


@dataclass
class FrameLibrary:
    name: str
    version: str = SCHEMA_VERSION
    assets: List[AssetReference] = field(default_factory=list)
    frames: List[Frame] = field(default_factory=list)


@dataclass
class TimelineClip:
    frame_name: str
    duration_ms: int


@dataclass
class Timeline:
    name: str
    library_name: str
    fps_override: Optional[int] = None
    loop: bool = True
    clips: List[TimelineClip] = field(default_factory=list)


def layer_to_dict(layer: LayerInstance) -> Dict:
    return asdict(layer)


def layer_from_dict(data: Dict) -> LayerInstance:
    return LayerInstance(
        layer_id=str(data["layer_id"]),
        asset_id=str(data["asset_id"]),
        x=int(data["x"]),
        y=int(data["y"]),
        z_index=int(data["z_index"]),
        flip_x=bool(data.get("flip_x", False)),
        flip_y=bool(data.get("flip_y", False)),
        visible=bool(data.get("visible", True)),
        opacity=max(0, min(255, int(data.get("opacity", 255)))),
    )


def frame_to_dict(frame: Frame) -> Dict:
    return {
        "version": SCHEMA_VERSION,
        "frame": {
            "name": frame.name,
            "canvas_width": frame.canvas_width,
            "canvas_height": frame.canvas_height,
            "background_rgba": list(frame.background_rgba),
            "layers": [layer_to_dict(layer) for layer in frame.layers],
        },
    }


def frame_from_dict(data: Dict) -> Frame:
    frame_data = data.get("frame", data)
    frame = Frame(
        name=str(frame_data["name"]),
        canvas_width=int(frame_data.get("canvas_width", DEFAULT_CANVAS_SIZE[0])),
        canvas_height=int(frame_data.get("canvas_height", DEFAULT_CANVAS_SIZE[1])),
        background_rgba=list(frame_data.get("background_rgba", [20, 20, 20, 255])),
        layers=[layer_from_dict(layer) for layer in frame_data.get("layers", [])],
    )
    validate_frame(frame)
    return frame


def library_to_dict(library: FrameLibrary) -> Dict:
    return {
        "version": SCHEMA_VERSION,
        "library": {
            "name": library.name,
            "version": library.version,
            "assets": [asdict(asset) for asset in library.assets],
            "frames": [frame_to_dict(frame)["frame"] for frame in library.frames],
        },
    }


def library_from_dict(data: Dict) -> FrameLibrary:
    lib_data = data.get("library", data)
    assets = [
        AssetReference(
            id=str(asset["id"]),
            file_path=str(asset["file_path"]),
            source_width=int(asset["source_width"]),
            source_height=int(asset["source_height"]),
        )
        for asset in lib_data.get("assets", [])
    ]

    frames = [
        frame_from_dict({"frame": frame_data})
        for frame_data in lib_data.get("frames", [])
    ]

    library = FrameLibrary(
        name=str(lib_data["name"]),
        version=str(lib_data.get("version", SCHEMA_VERSION)),
        assets=assets,
        frames=frames,
    )
    validate_library(library)
    return library


def timeline_to_dict(timeline: Timeline) -> Dict:
    return {
        "version": SCHEMA_VERSION,
        "timeline": {
            "name": timeline.name,
            "library_name": timeline.library_name,
            "fps_override": timeline.fps_override,
            "loop": timeline.loop,
            "clips": [asdict(clip) for clip in timeline.clips],
        },
    }


def timeline_from_dict(data: Dict) -> Timeline:
    tl_data = data.get("timeline", data)
    timeline = Timeline(
        name=str(tl_data["name"]),
        library_name=str(tl_data["library_name"]),
        fps_override=tl_data.get("fps_override"),
        loop=bool(tl_data.get("loop", True)),
        clips=[
            TimelineClip(
                frame_name=str(clip["frame_name"]),
                duration_ms=int(clip["duration_ms"]),
            )
            for clip in tl_data.get("clips", [])
        ],
    )
    validate_timeline(timeline)
    return timeline


def save_json(path: Path, payload: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(payload, file_handle, indent=2, sort_keys=True, ensure_ascii=True)


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def validate_frame(frame: Frame) -> None:
    if not frame.name.strip():
        raise ValueError("Frame name cannot be empty")

    for layer in frame.layers:
        if not layer.asset_id:
            raise ValueError("Layer asset_id cannot be empty")
        if layer.opacity < 0 or layer.opacity > 255:
            raise ValueError("Layer opacity must be in range 0-255")


def validate_library(library: FrameLibrary) -> None:
    if not library.name.strip():
        raise ValueError("Library name cannot be empty")

    names = [frame.name for frame in library.frames]
    duplicates = {name for name in names if names.count(name) > 1}
    if duplicates:
        raise ValueError(f"Duplicate frame names are not allowed: {sorted(duplicates)}")

    for frame in library.frames:
        validate_frame(frame)


def validate_timeline(timeline: Timeline, library: Optional[FrameLibrary] = None) -> None:
    if not timeline.name.strip():
        raise ValueError("Timeline name cannot be empty")

    if timeline.fps_override is not None and timeline.fps_override not in FPS_CHOICES:
        raise ValueError(f"fps_override must be one of {FPS_CHOICES}")

    valid_frame_names = set()
    if library:
        valid_frame_names = {frame.name for frame in library.frames}

    for clip in timeline.clips:
        if clip.duration_ms < 16:
            raise ValueError("Timeline clip duration must be >= 16 ms")
        if library and clip.frame_name not in valid_frame_names:
            raise ValueError(f"Timeline references missing frame: {clip.frame_name}")


def load_assets_from_directory(assets_dir: Path) -> List[AssetReference]:
    """Discover PNG assets and build references.

    This only inspects files and dimensions. Rendering surfaces are loaded by the app.
    """
    png_paths = sorted(path for path in assets_dir.rglob("*.png") if path.is_file())
    assets: List[AssetReference] = []

    for png_path in png_paths:
        rel_path = png_path.relative_to(assets_dir).as_posix()
        width, height = 64, 64

        # Prefer PIL for dimension probing to avoid pygame codec/module issues.
        if PIL_AVAILABLE:
            try:
                with Image.open(png_path) as image:
                    width, height = image.size
            except Exception:
                pass

        # Include all discovered PNG files even if dimension probing fails.
        assets.append(
            AssetReference(
                id=_asset_id_from_path(rel_path),
                file_path=rel_path,
                source_width=width,
                source_height=height,
            )
        )

    return assets


class AnimationStudioApp:
    """Simple pygame editor for composing frames and timelines."""

    def __init__(self, assets_dir: Path, output_dir: Path):
        try:
            import pygame
        except ImportError as exc:
            raise RuntimeError("pygame is required. Install with: pip install pygame") from exc

        self.pygame = pygame
        self.assets_dir = assets_dir
        self.output_dir = output_dir

        pygame.init()
        self.screen = pygame.display.set_mode((1400, 900))
        pygame.display.set_caption("Hole Wizards - Animation Studio")
        self.clock = pygame.time.Clock()

        self.font = None
        self.small_font = None
        self.freetype_font = None
        self.freetype_small_font = None
        self.text_renderer = "bitmap"
        self._init_text_renderer()

        self.panel_left = pygame.Rect(0, 30, 260, 700)
        self.panel_canvas = pygame.Rect(260, 30, 880, 700)
        self.panel_right = pygame.Rect(1140, 30, 260, 700)
        self.panel_bottom = pygame.Rect(0, 730, 1400, 170)

        self.library = FrameLibrary(name="default_library")
        self.current_frame = Frame(name="frame_001")
        self.timeline = Timeline(name="default_timeline", library_name=self.library.name)

        self.asset_surfaces: Dict[str, "pygame.Surface"] = {}
        self.selected_asset_id: Optional[str] = None
        self.selected_layer_id: Optional[str] = None
        self.drag_active = False
        self.drag_offset = (0, 0)

        self.timeline_selected_index = 0
        self.timeline_scroll_offset = 0
        self.timeline_row_height = 20
        self.timeline_visible_rows = 3
        self.playing = False
        self.play_cursor = 0
        self.play_elapsed_ms = 0

        self.path_prompt_active = False
        self.path_prompt_text = ""

        self.dirty = False
        self.status_message = "Ready"

        self._load_assets()
        self._auto_discover_library()

    def _reload_assets(self) -> None:
        """Reload assets while preserving current selection when possible."""
        previous_asset_id = self.selected_asset_id
        self._load_assets()

        if previous_asset_id and any(asset.id == previous_asset_id for asset in self.library.assets):
            self.selected_asset_id = previous_asset_id

        self.status_message = f"Reloaded assets: {len(self.library.assets)} found"

    def _init_text_renderer(self) -> None:
        """Initialize text rendering with robust fallback behavior.

        Python 3.14 + pygame 2.6.1 can fail on pygame.font in some environments,
        so prefer pygame.freetype first.
        """
        # Preferred path: pygame.freetype
        try:
            import pygame.freetype

            self.freetype_font = pygame.freetype.SysFont(None, 22)
            self.freetype_small_font = pygame.freetype.SysFont(None, 18)
            self.text_renderer = "freetype"
            self.status_message = "Using pygame.freetype text renderer"
            return
        except Exception:
            pass

        # Last resort: built-in bitmap renderer.
        self.text_renderer = "bitmap"
        self.status_message = "Using built-in bitmap text renderer"

    def _auto_discover_library(self) -> None:
        """Auto-load the first discovered library file on startup."""
        library_files = discover_library_files(self.output_dir)
        if not library_files:
            return

        library_path = library_files[0]
        try:
            self.load_from_path(library_path)
            self.status_message = f"Auto-loaded library: {library_path.name}"
        except Exception as exc:
            self.status_message = f"Auto-load failed: {library_path.name} ({exc})"

    def _load_assets(self) -> None:
        self.library.assets = load_assets_from_directory(self.assets_dir)
        self.asset_surfaces = {}
        loaded_surfaces = 0
        failed_surfaces = 0

        for asset in self.library.assets:
            absolute_path = self.assets_dir / asset.file_path
            try:
                surface = self._load_surface_with_fallback(absolute_path)
                if surface is not None:
                    self.asset_surfaces[asset.id] = surface
                    loaded_surfaces += 1
                else:
                    failed_surfaces += 1
            except Exception:
                # Keep missing assets represented with placeholder on render.
                failed_surfaces += 1

        if self.library.assets:
            self.selected_asset_id = self.library.assets[0].id
        self.status_message = (
            f"Loaded {len(self.library.assets)} assets "
            f"({loaded_surfaces} renderable, {failed_surfaces} placeholder)"
        )

    def _load_surface_with_fallback(self, absolute_path: Path):
        """Load an image as pygame surface, with PIL fallback for PNG decode issues."""
        # Fast path: pygame image decoder.
        try:
            return self.pygame.image.load(str(absolute_path)).convert_alpha()
        except Exception:
            pass

        # Fallback path: PIL decode -> pygame surface.
        if PIL_AVAILABLE:
            try:
                with Image.open(absolute_path) as image:
                    rgba_image = image.convert("RGBA")
                    data = rgba_image.tobytes()
                    surface = self.pygame.image.fromstring(data, rgba_image.size, "RGBA")
                    return surface.convert_alpha()
            except Exception:
                return None

        return None

    def _layer_by_id(self, layer_id: Optional[str]) -> Optional[LayerInstance]:
        if not layer_id:
            return None
        for layer in self.current_frame.layers:
            if layer.layer_id == layer_id:
                return layer
        return None

    def _sorted_layers(self) -> List[LayerInstance]:
        return sorted(self.current_frame.layers, key=lambda layer: layer.z_index)

    def _asset_by_id(self, asset_id: str) -> Optional[AssetReference]:
        for asset in self.library.assets:
            if asset.id == asset_id:
                return asset
        return None

    def _new_layer_from_selection(self, x: int, y: int) -> None:
        if not self.selected_asset_id:
            return

        z_index = max((layer.z_index for layer in self.current_frame.layers), default=-1) + 1
        layer = LayerInstance(
            layer_id=_new_id(),
            asset_id=self.selected_asset_id,
            x=x,
            y=y,
            z_index=z_index,
        )
        self.current_frame.layers.append(layer)
        self.selected_layer_id = layer.layer_id
        self.dirty = True

    def _frame_file(self) -> Path:
        return self.output_dir / f"{self.current_frame.name}.frame"

    def _library_file(self) -> Path:
        return self.output_dir / f"{self.library.name}.library"

    def _timeline_file(self) -> Path:
        return self.output_dir / f"{self.timeline.name}.timeline"

    def save_frame(self, path: Optional[Path] = None) -> None:
        validate_frame(self.current_frame)
        save_path = path or self._frame_file()
        save_json(save_path, frame_to_dict(self.current_frame))
        self.status_message = f"Saved frame: {save_path.name}"
        self.dirty = False

    def save_library(self, path: Optional[Path] = None) -> None:
        # Ensure current frame is reflected in the library list.
        self._upsert_current_frame_in_library()
        validate_library(self.library)
        save_path = path or self._library_file()
        save_json(save_path, library_to_dict(self.library))
        self.status_message = f"Saved library: {save_path.name}"
        self.dirty = False

    def save_timeline(self, path: Optional[Path] = None) -> None:
        self._upsert_current_frame_in_library()
        validate_timeline(self.timeline, self.library)
        save_path = path or self._timeline_file()
        save_json(save_path, timeline_to_dict(self.timeline))
        self.status_message = f"Saved timeline: {save_path.name}"
        self.dirty = False

    def _upsert_current_frame_in_library(self) -> None:
        for idx, frame in enumerate(self.library.frames):
            if frame.name == self.current_frame.name:
                self.library.frames[idx] = self.current_frame
                return
        self.library.frames.append(self.current_frame)

    def _set_current_frame_by_name(self, frame_name: str, source: str = "") -> bool:
        """Switch active frame and reset per-frame selection state.

        Returns True when a matching frame is found and activated.
        """
        for frame in self.library.frames:
            if frame.name == frame_name:
                self.current_frame = frame
                self.selected_layer_id = None
                if source:
                    self.status_message = f"Showing frame: {frame_name} ({source})"
                return True
        return False

    def _activate_timeline_clip(self, clip_index: int, source: str = "timeline") -> bool:
        """Activate a timeline clip and update displayed frame.

        If the frame is not currently in the loaded library, try to load a
        matching `.frame` file from the output directory.
        """
        if not self.timeline.clips:
            return False
        if clip_index < 0 or clip_index >= len(self.timeline.clips):
            return False

        self.timeline_selected_index = clip_index
        self._ensure_selected_timeline_visible()
        clip = self.timeline.clips[clip_index]

        if self._set_current_frame_by_name(clip.frame_name, source=source):
            self.play_cursor = clip_index
            self.play_elapsed_ms = 0
            return True

        # Fallback: attempt to load frame file when library and timeline drift.
        candidate = self.output_dir / f"{clip.frame_name}.frame"
        if candidate.exists():
            try:
                payload = load_json(candidate)
                frame = frame_from_dict(payload)

                replaced = False
                for idx, existing in enumerate(self.library.frames):
                    if existing.name == frame.name:
                        self.library.frames[idx] = frame
                        replaced = True
                        break
                if not replaced:
                    self.library.frames.append(frame)

                if self._set_current_frame_by_name(clip.frame_name, source=f"{source} (autoload)"):
                    self.play_cursor = clip_index
                    self.play_elapsed_ms = 0
                    return True
            except Exception:
                pass

        self.status_message = f"Timeline frame not found: {clip.frame_name}"
        return False

    def _get_timeline_list_rect(self):
        """Return the clickable and scrollable timeline list area."""
        list_x = self.panel_bottom.x + 10
        list_y = self.panel_bottom.y + 106
        list_width = 430
        list_height = self.timeline_visible_rows * self.timeline_row_height
        return self.pygame.Rect(list_x, list_y, list_width, list_height)

    def _ensure_selected_timeline_visible(self) -> None:
        """Keep selected timeline row in the visible window."""
        if not self.timeline.clips:
            self.timeline_scroll_offset = 0
            return

        max_offset = max(0, len(self.timeline.clips) - self.timeline_visible_rows)
        self.timeline_scroll_offset = max(0, min(self.timeline_scroll_offset, max_offset))

        if self.timeline_selected_index < self.timeline_scroll_offset:
            self.timeline_scroll_offset = self.timeline_selected_index
        elif self.timeline_selected_index >= self.timeline_scroll_offset + self.timeline_visible_rows:
            self.timeline_scroll_offset = self.timeline_selected_index - self.timeline_visible_rows + 1

        self.timeline_scroll_offset = max(0, min(self.timeline_scroll_offset, max_offset))

    def _scroll_timeline(self, delta_rows: int) -> None:
        """Scroll timeline list by a row delta."""
        if not self.timeline.clips:
            self.timeline_scroll_offset = 0
            return

        max_offset = max(0, len(self.timeline.clips) - self.timeline_visible_rows)
        self.timeline_scroll_offset = max(0, min(max_offset, self.timeline_scroll_offset + delta_rows))

    def load_from_path(self, path: Path) -> None:
        payload = load_json(path)
        suffix = path.suffix.lower()

        if suffix == ".frame":
            self.current_frame = frame_from_dict(payload)
            self.selected_layer_id = None
            self.status_message = f"Loaded frame: {path.name}"
        elif suffix == ".library":
            self.library = library_from_dict(payload)
            self.current_frame = self.library.frames[0] if self.library.frames else Frame(name="frame_001")
            self.timeline.library_name = self.library.name
            self.status_message = f"Loaded library: {path.name}"
            self._load_assets()
        elif suffix == ".timeline":
            loaded_timeline = timeline_from_dict(payload)
            validate_timeline(loaded_timeline, self.library)
            self.timeline = loaded_timeline
            self.status_message = f"Loaded timeline: {path.name}"
            if self.timeline.clips:
                self._activate_timeline_clip(0, source="timeline")
        else:
            raise ValueError("Unsupported file extension. Use .frame, .library, or .timeline")

        self.dirty = False

    def _pick_top_layer_at(self, canvas_x: int, canvas_y: int) -> Optional[LayerInstance]:
        for layer in sorted(self.current_frame.layers, key=lambda l: l.z_index, reverse=True):
            if not layer.visible:
                continue

            asset = self._asset_by_id(layer.asset_id)
            if not asset:
                continue

            width, height = asset.source_width, asset.source_height
            rect = self.pygame.Rect(layer.x, layer.y, width, height)
            if rect.collidepoint(canvas_x, canvas_y):
                return layer
        return None

    def _draw_placeholder(self, target_rect: "pygame.Rect") -> None:
        tile = 8
        light = (180, 180, 180)
        dark = (100, 100, 100)
        for y in range(target_rect.top, target_rect.bottom, tile):
            for x in range(target_rect.left, target_rect.right, tile):
                color = light if ((x // tile) + (y // tile)) % 2 == 0 else dark
                self.pygame.draw.rect(self.screen, color, (x, y, tile, tile))

    def _draw_text(self, text: str, x: int, y: int, color=(230, 230, 230), small=False) -> None:
        if self.text_renderer == "freetype":
            font = self.freetype_small_font if small else self.freetype_font
            if font is not None:
                font.render_to(self.screen, (x, y), text, color)
            return

        if self.text_renderer == "font":
            font = self.small_font if small else self.font
            if font is not None:
                surface = font.render(text, True, color)
                self.screen.blit(surface, (x, y))
            return

        # Built-in pixel text fallback.
        self._draw_bitmap_text(text, x, y, color=color, small=small)

    def _draw_bitmap_text(self, text: str, x: int, y: int, color=(230, 230, 230), small=False) -> None:
        """Draw text with 5x7 bitmap glyphs independent of pygame font modules."""
        scale = 1 if small else 2
        char_spacing = 1 * scale
        cursor_x = x

        for char in text.upper():
            glyph = BITMAP_FONT_5X7.get(char)
            if glyph is None:
                glyph = BITMAP_FONT_5X7.get("?")

            for row_idx, row_bits in enumerate(glyph):
                for col_idx, bit in enumerate(row_bits):
                    if bit == "1":
                        self.pygame.draw.rect(
                            self.screen,
                            color,
                            (
                                cursor_x + (col_idx * scale),
                                y + (row_idx * scale),
                                scale,
                                scale,
                            ),
                        )

            cursor_x += (5 * scale) + char_spacing

    def _draw_ui(self) -> None:
        pg = self.pygame
        self.screen.fill((18, 18, 22))

        # Top status bar.
        pg.draw.rect(self.screen, (35, 35, 45), (0, 0, 1400, 30))
        dirty_flag = "*" if self.dirty else ""
        self._draw_text(
            f"Animation Studio{dirty_flag} | Assets: {len(self.library.assets)} | Frame: {self.current_frame.name} | Timeline: {self.timeline.name}",
            8,
            7,
            color=(220, 220, 230),
            small=True,
        )
        self._draw_text(self.status_message, 800, 7, color=(160, 220, 160), small=True)

        # Panels.
        pg.draw.rect(self.screen, (28, 28, 36), self.panel_left)
        pg.draw.rect(self.screen, (24, 24, 30), self.panel_canvas)
        pg.draw.rect(self.screen, (28, 28, 36), self.panel_right)
        pg.draw.rect(self.screen, (22, 22, 28), self.panel_bottom)

        # Asset browser.
        self._draw_text("Assets", self.panel_left.x + 10, self.panel_left.y + 10)
        self._draw_text(f"Count: {len(self.library.assets)}", self.panel_left.x + 140, self.panel_left.y + 10, color=(170, 245, 170), small=True)
        y = self.panel_left.y + 40
        for asset in self.library.assets[:28]:
            selected = asset.id == self.selected_asset_id
            color = (120, 220, 255) if selected else (220, 220, 220)
            self._draw_text(asset.file_path, self.panel_left.x + 10, y, color=color, small=True)
            y += 22

        # Canvas area and frame bounds.
        canvas_x = self.panel_canvas.x + 40
        canvas_y = self.panel_canvas.y + 30
        frame_rect = pg.Rect(canvas_x, canvas_y, self.current_frame.canvas_width, self.current_frame.canvas_height)
        bg = tuple(self.current_frame.background_rgba[:3])
        pg.draw.rect(self.screen, bg, frame_rect)
        pg.draw.rect(self.screen, (100, 100, 120), frame_rect, 1)

        # First-run quick help overlay for discoverability.
        self._draw_quick_help_overlay(frame_rect)

        # Layers.
        for layer in self._sorted_layers():
            if not layer.visible:
                continue

            surface = self.asset_surfaces.get(layer.asset_id)
            if surface is None:
                asset = self._asset_by_id(layer.asset_id)
                placeholder_w = asset.source_width if asset else 48
                placeholder_h = asset.source_height if asset else 48
                placeholder_w = max(24, min(placeholder_w, 128))
                placeholder_h = max(24, min(placeholder_h, 128))
                self._draw_placeholder(pg.Rect(frame_rect.x + layer.x, frame_rect.y + layer.y, placeholder_w, placeholder_h))
                continue

            transformed = pg.transform.flip(surface, layer.flip_x, layer.flip_y)
            if layer.opacity < 255:
                transformed = transformed.copy()
                transformed.set_alpha(layer.opacity)

            draw_pos = (frame_rect.x + layer.x, frame_rect.y + layer.y)
            self.screen.blit(transformed, draw_pos)

            if layer.layer_id == self.selected_layer_id:
                border_rect = pg.Rect(draw_pos[0], draw_pos[1], transformed.get_width(), transformed.get_height())
                pg.draw.rect(self.screen, (255, 220, 120), border_rect, 2)

        # Inspector.
        self._draw_text("Layer Inspector", self.panel_right.x + 10, self.panel_right.y + 10)
        selected_layer = self._layer_by_id(self.selected_layer_id)
        if selected_layer:
            rows = [
                f"id: {selected_layer.layer_id[:8]}",
                f"x: {selected_layer.x}",
                f"y: {selected_layer.y}",
                f"z: {selected_layer.z_index}",
                f"flip_x: {selected_layer.flip_x}",
                f"flip_y: {selected_layer.flip_y}",
                f"visible: {selected_layer.visible}",
                f"opacity: {selected_layer.opacity}",
            ]
            y = self.panel_right.y + 42
            for row in rows:
                self._draw_text(row, self.panel_right.x + 10, y, small=True)
                y += 22
        else:
            self._draw_text("No layer selected", self.panel_right.x + 10, self.panel_right.y + 42, small=True)

        # Bottom timeline.
        self._draw_text("Timeline", self.panel_bottom.x + 10, self.panel_bottom.y + 10)
        self._draw_text(
            f"clips: {len(self.timeline.clips)} | loop: {self.timeline.loop} | playing: {self.playing}",
            self.panel_bottom.x + 10,
            self.panel_bottom.y + 34,
            small=True,
        )
        self._draw_text(
            "Shortcuts: Ctrl+R reload assets | Ctrl+S frame | Ctrl+L library | Ctrl+T timeline | Ctrl+O load path",
            self.panel_bottom.x + 10,
            self.panel_bottom.y + 58,
            small=True,
        )
        self._draw_text(
            "N new frame | A add clip | Arrows move | H/V flip | PgUp/PgDn z | Del remove | O/P opacity | Space play",
            self.panel_bottom.x + 10,
            self.panel_bottom.y + 80,
            small=True,
        )

        # Timeline clip list with scrollbar.
        list_rect = self._get_timeline_list_rect()
        self.pygame.draw.rect(self.screen, (12, 12, 18), list_rect)
        self.pygame.draw.rect(self.screen, (80, 80, 110), list_rect, 1)

        self._ensure_selected_timeline_visible()
        start_index = self.timeline_scroll_offset
        end_index = min(len(self.timeline.clips), start_index + self.timeline_visible_rows)

        y = list_rect.y
        for idx in range(start_index, end_index):
            clip = self.timeline.clips[idx]
            row_rect = self.pygame.Rect(list_rect.x, y, list_rect.width, self.timeline_row_height)
            if idx == self.timeline_selected_index:
                self.pygame.draw.rect(self.screen, (50, 70, 95), row_rect)

            marker = ">" if idx == self.timeline_selected_index else " "
            self._draw_text(f"{marker} {idx+1}. {clip.frame_name} ({clip.duration_ms}ms)", row_rect.x + 6, row_rect.y + 4, small=True)
            y += self.timeline_row_height

        if len(self.timeline.clips) > self.timeline_visible_rows:
            scrollbar_w = 10
            scrollbar_rect = self.pygame.Rect(list_rect.right + 6, list_rect.y, scrollbar_w, list_rect.height)
            self.pygame.draw.rect(self.screen, (26, 26, 32), scrollbar_rect)
            self.pygame.draw.rect(self.screen, (90, 90, 110), scrollbar_rect, 1)

            total = len(self.timeline.clips)
            visible = self.timeline_visible_rows
            max_offset = total - visible
            thumb_h = max(12, int((visible / total) * scrollbar_rect.height))
            travel = scrollbar_rect.height - thumb_h
            thumb_y = scrollbar_rect.y
            if max_offset > 0 and travel > 0:
                thumb_y += int((self.timeline_scroll_offset / max_offset) * travel)

            thumb_rect = self.pygame.Rect(scrollbar_rect.x + 1, thumb_y, scrollbar_w - 2, thumb_h)
            self.pygame.draw.rect(self.screen, (180, 180, 210), thumb_rect)

        if self.path_prompt_active:
            prompt_rect = pg.Rect(220, 370, 960, 60)
            pg.draw.rect(self.screen, (8, 8, 12), prompt_rect)
            pg.draw.rect(self.screen, (120, 120, 150), prompt_rect, 1)
            self._draw_text("Load file path (.frame/.library/.timeline):", prompt_rect.x + 10, prompt_rect.y + 10, small=True)
            self._draw_text(self.path_prompt_text or "", prompt_rect.x + 10, prompt_rect.y + 30, color=(150, 240, 150), small=True)

        pg.display.flip()

    def _draw_quick_help_overlay(self, frame_rect: "pygame.Rect") -> None:
        """Draw a high-contrast, always-visible quick-help panel."""
        panel_width = min(560, frame_rect.width - 20)
        panel_height = 74
        panel_x = frame_rect.x + 10
        panel_y = frame_rect.y + 10

        panel_rect = self.pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self.pygame.draw.rect(self.screen, (6, 6, 8), panel_rect)
        self.pygame.draw.rect(self.screen, (245, 220, 80), panel_rect, 2)

        self._draw_text("QUICK START", panel_x + 10, panel_y + 8, color=(255, 235, 120), small=True)
        self._draw_text(
            "1) Click asset (left)  2) Click canvas to place  3) Drag to move",
            panel_x + 10,
            panel_y + 24,
            color=(230, 230, 230),
            small=True,
        )
        self._draw_text(
            "A add timeline clip  |  SPACE play/pause  |  Ctrl+S save frame  |  Ctrl+R reload assets",
            panel_x + 10,
            panel_y + 40,
            color=(170, 245, 170),
            small=True,
        )
        self._draw_text(
            "H/V flip  PgUp/PgDn layer order  Delete remove  O/P opacity",
            panel_x + 10,
            panel_y + 56,
            color=(160, 220, 255),
            small=True,
        )

    def _handle_mouse_down(self, event) -> None:
        x, y = event.pos

        # Timeline list click-to-select displayed frame.
        list_rect = self._get_timeline_list_rect()
        if list_rect.collidepoint(x, y) and self.timeline.clips:
            clicked_row = (y - list_rect.y) // self.timeline_row_height
            clip_index = self.timeline_scroll_offset + clicked_row
            if 0 <= clip_index < len(self.timeline.clips):
                self._activate_timeline_clip(clip_index, source="timeline click")
            return

        if self.panel_left.collidepoint(x, y):
            local_y = y - (self.panel_left.y + 40)
            idx = local_y // 22
            if 0 <= idx < len(self.library.assets):
                self.selected_asset_id = self.library.assets[idx].id
                self.status_message = f"Selected asset: {self.library.assets[idx].file_path}"
            return

        canvas_rect = self.pygame.Rect(self.panel_canvas.x + 40, self.panel_canvas.y + 30, self.current_frame.canvas_width, self.current_frame.canvas_height)
        if canvas_rect.collidepoint(x, y):
            cx = x - canvas_rect.x
            cy = y - canvas_rect.y

            hit_layer = self._pick_top_layer_at(cx, cy)
            if hit_layer:
                self.selected_layer_id = hit_layer.layer_id
                self.drag_active = True
                self.drag_offset = (cx - hit_layer.x, cy - hit_layer.y)
            else:
                self._new_layer_from_selection(cx, cy)
            return

    def _handle_keydown(self, event) -> None:
        pg = self.pygame

        if self.path_prompt_active:
            if event.key == pg.K_RETURN:
                try:
                    path = Path(self.path_prompt_text.strip()).expanduser()
                    self.load_from_path(path)
                except Exception as exc:
                    self.status_message = f"Load failed: {exc}"
                self.path_prompt_active = False
                self.path_prompt_text = ""
            elif event.key == pg.K_ESCAPE:
                self.path_prompt_active = False
                self.path_prompt_text = ""
            elif event.key == pg.K_BACKSPACE:
                self.path_prompt_text = self.path_prompt_text[:-1]
            elif event.unicode and event.unicode.isprintable():
                self.path_prompt_text += event.unicode
            return

        mods = pg.key.get_mods()
        ctrl = bool(mods & pg.KMOD_CTRL)
        shift = bool(mods & pg.KMOD_SHIFT)

        if ctrl and event.key == pg.K_s:
            try:
                self.save_frame()
                # Keep timeline persistence in sync with frame edits.
                if self.timeline.clips:
                    self.save_timeline()
                    self.status_message = "Saved frame + timeline"
            except Exception as exc:
                self.status_message = f"Save frame failed: {exc}"
            return

        if ctrl and event.key == pg.K_l:
            try:
                self.save_library()
            except Exception as exc:
                self.status_message = f"Save library failed: {exc}"
            return

        if ctrl and event.key == pg.K_t:
            try:
                self.save_timeline()
            except Exception as exc:
                self.status_message = f"Save timeline failed: {exc}"
            return

        if ctrl and event.key == pg.K_r:
            try:
                self._reload_assets()
            except Exception as exc:
                self.status_message = f"Reload assets failed: {exc}"
            return

        if ctrl and event.key == pg.K_o:
            self.path_prompt_active = True
            self.path_prompt_text = ""
            return

        if event.key == pg.K_n:
            index = len(self.library.frames) + 1
            self.current_frame = Frame(name=f"frame_{index:03d}")
            self.selected_layer_id = None
            self.status_message = f"New frame: {self.current_frame.name}"
            self.dirty = True
            return

        if event.key == pg.K_a:
            self._upsert_current_frame_in_library()
            self.timeline.clips.append(TimelineClip(frame_name=self.current_frame.name, duration_ms=100))
            self.timeline_selected_index = len(self.timeline.clips) - 1
            self._ensure_selected_timeline_visible()
            self.dirty = True
            self.status_message = "Added frame to timeline"
            return

        if event.key == pg.K_SPACE:
            if shift:
                self.timeline.loop = not self.timeline.loop
                self.status_message = f"Timeline loop: {self.timeline.loop}"
            else:
                self.playing = not self.playing
                self.play_elapsed_ms = 0
                self.status_message = "Playback started" if self.playing else "Playback paused"
            return

        if event.key in (pg.K_1, pg.K_2, pg.K_3, pg.K_4):
            index = [pg.K_1, pg.K_2, pg.K_3, pg.K_4].index(event.key)
            self.timeline.fps_override = FPS_CHOICES[index]
            self.status_message = f"FPS override set: {self.timeline.fps_override}"
            return

        if event.key in (pg.K_LEFTBRACKET, pg.K_RIGHTBRACKET) and self.timeline.clips:
            clip = self.timeline.clips[self.timeline_selected_index]
            if event.key == pg.K_LEFTBRACKET:
                clip.duration_ms = max(16, clip.duration_ms - 16)
            else:
                clip.duration_ms += 16
            self.dirty = True
            return

        if event.key == pg.K_COMMA and self.timeline.clips:
            self._activate_timeline_clip(max(0, self.timeline_selected_index - 1), source="clip select")
            return

        if event.key == pg.K_PERIOD and self.timeline.clips:
            self._activate_timeline_clip(min(len(self.timeline.clips) - 1, self.timeline_selected_index + 1), source="clip select")
            return

        layer = self._layer_by_id(self.selected_layer_id)
        if not layer:
            return

        move_amount = 10 if shift else 1
        if event.key == pg.K_LEFT:
            layer.x -= move_amount
            self.dirty = True
        elif event.key == pg.K_RIGHT:
            layer.x += move_amount
            self.dirty = True
        elif event.key == pg.K_UP:
            layer.y -= move_amount
            self.dirty = True
        elif event.key == pg.K_DOWN:
            layer.y += move_amount
            self.dirty = True
        elif event.key == pg.K_h:
            layer.flip_x = not layer.flip_x
            self.dirty = True
        elif event.key == pg.K_v:
            layer.flip_y = not layer.flip_y
            self.dirty = True
        elif event.key == pg.K_PAGEUP:
            layer.z_index += 1
            self.dirty = True
        elif event.key == pg.K_PAGEDOWN:
            layer.z_index -= 1
            self.dirty = True
        elif event.key == pg.K_DELETE:
            self.current_frame.layers = [entry for entry in self.current_frame.layers if entry.layer_id != layer.layer_id]
            self.selected_layer_id = None
            self.dirty = True
        elif event.key == pg.K_i:
            layer.visible = not layer.visible
            self.dirty = True
        elif event.key == pg.K_o:
            layer.opacity = max(0, layer.opacity - 16)
            self.dirty = True
        elif event.key == pg.K_p:
            layer.opacity = min(255, layer.opacity + 16)
            self.dirty = True

    def _update_playback(self, delta_ms: int) -> None:
        if not self.playing or not self.timeline.clips:
            return

        if self.play_cursor >= len(self.timeline.clips):
            if self.timeline.loop:
                self.play_cursor = 0
            else:
                self.playing = False
                return

        clip = self.timeline.clips[self.play_cursor]
        self.play_elapsed_ms += delta_ms

        if self.play_elapsed_ms >= clip.duration_ms:
            self.play_elapsed_ms = 0
            self.play_cursor += 1
            if self.play_cursor >= len(self.timeline.clips):
                if self.timeline.loop:
                    self.play_cursor = 0
                else:
                    self.playing = False
                    return
            self._activate_timeline_clip(self.play_cursor, source="playback")

    def run(self) -> None:
        running = True
        while running:
            delta_ms = self.clock.tick(self.timeline.fps_override or 60)

            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                elif event.type == self.pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_mouse_down(event)
                elif event.type == self.pygame.MOUSEBUTTONDOWN and event.button == 4:
                    self._scroll_timeline(-1)
                elif event.type == self.pygame.MOUSEBUTTONDOWN and event.button == 5:
                    self._scroll_timeline(1)
                elif event.type == self.pygame.MOUSEBUTTONUP and event.button == 1:
                    self.drag_active = False
                elif event.type == self.pygame.MOUSEWHEEL:
                    self._scroll_timeline(-event.y)
                elif event.type == self.pygame.MOUSEMOTION and self.drag_active:
                    layer = self._layer_by_id(self.selected_layer_id)
                    if layer:
                        canvas_rect = self.pygame.Rect(self.panel_canvas.x + 40, self.panel_canvas.y + 30, self.current_frame.canvas_width, self.current_frame.canvas_height)
                        x, y = event.pos
                        layer.x = max(0, min(self.current_frame.canvas_width - 1, x - canvas_rect.x - self.drag_offset[0]))
                        layer.y = max(0, min(self.current_frame.canvas_height - 1, y - canvas_rect.y - self.drag_offset[1]))
                        self.dirty = True
                elif event.type == self.pygame.KEYDOWN:
                    self._handle_keydown(event)

            self._update_playback(delta_ms)
            self._draw_ui()

        self.pygame.quit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hole Wizards Animation Studio")
    parser.add_argument("--assets-dir", default="data/png", help="PNG asset directory")
    parser.add_argument(
        "--output-dir",
        default="utilities/animation_studio_output",
        help="Output directory for .frame/.library/.timeline files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    assets_dir = Path(args.assets_dir)
    output_dir = Path(args.output_dir)

    if not assets_dir.exists():
        raise SystemExit(f"Assets directory not found: {assets_dir}")

    app = AnimationStudioApp(assets_dir=assets_dir, output_dir=output_dir)
    app.run()


if __name__ == "__main__":
    main()
