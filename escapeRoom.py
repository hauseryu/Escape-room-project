
import convert_3d_to_2d
import globals
import tkinter

# define the room layout
room_width = 8 # 8m
room_height = 6 # 6m
room_coordinates = [["brown",
                     (-4,3,1), # front: corner left bottom (x/y/z coordinates)
                     (4,3,1), # front: corner right bottom
                     (4,3,4), # back: corner right bottom
                     (-4,3,4)], # back: corner left bottom
                    ["white",
                     (-4,-3,1), # front: corner left top (x/y/z coordinates)
                     (4,-3,1), # front: corner right top
                     (4,-3,4), # back: corner right top
                     (-4,-3,4)], # back: corner left top                    
                    ["white",
                     (-4,3,1), # wall left: corner left bottom (x/y/z coordinates)
                     (-4,-3,1), # wall left: corner left top
                     (-4,-3,4), # wall left: corner left top
                     (-4,3,4)], # wall left: corner left bottom                    
                    ["white",
                     (4,3,1), # wall right: corner right bottom (x/y/z coordinates)
                     (4,-3,1), # wall right: corner right top
                     (4,-3,4), # wall right: corner right top
                     (4,3,4)] # wall right: corner right bottom                    
                    ]

class EscapeApp(tkinter.Frame):

    # create frame Objekt and drawing area (canvas)
    def __init__(self,master):
        super().__init__(master)
        self.coordinates = []
        self.pack()
        self.canvas_area = tkinter.Canvas(self,
                                          width=globals.canvas_width,
                                          height=globals.canvas_height)
        self.canvas_area.pack()

        self.draw_room()

    # convert from world to pixel coordinates
    def convert_coordinates(self):
        for polygon in room_coordinates:
            poly = []            
            for index,point in enumerate(polygon):
                if index == 0:
                    poly.append(point)
                else:
                    (x,y,z) = point
                    (coord_x,coord_y) = convert_3d_to_2d.compute_2d_coordinates(x,y,z,globals.canvas_width,globals.canvas_height)
                    poly.append([coord_x])
                    poly.append([coord_y])
            self.coordinates.append(poly)

    # draw the room using world coordinates
    def draw_room(self):
        self.convert_coordinates()
        for polygon in self.coordinates:
            self.canvas_area.create_polygon(polygon[1:],width=1,fill=polygon[0],outline="black")
