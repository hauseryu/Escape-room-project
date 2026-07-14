import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.escape_room import globals


class GlobalsTest(unittest.TestCase):
    def test_canvas_size_is_configured(self):
        self.assertEqual(globals.canvas_width, 1600)
        self.assertEqual(globals.canvas_height, 1200)

    def test_canvas_size_values_are_positive(self):
        self.assertGreater(globals.canvas_width, 0)
        self.assertGreater(globals.canvas_height, 0)


if __name__ == "__main__":
    unittest.main()
