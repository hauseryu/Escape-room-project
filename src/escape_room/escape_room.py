
import tkinter

import os
import sys

# Ermittelt den Ordner, in dem diese escape_room.py Datei liegt
current_dir = os.path.dirname(os.path.abspath(__file__))

# Fügt diesen Ordner zu den Python-Suchpfaden hinzu, falls er noch nicht drin ist
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Jetzt findet Python die Datei "graphics.py" problemlos
import graphics
import globals
from .door import Door
import light

class EscapeApp(tkinter.Frame):

    # create frame Objekt and drawing area (canvas)
    def __init__(self,master):
        super().__init__(master)
        self.coordinates = []
        self.pack()
        self.canvas_area = tkinter.Canvas(self,
                                          width=globals.canvas_width,
                                          height=globals.canvas_height)
        
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
        self.doors = self.create_doors()
        self.light = light.Light()
        
        # create the canvas area and draw the room
        self.canvas_area.pack()
        self.draw_room()
        graphics.draw(self.canvas_area,self.light.coordinates_lampshade)
        graphics.draw_arc(self.canvas_area, 4, 2.5, 2, 0.1, "#FFF263", 180, 180)

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

    # draw the room using world coordinates
    def draw_room(self):        
        graphics.draw(self.canvas_area,self.room_coordinates)
        for door in self.doors:
            door.draw(self.canvas_area, globals.canvas_width, globals.canvas_height)
