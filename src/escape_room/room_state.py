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
            "wardrobe": {}
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