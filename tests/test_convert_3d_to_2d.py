import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.escape_room.convert_3d_to_2d import compute_2d_coordinates


class Convert3dTo2dTest(unittest.TestCase):
    def test_projects_center_point_to_screen_center(self):
        self.assertEqual(compute_2d_coordinates(0, 0, 10, 800, 600), (400, 300))

    def test_projects_point_with_perspective(self):
        self.assertEqual(compute_2d_coordinates(2, 1, 10, 800, 600), (430, 315))


if __name__ == "__main__":
    unittest.main()
