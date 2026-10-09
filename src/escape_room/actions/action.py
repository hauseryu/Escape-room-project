from src.escape_room.application.context_manager import ContextManager
from src.escape_room.application.game_over_screen import GameOverScreen
from src.escape_room.application.start_screen import StartScreen
from src.escape_room.objects.clock import Clock
from escape_room.objects.letter import Letter
from src.escape_room.objects.inventory_item import InventoryItem
from src.escape_room.objects.figure import Figure
from src.escape_room.gui_utilities.speech_bubble import SpeechBubble
from src.chatbot.dialog import Dialog
import winsound

# specific actions
def game_over(action_mgr):
    canvas = ContextManager().get_canvas()
    game_over_screen = GameOverScreen(canvas,None,None)
    game_over_screen.draw()
    print("[DEBUG] Game over!")

ELAPSE_TIME = 1500
def time_elapse(action_mgr,time,sound=None):
    print(f"[DEBUG] Time elapses: {time} hours.")    
    clock = ContextManager().get_clock()
    canvas = ContextManager().get_canvas()
    counter = time
    if clock != None and canvas != None and counter>0:
        canvas.after(ELAPSE_TIME,time_elapse_callback,action_mgr,counter-1,clock,canvas,sound)
    else:
        action_mgr.execute_next_action()

def figure_appears(action_mgr,figure,image_name,x_xoord,y_coord,width,height,
                   action_sequence_talk=None,action_sequence_generic=None):
    print(f"[DEBUG] Person appears: {figure}")
    image = ContextManager().get_image_path() / image_name
    figure = Figure(figure,image,x_xoord,y_coord,width,height,action_sequence_talk,action_sequence_generic)
    ContextManager().get_room().add_figure(figure)
    figure.draw_image(ContextManager().get_canvas())
    action_mgr.execute_next_action()

def figure_disappears(action_mgr,figure):
    print(f"[DEBUG] Person disappears: {figure}")
    obj = ContextManager().get_room().get_figure(figure)
    obj.remove_image(ContextManager().get_canvas())
    ContextManager().get_room().remove_figure(figure)
    action_mgr.execute_next_action()
                   
def figure_talks(action_mgr,figure,speech,figure_id,player_role,button_text="End Dialog",entry_field=True):
    print(f"[DEBUG] Person talks: {figure}")
    speech_bubble = SpeechBubble([speech]) 
    speech_bubble.show_bubble(ContextManager().get_canvas(),"top")
    bubble_entry=None
    if entry_field:
        speech_bubble2 = SpeechBubble(["You:"])
        bubble_entry = speech_bubble2.show_bubble(ContextManager().get_canvas(),skip_overlay=True,
                                                entry_field=entry_field,position="bottom",
                                                button_text=button_text,action_data="sherlock_client_disappears")
    if bubble_entry!=None:
        bubble_entry.bind("<Return>", lambda event: process_entry(action_mgr,event, bubble_entry, speech_bubble, 
                                                                  figure, figure_id, player_role))

def letter_appears(action_mgr,unique_id,action_sequence=None):
    print(f"[DEBUG] Letter appears: {unique_id}")
    room = ContextManager().get_room()
    room_data = room.room_data
    obj = None
    canvas = ContextManager().get_canvas()
    for index,letter in enumerate(room_data["letter"]):
        if letter[1] == unique_id:
            obj = Letter(room_data,index,canvas,action_sequence=action_sequence)
            room.addObject(obj)
            break
    if obj != None:
        obj.draw(canvas)
    action_mgr.execute_next_action()

def remove_letter(action_mgr,unique_id):
    room = ContextManager().get_room()
    letter = room.get_letter(unique_id)
    letter.delObject()
    room.removeObject(letter)

def inventory_item_appears(action_mgr,name,unique_id,image,resize_room=None,resize_inventory=None):
    print(f"[DEBUG] Inventory item appears: {unique_id}")
    room_data = ContextManager().get_room().room_data
    player_name = ContextManager().get_player_name()
    obj = None
    canvas = ContextManager().get_canvas()
    inventory = ContextManager().get_inventory()
    room_state = ContextManager().get_room_state()
    for index,inventory_item in enumerate(room_data[name]):
        if inventory_item["unique_id"] == unique_id:
            obj = InventoryItem(name,room_data,index,image,inventory,room_state,
                                resize_room=resize_room,resize_inventory=resize_inventory)  
            obj.object_owner = player_name
    if obj != None:
        obj.draw(canvas)
    action_mgr.execute_next_action()

def put_item_in_inventory(action_mgr,name,unique_id, object_owner=None):
    inventory = ContextManager().get_inventory()
    room_state = ContextManager().get_room_state()
    canvas = ContextManager().get_canvas()
    if object_owner == None:
        object_owner = ContextManager().get_player_name()
    # select attributes depending on item type
    if name=="magnifier": 
        image="magnifier.png"
        obj = InventoryItem("magnifier",None,None,
                            image,inventory,room_state, unique_id=unique_id, 
                            object_owner = object_owner, resize_inventory=(100, 50))    
    if name=="key": 
        image="key_transparent.png"
        obj = InventoryItem("key",None,None,
                            image,inventory,room_state, unique_id=unique_id, 
                            sound="grab_key.wav", object_owner = object_owner, resize_inventory=(100, 50)) 
    
    if name=="diamond": 
        image="diamond.png"
        obj = InventoryItem("diamond",None,None,
                            image,inventory,room_state, unique_id=unique_id, 
                            object_owner = object_owner, 
                            resize_room=(30, 50), resize_inventory=(50, 70))  
    if name=="revolver": 
        image="revolver.png"
        obj = InventoryItem("revolver",None,None,
                            image,inventory,room_state, unique_id=unique_id, 
                            object_owner = object_owner, resize_inventory=(100, 50))
    if name=="water_glass": 
        image="water_glass.png"
        obj = InventoryItem("water_glass",None,None,
                            image,inventory,room_state, unique_id=unique_id, 
                            object_owner = object_owner, resize_room=(50, 100), 
                            resize_inventory=(40, 80))
        
    if name=="poker": 
        image="poker.png"
        obj = InventoryItem("poker",None,None,
                            image,inventory,room_state, unique_id=unique_id, 
                            object_owner = object_owner, resize_room=(70, 130), 
                            resize_inventory=(40, 80))    
    
    inventory.addObject(name,unique_id, object_owner,obj)
    obj.draw(canvas)
    action_mgr.execute_next_action()

def play_sound(action_mgr,sound):
    _play_sound(sound)
    action_mgr.execute_next_action()

def show_speechbubble(action_mgr,text):
    speech_bubble = SpeechBubble([text])
    canvas = ContextManager().get_canvas()
    speech_bubble.show_bubble(canvas,callback=show_speechbubble_callback,callback_arg=action_mgr)

def set_object_state(action_mgr,object,unique_id,value):
    room_state = ContextManager().get_room_state()
    room_state.set_state_object(object,unique_id,value)
    action_mgr.execute_next_action()

def stop_sequence_conditionally(action_mgr,*condition): # this stops the whole action sequence if the condition doesn't hold
    result = condition[0](action_mgr,*condition[1:])
    if result:
        action_mgr.execute_next_action()

def skip_actions_if_false(action_mgr,number=1,*condition):
    result = condition[0](action_mgr,*condition[1:])
    if not result:
        action_mgr.skip_actions(number)
    action_mgr.execute_next_action()

# helper functions
action_data_dictionary = None

def set_action_data_dict(action_data_dict):
    global action_data_dictionary
    action_data_dictionary = action_data_dict

def process_entry(action_mgr,event, bubble_entry, speech_bubble, figure, figure_id, player_role):
    if not hasattr(process_entry, "dialog"):
        process_entry.dialog = Dialog()
    dialog = process_entry.dialog
    player_message = event.widget.get()
    event.widget.delete(0, len(event.widget.get()))
    npc_response = dialog.talk_with_npc(figure_id, player_role, player_message)
    figure_talks(action_mgr,figure, npc_response, figure_id, player_role)

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

def time_elapse_callback(action_mgr,counter,clock,canvas,sound):
    # push clock forward
    for clck in clock:
        clck.draw_delete()
        current_time = clck.get_time()
        clck.set_time(current_time+1)
        clck.draw()
        _play_sound(sound)
    if counter>0:
        canvas.after(ELAPSE_TIME,time_elapse_callback,action_mgr,counter-1,clock,canvas,sound)
    else:
        action_mgr.execute_next_action()

def show_speechbubble_callback(action_mgr):
    action_mgr.execute_next_action()

# check actions (return a boolean value which can be evaluated by caller)
def check_figure_in_room(action_mgr,figure_name):
    figure = ContextManager().get_room().get_figure(figure_name)
    if figure==None:
        return False
    else:
        return True

def check_figure_not_yet_in_room(action_mgr,figure_name):
    state = ContextManager().get_room_state().get_object_state("figure",figure_name)
    if state=="not_in_room":
        return True
    else:
        return False
    
def check_object_state(action_mgr,object,unique_id,value):
    room_state = ContextManager().get_room_state()
    state = room_state.get_state_object(object,unique_id)
    return state == value

def check_role(action_mgr,role):
    player_role = ContextManager().get_role()
    return player_role == role

def check_is_selected_inventory(action_mgr,name,unique_id):
    inv = ContextManager().get_inventory()
    player = ContextManager().get_player_name()
    return inv.objectIsSelected(name,unique_id,player)
    
# factory to create manager instances
def action_mgr_create():
    return ActionManager()

# action evaluation
class ActionManager():

    def __init__(self):
        self.action_sequence = []

    def evaluate_choices(self,choices,choice):
        print(f"[DEBUG] Evaluate choice {choice}")
        self.action_sequence = action_data_dictionary[choices[choice][1]] 
        self.execute_next_action()

    def execute_action_sequence(self,action_sequence):
        print(f"[DEBUG] Execute action sequence {action_sequence}")
        act_sequence = action_data_dictionary[action_sequence] 
        self.action_sequence = act_sequence.copy()
        return self.execute_next_action()

    def execute_next_action(self):
        if self.action_sequence == []:
            print("[DEBUG] action sequence processing completed.")
            return
        action = self.action_sequence.pop(0) # get first element from list
        return action[0](self,*action[1:]) # call action with unknown number of parameters

    def skip_actions(self,number):
        for counter in range(number):
            self.action_sequence.pop(0)
