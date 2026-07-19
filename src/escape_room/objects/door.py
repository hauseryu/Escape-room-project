from escape_room.graphics import compute_2d_coordinates

_DEFAULT_DOOR_RGB = (111, 63, 32)

# Tkinter can draw named colors directly, but our color mixing needs RGB values.
_NAMED_COLORS = {
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "brown": (165, 42, 42),
    "cyan": (0, 255, 255),
    "gray": (128, 128, 128),
    "green": (0, 128, 0),
    "grey": (128, 128, 128),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
}


def _color_to_rgb(color):
    if not isinstance(color, str):
        return _DEFAULT_DOOR_RGB

    normalized = color.lower()
    if normalized in _NAMED_COLORS:
        return _NAMED_COLORS[normalized]

    if not normalized.startswith("#") or len(normalized) != 7:
        return _DEFAULT_DOOR_RGB

    try:
        return tuple(int(normalized[index : index + 2], 16) for index in (1, 3, 5))
    except ValueError:
        return _DEFAULT_DOOR_RGB


def _rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def _mix_color(color, target, amount):
    # Move the door color a little toward black or white for shadows and highlights.
    amount = max(0, min(1, amount))
    start = _color_to_rgb(color)
    rgb = tuple(int(start[index] + (target[index] - start[index]) * amount) for index in range(3))
    return _rgb_to_hex(rgb)


class Door:
    def __init__(
        self,
        corners,
        color="#6f3f20",
        tag="door",
    ):
        self.corners = self._create_corners(corners)
        self.color = color
        self.tag = tag
        self.is_open = False

    def _create_corners(self, corners):
        if len(corners) != 4:
            raise ValueError("corners must contain four 3D points")
        return [tuple(point) for point in corners]

    def _tags(self):
        return (self.tag, "door")
    
    def open_door(self):
        self.is_open = True


    def close_door(self):
        self.is_open = False


    def toggle(self):
        self.is_open = not self.is_open
    
    def clicked(self, canvas, event):
        items = canvas.find_overlapping(
            event.x,
            event.y,
            event.x,
            event.y
        )

        for item in items:
            if self.tag in canvas.gettags(item):
                return True

        return False
    
    def handle_click(self, canvas, event):
        if self.clicked(canvas, event):
            self.toggle()
            return True

        return False
    
    def draw(self, canvas, win_width, win_height):
        if self.is_open:
            self._draw_opening(canvas, win_width, win_height)

        self._draw_frame(canvas, win_width, win_height)

        if self.is_open:
            self._draw_open_door(canvas, win_width, win_height)
        else:
            self._draw_door_leaf(canvas, win_width, win_height, knob_u=0.82)

            
    def _project(self, u, v, win_width, win_height):
        # First pick a point on the 3D door, then project it onto the 2D canvas.
        x, y, z = self._point_in_3d_quad(u, v)
        return compute_2d_coordinates(x, y, z, win_width, win_height)

    def _point_in_3d_quad(self, u, v):
        # Corners are always ordered: top-left, top-right, bottom-right, bottom-left.
        top_left, top_right, bottom_right, bottom_left = self.corners
        top = self._point_between_3d(top_left, top_right, u)
        bottom = self._point_between_3d(bottom_left, bottom_right, u)
        return self._point_between_3d(top, bottom, v)

    def _draw_frame(self, canvas, win_width, win_height):
        frame = 0.033

        fill = _mix_color(self.color, (0, 0, 0), 0.24)
        outline = _mix_color(self.color, (0, 0, 0), 0.44)
        
        # linker Pfosten
        self._draw_projected_rect(
            canvas,
            win_width,
            win_height,
            0,
            0,
            frame,
            1,
            fill=fill,
            outline=outline,
            width=1,
        )

        # rechter Pfosten
        self._draw_projected_rect(
            canvas,
            win_width,
            win_height,
            1-frame,
            0,
            1,
            1,
            fill=fill,
            outline=outline,
            width=1,
        )

        # oberer Balken
        self._draw_projected_rect(
            canvas,
            win_width,
            win_height,
            0,
            0,
            1,
            0.02,
            fill=fill,
            outline=outline,
            width=1,
        )

    def _draw_door_leaf(self, canvas, win_width, win_height, knob_u):
        top_inset = 0.02
        bottom_inset = 0.0

        corners = [
            self._project(top_inset, top_inset, win_width, win_height),
            self._project(1 - top_inset, top_inset, win_width, win_height),
            self._project(1 - top_inset, 1 - bottom_inset, win_width, win_height),
            self._project(top_inset, 1 - bottom_inset, win_width, win_height),
        ]

        
        self._draw_leaf_in_quad(canvas, corners, knob_u)
        
    def _draw_leaf_in_quad(self, canvas, corners, knob_u):
        frame = 0.08
        panel_gap = 0.05
        panel_width = (1 - frame * 2 - panel_gap) / 2
        panel_height = 0.34

        self._draw_quad_rect(
            canvas,
            corners,
            0,
            0,
            1,
            1,
            fill=self.color,
            outline=_mix_color(self.color, (0, 0, 0), 0.5),
            width=2,
        )

        self._draw_planks(canvas, corners)
        self._draw_panels(canvas, corners, frame, panel_gap, panel_width, panel_height)
        self._draw_knob(canvas, corners, knob_u)

    def _draw_planks(self, canvas, corners):
        for index in range(1, 5):
            # u moves from left to right across the door; these values split it into planks.
            u = index / 5
            top = self._point_in_quad(corners, u, 0.03)
            bottom = self._point_in_quad(corners, u, 0.97)
            canvas.create_line(
                top[0],
                top[1],
                bottom[0],
                bottom[1],
                fill=_mix_color(self.color, (0, 0, 0), 0.55),
                width=2,
                tags=self._tags(),
            )
            # A thin bright line beside the dark line gives each plank a small edge.
            light_top = self._point_in_quad(corners, u + 0.01, 0.035)
            light_bottom = self._point_in_quad(corners, u + 0.01, 0.965)
            canvas.create_line(
                light_top[0],
                light_top[1],
                light_bottom[0],
                light_bottom[1],
                fill=_mix_color(self.color, (255, 255, 255), 0.22),
                width=1,
                tags=self._tags(),
            )

    def _draw_panels(self, canvas, corners, frame, panel_gap, panel_width, panel_height):
        for row in range(2):
            panel_y = 0.14 + row * (panel_height + 0.14)
            for col in range(2):
                panel_x = frame + col * (panel_width + panel_gap)
                self._draw_quad_rect(
                    canvas,
                    corners,
                    panel_x,
                    panel_y,
                    panel_x + panel_width,
                    panel_y + panel_height,
                    fill=_mix_color(self.color, (120, 120, 120), 0.45),
                    outline=_mix_color(self.color, (255, 255, 255), 0.28),
                    width=2,
                )
                inset = panel_width * 0.12
                self._draw_quad_rect(
                    canvas,
                    corners,
                    panel_x + inset,
                    panel_y + inset,
                    panel_x + panel_width - inset,
                    panel_y + panel_height - inset,
                    fill="#222222",
                    outline=_mix_color(self.color, (0, 0, 0), 0.6),
                    width=1,
                )

    def _draw_knob(self, canvas, corners, knob_u):
        knob = self._point_in_quad(corners, knob_u, 0.52)
        top_left, top_right, _, _ = corners
        radius = max(6, abs(top_right[0] - top_left[0]) * 0.06)
        canvas.create_oval(
            knob[0] - radius,
            knob[1] - radius,
            knob[0] + radius,
            knob[1] + radius,
            fill="#c28a3d",
            outline="#ffe1a0",
            width=2,
            tags=self._tags(),
        )
        canvas.create_oval(
            knob[0] - radius * 0.35,
            knob[1] - radius * 0.35,
            knob[0] + radius * 0.35,
            knob[1] + radius * 0.35,
            fill="#70451c",
            outline="",
            tags=self._tags(),
        )

    def _draw_projected_rect(self, canvas, win_width, win_height, u1, v1, u2, v2, **kwargs):
        corners = [
            self._project(u1, v1, win_width, win_height),
            self._project(u2, v1, win_width, win_height),
            self._project(u2, v2, win_width, win_height),
            self._project(u1, v2, win_width, win_height),
        ]
        canvas.create_polygon(self._flatten(corners), tags=self._tags(), **kwargs)

    def _draw_quad_rect(self, canvas, corners, u1, v1, u2, v2, **kwargs):
        points = [
            self._point_in_quad(corners, u1, v1),
            self._point_in_quad(corners, u2, v1),
            self._point_in_quad(corners, u2, v2),
            self._point_in_quad(corners, u1, v2),
        ]
        canvas.create_polygon(self._flatten(points), tags=self._tags(), **kwargs)

    def _point_between(self, start, end, amount):
        return (
            start[0] + (end[0] - start[0]) * amount,
            start[1] + (end[1] - start[1]) * amount,
        )

    def _point_between_3d(self, start, end, amount):
        return (
            start[0] + (end[0] - start[0]) * amount,
            start[1] + (end[1] - start[1]) * amount,
            start[2] + (end[2] - start[2]) * amount,
        )

    def _point_in_quad(self, corners, u, v):
        # u is left-to-right and v is top-to-bottom inside the given 2D quadrilateral.
        top_left, top_right, bottom_right, bottom_left = corners
        top = self._point_between(top_left, top_right, u)
        bottom = self._point_between(bottom_left, bottom_right, u)
        return self._point_between(top, bottom, v)

    def _flatten(self, points):
        # Tkinter polygons need [x1, y1, x2, y2, ...] instead of [(x1, y1), ...].
        coordinates = []
        for x, y in points:
            coordinates.extend((x, y))
        return coordinates
    
    def _draw_open_door(self, canvas, win_width, win_height):

        hinge = 0.02

        corners = [
            self._project(hinge, 0.02, win_width, win_height),
            self._project(0.35, 0.15, win_width, win_height),
            self._project(0.35, 0.85, win_width, win_height),
            self._project(hinge, 1.002, win_width, win_height),
        ]

        self._draw_leaf_in_quad(
            canvas,
            corners,
            knob_u=0.82,
        )
        
    def _draw_opening(self, canvas, win_width, win_height):
        frame = 0.0

        points = [
            self._project(frame, frame, win_width, win_height),
            self._project(1-frame, frame, win_width, win_height),
            self._project(1-frame, 1-frame, win_width, win_height),
            self._project(frame, 1-frame, win_width, win_height),
        ]

        canvas.create_polygon(
            self._flatten(points),
            fill="#222222",
            outline="",
            tags=self._tags(),
        )