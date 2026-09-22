from src.escape_room.gui_utilities.speech_bubble import SpeechBubble
from src.escape_room.application.context_manager import ContextManager
from src.escape_room.gui_utilities import graphics

class Letter():
    def __init__(self, room_data, index, canvas, action_sequence=None):

        # evaluate room data
        (x,y,z) = room_data["letter"][index][0] # get letter coordinates (first element in list)
        unique_id = room_data["letter"][index][1]
        text = room_data["letter"][index][2] # get letter text
        choices = room_data["letter"][index][3] # get choices for letter
        check_action = room_data["letter"][index][4] # get action that checks preconditions
        shift_coordinates = (x-3.5,y-0,z-2)

        # set attributes
        self.name = "letter"
        self.shift_coordinates = shift_coordinates
        self.text = text
        self.choices = choices
        self.unique_id = unique_id
        self.check_action = check_action
        self.speech_bubble = SpeechBubble([text],choices,
                                          evaluate_choices_callback=
                                          ContextManager().get_action_manager().evaluate_choices)
        self.canvas = canvas
        self.action_sequence = action_sequence
        self.coordinates = [
            ["#F5F2EB", (3.5, 0, 2), (3.7, 0, 2), (3.7, 0, 1.8), (3.5, 0, 1.8)],
            ["#F5F2EB", (3.5, 0, 2), (3.6, 0, 1.86), (3.7, 0, 2)]
        ]
        self.coordinates_stamp = [
            [3.6, 0, 1.86, 0.015, "#B02525", 0, 360]
            ]

    # class method create has to be used to create objects, if based on preconditions
    @classmethod
    def create(cls, room_data, index, canvas):
        room_state = ContextManager().get_room_state()
        unique_id = room_data["letter"][index][1] 
        if room_state.object_is_removed("letter",unique_id):
            return None
        check_action = room_data["letter"][index][4] # get action that checks preconditions
        if check_action == None:
            return cls(room_data, index, canvas)
        create_allowed = ContextManager().get_action_manager().execute_action_sequence(check_action)
        if create_allowed:
            return cls(room_data, index, canvas)
        else:
            return None # check failed => forbid creation
    
    def draw(self,canvas):
        graphics.draw(canvas,self.coordinates,tag=self.unique_id,object=self,shift_coordinates=self.shift_coordinates)
        graphics.draw_arc(canvas, *self.coordinates_stamp[0], tag=self.unique_id, shift_coordinates=self.shift_coordinates)

    def clicked(self,event,tag,object,canvas,world_coordinates,arc_coordinates):
        print("[DEBUG] Letter clicked!")
        self.speech_bubble.show_bubble(canvas,action_sequence=self.action_sequence)

    def delObject(self):
        self.canvas.delete(self.unique_id)    