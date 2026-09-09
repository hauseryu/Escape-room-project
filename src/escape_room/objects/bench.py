from src.escape_room.gui_utilities import graphics
from src.escape_room.application.context_manager import ContextManager

IMAGE_DIR = ContextManager().get_image_path()
CLOTH_TEXTURE = IMAGE_DIR / "Texturelabs_Fabric.jpg"

class Bench():
    # def __init__(self,direction,shift_coordinates=(0,0,0),unique_id=None):
    def __init__(self, x, y, z, direction="right", shift_coordinates=(0, 0, 0),unique_id=None):
        self.x = x
        self.y = y
        self.z = z
        self.width_small = 0.1
        self.width_large = 1.7
        self.direction = direction
        self.shift_coordinates = shift_coordinates

        # 1. Base Parts: The main seat panel (Always spans full 0.7 width)
        self.coordinates_benchseat = self._create_panel_coordinates(direction,x_pos1=3.45, x_pos2=5.05+self.width_small,
                                                                    z1=3.15,z2=2.6,
                                                                    height1=0.4, height2=0.51)

        # All 4 lower legs beneath the seat
        self.coordinates_benchlegs = [
            *self._create_leg_coordinates(3.45, 3.15-self.width_small,direction),
            *self._create_leg_coordinates(5.05, 3.15-self.width_small,direction),
            *self._create_leg_coordinates(3.45, 2.6,direction),
            *self._create_leg_coordinates(5.05, 2.6,direction)
        ]

        # 3. Upper Parts: Mounted dynamically using 'x_backrest' and 'z_backrest'
        x_backrest1 = 5.05
        x_backrest2 = 5.05
        z_backrest1 = 3.15
        z_backrest2 = 2.6
        coordinates_benchlegs_back1 = [
            *self._create_leg_coordinates(x_backrest1, z_backrest1-self.width_small, direction,back=True),
            *self._create_leg_coordinates(x_backrest2, z_backrest2, direction,back=True),
            *self._create_panel_coordinates(direction,x_pos1=5.05, x_pos2=5.05+self.width_small,
                                                    z1=3.15,z2=2.6,
                                                    height1=0.7, height2=0.81)
        ]
        coordinates_benchlegs_back2 = [
            *self._create_panel_coordinates(direction,x_pos1=3.45, x_pos2=5.05+self.width_small,
                                                    z1=3.15,z2=3.05,
                                                    height1=0.55, height2=0.81,front_texture=True)
        ]
        x_backrest1 = 3.45
        x_backrest2 = 3.45
        z_backrest1 = 3.15
        z_backrest2 = 2.6
        coordinates_benchlegs_back3 = [
            *self._create_leg_coordinates(x_backrest1, z_backrest1-self.width_small, direction,back=True),
            *self._create_leg_coordinates(x_backrest2, z_backrest2, direction,back=True),
            *self._create_panel_coordinates(direction,x_pos1=3.45, x_pos2=3.45+self.width_small,
                                                    z1=3.15,z2=2.6,
                                                    height1=0.7, height2=0.81)

        ]

        self.coordinates_benchlegs_back = coordinates_benchlegs_back2 + coordinates_benchlegs_back1 + \
            coordinates_benchlegs_back3

        # 4. Master Assembly Sequence
        self.bench_coordinates = self.coordinates_benchlegs + self.coordinates_benchseat + \
            self.coordinates_benchlegs_back

        # swap (for left perspective)
        if self.direction == "left":
            self.swap_coordinates()

    def swap_coordinates(self):
        for count_polygon,polygon in enumerate(self.bench_coordinates):
            head,polygon_data = polygon[0],polygon[1:]
            for count_coord,coord in enumerate(polygon_data):
                x,y,z = coord
                self.bench_coordinates[count_polygon][count_coord+1] = (3.15-z,y,x) # swap operation, mirror at z-axis

    def _create_leg_coordinates(self, x, z, direction,back=False):
        x2 = x + self.width_small
        z2 = z + self.width_small

        if not back:
            low = 0
            high = 0.4
        else:
            low = 0.51
            high = 0.71

        if direction=="front":
            return [
                ["#4A2C14", (x2, low, z2), (x, low, z2), (x, high, z2), (x2, high, z2)],
                ["#6F4520", (x, low, z2), (x, low, z), (x, high, z), (x, high, z2)],
                ["#6F4520", (x2, low, z), (x2, low, z2), (x2, high, z2), (x2, high, z)],
                ["#7A4A22", (x, low, z), (x2, low, z), (x2, high, z), (x, high, z)],
            ]
        elif direction=="left":
            return [
                ["#4A2C14", (x2, low, z2), (x, low, z2), (x, high, z2), (x2, high, z2)],
                ["#6F4520", (x2, low, z), (x2, low, z2), (x2, high, z2), (x2, high, z)],
                ["#7A4A22", (x, low, z), (x2, low, z), (x2, high, z), (x, high, z)],
                ["#6F4520", (x, low, z2), (x, low, z), (x, high, z), (x, high, z2)],
            ]

    def _create_panel_coordinates(self, direction, x_pos1,x_pos2,z1,z2,height1,height2,front_texture=False):    

        backpart=["#5A3518",
            (x_pos2, height1, z1),
            (x_pos1, height1, z1),
            (x_pos1, height2, z1),
            (x_pos2, height2, z1)]
        left=["#6F4520", 
            (x_pos1, height1, z2),
            (x_pos1, height1, z1),
            (x_pos1, height2, z1),
            (x_pos1, height2, z2)]
        right=["#6F4520", 
            (x_pos2, height1, z1),
            (x_pos2, height1, z2),
            (x_pos2, height2, z2),
            (x_pos2, height2, z1)]
        surface=[("white",CLOTH_TEXTURE), 
            (x_pos2, height2, z1),
            (x_pos1, height2, z1),
            (x_pos1, height2, z2),
            (x_pos2, height2, z2)]
        if front_texture:
            front_text = ("white",CLOTH_TEXTURE)
        else:
            front_text = "#8B5A2B"
        front=[front_text, 
            (x_pos2, height1, z2),
            (x_pos1, height1, z2),
            (x_pos1, height2, z2),
            (x_pos2, height2, z2)]

        if direction=="front":
            return[backpart,left,right,surface,front]
        elif direction=="left":
            #return[right,front,left,surface,backpart]
            return[backpart,right,front,left,surface]



