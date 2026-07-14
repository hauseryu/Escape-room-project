import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.escape_room.escape_room import EscapeApp
from src.escape_room.light import Light
from src.escape_room.table import Table


class FakeCanvas:
    def __init__(self):
        self.polygons = []
        self.lines = []
        self.ovals = []
        self.arcs = []

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

    def create_arc(self, *points, **kwargs):
        self.arcs.append({
            "points": points,
            **kwargs,
        })


class EscapeRoomTest(unittest.TestCase):
    def test_draw_room_creates_drawable_polygons(self):
        app = EscapeApp.__new__(EscapeApp)
        app.canvas_area = FakeCanvas()
        app.doors = []
        app.light = Light()
        app.table = Table()
        app.room_coordinates = [
            ["#8B4513", (0, 0, 0), (8, 0, 0), (8, 0, 4), (0, 0, 4)],
            ["white", (0, 3, 0), (8, 3, 0), (8, 3, 4), (0, 3, 4)],
            ["white", (0, 0, 0), (0, 3, 0), (0, 3, 4), (0, 0, 4)],
            ["white", (8, 0, 0), (8, 3, 0), (8, 3, 4), (8, 0, 4)],
        ]

        app.draw_room()

        self.assertEqual(len(app.canvas_area.polygons), 27)
        self.assertEqual(len(app.canvas_area.arcs), 1)
        for polygon in app.canvas_area.polygons[:4]:
            self.assertEqual(len(polygon["points"]), 8)
        self.assertEqual(app.canvas_area.polygons[0]["fill"], "#8B4513")
        self.assertEqual(app.canvas_area.polygons[0]["outline"], "black")

    def test_create_doors_creates_three_doors(self):
        app = EscapeApp.__new__(EscapeApp)

        doors = app.create_doors()

        self.assertEqual(len(doors), 3)
        self.assertEqual([door.tag for door in doors], ["back_door", "left_door", "right_door"])
        for door in doors:
            self.assertEqual(len(door.corners), 4)
            y_values = [point[1] for point in door.corners]
            self.assertEqual(min(y_values), 0)
            self.assertEqual(max(y_values), 2)
        self.assertEqual(
            doors[2].corners,
            [
                (8, 2, 3.2),
                (8, 2, 2),
                (8, 0, 2),
                (8, 0, 3.2),
            ],
        )


if __name__ == "__main__":
    unittest.main()
