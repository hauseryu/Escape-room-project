
import tkinter

from . import convert_3d_to_2d
from . import globals

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
        
        # create the canvas area and draw the room
        self.canvas_area.pack()
        self.draw_room()

    # draw the room using world coordinates
    def draw_room(self):
        self.coordinates = convert_3d_to_2d.convert_polygon_coordinates(self.room_coordinates)
        # draw the polygons on the canvas
        for polygon in self.coordinates:
            self.canvas_area.create_polygon(polygon[1:],width=1,fill=polygon[0],outline="black")
