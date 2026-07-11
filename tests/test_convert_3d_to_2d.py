import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.escape_room.convert_3d_to_2d import compute_2d_coordinates, convert_polygon_coordinates


class Convert3dTo2dTest(unittest.TestCase):
    def test_projects_point_with_world_offset_and_perspective(self):
        x, y = compute_2d_coordinates(0, 0, 10, 800, 600)

        self.assertAlmostEqual(x, 309.0909090909091)
        self.assertAlmostEqual(y, 368.1818181818182)

    def test_projects_point_with_perspective(self):
        x, y = compute_2d_coordinates(2, 1, 10, 800, 600)

        self.assertAlmostEqual(x, 354.54545454545456)
        self.assertAlmostEqual(y, 322.72727272727275)

    def test_convert_polygon_coordinates_keeps_color_and_converts_four_points(self):
        coordinates = convert_polygon_coordinates([
            ["white", (0, 0, 0), (8, 0, 0), (8, 3, 4), (0, 3, 4)]
        ])

        self.assertEqual(len(coordinates), 1)
        self.assertEqual(coordinates[0][0], "white")
        self.assertEqual(len(coordinates[0][1:]), 8)


if __name__ == "__main__":
    unittest.main()
