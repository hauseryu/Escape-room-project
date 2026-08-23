LEG_SHADOW = "#4A2C14"
LEG_MIDTONE = "#6F4520"
LEG_HIGHLIGHT = "#7A4A22"
WOOD_SHADOW = "#5A3518"
WOOD_MIDTONE = "#6F4520"
WOOD_HIGHLIGHT = "#7A4A22"
WOOD_TOP = "#8B5A2B"

class Chair():
    def __init__(self, x, y, z, direction="right", shift_coordinates=(0, 0, 0)):
        self.x = x
        self.y = y
        self.z = z
        self.width_small = 0.1
        self.width_large = 0.7
        self.direction = direction
        self.shift_coordinates = shift_coordinates

        # 1. Base Parts: The main seat panel (Always spans full 0.7 width)
        self.coordinates_chairseat = self._create_panel_coordinates(z1=2.6,z2=3.15,back=False)

        # All 4 lower legs beneath the seat
        self.coordinates_chairlegs = [
            *self._create_leg_coordinates(4.45, 3.15-self.width_small),
            *self._create_leg_coordinates(5.05, 3.15-self.width_small),
            *self._create_leg_coordinates(4.45, 2.6),
            *self._create_leg_coordinates(5.05, 2.6),
        ]

        # 2. Handle Direction (Determine X-position of the backrest)
        if self.direction == "right":
            # Backrest is on the left side of the chair (X = 4.45)
            # This makes the chair face towards the RIGHT
            x_backrest = 4.45
        else: # direction == "left"
            # Backrest shifts to the right side of the chair (X = 5.05)
            # This makes the chair face towards the LEFT
            x_backrest = 5.05

        # 3. Upper Parts: Mounted dynamically using 'x_backrest'
        self.coordinates_chairlegs_back = [
            *self._create_leg_coordinates(x_backrest, 3.15-self.width_small, back=True),
            *self._create_panel_coordinates(z1=2.6,z2=3.15,back=True, x_pos=x_backrest),
            *self._create_leg_coordinates(x_backrest, 2.6, back=True),
        ]

        # 4. Master Assembly Sequence
        self.coordinates_chair = self.coordinates_chairlegs + self.coordinates_chairseat + \
            self.coordinates_chairlegs_back

    def _create_leg_coordinates(self, x, z, back=False):
        x2 = x + self.width_small
        z2 = z + self.width_small

        if not back:
            low = 0
            high = 0.4
        else:
            low = 0.51
            high = 0.91

        return [
            ["#4A2C14", (x2, low, z2), (x, low, z2), (x, high, z2), (x2, high, z2)],
            ["#6F4520", (x, low, z2), (x, low, z), (x, high, z), (x, high, z2)],
            ["#6F4520", (x2, low, z), (x2, low, z2), (x2, high, z2), (x2, high, z)],
            ["#7A4A22", (x, low, z), (x2, low, z), (x2, high, z), (x, high, z)],
        ]

    def _create_panel_coordinates(self, z1=0, z2=0, back=False, x_pos=4.45):    
        if not back:
            width = self.width_large
            height1 = 0.4
            height2 = 0.51
        else:
            width = self.width_small
            height1 = 0.8
            height2 = 0.91
            z2 -= self.width_small
            
        return [
            ["#5A3518",
             (x_pos + width, height1, z2),
             (x_pos, height1, z2),
             (x_pos, height2, z2),
             (x_pos + width, height2, z2)],
            ["#6F4520",
             (x_pos, height1, z2),
             (x_pos, height1, z1),
             (x_pos, height2, z1),
             (x_pos, height2, z2)],
            ["#6F4520",
             (x_pos + width, height1, z1),
             (x_pos + width, height1, z2),
             (x_pos + width, height2, z2),
             (x_pos + width, height2, z1)],
            ["#8B5A2B",
             (x_pos, height2, z1),
             (x_pos + width, height2, z1),
             (x_pos + width, height2, z2),
             (x_pos, height2, z2)],
            ["#7A4A22",
             (x_pos, height1, z1),
             (x_pos + width, height1, z1),
             (x_pos + width, height2, z1),
             (x_pos, height2, z1)],
        ]
