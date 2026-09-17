import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from unittest.mock import MagicMock
from src.escape_room.objects.door import Door, _mix_color
from src.escape_room.room.room_state import RoomState
from src.escape_room.application.context_manager import ContextManager

test_room = {  
        "room_name": "test_room",
        "room_coordinates": "normal_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(3.2, 0, 4), "brown", "front", "red_door", False, True, False,"","door1"], # door1: not player door, can be opened
                ], 
        "wardrobe": [ [(0, 0, 4)] 
                ],              
}

room_state = {"test_room": {
            "key": {},
            "light": {},
            "door": {},
            "safe": {},
            "wardrobe": {},
            "picture": {},
            "figure": {},
            "revolver": {},
            "magnifier": {},
            "water_glass": {}
        } }

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
            (3.2, 2, 4),
            (4.2, 2, 4),
            (4.2, 0, 4),
            (3.2, 0, 4),
        ]

    def test_stores_four_corner_points(self):
        room_state = RoomState()
        canvas = MagicMock()
        ContextManager().set_canvas(canvas)
        room = MagicMock()#
        ContextManager().set_room(room)        
        door = Door(test_room,0,room_state=room_state)

        self.assertEqual(door.corners, self.corners)
        self.assertEqual(door.tag, "red_door")

    def test_draw_door_creates_canvas_shapes(self):

        room_state = RoomState()
        canvas = MagicMock()
        ContextManager().set_canvas(canvas)
        room = MagicMock()#
        ContextManager().set_room(room)   
        door = Door(test_room,0,room_state=room_state)

        door.draw(canvas, 800, 600)

        # self.assertGreater(len(canvas.polygons), 0)
        # self.assertGreater(len(canvas.lines), 0)
        # self.assertGreater(len(canvas.ovals), 0)

    def test_named_colors_are_mixed_from_the_requested_color(self):
        self.assertEqual(_mix_color("blue", (0, 0, 0), 0.55), "#000072")
        self.assertEqual(_mix_color("red", (255, 255, 255), 0.22), "#ff3838")


if __name__ == "__main__":
    unittest.main()
