
import tkinter
from pathlib import Path
import queue
import threading
import time
import os
from tkinter import messagebox

# Jetzt findet Python die Datei "graphics.py" problemlos
from escape_room import globals
from escape_room import graphics
from escape_room import inventory
from escape_room import player_panel
from escape_room.escape_server import EscapeServer
from escape_room.escape_client import EscapeClient

from escape_room.objects.chair import Chair
from escape_room.objects.door import Door
from escape_room.objects.light import Light
from escape_room.objects.smallkey import Key
from escape_room.objects.table import Table
from escape_room.objects.wardrobe import Wardrobe
from escape_room.start_screen import StartScreen
from escape_room.objects.picture import Picture
from escape_room.objects.bookshelf import Bookshelf

IMAGE_DIR = Path(__file__).resolve().parent / "assets" / "images"
FLOOR_TEXTURE = IMAGE_DIR / "weathered_brown_planks1.jpg"
WALL_TEXTURE = IMAGE_DIR / "woodchip_texture.jpg"

class EscapeApp(tkinter.Frame):

    # create frame Objekt and drawing area (canvas)
    def __init__(self,master):
        super().__init__(master)

        # multiplayer and data transfer related coding
        self.network_queue = queue.Queue() # communication for server events
        self.icon_queue = queue.Queue() # communication for icon events
        # bind network events to a processing event handler
        master.bind("<<NetworkEvent>>", self.on_network_event)
        master.bind("<<IconEvent>>", self.on_icon_event)
        self.start_server = None
        self.player_name = None
        self.player_icon_number = None
        self.escape_server = EscapeServer()

        # create client network object and configure it
        # we pass the GUI queue so it can be written to by the network object
        self.game_client = EscapeClient(
            server_ip="127.0.0.1", 
            port=globals.SERVER_PORT, 
            player_name="", 
            player_icon_number=1, # set some default icon number
            network_queue=self.network_queue,
            gui_master=master
        )
        # now retrieve list of local devices
        found_devices = self.game_client.get_devices_local_network()
        self.server = self.game_client.check_server_port(found_devices,globals.SERVER_PORT)
        if self.server == None:
            print("no game server running.")
        else:
            print("server running on device: ",self.server)

        # UI-related coding
        self.coordinates = []
        self.pack()
        self.canvas_area = tkinter.Canvas(self,
                                          width=globals.canvas_width,
                                          height=globals.canvas_height)
        self.start_screen = StartScreen(self.canvas_area, self.start_game,self.server)
        
        # room coordinates in 3D space (x, y, z)
        self.room_coordinates = [["#8B4513",
                     (0,0,0), # front: corner left bottom (x/y/z coordinates)
                     (8,0,0), # front: corner right bottom
                     (8,0,4), # back: corner right bottom
                     (0,0,4)], # back: corner left bottom
                    ["white",
                     (0,3,0), # front: corner left top (x/y/z coordinates)
                     (8,3,0), # front: corner right top
                     (8,3,4), # back: corner right top
                     (0,3,4)], # back: corner left top                    
                    ["white",
                     (0,0,0), # wall left: corner left bottom (x/y/z coordinates)
                     (0,3,0), # wall left: corner left top
                     (0,3,4), # wall left: corner left top
                     (0,0,4)], # wall left: corner left bottom                    
                    ["white",
                     (8,0,0), # wall right: corner right bottom (x/y/z coordinates)
                     (8,3,0), # wall right: corner right top
                     (8,3,4), # wall right: corner right top
                     (8,0,4)] # wall right: corner right bottom                    
                     ]
        self.image_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "images",
        )
        self.inventory = inventory.Inventory()
        self.player_panel = player_panel.PlayerPanel(master, self.image_path,
                                                     icon_queue=self.icon_queue,
                                                     gui_master=master)
        # self.load_mock_game_state()
        self.doors = self.create_doors()
        self.light = Light()
        self.table = Table()
        self.chair = Chair(5.00, 2.35, "right")
        self.key = Key(self.inventory)
        self.wardrobe = Wardrobe()
        self.picture = Picture(IMAGE_DIR / "riddle_not_readable.png")
        self.bookshelf = Bookshelf()

        # create the canvas area and draw the start screen
        self.canvas_area.pack()
        
        self.canvas_area.bind("<Button-1>", self.handle_door_click)
        self.show_start_screen()

    def load_mock_game_state(self):
        # Setup Current Player
        self.player_panel.update_current_player("Alice (You)", "playerpic_woman_happy.png")

        # Setup List of Other Connected Network Players
        connected_players = [
            {"name": "Bob_The_Builder", "icon": "playerpic_running_man.png"},
            {"name": "Charlie_99", "icon": "playerpic_woman_thinking.png"},
            {"name": "DragonSlayer", "icon": "playerpic_wonder_woman.png"}
        ]
        self.player_panel.update_players_list(connected_players)

    def create_doors(self):
        return [
            Door(
                corners=[
                    (3.2, 2, 4),
                    (4.8, 2, 4),
                    (4.8, 0, 4),
                    (3.2, 0, 4),
                ],
                color = "red",
                tag="back_door",
            ),
            Door(
                corners=[
                    (0, 2, 2),
                    (0, 2, 3.2),
                    (0, 0, 3.2),
                    (0, 0, 2),
                ],
                tag="left_door",
            ),
            Door(
                corners=[
                    (8, 2, 3.2),
                    (8, 2, 2),
                    (8, 0, 2),
                    (8, 0, 3.2),
                ],
                color = "blue",
                tag="right_door",
            ),
        ]

    def show_start_screen(self):
        self.start_screen.draw()

    def start_game(self, event=None):
        self.canvas_area.delete("all")
        # get values from start screen fields
        self.player_name = self.start_screen.player_name.get()
        self.start_server = self.start_screen.server_var.get()
        self.player_icon_number = self.start_screen.player_icon_number
        # check if we have to start the server
        if self.start_server == 1:
            threading.Thread(target=self.escape_server.start_server, daemon=True).start()
        time.sleep(0.2) # give server object some time to start up....

        # start client connection
        if self.start_screen.server_use_var.get() == 1:
            self.game_client.server_ip = self.server    
        else:
            self.game_client.server_ip = "127.0.0.1"
        self.game_client.player_name = self.player_name
        self.game_client.player_icon_number = self.player_icon_number
        if self.game_client.connect_and_start():
            print("client network connection started successfully.")
        else:
            print("Game could not be started due to failing connection.")
            messagebox.showerror("error", "connection to server failed.")
            raise RuntimeError("server connection failed")
        # update of inventory 
        self.key.object_owner = self.player_name
        # create and show room 
        self.draw_room()

    # draw the room using world coordinates
    def draw_room(self):
        back_wall_coordinates = ["white", (0, 0, 4), (8, 0, 4), (8, 3, 4), (0, 3, 4)]

        # draw the floor and walls with textures
        graphics.draw_textured_polygon(self.canvas_area, self.room_coordinates[0], FLOOR_TEXTURE)
        if hasattr(self.canvas_area, "tk"):
            graphics.draw_textured_polygon(self.canvas_area, back_wall_coordinates, WALL_TEXTURE, "white")
        graphics.draw_textured_polygon(self.canvas_area, self.room_coordinates[1], WALL_TEXTURE, "white")
        graphics.draw_textured_polygon(self.canvas_area, self.room_coordinates[2], WALL_TEXTURE, "white")
        graphics.draw_textured_polygon(self.canvas_area, self.room_coordinates[3], WALL_TEXTURE, "white")
        
        # draw the doors
        for door in self.doors:
            door.draw(self.canvas_area, globals.canvas_width, globals.canvas_height)
        
        # draw the light
        graphics.draw(self.canvas_area,self.light.coordinates_lampshade)
        if self.light.state == 0 or self.light.state == -1:
            graphics.draw(self.canvas_area,self.light.coordinates_light_switch_off,tag="light_switch",object=self.light,
                          world_coordinates_changed=self.light.coordinates_light_switch_on,arc_coordinates=self.light.arc_coordinates)
            graphics.draw_arc(self.canvas_area, *self.light.arc_coordinates[0], tag="light_bulb")
        elif self.light.state == 1:
            graphics.draw(self.canvas_area,self.light.coordinates_light_switch_on,tag="light_switch",object=self.light,
                          world_coordinates_changed=self.light.coordinates_light_switch_off,arc_coordinates=self.light.arc_coordinates)
            graphics.draw_arc(self.canvas_area, *self.light.arc_coordinates[1], tag="light_bulb")
            graphics.draw_arc(self.canvas_area, *self.light.arc_coordinates[2], tag="light_shine")
        
        # draw the picture
        graphics.draw(self.canvas_area,self.picture.coordinates_frame)
        graphics.draw(self.canvas_area,self.picture.coordinates_image,tag="picture")
        self.picture.draw_image(self.canvas_area, tag="picture")

        # draw the table and chair
        graphics.draw(self.canvas_area,self.table.coordinates_table)
        graphics.draw(self.canvas_area,self.chair.coordinates_chair)
        
        # draw the wardrobe or bookshelf
        draw_choice = 1 # 0 = wardrobe, 1 = bookshelf
        if draw_choice == 0:
            graphics.draw(self.canvas_area,self.wardrobe.wardrobe_coordinates)
            graphics.draw_arc(self.canvas_area, *self.wardrobe.wardrobe_coordinates_knobes[0])
            graphics.draw_arc(self.canvas_area, *self.wardrobe.wardrobe_coordinates_knobes[1])
        elif draw_choice == 1:
            graphics.draw(self.canvas_area,self.bookshelf.coordinates_shelf)
            graphics.draw(self.canvas_area,self.bookshelf.coordinates_books)
            self.bookshelf.draw_titles(self.canvas_area, globals.canvas_width, globals.canvas_height)

        # draw the key and inventory
        self.inventory.draw(self.canvas_area)
        self.key.draw(self.canvas_area)

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
        
    def handle_door_click(self, event):
        for door in self.doors:
            if door.handle_click(self.canvas_area, event):
                self.draw_room()
                break

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
                    # self.inventory.draw(self.canvas_area)
                    key.draw(self.canvas_area) # draw key into inventory

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
            # remove from inventory
            self.inventory.delObject(object,object_owner)
            # remove key image from canvas
            if object == "key" and object_owner == self.key.object_owner:
                self.canvas_area.delete(self.key.object_id)
                self.canvas_area.delete(self.key.selection)
            else:
                obj = self.inventory.getObject(object,object_owner)
                if obj != None:
                    self.canvas_area.delete(obj.object_id)
                    self.canvas_area.delete(obj.selection)
            self.inventory.refresh_inventory()



