from src.escape_room.objects.figure import Figure

class RoomState():
    def __init__(self):
        self.room_state= {} # keep a room state for each room
        self.current_room = None

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
            "figure": {}
        } }) # add initial entry for the named room

    # when entering room, the current room is remembered
    def set_current_room(self,current_room):
        self.current_room = current_room

    # status change: object removed from room
    def remove(self,object,unique_id):
        self.room_state[self.current_room][object].update({unique_id:"removed"})

    def object_is_removed(self,object,unique_id):
        try:
            if self.room_state[self.current_room][object][unique_id] == "removed":
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