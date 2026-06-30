#!/usr/bin/env python3
"""Tests for Animation Studio serialization and validation."""

from pathlib import Path
import tempfile
import unittest

from utilities.animation_studio import (
    Frame,
    FrameLibrary,
    LayerInstance,
    Timeline,
    TimelineClip,
    _asset_id_from_path,
    discover_library_files,
    frame_from_dict,
    frame_to_dict,
    library_from_dict,
    library_to_dict,
    load_json,
    save_json,
    timeline_from_dict,
    timeline_to_dict,
    validate_library,
    validate_timeline,
)


class AnimationStudioSerializationTests(unittest.TestCase):
    def test_frame_round_trip(self):
        frame = Frame(
            name="frame_test",
            layers=[
                LayerInstance(
                    layer_id="layer-1",
                    asset_id="asset-1",
                    x=10,
                    y=20,
                    z_index=3,
                    flip_x=True,
                    opacity=200,
                )
            ],
        )

        payload = frame_to_dict(frame)
        restored = frame_from_dict(payload)

        self.assertEqual(restored.name, frame.name)
        self.assertEqual(len(restored.layers), 1)
        self.assertEqual(restored.layers[0].asset_id, "asset-1")
        self.assertTrue(restored.layers[0].flip_x)
        self.assertEqual(restored.layers[0].opacity, 200)

    def test_library_round_trip(self):
        frame = Frame(
            name="frame_alpha",
            layers=[LayerInstance(layer_id="l", asset_id="a", x=1, y=2, z_index=1)],
        )
        library = FrameLibrary(name="lib_one", frames=[frame])

        payload = library_to_dict(library)
        restored = library_from_dict(payload)

        self.assertEqual(restored.name, "lib_one")
        self.assertEqual(len(restored.frames), 1)
        self.assertEqual(restored.frames[0].name, "frame_alpha")

    def test_timeline_round_trip(self):
        timeline = Timeline(
            name="tl_one",
            library_name="lib_one",
            fps_override=30,
            loop=True,
            clips=[TimelineClip(frame_name="frame_alpha", duration_ms=120)],
        )

        payload = timeline_to_dict(timeline)
        restored = timeline_from_dict(payload)

        self.assertEqual(restored.name, "tl_one")
        self.assertEqual(restored.fps_override, 30)
        self.assertEqual(len(restored.clips), 1)
        self.assertEqual(restored.clips[0].duration_ms, 120)

    def test_json_save_load(self):
        payload = {"version": "1", "value": 42}
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "sample.json"
            save_json(path, payload)
            loaded = load_json(path)
            self.assertEqual(loaded["value"], 42)


class AnimationStudioValidationTests(unittest.TestCase):
    def test_duplicate_frame_names_rejected(self):
        library = FrameLibrary(
            name="lib",
            frames=[Frame(name="same"), Frame(name="same")],
        )

        with self.assertRaises(ValueError):
            validate_library(library)

    def test_missing_timeline_frame_rejected(self):
        library = FrameLibrary(name="lib", frames=[Frame(name="frame_ok")])
        timeline = Timeline(
            name="tl",
            library_name="lib",
            clips=[TimelineClip(frame_name="frame_missing", duration_ms=100)],
        )

        with self.assertRaises(ValueError):
            validate_timeline(timeline, library)

    def test_short_timeline_clip_rejected(self):
        timeline = Timeline(
            name="tl",
            library_name="lib",
            clips=[TimelineClip(frame_name="frame_any", duration_ms=15)],
        )

        with self.assertRaises(ValueError):
            validate_timeline(timeline)


class AnimationStudioDiscoveryTests(unittest.TestCase):
    def test_discover_library_files_sorted(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            (base / "zeta.library").write_text("{}", encoding="utf-8")
            (base / "alpha.library").write_text("{}", encoding="utf-8")
            (base / "note.txt").write_text("ignore", encoding="utf-8")

            discovered = discover_library_files(base)
            names = [path.name for path in discovered]
            self.assertEqual(names, ["alpha.library", "zeta.library"])

    def test_asset_id_stable_for_same_path(self):
        one = _asset_id_from_path("sprites/wizard.png")
        two = _asset_id_from_path("sprites/wizard.png")
        other = _asset_id_from_path("sprites/enemy.png")

        self.assertEqual(one, two)
        self.assertNotEqual(one, other)


if __name__ == "__main__":
    unittest.main()
