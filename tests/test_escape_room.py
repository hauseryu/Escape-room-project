import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from escape_room.escape_room import EscapeApp
from escape_room.objects.chair import Chair
from escape_room.objects.light import Light
from escape_room.objects.table import Table
from escape_room.objects.wardrobe import Wardrobe


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

    def tag_bind(self, tag, event, callback):
        self.bindings.append((tag, event, callback))

    def delete(self, target):
        self.deleted.append(target)


class EscapeRoomTest(unittest.TestCase):
    def test_draw_room_creates_drawable_polygons(self):
        app = EscapeApp.__new__(EscapeApp)
        app.canvas_area = FakeCanvas()
        app.doors = []
        app.light = Light()
        app.table = Table()
        app.chair = Chair(4.85, 2.35, "right")
        app.wardrobe = Wardrobe()
        app.key = FakeDrawable()
        app.inventory = FakeDrawable()
        app.room_coordinates = [
            ["#8B4513", (0, 0, 0), (8, 0, 0), (8, 0, 4), (0, 0, 4)],
            ["white", (0, 3, 0), (8, 3, 0), (8, 3, 4), (0, 3, 4)],
            ["white", (0, 0, 0), (0, 3, 0), (0, 3, 4), (0, 0, 4)],
            ["white", (8, 0, 0), (8, 3, 0), (8, 3, 4), (8, 0, 4)],
        ]

        app.draw_room()

        self.assertEqual(len(app.canvas_area.polygons), 74)
        self.assertEqual(len(app.canvas_area.arcs), 3)
        for polygon in app.canvas_area.polygons[:4]:
            self.assertEqual(len(polygon["points"]), 8)
        self.assertEqual(app.canvas_area.polygons[0]["fill"], "#8B4513")
        self.assertEqual(app.canvas_area.polygons[0]["outline"], "black")
        self.assertIs(app.key.drawn_on, app.canvas_area)
        self.assertIs(app.inventory.drawn_on, app.canvas_area)

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

    def test_show_start_screen_delegates_to_start_screen(self):
        app = EscapeApp.__new__(EscapeApp)
        app.start_screen = FakeStartScreen()

        app.show_start_screen()

        self.assertTrue(app.start_screen.was_drawn)

    def test_start_game_clears_start_screen_and_draws_room(self):
        app = EscapeApp.__new__(EscapeApp)
        app.canvas_area = FakeCanvas()
        app.doors = []
        app.light = Light()
        app.table = Table()
        app.chair = Chair(4.85, 2.35, "right")
        app.wardrobe = Wardrobe()
        app.key = FakeDrawable()
        app.inventory = FakeDrawable()
        app.room_coordinates = [
            ["#8B4513", (0, 0, 0), (8, 0, 0), (8, 0, 4), (0, 0, 4)],
            ["white", (0, 3, 0), (8, 3, 0), (8, 3, 4), (0, 3, 4)],
            ["white", (0, 0, 0), (0, 3, 0), (0, 3, 4), (0, 0, 4)],
            ["white", (8, 0, 0), (8, 3, 0), (8, 3, 4), (8, 0, 4)],
        ]

        app.start_game()

        self.assertIn("all", app.canvas_area.deleted)
        self.assertGreater(len(app.canvas_area.polygons), 0)
        self.assertIs(app.key.drawn_on, app.canvas_area)

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
