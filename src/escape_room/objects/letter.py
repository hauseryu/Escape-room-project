from src.escape_room.gui_utilities.speech_bubble import SpeechBubble
from src.escape_room.application.context_manager import ContextManager
from src.escape_room.gui_utilities import graphics

class Letter():
    def __init__(self, room_data, index, canvas):

        # evaluate room data
        (x,y,z) = room_data["letter"][index][0] # get letter coordinates (first element in list)
        text = room_data["letter"][index][1] # get letter text
        choices = room_data["letter"][index][2] # get choices for letter
        shift_coordinates = (x-3.5,y-0,z-2)

        # set attributes
        self.shift_coordinates = shift_coordinates
        self.text = text
        self.choices = choices
        self.speech_bubble = SpeechBubble([text],choices,
                                          evaluate_choices_callback=
                                          ContextManager().get_action_manager().evaluate_choices)
        self.canvas = canvas
        self.coordinates = [
            ["#F5F2EB", (3.5, 0, 2), (3.7, 0, 2), (3.7, 0, 1.8), (3.5, 0, 1.8)],
            ["#F5F2EB", (3.5, 0, 2), (3.6, 0, 1.86), (3.7, 0, 2)]
        ]
        self.coordinates_stamp = [
            [3.6, 0, 1.86, 0.015, "#B02525", 0, 360]
            ]

    def draw(self,canvas):
        graphics.draw(canvas,self.coordinates,tag="letter",object=self,shift_coordinates=self.shift_coordinates)
        graphics.draw_arc(canvas, *self.coordinates_stamp[0], tag="letter", shift_coordinates=self.shift_coordinates)

    def clicked(self,event,tag,object,canvas,world_coordinates,arc_coordinates):
        print("[DEBUG] Letter clicked!")
        self.speech_bubble.show_bubble(canvas)


    