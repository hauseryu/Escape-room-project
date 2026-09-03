
import tkinter
from pathlib import Path
import queue
import os

from src.escape_room.gui_utilities import graphics
from src.escape_room.toolbar import inventory
from src.escape_room.toolbar import player_panel
from src.escape_room.toolbar import chat_panel
from src.escape_room.application import globals
from src.escape_room.room import room_data
from src.escape_room.room.room_state import RoomState
from src.escape_room.room.room_coordinates import room_coord

from escape_room.objects.chair import Chair
from escape_room.objects.door import Door
from escape_room.objects.light import Light
from escape_room.objects.key import Key
from escape_room.objects.table import Table
from escape_room.objects.wardrobe import Wardrobe
from escape_room.objects.picture import Picture
from escape_room.objects.bookshelf import Bookshelf
from escape_room.objects.safe import Safe
from escape_room.objects.letter import Letter
from escape_room.objects.clock import Clock
from src.escape_room.toolbar.menu import Menu
from src.escape_room.application.context_manager import ContextManager

IMAGE_DIR = ContextManager().get_image_path()
FLOOR_TEXTURE = IMAGE_DIR / "weathered_brown_planks1.jpg"
WALL_TEXTURE = IMAGE_DIR / "woodchip_texture.jpg"

class Room(tkinter.Frame):
    
    # create frame Objekt and drawing area (canvas)
    def __init__(self,master, escape_app):
        super().__init__(master)

        # set GUI master
        self.master = master
        self.escape_app = escape_app

        # multiplayer and data transfer related coding
        # using queues, which are thread-safe (no danger of different threads accessing same queue)
        self.network_queue = queue.Queue() # communication for server events
        self.icon_queue = queue.Queue() # communication for icon events     
        self.chat_queue = queue.Queue() # communication of chat messages

        # bind network events to a processing event handler
        master.bind("<<NetworkEvent>>", self.on_network_event)
        master.bind("<<IconEvent>>", self.on_icon_event)
        master.bind("<<ChatEvent>>", self.on_message_event)
        self.goto_next_room = False

        # UI-related coding
        self.canvas_area = tkinter.Canvas(self,
                                          width=globals.canvas_width,
                                          height=globals.canvas_height)
        ContextManager().set_canvas(self.canvas_area)
        self.canvas_area.pack()
        self.pack()
        # object-related coding
        self.room_state = RoomState()
        self.reset_objects()

    # reset objects to initial state
    def reset_objects(self):
        # object-related coding
        self.key = []
        self.bookshelf = []
        self.wardrobe = []
        self.chair = []
        self.table = []
        self.door = []
        self.light = []
        self.picture = []
        self.safe = []
        self.letter = []
        self.clock = []
        self.figure = []
        for door in self.door:
            door.is_open = False        

    # initialize room with all relevant settings
    def init_room(self,game_client,room_data = room_data.start_room,next_room=False):
        if not next_room:
            self.player_name = None
            self.player_icon_number = None
        self.game_client = game_client
        # get room data that determines the room layout + objects
        self.room_data = room_data
        # keep room state in own object
        self.room_state.add_room(self.room_data["room_name"])
        self.room_state.set_current_room(self.room_data["room_name"])
        ContextManager().set_room(self)
        if not next_room:
            self.next_room = None

        # UI-related coding
        self.coordinates = []
        
        # room coordinates in 3D space (x, y, z)
        room_coord_name = self.room_data["room_coordinates"]
        self.room_coordinates = room_coord[room_coord_name]
        self.image_path = ContextManager().get_image_path()
        if not next_room:
            self.inventory = inventory.Inventory()
        self.player_panel = player_panel.PlayerPanel(self.master, self.image_path,
                                                     icon_queue=self.icon_queue,
                                                     gui_master=self.master)
        self.chat_panel = chat_panel.ChatPanel(self.master, 
                                               message_queue=self.chat_queue,
                                               gui_master=self.master)
        self.menu = Menu(self, self.escape_app)

        # create doors
        for index,door in enumerate(self.room_data["door"]):
            coord = self.room_data["door"][index][0] # get door coordinates (first element in list)
            color = self.room_data["door"][index][1]
            direction = self.room_data["door"][index][2]
            tag = self.room_data["door"][index][3] # tags for door
            player_door = self.room_data["door"][index][4] # player doors can be opened with own key
            can_be_opened = self.room_data["door"][index][5] # door can be opened
            always_open = self.room_data["door"][index][6] # door is always open
            next_room = self.room_data["door"][index][7] # next room
            unique_id = self.room_data["door"][index][8] # unique identifier
            if direction == "front":
                shift_coord = (coord[0]-3.2,coord[1]-0,coord[2]-4)
            elif direction == "left":
                shift_coord = (coord[0]-0,coord[1]-0,coord[2]-1.5)
            elif direction == "right":
                shift_coord = (coord[0]-8,coord[1]-0,coord[2]-3.1)
            tag = self.room_data["door"][index][3]            
            obj = Door(coord,color,direction,tag,
                       next_room_callback=self.next_room_callback,player_name=self.player_name,
                       is_player_door=player_door,can_be_opened=can_be_opened,always_open=always_open,next_room=next_room,
                       room_state=self.room_state,unique_id=unique_id)
            self.canvas_area.tag_bind(tag, "<Button-1>", self.handle_door_click)
            # check for state if room is re-entered
            state = self.room_state.get_state_object("door",unique_id)
            if state=="OPEN":
                obj.is_open = True
            elif state=="CLOSED":
                obj.is_open = False
            self.door.append(obj)        
        # create lights
        for index,light in enumerate(self.room_data["light"]):
            coord = self.room_data["light"][index][0] # get light coordinates (first element in list)
            unique_id = self.room_data["light"][index][1] # unique id for the light
            shift_coord = (coord[0]-3.88,coord[1]-3.0,coord[2]-1.92)
            obj = Light(room_state=self.room_state,unique_id=unique_id,shift_coordinates=shift_coord)
            # check for state if room is re-entered
            state = self.room_state.get_state_object("light",unique_id)
            if state!=None:
                obj.state = state
            self.light.append(obj)
        # create tables 
        for index,table in enumerate(self.room_data["table"]):
            coord = self.room_data["table"][index][0] # get table coordinates (first element in list)
            shift_coord = (coord[0]-7.55,coord[1]-0.67,coord[2]-3.75)
            obj = Table(shift_coordinates=shift_coord)
            self.table.append(obj)
        # create chairs
        for index,chair in enumerate(self.room_data["chair"]):
            coord = self.room_data["chair"][index][0] # get chair coordinates (first element in list)
            direction = self.room_data["chair"][index][1] # get chair direction (right/left)
            shift_coord = (coord[0]-5.00,coord[1]-0,coord[2]-2.35) 
            obj = Chair(coord[0],coord[1],coord[2],direction,shift_coordinates=shift_coord)
            # obj = Chair(direction,shift_coordinates=shift_coord)
            self.chair.append(obj)        
        # create keys
        for index,key in enumerate(self.room_data["key"]):
            coord = self.room_data["key"][index][0] # get key coordinates (first element in list)
            unique_id = self.room_data["key"][index][1] # unique identifier for the key
            if self.room_state.object_is_removed("key",unique_id):
                continue
            shift_coord = (coord[0]-6.5,coord[1]-0.78,coord[2]-3.0)
            obj = Key(self.inventory,self.room_state,
                      shift_coordinates=shift_coord,unique_id=unique_id,room_placement=True)
            self.key.append(obj)
        #create safes
        for index,safe in enumerate(self.room_data["safe"]):
            coord = self.room_data["safe"][index][0] # get safe coordinates (first element in list)
            shift_coord = (coord[0]-5.0,coord[1]-1.0,coord[2]-4.0)       
            unique_id = self.room_data["safe"][index][2]
            safe_created = False
            if(self.room_data["safe"][index][1]!=""):
                for key in self.key:
                    if key.unique_id == self.room_data["safe"][index][1]:
                        obj = Safe(key, shift_coordinates=shift_coord,
                                   room_state=self.room_state,unique_id=unique_id)
                        safe_created = True
            if not safe_created:
                obj = Safe(None, shift_coordinates=shift_coord,
                           room_state=self.room_state,unique_id=unique_id)
            # check for state if room is re-entered
            state = self.room_state.get_state_object("safe",unique_id)
            if state=="OPEN":
                obj.state = 1
            else:
                obj.state = 0
            self.safe.append(obj)
        # create pictures
        for index,picture in enumerate(self.room_data["picture"]):
            coord = self.room_data["picture"][index][0] # get wardrobe coordinates (first element in list)
            file_name = self.room_data["picture"][index][1] 
            is_riddle = self.room_data["picture"][index][2]
            direction = self.room_data["picture"][index][3]
            unique_id = self.room_data["picture"][index][4] # unique identifier
            shift_coord = (coord[0]-5.05,coord[1]-2.35,coord[2]-4.0)            
            obj = Picture(IMAGE_DIR / file_name,shift_coordinates=shift_coord,
                          is_riddle=is_riddle, direction=direction, unique_id=unique_id, room_state=self.room_state)
            self.picture.append(obj)
        # create bookshelves
        for index,bookshelf in enumerate(self.room_data["bookshelf"]):
            coord = self.room_data["bookshelf"][index][0] # get bookshelf coordinates (first element in list)
            shift_coord = (coord[0]-0,coord[1]-0,coord[2]-4)
            obj = Bookshelf(shift_coordinates=shift_coord)
            self.bookshelf.append(obj)
        # create wardrobes
        for index,wardrobe in enumerate(self.room_data["wardrobe"]):
            coord = self.room_data["wardrobe"][index][0] # get wardrobe coordinates (first element in list)
            direction = self.room_data["wardrobe"][index][1] # get wardrobe direction (right/left)
            unique_id = self.room_data["wardrobe"][index][2] # unique identifier
            shift_coord = (coord[0]-0,coord[1]-0,coord[2]-4)
            obj = Wardrobe(direction,shift_coordinates=shift_coord,
                           room_state=self.room_state,unique_id=unique_id)
            # check for state if room is re-entered
            state = self.room_state.get_state_object("wardrobe",unique_id)
            if state==1:
                obj.state = 1
            else:
                obj.state = 0
            self.wardrobe.append(obj)
        # create clocks
        for index,clock in enumerate(self.room_data["clock"]):
            coord = self.room_data["clock"][index][0] # get clock coordinates (first element in list)
            shift_coord = (coord[0]-5.15,coord[1]-0.42,coord[2]-4.00)
            obj = Clock(self.canvas_area, time=1, shift_coordinates=shift_coord)
            self.clock.append(obj)
        ContextManager().set_clock(self.clock)
        # create letters
        for index,letter in enumerate(self.room_data["letter"]):
            coord = self.room_data["letter"][index][0] # get letter coordinates (first element in list)
            text = self.room_data["letter"][index][1] # get letter text
            choices = self.room_data["letter"][index][2] # get choices for letter
            shift_coord = (coord[0]-3.5,coord[1]-0,coord[2]-2)
            obj = Letter(self.canvas_area,shift_coordinates=shift_coord,text=text,choices=choices)
            self.letter.append(obj)

        # create the canvas area and draw the start screen
        self.canvas_area.pack()        

    def update_player_data(self,player_name,player_icon_number):
        # player name + icon
        self.player_name = player_name
        self.player_icon_number = player_icon_number
        # inform chat panel
        self.chat_panel.player_name = player_name
        # set ownership of key
        for key in self.key:
            key.object_owner = self.player_name
        for door in self.door:
            door.player_name = self.player_name

    # draw the room using world coordinates
    def draw_room(self):

        # draw room layout
        shift_coord = graphics.shift_coordinates(self.room_coordinates[0][1],self.room_data["room"])
        for polygon in self.room_coordinates:
            # in case a tuple defines multiple attributes....
            if type(polygon[0]) == tuple:
                (color,texture) = polygon[0]
            else:
                color = polygon[0]
                texture = WALL_TEXTURE # use wall texture as default
            # draw the floor and walls with textures
            graphics.draw_textured_polygon(self.canvas_area, polygon, texture, color,
                                        shift_coordinates=shift_coord)

        # draw the doors
        for index,door in enumerate(self.door):
            door.draw(self.canvas_area, globals.canvas_width, globals.canvas_height)
        
        # draw the lights
        for light in self.light:
            graphics.draw(self.canvas_area,light.coordinates_lampshade,shift_coordinates=light.shift_coordinates)
            if light.state == 0 or light.state == -1:
                graphics.draw(self.canvas_area,light.coordinates_light_switch_off,tag="light_switch",object=light,
                            arc_coordinates=light.arc_coordinates,
                            shift_coordinates=light.shift_coordinates)
                graphics.draw_arc(self.canvas_area, *light.arc_coordinates[0], tag="light_bulb",
                                  shift_coordinates=light.shift_coordinates)
            elif light.state == 1:
                graphics.draw(self.canvas_area,light.coordinates_light_switch_on,tag="light_switch",object=light,
                            arc_coordinates=light.arc_coordinates,
                            shift_coordinates=light.shift_coordinates)
                graphics.draw_arc(self.canvas_area, *light.arc_coordinates[1], tag="light_bulb",
                                  shift_coordinates=light.shift_coordinates)
                graphics.draw_arc(self.canvas_area, *light.arc_coordinates[2], tag="light_shine",
                                  shift_coordinates=light.shift_coordinates)
        
        # draw the pictures
        for picture in self.picture:
            graphics.draw(self.canvas_area,picture.coordinates_frame,shift_coordinates=picture.shift_coordinates)
            graphics.draw(self.canvas_area,picture.coordinates_image,tag="picture",
                          shift_coordinates=picture.shift_coordinates)
            picture.draw_image(self.canvas_area, tag="picture")

        # draw the table
        for table in self.table:
            graphics.draw(self.canvas_area,table.coordinates_table,shift_coordinates=table.shift_coordinates)

        # draw the chair
        for chair in self.chair:
            graphics.draw(self.canvas_area,chair.coordinates_chair,shift_coordinates=chair.shift_coordinates)

        # draw the bookshelves
        for bookshelf in self.bookshelf:
            graphics.draw(self.canvas_area,bookshelf.coordinates_shelf,
                          shift_coordinates=bookshelf.shift_coordinates)
            graphics.draw(self.canvas_area,bookshelf.coordinates_books,
                          shift_coordinates=bookshelf.shift_coordinates)
            bookshelf.draw_titles(self.canvas_area, globals.canvas_width, globals.canvas_height)
        # draw the wardrobes
        for wardrobe in self.wardrobe:
            if wardrobe.state == 0:
                graphics.draw(self.canvas_area,wardrobe.wardrobe_coordinates, tag="wardrobe", object=wardrobe,
                            shift_coordinates=wardrobe.shift_coordinates)
                graphics.draw_arc(self.canvas_area, *wardrobe.wardrobe_coordinates_knobes[0], tag="wardrobe", 
                                shift_coordinates=wardrobe.shift_coordinates)
                graphics.draw_arc(self.canvas_area, *wardrobe.wardrobe_coordinates_knobes[1], tag="wardrobe", 
                                shift_coordinates=wardrobe.shift_coordinates)
            elif wardrobe.state == 1:
                graphics.draw(self.canvas_area,wardrobe.wardrobe_coordinates_open, tag="wardrobe", object=wardrobe,
                            shift_coordinates=wardrobe.shift_coordinates)
                graphics.draw_arc(self.canvas_area, *wardrobe.wardrobe_coordinates_knobes_open[0], tag="wardrobe", 
                                shift_coordinates=wardrobe.shift_coordinates)
                graphics.draw_arc(self.canvas_area, *wardrobe.wardrobe_coordinates_knobes_open[1], tag="wardrobe", 
                                shift_coordinates=wardrobe.shift_coordinates)

        # draw the safes
        for safe in self.safe:
            if safe.state == 0:
                safe.set_password(picture.correct_answers)
                graphics.draw(self.canvas_area, safe.safe_coordinates, tag = "safe", object = safe, shift_coordinates=safe.shift_coordinates)    
            elif safe.state == 1:
                graphics.draw(self.canvas_area, safe.safe_coordinates_open, tag = "safe", object = safe, shift_coordinates=safe.shift_coordinates)

        # draw the clocks
        for clock in self.clock:
            graphics.draw(self.canvas_area, clock.coordinates, tag="clock", object=clock, shift_coordinates=clock.shift_coordinates)
            graphics.draw(self.canvas_area, clock.coordinates_clock_hands, tag="clock", object=clock, shift_coordinates=clock.shift_coordinates)

        # draw the letter
        for letter in self.letter:
            graphics.draw(self.canvas_area,letter.coordinates,tag="letter",object=letter,shift_coordinates=letter.shift_coordinates)
            graphics.draw_arc(self.canvas_area, *letter.coordinates_stamp[0], tag="letter", shift_coordinates=letter.shift_coordinates)

        # draw the key and inventory
        self.inventory.draw(self.canvas_area)
        draw_key = True
        for key in self.key:
            for safe in self.safe:
                if (key.unique_id == safe.key.unique_id and safe.state == 1):
                    key.draw(self.canvas_area)
                elif (key.unique_id == safe.key.unique_id and safe.state == 0):
                    draw_key = False
            if draw_key:
                key.draw(self.canvas_area) 
            draw_key = True

        # draw the figures (persons etc.)
        for figure in self.figure:
            picture.draw_image(self.canvas_area, tag="figure")

        # draw player frame
        self.panel_canvas_id = self.canvas_area.create_window(
            355, 1,                   # X and Y coordinates inside the canvas
            window=self.player_panel,  # The frame object to embed
            anchor="nw",               # Top-left corner alignment
            width=900,                 # Optional: Explicitly force width
            height=202                 # Optional: Explicitly force height
        )        
        self.player_panel.update_current_player(self.player_name, 
                                                globals.icon_mapping.get(self.player_icon_number, "playerpic_running_man.png"))
        # draw chat frame
        self.chat_panel_canvas_id = self.canvas_area.create_window(
            355+900, 1,                   # X and Y coordinates inside the canvas
            window=self.chat_panel,  # The frame object to embed
            anchor="nw",               # Top-left corner alignment
            width=600,                 # Optional: Explicitly force width
            height=202                 # Optional: Explicitly force height
        )        
                # draw chat frame
        self.menu_canvas_id = self.canvas_area.create_window(
            355+900+600, 1,                   # X and Y coordinates inside the canvas
            window=self.menu,  # The frame object to embed
            anchor="nw",               # Top-left corner alignment
            width=150,                 # Optional: Explicitly force width
            height=202                 # Optional: Explicitly force height
        )     
        
        
    def handle_door_click(self, event):
        for door in self.door:
            if door.handle_click(self.canvas_area, event, self.inventory.getSelectedObject()):
                self.draw_room()
                if self.goto_next_room:
                    self.canvas_area.after(1000, self.execute_room_switch) # wait 1 second before entering next room...
                break

    def next_room_callback(self,next_room):
        self.goto_next_room = True
        self.next_room = next_room

    def execute_room_switch(self):
        print("[GAME]: room switch")
        self.goto_next_room = False # reset the room switch attribute
        self.canvas_area.delete("all")
        self.room_data = room_data.all_rooms[self.next_room]
        self.reset_objects()
        self.init_room(self.game_client,room_data=self.room_data,next_room=True)
        self.draw_room()

    def add_figure(self,figure):
        self.figure.append(figure)

    def on_network_event(self, event):
        """is called as soon as the network thread fires a signal."""

        # in case of normal GUI events, leave immediately
        if str(event.type) != "VirtualEvent" and str(event.type) != "35":
            return
        
        try:
            # as an event was triggered, there should be something in the queue
            while True:
                event_data = self.network_queue.get_nowait()
                if not isinstance(event_data, dict):
                    print(f"[WARNING] Alien objekt in network queue was ignored: {type(event_data)}")
                    continue  # jump to next element in queue       
                event_type = event_data.get("action")
                
                if event_type == "player_list":
                    players = event_data.get("players", [])
                    print(f"[GUI Event] event-based update of player list: {players}")
                    connected_players = [
                        {
                            "name": player["name"], 
                            # .get() sorgt für ein Fallback-Bild, falls eine unbekannte Nummer kommt
                            "icon": globals.icon_mapping.get(player["icon"], "playerpic_running_man.png") 
                        } 
                        for player in players
                        if player["name"] != self.player_name
                    ]
                    self.player_panel.update_players_list(connected_players)
                    
                elif event_type == "inventory_received": 
                    inventory = event_data.get("inventory")
                    player = event_data.get("from")
                    owner = event_data.get("owner")
                    print(f"[GUI Event] event-based passing of inventory {inventory},",
                           f"owner {owner} from player {player}")
                    key = Key(self.inventory)
                    key.object_owner = owner
                    self.inventory.addObject("key",key.object_owner,key)
                    # draw the key and inventory
                    key.draw(self.canvas_area) # draw key into inventory

                elif event_type == "chat_message":
                    print("[GUI Event] received chat message")
                    text = event_data.get("text")
                    sent_from = event_data.get("sent_from")
                    self.chat_panel.append_message(sent_from,text)

        except queue.Empty:
            pass

    def on_icon_event(self, event):
        """is called when a player icon is clicked."""
        # as an event was triggered, there should be something in the queue
        event_data = self.icon_queue.get_nowait()
        event_type = event_data.get("action")
        (object,object_owner) = self.inventory.getSelectedObject()
        if object == None: # if nothing is selected, we quit
            return
        if event_type == "send_inventory":
            inventory = event_data.get("inventory")
            player = event_data.get("player_name")
            print(f"[GUI Event] received send_inventory event for inventory {inventory},",
                   f"owner {object_owner} for player {player}")
            self.game_client.send_action(event_type,player,inventory,object_owner)
            # remove key image from canvas
            self.inventory.remove_inventory_pictures()
            # remove from inventory
            self.inventory.delObject(object,object_owner)
            self.inventory.redraw_inventory()

    def on_message_event(self, event):
        """Event handler triggered automatically when a new chat item lands in the queue."""
        print("[ROOM] <<ChatEvent>> received! Processing queue items...")
        
        # Empty the queue safely using block=False
        while True:
            try:
                next_chat_payload = self.chat_queue.get(block=False)
                
                # Forward to your network EscapeClient
                print(f"[ROOM] Forwarding payload to client: {next_chat_payload}")
                self.game_client.send_action(action_type="chat_message", json_payload=next_chat_payload)
                
                self.chat_queue.task_done()
                
            except queue.Empty:
                # Break out when the queue is completely empty
                break

