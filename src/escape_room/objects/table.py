from src.escape_room.gui_utilities import graphics

class Table():
    def __init__(self, room_data, index, room_state):
        coord = room_data["table"][index][0] # get table coordinates (first element in list)
        unique_id = room_data["chair"][index][1] # unique identifier
        shift_coord = (coord[0]-7.55,coord[1]-0.67,coord[2]-3.75)        
        self.shift_coordinates = shift_coord
        self.room_state = room_state
        self.unique_id = unique_id
        self.state="initial"
        movement_vector=None
        try:
            movement_vector = room_data["table"][index][2]
        except:
            pass
        self.movement_vector = movement_vector
        # consider room state (bench is moved)
        if room_state.object_is_moved("table",unique_id):
            self.move_table()

        self.coordinates_tabletop = [
            ["#5A3518",
             (7.55, 0.67, 3.75),
             (5.55, 0.67, 3.75),
             (5.55, 0.78, 3.75),
             (7.55, 0.78, 3.75)],
            ["#6F4520",
             (5.55, 0.67, 3.75),
             (5.55, 0.67, 2.0),
             (5.55, 0.78, 2.0),
             (5.55, 0.78, 3.75)],
            ["#6F4520",
             (7.55, 0.67, 2.0),
             (7.55, 0.67, 3.75),
             (7.55, 0.78, 3.75),
             (7.55, 0.78, 2.0)],
            ["#8B5A2B",
             (5.55, 0.78, 2.0),
             (7.55, 0.78, 2.0),
             (7.55, 0.78, 3.75),
             (5.55, 0.78, 3.75)],
            ["#7A4A22",
             (5.55, 0.67, 2.0),
             (7.55, 0.67, 2.0),
             (7.55, 0.78, 2.0),
             (5.55, 0.78, 2.0)],
        ]

        self.coordinates_tablelegs = [
            *self._create_leg_coordinates(5.72, 3.52),
            *self._create_leg_coordinates(7.20, 3.52),
            *self._create_leg_coordinates(5.72, 2.15),
            *self._create_leg_coordinates(7.20, 2.15),
        ]

        self.coordinates_table = self.coordinates_tablelegs + self.coordinates_tabletop

    def _create_leg_coordinates(self, x, z):
        width = 0.16
        x2 = x + width
        z2 = z + width

        return [
            ["#4A2C14",
             (x2, 0, z2),
             (x, 0, z2),
             (x, 0.67, z2),
             (x2, 0.67, z2)],
            ["#6F4520",
             (x, 0, z2),
             (x, 0, z),
             (x, 0.67, z),
             (x, 0.67, z2)],
            ["#6F4520",
             (x2, 0, z),
             (x2, 0, z2),
             (x2, 0.67, z2),
             (x2, 0.67, z)],
            ["#7A4A22",
             (x, 0, z),
             (x2, 0, z),
             (x2, 0.67, z),
             (x, 0.67, z)]
        ]

    def draw(self,canvas):
        graphics.draw(canvas,self.coordinates_table,shift_coordinates=self.shift_coordinates,tag="table",object=self)

    def clicked(self, event, tag, object, canvas, world_coordinates):
        if tag=="table" and self.state=="initial":
            print("[DEBUG] table clicked!")
            canvas.delete(tag)
            self.move_table()
            self.room_state.move("table",self.unique_id)
            self.draw(canvas)

    def move_table(self):
        self.state = "moved"
        (a,b,c) = self.shift_coordinates
        if self.movement_vector[0]=="x":
            a+=self.movement_vector[1]
        elif self.movement_vector[0]=="y":
            b+=self.movement_vector[1]
        elif self.movement_vector[0]=="z":
            c+=self.movement_vector[1]
        self.shift_coordinates = (a,b,c)                