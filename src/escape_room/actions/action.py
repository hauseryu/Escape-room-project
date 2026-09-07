from src.escape_room.application.context_manager import ContextManager
from src.escape_room.objects.clock import Clock
from src.escape_room.objects.figure import Figure
from src.escape_room.gui_utilities.speech_bubble import SpeechBubble
from src.llm.dialog import Dialog

# specific actions
def game_over():
    print("[DEBUG] Game over!")
    pass

ELAPSE_TIME = 1500
def time_elapse(time):
    print(f"[DEBUG] Time elapses: {time} hours.")    
    clock = ContextManager().get_clock()
    canvas = ContextManager().get_canvas()
    counter = time
    if clock != None and canvas != None and counter>0:
        canvas.after(ELAPSE_TIME,time_elapse_callback,counter-1,clock,canvas)
    else:
        ContextManager().get_action_manager().execute_next_action()

def figure_appears(figure,image_name,x_xoord,y_coord,width,height,figure_talk):
    print(f"[DEBUG] Person appears: {figure}")
    image = ContextManager().get_image_path() / image_name
    figure = Figure(figure,image,x_xoord,y_coord,width,height,figure_talk)
    ContextManager().get_room().add_figure(figure)
    figure.draw_image(ContextManager().get_canvas())
    ContextManager().get_action_manager().execute_next_action()

def figure_talks(figure,speech,figure_id,player_role):
    print(f"[DEBUG] Person talks: {figure}")
    speech_bubble = SpeechBubble([speech])  # ([speech])
    speech_bubble.show_bubble(ContextManager().get_canvas(),"top")
    speech_bubble2 = SpeechBubble(["You:"])
    bubble_entry = speech_bubble2.show_bubble(ContextManager().get_canvas(),"bottom",skip_overlay=True,entry_field=True)
    bubble_entry.bind("<Return>", lambda event: process_entry(event, bubble_entry, speech_bubble, figure, figure_id, player_role))
    # ContextManager().get_action_manager().execute_next_action()

def process_entry(event, bubble_entry, speech_bubble, figure, figure_id, player_role):
    if not hasattr(process_entry, "dialog"):
        process_entry.dialog = Dialog()
    dialog = process_entry.dialog
    player_message = event.widget.get()
    event.widget.delete(0, len(event.widget.get()))
    npc_response = dialog.talk_with_npc(figure_id, player_role, player_message)
    figure_talks(figure, npc_response, figure_id, player_role)

# helper functions
def time_elapse_callback(counter,clock,canvas):
    # push clock forward
    for clck in clock:
        clck.draw_delete()
        current_time = clck.get_time()
        clck.set_time(current_time+1)
        clck.draw()
    if counter>0:
        canvas.after(ELAPSE_TIME,time_elapse_callback,counter-1,clock,canvas)
    else:
        ContextManager().get_action_manager().execute_next_action()

# action evaluation
class ActionManager():
    def __init__(self):
        self.action_sequence = []

    def evaluate_choices(self,choices,choice):
        print(f"[DEBUG] Evaluate choice {choice}")
        self.action_sequence = choices[choice][1]
        self.execute_next_action()

    def execute_action_sequence(self,action_sequence):
        print(f"[DEBUG] Execute action sequence {action_sequence}")
        self.action_sequence = action_sequence
        self.execute_next_action()

    def execute_next_action(self):
        if self.action_sequence == []:
            print("[DEBUG] action sequence processing completed.")
            return
        action = self.action_sequence.pop(0) # get first element from list
        action[0](*action[1:]) # call action with unknown number of parameters
