import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.escape_room.door import Door, _mix_color


class FakeCanvas:
    def __init__(self):
        self.polygons = []
        self.lines = []
        self.ovals = []

    def create_polygon(self, points, **kwargs):
        self.polygons.append({
            "points": points,
            **kwargs,
        })

    def create_line(self, *points, **kwargs):
        self.lines.append({
            "points": points,
            **kwargs,
        })

    def create_oval(self, *points, **kwargs):
        self.ovals.append({
            "points": points,
            **kwargs,
        })


class DoorTest(unittest.TestCase):
    def setUp(self):
        self.corners = [
            (3, 3, 4),
            (5, 3, 4),
            (5, 0, 4),
            (3, 0, 4),
        ]

    def test_stores_four_corner_points(self):
        door = Door(corners=self.corners, tag="test_door")

        self.assertEqual(door.corners, self.corners)
        self.assertEqual(door.tag, "test_door")

    def test_requires_four_corner_points(self):
        with self.assertRaises(ValueError):
            Door(corners=[(0, 0, 1), (1, 0, 1), (1, 1, 1)])

    def test_draw_door_creates_canvas_shapes(self):
        canvas = FakeCanvas()
        door = Door(corners=self.corners, tag="test_door")

        door.draw(canvas, 800, 600)

        self.assertGreater(len(canvas.polygons), 0)
        self.assertGreater(len(canvas.lines), 0)
        self.assertGreater(len(canvas.ovals), 0)

    def test_named_colors_are_mixed_from_the_requested_color(self):
        self.assertEqual(_mix_color("blue", (0, 0, 0), 0.55), "#000072")
        self.assertEqual(_mix_color("red", (255, 255, 255), 0.22), "#ff3838")


if __name__ == "__main__":
    unittest.main()
