import unittest
from pathlib import Path
import sys
from unittest.mock import patch
from unittest.mock import MagicMock
import tkinter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.escape_room.escape_app import EscapeApp
from src.escape_room.escape_app import StartScreen
from src.escape_room.escape_app import EscapeClient
from src.escape_room.escape_app import Room

from src.escape_room.objects.chair import Chair
from src.escape_room.objects.light import Light
from src.escape_room.objects.table import Table
from src.escape_room.objects.wardrobe import Wardrobe
from src.escape_room.objects.picture import Picture
from src.escape_room.objects.bookshelf import Bookshelf

IMAGE_DIR = Path(__file__).resolve().parent 

class FakeDrawable:
    def __init__(self):
        self.drawn_on = None

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
        app.room = Room.__new__(Room)
        app.room.canvas_area = FakeCanvas()
        app.room.doors = []
        app.room.light = Light()
        app.room.table = Table()
        app.room.chair = Chair(4.85, 2.35, "right")
        app.room.wardrobe = Wardrobe()
        app.room.picture = MagicMock() #Picture(IMAGE_DIR / "../src/escape_room/assets/images/riddle_not_readable.png")
        app.room.bookshelf = Bookshelf()
        app.room.key = FakeDrawable()
        app.room.inventory = FakeDrawable()
        app.room.player_panel = MagicMock() 
        app.room.player_name = ""
        app.room.player_icon_number = 1
        app.room.room_coordinates = [
            ["#8B4513", (0, 0, 0), (8, 0, 0), (8, 0, 4), (0, 0, 4)],
            ["white", (0, 3, 0), (8, 3, 0), (8, 3, 4), (0, 3, 4)],
            ["white", (0, 0, 0), (0, 3, 0), (0, 3, 4), (0, 0, 4)],
            ["white", (8, 0, 0), (8, 3, 0), (8, 3, 4), (8, 0, 4)],
        ]

        app.room.draw_room()

      
        self.assertIs(app.room.key.drawn_on, app.room.canvas_area)
        self.assertIs(app.room.inventory.drawn_on, app.room.canvas_area)

    def test_create_doors_creates_three_doors(self):
        app = EscapeApp.__new__(EscapeApp)
        app.room = Room.__new__(Room)
        doors = app.room.create_doors()

        self.assertEqual(len(doors), 3)
        self.assertEqual([door.tag for door in doors], ["red_door", "green_door", "blue_door"])
        for door in doors:
            self.assertEqual(len(door.corners), 4)
            y_values = [point[1] for point in door.corners]
            self.assertEqual(min(y_values), 0)
            self.assertEqual(max(y_values), 2)
        self.assertEqual(
            doors[2].corners,
            [
                (8, 2, 3.1),
                (8, 2, 1.5),
                (8, 0, 1.5),
                (8, 0, 3.1),
            ],
        )

    def test_show_start_screen_delegates_to_start_screen(self):
        # 1. Setup the empty app instance
        app = EscapeApp.__new__(EscapeApp)
        app.server = "mock_server_data"
        app.room = MagicMock()
        app.start_game = MagicMock()

        # 2. Patch the StartScreen class where it is USED (inside escape_app)
        with patch('src.escape_room.escape_app.StartScreen') as mock_start_screen_class:
            
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
    
    @patch("escape_room.objects.picture.generate_riddle")
    @patch("escape_room.objects.picture.ImageTk.PhotoImage")
    def test_start_game_clears_start_screen_and_draws_room(self, mock_photo, mock_generate_riddle):
        mock_generate_riddle.return_value = "Test riddle"

        app = EscapeApp.__new__(EscapeApp)
        app.room = Room.__new__(Room)
        app.room.canvas_area = FakeCanvas()
        app.room.doors = []
        app.room.light = Light()
        app.room.table = Table()
        app.room.chair = Chair(4.85, 2.35, "right")
        app.room.wardrobe = Wardrobe()
        app.room.picture = MagicMock() #Picture(IMAGE_DIR / "../src/escape_room/assets/images/riddle_not_readable.png")
        app.room.bookshelf = Bookshelf()
        app.room.key = FakeDrawable()
        app.room.inventory = FakeDrawable()
        app.room.player_panel = MagicMock() 
        app.room.player_name = ""
        app.room.player_icon_number = 1
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
        self.assertIs(app.room.key.drawn_on, app.room.canvas_area)

    def test_chair_can_face_different_directions(self):
        right_chair = Chair(4, 2, "right")
        left_chair = Chair(4, 2, "left")
        front_chair = Chair(4, 2, "front")
        back_chair = Chair(4, 2, "back")

        self.assertEqual(right_chair.coordinates_seat[0][2], (4.45, 0.55, 2))
        self.assertEqual(left_chair.coordinates_seat[0][2], (3.55, 0.55, 2))
        self.assertEqual(front_chair.coordinates_seat[0][2], (4, 0.55, 1.55))
        self.assertEqual(back_chair.coordinates_seat[0][2], (4, 0.55, 2.45))
        self.assertEqual(left_chair.coordinates_seat[0][3], (3.55, 0.55, 2.45))
        self.assertEqual(back_chair.coordinates_seat[0][3], (3.55, 0.55, 2.45))

    def test_right_and_back_chair_draw_backrest_after_seat(self):
        right_chair = Chair(4, 2, "right")
        back_chair = Chair(4, 2, "back")

        self.assertEqual(
            right_chair.coordinates_chair[-15:],
            right_chair._sorted_surfaces(right_chair.coordinates_backrest),
        )
        self.assertEqual(
            back_chair.coordinates_chair[-15:],
            back_chair._sorted_surfaces(back_chair.coordinates_backrest),
        )

    def test_front_chair_draws_seat_after_backrest(self):
        chair = Chair(4, 2, "front")

        self.assertEqual(chair.coordinates_chair[-5:], chair._sorted_surfaces(chair.coordinates_seat))

    def test_chair_legs_are_drawn_like_table_legs(self):
        chair = Chair(4, 2, "right")

        self.assertEqual(len(chair.coordinates_legs), 20)
        for leg_surface in chair.coordinates_legs:
            self.assertEqual(len(leg_surface), 5)

    def test_chair_legs_fit_under_seat(self):
        chair = Chair(4, 2, "front")
        leg_points = [
            point
            for polygon in chair.coordinates_legs
            for point in polygon[1:]
        ]

        self.assertEqual(min(point[0] for point in leg_points), 4)
        self.assertEqual(max(point[0] for point in leg_points), 4.45)
        self.assertEqual(max(point[1] for point in leg_points), 0.45)

    def test_back_legs_align_with_backrest_posts(self):
        chair = Chair(4, 2, "right")
        right_back_leg_points = [
            point
            for polygon in chair.coordinates_legs[:5]
            for point in polygon[1:]
        ]
        left_back_leg_points = [
            point
            for polygon in chair.coordinates_legs[5:10]
            for point in polygon[1:]
        ]

        self.assertEqual(min(point[2] for point in left_back_leg_points), 2)
        self.assertEqual(max(point[2] for point in left_back_leg_points), 2.1)
        self.assertEqual(min(point[2] for point in right_back_leg_points), 2.35)
        self.assertEqual(max(point[2] for point in right_back_leg_points), 2.45)

    def test_chair_parts_include_top_and_four_sides(self):
        chair = Chair(4, 2, "left")

        self.assertEqual(len(chair.coordinates_seat), 5)
        self.assertEqual(len(chair.coordinates_backrest), 15)

    def test_chair_rejects_unknown_direction(self):
        with self.assertRaises(ValueError):
            Chair(4, 2, "diagonal")


if __name__ == "__main__":
    unittest.main()
