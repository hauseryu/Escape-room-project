import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.escape_room.escape_room import EscapeApp, room_coordinates


class EscapeRoomTest(unittest.TestCase):
    def test_room_has_floor_ceiling_and_two_walls(self):
        self.assertEqual(len(room_coordinates), 4)
        self.assertEqual([polygon[0] for polygon in room_coordinates], ["brown", "white", "white", "white"])

    def test_each_room_polygon_has_color_and_four_3d_points(self):
        for polygon in room_coordinates:
            self.assertEqual(len(polygon), 5)
            for point in polygon[1:]:
                self.assertEqual(len(point), 3)

    def test_convert_coordinates_creates_drawable_polygons(self):
        app = EscapeApp.__new__(EscapeApp)
        app.coordinates = []

        app.convert_coordinates()

        self.assertEqual(len(app.coordinates), 4)
        for polygon in app.coordinates:
            self.assertIsInstance(polygon[0], str)
            self.assertEqual(len(polygon[1:]), 8)


if __name__ == "__main__":
    unittest.main()
