import unittest
from pathlib import Path
import sys
from unittest.mock import patch
from unittest.mock import MagicMock
import tkinter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.escape_room.application.escape_app import EscapeApp
from src.escape_room.application.escape_app import StartScreen
from src.escape_room.application.escape_app import EscapeClient
from src.escape_room.application.escape_app import Room
from src.escape_room.room import room_data

from src.escape_room.objects.chair import Chair
from src.escape_room.objects.door import Door
from src.escape_room.objects.light import Light
from src.escape_room.objects.table import Table
from src.escape_room.objects.wardrobe import Wardrobe
from src.escape_room.objects.picture import Picture
from src.escape_room.objects.bookshelf import Bookshelf
from src.escape_room.objects.letter import Letter
from src.escape_room.objects.fireplace import Fireplace
from src.escape_room.objects.window import Window
from src.escape_room.objects.metal_cassette import MetalCassette
from src.escape_room.application.context_manager import ContextManager
from src.escape_room.actions.action import ActionManager
from src.escape_room.room.room_state import RoomState

IMAGE_DIR = ContextManager.get_image_path()

test_room = {  
        "room_name": "test_room",
        "room_coordinates": "normal_room",
        "room": (0,0,0), #front: corner left bottom (x/y/z coordinates)
        "door": [[(3.2, 0, 4), "brown", "front", "red_door", False, True, False,"","door1"]], # door1: not player door, can be opened
        "chair": [[(5.00,0,2.35),"right","chair1"]
                ], 
        "wardrobe": [ [(0, 0, 4),"left","wardrobe1"] 
                ],              
    
}

# room_state = {"test_room": {
#             "key": {},
#             "light": {},
#             "door": {},
#             "safe": {},
#             "wardrobe": {},
#             "picture": {},
#             "figure": {},
#             "revolver": {},
#             "magnifier": {},
#             "water_glass": {}
#         } }

class FakeDrawable:
    def __init__(self):
        self.drawn_on = None
        self.unique_id = ""

    def draw(self, canvas):
        self.drawn_on = canvas


class FakeStartScreen:
    def __init__(self):
        self.was_drawn = False

    def draw(self):
        self.was_drawn = True


class FakeCanvas:
    def __init__(self):
        self.polygons = []
        self.lines = []
        self.ovals = []
        self.arcs = []
        self.images = []
        self.rectangles = []
        self.texts = []
        self.bindings = []
        self.deleted = []
        self.windows = []

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

    def create_image(self, *points, **kwargs):
        self.images.append({
            "points": points,
            **kwargs,
        })

    def create_window(self, *points, **kwargs):
        self.windows.append({
            "points": points,
            **kwargs,
        })

    def create_rectangle(self, *points, **kwargs):
        self.rectangles.append({
            "points": points,
            **kwargs,
        })

    def create_text(self, *points, **kwargs):
        if len(points) != 2:
            raise ValueError("create_text expects x and y coordinates")
        self.texts.append({
            "points": points,
            **kwargs,
        })

    def bbox(self, tag):
        return (10, 10, 140, 180)

    def tag_bind(self, tag, event, callback):
        self.bindings.append((tag, event, callback))

    def delete(self, target):
        self.deleted.append(target)


class EscapeRoomTest(unittest.TestCase):
    @patch("escape_room.objects.picture.generate_riddle")
    @patch("escape_room.objects.picture.ImageTk.PhotoImage")
    def test_draw_room_creates_drawable_polygons(
        self, mock_photo, mock_generate_riddle
    ):
        mock_generate_riddle.return_value = "Test riddle"

        app = EscapeApp.__new__(EscapeApp)
        action_manager = ActionManager()
        ContextManager().set_action_manager(action_manager)
        room_state = RoomState()


        app.room = Room.__new__(Room)
        app.room.canvas_area = FakeCanvas()
        app.room.room_data = room_data.start_room
        app.room.door = []
        app.room.light = [MagicMock()]
        app.room.table = [MagicMock()]
        app.room.chair = [Chair(test_room,0,room_state)]
        app.room.wardrobe = [MagicMock()] # [Wardrobe(test_room,0,room_state)]
        app.room.picture = [MagicMock()] 
        app.room.bookshelf = [MagicMock()] # [Bookshelf()]
        app.room.safe = [MagicMock()]
        app.room.clock = [MagicMock()]
        app.room.letter = [MagicMock()] # [Letter(app.room.canvas_area)]
        app.room.key = [FakeDrawable()]
        app.room.revolver = [FakeDrawable()]
        app.room.magnifier = [FakeDrawable()]
        app.room.water_glass = [FakeDrawable()]
        app.room.poker = [FakeDrawable()]
        app.room.diamond = [FakeDrawable()]
        app.room.metal_cassette = [MagicMock()] #[MetalCassette()]
        app.room.figure = []
        app.room.bench = [MagicMock()]
        app.room.fireplace = [MagicMock()] # [Fireplace()]
        app.room.window = [Window()]
        app.room.inventory = FakeDrawable()
        app.room.player_panel = MagicMock() 
        app.room.chat_panel = MagicMock() 
        app.room.menu = MagicMock()
        app.room.player_name = ""
        app.room.player_icon_number = 1
        app.room.role = MagicMock()
        app.room.room_coordinates = [
            ["#8B4513", (0, 0, 0), (8, 0, 0), (8, 0, 4), (0, 0, 4)],
            ["white", (0, 3, 0), (8, 3, 0), (8, 3, 4), (0, 3, 4)],
            ["white", (0, 0, 0), (0, 3, 0), (0, 3, 4), (0, 0, 4)],
            ["white", (8, 0, 0), (8, 3, 0), (8, 3, 4), (8, 0, 4)],
        ]

        app.room.draw_room()

      
        self.assertIs(app.room.key[0].drawn_on, app.room.canvas_area)
        self.assertIs(app.room.inventory.drawn_on, app.room.canvas_area)

    def test_create_doors_creates_three_doors(self):
        app = EscapeApp.__new__(EscapeApp)
        app.room = Room.__new__(Room)
        app.room.room_data = room_data.start_room
        # create doors
        doors = []
        room_state = RoomState()
        canvas = MagicMock()
        ContextManager().set_canvas(canvas)
        room = MagicMock()#
        ContextManager().set_room(room)
        for index,door in enumerate(app.room.room_data["door"]):         
            obj = Door(test_room,0,room_state=room_state)
            doors.append(obj)       

        self.assertEqual(len(doors), 3)
        self.assertEqual([door.tag for door in doors], ["red_door", "red_door", "red_door"])
        for door in doors:
            self.assertEqual(len(door.corners), 4)
            y_values = [point[1] for point in door.corners]
            self.assertEqual(min(y_values), 0)
            self.assertEqual(max(y_values), 2)
        self.assertEqual(
            doors[2].corners,
            [
                (3.2, 2.0, 4), 
                (4.2, 2.0, 4), 
                (4.2, 0, 4), 
                (3.2, 0, 4)
            ],
        )

    def test_show_start_screen_delegates_to_start_screen(self):
        root = tkinter.Tk()
        root.withdraw()

        # 1. Setup the empty app instance
        app = EscapeApp.__new__(EscapeApp)
        app.server = "mock_server_data"
        app.room = MagicMock()
        app.start_game = MagicMock()

        # 2. Patch the StartScreen class where it is USED (inside escape_app)
        with patch('src.escape_room.application.escape_app.StartScreen') as mock_start_screen_class:
            
            # Create the mock instance that will be returned when StartScreen() is called
            mock_instance = MagicMock()
            mock_start_screen_class.return_value = mock_instance

            # 3. Call the real method 
            app.show_start_screen()

            # 4. Asserts:
            # A) Check if the StartScreen was created with the right parameters
            mock_start_screen_class.assert_called_once_with(
                app.room.canvas_area, 
                app.start_game, 
                app.server
            )
            
            # B) Check if the .draw() method was actually called on the instance!
            mock_instance.draw.assert_called_once()
            
            # C) Check if it was saved as an attribute in your app
            self.assertEqual(app.start_screen, mock_instance)    
        root.destroy()
    
    @patch("escape_room.objects.picture.generate_riddle")
    @patch("escape_room.objects.picture.ImageTk.PhotoImage")
    def test_start_game_clears_start_screen_and_draws_room(self, mock_photo, mock_generate_riddle):
        mock_generate_riddle.return_value = "Test riddle"

        app = EscapeApp.__new__(EscapeApp)
        action_manager = ActionManager()
        ContextManager().set_action_manager(action_manager)
        room_state = RoomState()

        app.room = Room.__new__(Room)
        app.room.canvas_area = FakeCanvas()
        app.room.room_data = room_data.start_room
        app.room.door = []
        app.room.light = [MagicMock()]
        app.room.table = [MagicMock()]
        app.room.chair = [Chair(test_room,0,room_state)]
        app.room.wardrobe = [MagicMock()]
        app.room.picture = [MagicMock()] 
        app.room.bookshelf = [MagicMock()]
        app.room.safe = [MagicMock()]
        app.room.clock = [MagicMock()]
        app.room.letter = [MagicMock()]
        app.room.key = [FakeDrawable()]
        app.room.revolver = [FakeDrawable()]
        app.room.magnifier = [FakeDrawable()]
        app.room.water_glass = [FakeDrawable()]
        app.room.poker = [FakeDrawable()]
        app.room.diamond = [FakeDrawable()]
        app.room.metal_cassette = [MagicMock()] #[MetalCassette()]
        app.room.figure = []
        app.room.bench = [MagicMock()]
        app.room.fireplace = [MagicMock()]
        app.room.window = [Window()]
        app.room.inventory = FakeDrawable()
        app.room.player_panel = MagicMock() 
        app.room.chat_panel = MagicMock() 
        app.room.menu = MagicMock()
        app.room.player_name = ""
        app.room.player_icon_number = 1
        app.room.role = MagicMock()

        canvas = FakeCanvas()
        canvas.master = tkinter.Tk() 
        callback = object()
        app.start_screen = StartScreen(canvas, callback,"")    
        app.start_screen.player_icon_number = 1
        app.game_client = MagicMock() 
        app.room.room_coordinates = [
            ["#8B4513", (0, 0, 0), (8, 0, 0), (8, 0, 4), (0, 0, 4)],
            ["white", (0, 3, 0), (8, 3, 0), (8, 3, 4), (0, 3, 4)],
            ["white", (0, 0, 0), (0, 3, 0), (0, 3, 4), (0, 0, 4)],
            ["white", (8, 0, 0), (8, 3, 0), (8, 3, 4), (8, 0, 4)],
        ]

        app.start_game()

        self.assertIn("all", app.room.canvas_area.deleted)
        self.assertGreater(len(app.room.canvas_area.polygons), 0)
        self.assertIs(app.room.key[0].drawn_on, app.room.canvas_area)

    def test_chair_can_face_different_directions(self):
        room_state = RoomState()
        right_chair = Chair(test_room,0,room_state)
        left_chair = Chair(test_room,0,room_state)
        front_chair = Chair(test_room,0,room_state)
        back_chair = Chair(test_room,0,room_state)

        self.assertEqual(right_chair.coordinates_chairseat[0][2], (4.45, 0.4, 3.15))
        self.assertEqual(left_chair.coordinates_chairseat[0][2], (4.45, 0.4, 3.15))
        self.assertEqual(front_chair.coordinates_chairseat[0][2], (4.45, 0.4, 3.15))
        self.assertEqual(back_chair.coordinates_chairseat[0][2], (4.45, 0.4, 3.15))
        self.assertEqual(left_chair.coordinates_chairseat[0][3], (4.45, 0.51, 3.15))
        self.assertEqual(back_chair.coordinates_chairseat[0][3], (4.45, 0.51, 3.15))

    def test_chair_legs_are_drawn_like_table_legs(self):
        room_state = RoomState()
        chair = Chair(test_room,0,room_state)

        self.assertEqual(len(chair.coordinates_chairlegs), 16)
        for leg_surface in chair.coordinates_chairlegs:
            self.assertEqual(len(leg_surface), 5)

    def test_chair_legs_fit_under_seat(self):
        room_state = RoomState()
        chair = Chair(test_room,0,room_state)
        leg_points = [
            point
            for polygon in chair.coordinates_chairlegs
            for point in polygon[1:]
        ]

        self.assertEqual(min(point[0] for point in leg_points), 4.45)
        self.assertEqual(max(point[0] for point in leg_points), 5.1499999999999995)
        self.assertEqual(max(point[1] for point in leg_points), 0.4)

    def test_back_legs_align_with_backrest_posts(self):
        room_state = RoomState()
        chair = Chair(test_room,0,room_state)
        right_back_leg_points = [
            point
            for polygon in chair.coordinates_chairlegs[:5]
            for point in polygon[1:]
        ]
        left_back_leg_points = [
            point
            for polygon in chair.coordinates_chairlegs[5:10]
            for point in polygon[1:]
        ]

        self.assertEqual(min(point[2] for point in left_back_leg_points), 2.6)
        self.assertEqual(max(point[2] for point in left_back_leg_points), 3.15)
        self.assertEqual(min(point[2] for point in right_back_leg_points), 3.05)
        self.assertEqual(max(point[2] for point in right_back_leg_points), 3.15)

    def test_chair_parts_include_top_and_four_sides(self):
        room_state = RoomState()
        chair = Chair(test_room,0,room_state)

        self.assertEqual(len(chair.coordinates_chairseat), 5)
        self.assertEqual(len(chair.coordinates_chairlegs_back), 13)


if __name__ == "__main__":
    unittest.main()
