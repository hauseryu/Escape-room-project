import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.escape_room.escape_room import EscapeApp


class FakeCanvas:
    def __init__(self):
        self.polygons = []

    def create_polygon(self, points, width, fill, outline):
        self.polygons.append({
            "points": points,
            "width": width,
            "fill": fill,
            "outline": outline,
        })


class EscapeRoomTest(unittest.TestCase):
    def test_draw_room_creates_drawable_polygons(self):
        app = EscapeApp.__new__(EscapeApp)
        app.canvas_area = FakeCanvas()
        app.room_coordinates = [
            ["#8B4513", (0, 0, 0), (8, 0, 0), (8, 0, 4), (0, 0, 4)],
            ["white", (0, 3, 0), (8, 3, 0), (8, 3, 4), (0, 3, 4)],
            ["white", (0, 0, 0), (0, 3, 0), (0, 3, 4), (0, 0, 4)],
            ["white", (8, 0, 0), (8, 3, 0), (8, 3, 4), (8, 0, 4)],
        ]

        app.draw_room()

        self.assertEqual(len(app.coordinates), 4)
        for polygon in app.coordinates:
            self.assertIsInstance(polygon[0], str)
            self.assertEqual(len(polygon[1:]), 8)
        self.assertEqual(len(app.canvas_area.polygons), 4)
        self.assertEqual(app.canvas_area.polygons[0]["fill"], "#8B4513")
        self.assertEqual(app.canvas_area.polygons[0]["outline"], "black")


if __name__ == "__main__":
    unittest.main()
