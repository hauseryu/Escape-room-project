from src.escape_room.gui_utilities import graphics

class Carpet():
    def __init__(self, room_data, index):

        # evaluate room data
        self.unique_id = room_data["carpet"][index][5]
        self.index = index
        self.room_data = room_data
        self.carpet_coordinates = room_data["carpet"][index][0:5]     

    def draw(self, canvas):
        graphics.draw(canvas,[self.carpet_coordinates])

