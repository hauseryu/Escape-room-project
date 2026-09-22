from src.escape_room.objects.figure import Figure
from src.escape_room.room.room_state_repository import RoomStateRepository

class RoomState():
    def __init__(self):
        self.room_state= {} # keep a room state for each room
        self.current_room = None
        self.repo = RoomStateRepository()
        self.room_state = self.repo.load_all_rooms()

    # when entering room, new room state is added
    def add_room(self,room_name = ""):
        # check if entry already exists
        try:
            if self.room_state[room_name] != None:
                return
        except KeyError:
            pass

        # if not, add it
        self.room_state.update({room_name: {
            "key": {},
            "light": {},
            "door": {},
            "safe": {},
            "wardrobe": {},
            "picture": {},
            "figure": {},
            "revolver": {},
            "magnifier": {},
            "water_glass": {},
            "bench": {},
            "chair": {},
            "table": {},
            "fireplace": {},
            "poker": {},
            "diamond": {},
            "metal_cassette": {}
        } }) # add initial entry for the named room

    # when entering room, the current room is remembered
    def set_current_room(self,current_room):
        self.current_room = current_room

    # status change: object removed from room
    def remove(self,object,unique_id):
        self.room_state[self.current_room][object].update({unique_id:"removed"})

    # status change: object removed from room
    def move(self,object,unique_id):
        self.room_state[self.current_room][object].update({unique_id:"moved"})

    def object_is_removed(self,object,unique_id):
        try:
            if self.room_state[self.current_room][object][unique_id] == "removed":
                return True
        except KeyError:
            pass
        return False

    def object_is_moved(self,object,unique_id):
        try:
            if self.room_state[self.current_room][object][unique_id] == "moved":
                return True
        except KeyError:
            pass
        return False
    
    def set_state_object(self,object,unique_id,state):
        self.room_state[self.current_room][object].update({unique_id:state})

    def get_state_object(self,object,unique_id):
        try:
            state = self.room_state[self.current_room][object][unique_id]
            return state
        except KeyError:
            return None        

    def get_objects(self,type):
        if type=='figure':
            figures = []
            for figure_name,attribs in self.room_state[self.current_room]["figure"].items():
                image = attribs[0]
                x_coord,y_coord,width,height = attribs[1:5]
                figure_talk = attribs[5]
                figure = Figure(figure_name,image,x_coord,y_coord,width,height,figure_talk)
                figures.append(figure)
            return figures

    def set_object(self,type,object):
        if type=='figure':
            self.room_state[self.current_room]["figure"][object.figure_name] = [ \
                object.image_path, object.x_coord, object.y_coord, object.width, object.height, \
                object.action_sequence_talk ]
    
    def save_to_db(self):
        """Stores the corrent state of every room in the database"""
        self.repo.save_all_rooms(self.room_state)
    
    def close(self):
        self.repo.close()