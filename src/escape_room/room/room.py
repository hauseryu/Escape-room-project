
from ast import In
import tkinter
from pathlib import Path
import queue
import os
import random

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
from escape_room.objects.table import Table
from escape_room.objects.wardrobe import Wardrobe
from escape_room.objects.picture import Picture
from escape_room.objects.bookshelf import Bookshelf
from escape_room.objects.safe import Safe
from escape_room.objects.letter import Letter
from escape_room.objects.clock import Clock
from src.escape_room.objects.fireplace import Fireplace
from src.escape_room.objects.bench import Bench
from src.escape_room.objects.window import Window
from src.escape_room.objects.inventory_item import InventoryItem
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
        self.chat_panel = None
        self.player_panel = None
        self.canvas_area.pack()
        self.pack()
        # object-related coding
        self.room_state = RoomState()
        ContextManager().set_room_state(self.room_state)
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
        self.revolver = []
        self.bench = []
        self.fireplace = []
        self.magnifier = []
        self.water_glass = []
        self.window = []
        for door in self.door:
            door.is_open = False        

    # initialize room with all relevant settings
    def init_room(self,game_client,room_data = room_data.start_room,next_room=False):
        if not next_room:
            self.player_name = None
            self.player_icon_number = None
            self.role = ""
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
        if self.player_panel == None:
            self.player_panel = player_panel.PlayerPanel(self.master, self.image_path,
                                                        icon_queue=self.icon_queue,
                                                        gui_master=self.master)
        if self.chat_panel == None:
            self.chat_panel = chat_panel.ChatPanel(self.master, 
                                                message_queue=self.chat_queue,
                                                gui_master=self.master)
        self.menu = Menu(self, self.escape_app)

        # process roles
        try:
            # determine own role based on random
            roles = self.room_data["role"]
            free_roles = self.player_panel.get_free_roles(roles)
            number_roles = len(free_roles)
            random_role = random.randint(1,number_roles)
            self.role = free_roles[random_role-1]
            self.player_panel.update_current_player(self.player_name,
                                                    globals.icon_mapping.get(self.player_icon_number, "playerpic_running_man.png"),
                                                    self.role)
            self.game_client.role = self.role
            action_type = "update_player_list"
            self.game_client.send_action(action_type) # all players need to know the role assignment
        except: # in case no roles are defined for the room, just pass on
            pass

        # create doors
        for index,door in enumerate(self.room_data["door"]):
            obj = Door(room_data,index,
                       next_room_callback=self.next_room_callback,player_name=self.player_name,                       
                       room_state=self.room_state)
            self.door.append(obj)        
        # create lights
        for index,light in enumerate(self.room_data["light"]):
            obj = Light(self.room_data,index,room_state=self.room_state)
            self.light.append(obj)            
        # create windows
        for index,window in enumerate(self.room_data["window"]):
            coord = self.room_data["window"][index][0] # get window coordinates (first element in list)
            shift_coord = (coord[0]-0,coord[1]-1,coord[2]-1.8)
            obj = Window(shift_coordinates=shift_coord)
            self.window.append(obj)
        # create tables 
        for index,table in enumerate(self.room_data["table"]):
            obj = Table(room_data,index)
            self.table.append(obj)
        # create chairs
        for index,chair in enumerate(self.room_data["chair"]):
            obj = Chair(room_data,index)
            self.chair.append(obj)        
        # create keys
        for index,key in enumerate(self.room_data["key"]):        
            obj = InventoryItem.create("key",room_data,index,
                                "key_transparent.png",self.inventory,self.room_state)
            if obj!=None:
                self.key.append(obj)
        #create safes
        for index,safe in enumerate(self.room_data["safe"]):
            obj = Safe(room_data,index,self.room_state)
            self.safe.append(obj)
        # create pictures
        for index,picture in enumerate(self.room_data["picture"]):
            obj = Picture(room_data,index,IMAGE_DIR,self.room_state)
            self.picture.append(obj)
        # create bookshelves
        for index,bookshelf in enumerate(self.room_data["bookshelf"]):
            obj = Bookshelf(room_data,index)
            self.bookshelf.append(obj)
        # create wardrobes
        for index,wardrobe in enumerate(self.room_data["wardrobe"]):
            obj = Wardrobe(room_data,index,self.room_state)
            self.wardrobe.append(obj)
        # create clocks
        for index,clock in enumerate(self.room_data["clock"]):
            obj = Clock(room_data,index,self.canvas_area, time=1)
            self.clock.append(obj)
        ContextManager().set_clock(self.clock)
        # create fireplaces
        for index,fireplace in enumerate(self.room_data["fireplace"]):
            obj = Fireplace(room_data,index)
            self.fireplace.append(obj)
        # create letters
        for index,letter in enumerate(self.room_data["letter"]):
            obj = Letter(room_data,index,self.canvas_area)
            self.letter.append(obj)   
        # create revolver
        for index,revolver in enumerate(self.room_data["revolver"]):    
            obj = InventoryItem.create("revolver",room_data,index,
                                "revolver.png",self.inventory,self.room_state, resize_inventory=(50, 25))
            if obj!=None:
                self.revolver.append(obj)
        # create magnifier
        for index,magnifier in enumerate(self.room_data["magnifier"]):
            obj = InventoryItem.create("magnifier",room_data,index,
                                "magnifier.png",self.inventory,self.room_state, resize_inventory=(100, 50))
            if obj!=None:
                self.magnifier.append(obj)
        # create glass of water
        for index,water_glass in enumerate(self.room_data["water_glass"]):
            obj = InventoryItem.create("water_glass",room_data,index,
                                "water_glass.png",self.inventory,self.room_state, resize_room=(50, 100), resize_inventory=(40, 80))
            if obj!=None:
                self.water_glass.append(obj)
        # create benchs
        for index,bench in enumerate(self.room_data["bench"]):
            obj = Bench(room_data,index,self.canvas_area)
            self.bench.append(obj)

        # create figures
        # check for state if figure has appeared
        if self.figure == []:
            self.figure = self.room_state.get_objects("figure")
        # pass over player data to the room object
        self.update_player_data(self.player_name,self.player_icon_number)

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
        for magnifier in self.magnifier:
            magnifier.object_owner = self.player_name        
        for revolver in self.revolver:
            revolver.object_owner = self.player_name
        for water_glass in self.water_glass:
            water_glass.object_owner = self.player_name

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
            light.draw(self.canvas_area)
        
        # draw the windows
        for window in self.window:
            window_corners = []
            for sky_coordinate in window.sky_coordinates:
                (window_x, window_y, window_z) = sky_coordinate
                x_corner, y_corner = graphics.compute_2d_coordinates(window_x, window_y, window_z, globals.canvas_width, globals.canvas_height, window.shift_coordinates)
                window_corners.append((x_corner, y_corner))
            window.draw_sky(self.canvas_area, window_corners)
            graphics.draw(self.canvas_area,window.window_coordinates,shift_coordinates=window.shift_coordinates)

        # draw the pictures
        for picture in self.picture:
            picture.draw(self.canvas_area, tag="picture")

        # draw the fireplaces
        for fireplace in self.fireplace:
            fireplace.draw(self.canvas_area, self.inventory, self.player_name)

        # draw the chair
        for chair in self.chair:
            chair.draw(self.canvas_area)

        # draw the bookshelves
        for bookshelf in self.bookshelf:
            bookshelf.draw(self.canvas_area)
        
        # draw the wardrobes
        for wardrobe in self.wardrobe:
            wardrobe.draw(self.canvas_area)

        # draw the safes
        for safe in self.safe:
            safe.draw(self.canvas_area)

        # draw the clocks
        for clock in self.clock:
            clock.draw()

        # draw the table
        for table in self.table:
            table.draw(self.canvas_area)

        # draw the letter
        for letter in self.letter:
            letter.draw(self.canvas_area)

        # draw the key
        for key in self.key:
            key.draw(self.canvas_area)
            
        # draw the revolver
        for revolver in self.revolver:
            revolver.draw(self.canvas_area)
            
        # draw the magnifier
        for magnifier in self.magnifier:
            magnifier.draw(self.canvas_area)

        # draw the glass of water
        for water_glass in self.water_glass:
            water_glass.draw(self.canvas_area)

        # draw the benchs
        for bench in self.bench:
            bench.draw()

        # draw the figures (persons etc.)
        for figure in self.figure:
            figure.draw_image(self.canvas_area)

        # draw top bar (inventory, player panel etc.)
        self.draw_top_bar()

    def draw_top_bar(self):

        # draw the inventory
        self.inventory.draw(self.canvas_area)

        # draw player frame
        self.panel_canvas_id = self.canvas_area.create_window(
            355, 1,                   # X and Y coordinates inside the canvas
            window=self.player_panel,  # The frame object to embed
            anchor="nw",               # Top-left corner alignment
            width=900,                 # Optional: Explicitly force width
            height=202                 # Optional: Explicitly force height
        )        
        self.player_panel.update_current_player(self.player_name, 
                                                globals.icon_mapping.get(self.player_icon_number, "playerpic_running_man.png"),
                                                self.role)
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
        self.room_state.set_object("figure",figure)

    def remove_figure(self,figure_name):
        for index,figure in enumerate(self.figure):
            if figure.figure_name == figure_name:
                del self.figure[index]
                break

    def get_figure(self,figure_name):
        for figure in self.figure:
            if figure.figure_name == figure_name:
                return figure
        return None

    def removeObject(self,object):
        if object.name == "key":
            for index,key in enumerate(self.key):
                if key == object:
                    del self.key[index]
        if object.name == "revolver":
            for index,revolver in enumerate(self.revolver):
                if revolver == object:
                    del self.revolver[index]
        if object.name == "water_glass":
            for index,water_glass in enumerate(self.water_glass):
                if water_glass == object:
                    del self.water_glass[index]
        if object.name == "magnifier":
            for index,magnifier in enumerate(self.magnifier):
                if magnifier == object:
                    del self.magnifier[index]

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
                            "icon": globals.icon_mapping.get(player["icon"], "playerpic_running_man.png"), # 2nd option: fallback
                            "role": player["role"]
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
                    key = InventoryItem("key","key_transparent.png",self.inventory,self.room_state)
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

