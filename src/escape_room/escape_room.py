
import tkinter
from pathlib import Path


# Ermittelt den Ordner, in dem diese escape_room.py Datei liegt

# Fügt diesen Ordner zu den Python-Suchpfaden hinzu, falls er noch nicht drin ist

# Jetzt findet Python die Datei "graphics.py" problemlos
from escape_room import globals
from escape_room import graphics
from escape_room import inventory
from escape_room.objects.chair import Chair
from escape_room.objects.door import Door
from escape_room.objects.light import Light
from escape_room.objects.smallkey import Key
from escape_room.objects.table import Table
from escape_room.start_screen import StartScreen

IMAGE_DIR = Path(__file__).resolve().parent / "assets" / "images"
FLOOR_TEXTURE = IMAGE_DIR / "weathered_brown_planks1.jpg"
WALL_TEXTURE = IMAGE_DIR / "woodchip_texture.jpg"

class EscapeApp(tkinter.Frame):

    # create frame Objekt and drawing area (canvas)
    def __init__(self,master):
        super().__init__(master)
        self.coordinates = []
        self.pack()
        self.canvas_area = tkinter.Canvas(self,
                                          width=globals.canvas_width,
                                          height=globals.canvas_height)
        self.start_screen = StartScreen(self.canvas_area, self.start_game)
        
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
        
        # create the canvas area and draw the start screen
        self.canvas_area.pack()
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
        self.draw_room()

    # draw the room using world coordinates
    def draw_room(self):
        back_wall_coordinates = ["white", (0, 0, 4), (8, 0, 4), (8, 3, 4), (0, 3, 4)]

        graphics.draw_textured_polygon(self.canvas_area, self.room_coordinates[0], FLOOR_TEXTURE)
        if hasattr(self.canvas_area, "tk"):
            graphics.draw_textured_polygon(self.canvas_area, back_wall_coordinates, WALL_TEXTURE, "white")
        graphics.draw_textured_polygon(self.canvas_area, self.room_coordinates[1], WALL_TEXTURE, "white")
        graphics.draw_textured_polygon(self.canvas_area, self.room_coordinates[2], WALL_TEXTURE, "white")
        graphics.draw_textured_polygon(self.canvas_area, self.room_coordinates[3], WALL_TEXTURE, "white")
        for door in self.doors:
            door.draw(self.canvas_area, globals.canvas_width, globals.canvas_height)
        graphics.draw(self.canvas_area,self.light.coordinates_lampshade)
        graphics.draw_arc(self.canvas_area, 4, 2.5, 2, 0.1, "#FFF263", 180, 180)
        graphics.draw(self.canvas_area,self.table.coordinates_table)
        graphics.draw(self.canvas_area,self.chair.coordinates_chair)
        self.key.draw(self.canvas_area)
        self.inventory.draw(self.canvas_area)
