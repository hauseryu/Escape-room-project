from src.escape_room.application.context_manager import ContextManager
from src.escape_room.application.game_over_screen import GameOverScreen
from src.escape_room.application.start_screen import StartScreen
from src.escape_room.objects.clock import Clock
from escape_room.objects.letter import Letter
from src.escape_room.objects.inventory_item import InventoryItem
from src.escape_room.objects.figure import Figure
from src.escape_room.gui_utilities.speech_bubble import SpeechBubble
from src.escape_room.actions import action_data 
from src.llm.dialog import Dialog
import winsound

# specific actions
def game_over():
    canvas = ContextManager().get_canvas()
    game_over_screen = GameOverScreen(canvas,None,None)
    game_over_screen.draw()
    print("[DEBUG] Game over!")

ELAPSE_TIME = 1500
def time_elapse(time,sound=None):
    print(f"[DEBUG] Time elapses: {time} hours.")    
    clock = ContextManager().get_clock()
    canvas = ContextManager().get_canvas()
    counter = time
    if clock != None and canvas != None and counter>0:
        canvas.after(ELAPSE_TIME,time_elapse_callback,counter-1,clock,canvas,sound)
    else:
        ContextManager().get_action_manager().execute_next_action()

def figure_appears(figure,image_name,x_xoord,y_coord,width,height,figure_talk):
    print(f"[DEBUG] Person appears: {figure}")
    image = ContextManager().get_image_path() / image_name
    figure = Figure(figure,image,x_xoord,y_coord,width,height,figure_talk)
    ContextManager().get_room().add_figure(figure)
    figure.draw_image(ContextManager().get_canvas())
    ContextManager().get_action_manager().execute_next_action()

def figure_disappears(figure):
    print(f"[DEBUG] Person disappears: {figure}")
    obj = ContextManager().get_room().get_figure(figure)
    obj.remove_image(ContextManager().get_canvas())
    ContextManager().get_room().remove_figure(figure)
    ContextManager().get_action_manager().execute_next_action()
                   
def figure_talks(figure,speech,figure_id,player_role):
    print(f"[DEBUG] Person talks: {figure}")
    speech_bubble = SpeechBubble([speech])  # ([speech])
    speech_bubble.show_bubble(ContextManager().get_canvas(),"top")
    speech_bubble2 = SpeechBubble(["You:"])
    bubble_entry = speech_bubble2.show_bubble(ContextManager().get_canvas(),"bottom",skip_overlay=True,entry_field=True,
                                              button_text="End dialog",action_data=action_data.sherlock_client_disappears)
    bubble_entry.bind("<Return>", lambda event: process_entry(event, bubble_entry, speech_bubble, figure, figure_id, player_role))

def letter_appears(unique_id):
    print(f"[DEBUG] Inventory item appears: {unique_id}")
    room_data = ContextManager().get_room().room_data
    obj = None
    canvas = ContextManager().get_canvas()
    for index,letter in enumerate(room_data["letter"]):
        if letter[1] == unique_id:
            obj = Letter(room_data,index,canvas)    
    if obj != None:
        obj.draw(canvas)
    ContextManager().get_action_manager().execute_next_action()

def put_magnifier_in_inventory(unique_id):
    inventory = ContextManager().get_inventory()
    room_state = ContextManager().get_room_state()
    canvas = ContextManager().get_canvas()
    player_name = ContextManager().get_player_name()
    obj = InventoryItem("magnifier",None,None,
                        "magnifier.png",inventory,room_state, unique_identifier=unique_id, 
                        object_owner = player_name, resize_inventory=(100, 50))    
    inventory.addObject("magnifier",player_name,obj)
    obj.draw(canvas)
    ContextManager().get_action_manager().execute_next_action()

def process_entry(event, bubble_entry, speech_bubble, figure, figure_id, player_role):
    if not hasattr(process_entry, "dialog"):
        process_entry.dialog = Dialog()
    dialog = process_entry.dialog
    player_message = event.widget.get()
    event.widget.delete(0, len(event.widget.get()))
    npc_response = dialog.talk_with_npc(figure_id, player_role, player_message)
    figure_talks(figure, npc_response, figure_id, player_role)

def play_sound(sound):
    _play_sound(sound)
    ContextManager().get_action_manager().execute_next_action()

# helper functions
def _play_sound(sound):
    if sound==None:
        return
    sound_path=ContextManager.get_sound_path().joinpath(sound)
    try:
        winsound.PlaySound(
            sound_path,
            winsound.SND_FILENAME | winsound.SND_ASYNC,
        )
    except Exception as e:
        print(f"[DEBUG] Sound could not be played: {e}")

def time_elapse_callback(counter,clock,canvas,sound):
    # push clock forward
    for clck in clock:
        clck.draw_delete()
        current_time = clck.get_time()
        clck.set_time(current_time+1)
        clck.draw()
        _play_sound(sound)
    if counter>0:
        canvas.after(ELAPSE_TIME,time_elapse_callback,counter-1,clock,canvas,sound)
    else:
        ContextManager().get_action_manager().execute_next_action()

def show_speechbubble(text):
    speech_bubble = SpeechBubble([text])
    canvas = ContextManager().get_canvas()
    speech_bubble.show_bubble(canvas,callback=show_speechbubble_callback)

def show_speechbubble_callback():
    ContextManager().get_action_manager().execute_next_action()

# check actions (return a boolean value which can be evaluated by caller)
def check_figure_in_room(figure_name):
    figure = ContextManager().get_room().get_figure(figure_name)
    if figure==None:
        return False
    else:
        return True

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
        return self.execute_next_action()

    def execute_next_action(self):
        if self.action_sequence == []:
            print("[DEBUG] action sequence processing completed.")
            return
        action = self.action_sequence.pop(0) # get first element from list
        return action[0](*action[1:]) # call action with unknown number of parameters
