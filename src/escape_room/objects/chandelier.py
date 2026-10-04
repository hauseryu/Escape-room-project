from src.escape_room.gui_utilities import graphics
from src.escape_room.application.context_manager import ContextManager
from PIL import Image, ImageTk, ImageOps
from src.escape_room.application import globals


class Chandelier():
    def __init__(self, room_data, index):

        # evaluate room data
        (x,y,z) = room_data["chandelier"][index][0] # get chandelier coordinates (first element in list)
        self.unique_id = room_data["chandelier"][index][1]
        self.index = index
        self.room_data = room_data
        self.shift_coordinates = (x-5,y-8,z-9)
        self.chand_coordinate = (5, 8, 9)

    def draw(self, canvas):
        chand_x, chand_y, chand_z = self.chand_coordinate
        x_pos, y_pos = graphics.compute_2d_coordinates(chand_x, chand_y, chand_z, globals.canvas_width, globals.canvas_height, self.shift_coordinates)
        chand_image_path = ContextManager.get_image_path().joinpath("chandelier.png")
        chand_image = Image.open(chand_image_path)
        resized_image = ImageOps.contain(chand_image, (200, 200)) 
        self.chand_image_tk = ImageTk.PhotoImage(resized_image)
        # Draw the chandelier image on the canvas
        self.chand_image_id = canvas.create_image(x_pos, y_pos, image=self.chand_image_tk, anchor="nw", tags="chandelier")