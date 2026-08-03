
import tkinter
from pathlib import Path
import queue
import threading
import time
from tkinter import messagebox

# Jetzt findet Python die Datei "graphics.py" problemlos
from escape_room import globals
from escape_room import graphics
from escape_room import inventory
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
        self.gui_queue = queue.Queue() # communication for server events
        self.start_server = None
        self.player_name = None
        self.escape_server = EscapeServer()

        # create client network object and configure it
        # we pass the GUI queue so it can be written to by the network object
        self.game_client = EscapeClient(
            server_ip="127.0.0.1", 
            port=globals.SERVER_PORT, 
            player_name="", 
            gui_queue=self.gui_queue
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
        self.inventory = inventory.Inventory()
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
        if self.game_client.connect_and_start():
            print("client network connection started successfully.")
        else:
            print("Game could not be started due to failing connection.")
            messagebox.showerror("error", "connection to server failed.")
            raise RuntimeError("server connection failed")
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

    def handle_door_click(self, event):
        for door in self.doors:
            if door.handle_click(self.canvas_area, event):
                self.draw_room()
                break