LEG_SHADOW = "#4A2C14"
LEG_MIDTONE = "#6F4520"
LEG_HIGHLIGHT = "#7A4A22"
WOOD_SHADOW = "#5A3518"
WOOD_MIDTONE = "#6F4520"
WOOD_HIGHLIGHT = "#7A4A22"
WOOD_TOP = "#8B5A2B"


class Chair():
    def __init__(self, x, z, direction="left"):
        self.x = x
        self.z = z
        self.direction = direction

        seat_height = 0.45
        seat_thickness = 0.10
        seat_length = 0.45
        chair_width = 0.45
        height_backrest = 1.25
        back_post_width = 0.10
        back_rail_height = 0.35
        leg_width = 0.12
        seat_top = seat_height + seat_thickness

        # The backrest is built from two vertical posts and one horizontal rail.
        self.coordinates_backrest = [
            *self._create_backrest_part(0, back_post_width, seat_height, height_backrest),
            *self._create_backrest_part(
                chair_width - back_post_width,
                chair_width,
                seat_height,
                height_backrest,
            ),
            *self._create_backrest_part(
                back_post_width,
                chair_width - back_post_width,
                height_backrest - back_rail_height,
                height_backrest,
            ),
        ]

        self.coordinates_seat = self._create_box_coordinates(
            0,
            seat_length,
            0,
            chair_width,
            seat_height,
            seat_top,
            top_color=WOOD_TOP,
            front_color=WOOD_MIDTONE,
            back_color=WOOD_SHADOW,
            left_color=WOOD_SHADOW,
            right_color=WOOD_HIGHLIGHT,
        )

        # Back legs line up with the backrest posts so they look connected.
        self.coordinates_legs = [
            *self._create_back_leg_coordinates(chair_width - back_post_width, chair_width, seat_height),
            *self._create_back_leg_coordinates(0, back_post_width, seat_height),
            *self._create_leg_coordinates(seat_length - leg_width, chair_width - leg_width, seat_height),
            *self._create_leg_coordinates(seat_length - leg_width, 0, seat_height),
            
        ]

        self.coordinates_chair = self._create_chair_coordinates()

    def _point(self, forward, y, side):
        # Convert chair-local coordinates into room coordinates for each facing direction.
        if self.direction == "right":
            return (self.x + forward, y, self.z + side)
        if self.direction == "left":
            return (self.x - forward, y, self.z + side)
        if self.direction == "back":
            return (self.x - side, y, self.z + forward)
        if self.direction == "front":
            return (self.x + side, y, self.z - forward)
        raise ValueError("direction must be right, left, front, or back")

    def _average_depth(self, polygon):
        return sum(point[2] for point in polygon[1:]) / (len(polygon) - 1)

    def _average_height(self, polygon):
        return sum(point[1] for point in polygon[1:]) / (len(polygon) - 1)

    def _draw_order(self, polygon):
        return (self._average_depth(polygon), -self._average_height(polygon))

    def _sorted_surfaces(self, polygons):
        return sorted(polygons, key=self._draw_order, reverse=True)

    def _create_chair_coordinates(self):
        legs = self._sorted_surfaces(self.coordinates_legs)
        seat = self._sorted_surfaces(self.coordinates_seat)
        backrest = self._sorted_surfaces(self.coordinates_backrest)

        # Some directions need the backrest drawn last so it stays visible.
        if self.direction in ("right", "back"):
            return legs + seat + backrest
        return legs + backrest + seat

    def _create_box_coordinates(
        self,
        forward_start,
        forward_end,
        side_start,
        side_end,
        y_bottom,
        y_top,
        top_color,
        front_color,
        back_color,
        left_color,
        right_color,
    ):
        # A box is represented by its top and four vertical side polygons.
        return [
            [top_color,
             self._point(forward_start, y_top, side_start),
             self._point(forward_end, y_top, side_start),
             self._point(forward_end, y_top, side_end),
             self._point(forward_start, y_top, side_end)],
            [front_color,
             self._point(forward_start, y_bottom, side_start),
             self._point(forward_end, y_bottom, side_start),
             self._point(forward_end, y_top, side_start),
             self._point(forward_start, y_top, side_start)],
            [back_color,
             self._point(forward_end, y_bottom, side_end),
             self._point(forward_start, y_bottom, side_end),
             self._point(forward_start, y_top, side_end),
             self._point(forward_end, y_top, side_end)],
            [left_color,
             self._point(forward_start, y_bottom, side_end),
             self._point(forward_start, y_bottom, side_start),
             self._point(forward_start, y_top, side_start),
             self._point(forward_start, y_top, side_end)],
            [right_color,
             self._point(forward_end, y_bottom, side_start),
             self._point(forward_end, y_bottom, side_end),
             self._point(forward_end, y_top, side_end),
             self._point(forward_end, y_top, side_start)],
        ]

    def _create_backrest_part(self, side_start, side_end, y_bottom, y_top):
        return self._create_box_coordinates(
            -0.12,
            0,
            side_start,
            side_end,
            y_bottom,
            y_top,
            top_color=WOOD_HIGHLIGHT,
            front_color=WOOD_MIDTONE,
            back_color=WOOD_SHADOW,
            left_color=WOOD_SHADOW,
            right_color=WOOD_MIDTONE,
        )

    def _create_back_leg_coordinates(self, side_start, side_end, height):
        return self._create_box_coordinates(
            -0.12,
            0,
            side_start,
            side_end,
            0,
            height,
            top_color=LEG_HIGHLIGHT,
            front_color=LEG_HIGHLIGHT,
            back_color=LEG_SHADOW,
            left_color=LEG_MIDTONE,
            right_color=LEG_MIDTONE,
        )

    def _create_leg_coordinates(self, forward, side, height):
        width = 0.12
        forward_end = forward + width
        side_end = side + width

        return self._create_box_coordinates(
            forward,
            forward_end,
            side,
            side_end,
            0,
            height,
            top_color=LEG_HIGHLIGHT,
            front_color=LEG_HIGHLIGHT,
            back_color=LEG_SHADOW,
            left_color=LEG_MIDTONE,
            right_color=LEG_MIDTONE,
        )
