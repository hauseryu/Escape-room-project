from escape_room import globals

# Ermittelt den Ordner, in dem diese escape_room.py Datei liegt

# Fügt diesen Ordner zu den Python-Suchpfaden hinzu, falls er noch nicht drin ist


# convert 3D coordinates to 2D coordinates
def compute_2d_coordinates(x, y, z, win_width,win_height):
    y = -2*y+3
    x_2d = (450*(x-4))/(z+1)+(win_width/2)
    y_2d = (450*(y))/(z+1)+(win_height/2)
    
    return (x_2d, y_2d)

# convert from world to pixel coordinates
# passed argument world_coordinates: list of polygons, each polygon = list of points, each point = (x,y,z)
def convert_polygon_coordinates(world_coordinates):
    coordinates = []
    
    # iterate through the list of polygons and convert each point to 2D coordinates
    for polygon in world_coordinates:
        poly = []            
        for index,point in enumerate(polygon):
            if index == 0:
                poly.append(point)
            else:
                (x,y,z) = point
                (coord_x,coord_y) = compute_2d_coordinates(x,y,z,globals.canvas_width,globals.canvas_height)
                poly.append([coord_x])
                poly.append([coord_y])
        coordinates.append(poly)

    # return list of polygons with 2D coordinates
    return coordinates

    # draw an object using world coordinates
def draw(canvas,world_coordinates): #tkinter.Canvas
    coordinates = convert_polygon_coordinates(world_coordinates)
    # draw the polygons on the canvas
    for polygon in coordinates:
        canvas.create_polygon(polygon[1:],width=1,fill=polygon[0],outline="black")

def draw_arc(canvas, x, y, z, radius, color, start, extent):
    (x0, y0) = compute_2d_coordinates(x - radius, y + radius, z, globals.canvas_width, globals.canvas_height)
    (x1, y1) = compute_2d_coordinates(x + radius, y - radius, z, globals.canvas_width, globals.canvas_height)
    canvas.create_arc(x0, y0, x1, y1, start=start, extent=extent, fill=color, outline="black")
