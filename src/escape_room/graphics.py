from escape_room import globals
from PIL import Image, ImageDraw, ImageTk

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
def draw(canvas,world_coordinates,tag=None,world_coordinates_changed=None,arc_coordinates=None): #tkinter.Canvas
    coordinates = convert_polygon_coordinates(world_coordinates)
    # draw the polygons on the canvas
    for polygon in coordinates:
        canvas.create_polygon(polygon[1:],width=1,fill=polygon[0],outline="black",tags=tag)
        if tag != None:
            canvas.tag_bind(tag,"<Button-1>",lambda event: clicked(event, tag, canvas, world_coordinates,world_coordinates_changed,arc_coordinates))

def draw_textured_polygon(canvas, polygon, texture_path, fallback_fill="#8B4513"):
    coordinates = convert_polygon_coordinates([polygon])[0]
    points = _flatten_points(coordinates[1:])

    canvas.create_polygon(points, width=1, fill=fallback_fill, outline="black")

    texture = Image.open(texture_path).convert("RGBA")
    tiled_texture = _tile_texture(texture, globals.canvas_width, globals.canvas_height)

    mask = Image.new("L", (globals.canvas_width, globals.canvas_height), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.polygon(points, fill=255)

    textured_polygon = Image.new("RGBA", (globals.canvas_width, globals.canvas_height), (0, 0, 0, 0))
    textured_polygon.paste(tiled_texture, (0, 0), mask)

    try:
        image = ImageTk.PhotoImage(textured_polygon, master=canvas)
    except (RuntimeError, AttributeError):
        return

    canvas.create_image(0, 0, anchor="nw", image=image)
    canvas.create_polygon(points, width=1, fill="", outline="black")

    if not hasattr(canvas, "_texture_images"):
        canvas._texture_images = []
    canvas._texture_images.append(image)

def _flatten_points(points):
    flattened_points = []
    for point in points:
        flattened_points.append(point[0])
    return flattened_points

def _tile_texture(texture, width, height):
    tiled_texture = Image.new("RGBA", (width, height))
    for x in range(0, width, texture.width):
        for y in range(0, height, texture.height):
            tiled_texture.paste(texture, (x, y))
    return tiled_texture

def draw_arc(canvas, x, y, z, radius, color, start, extent, tag=None):
    x_center, y_center = compute_2d_coordinates(x, y, z, globals.canvas_width, globals.canvas_height)
    radius = radius*165
    (x0, y0) = x_center - radius, y_center + radius
    (x1, y1) = x_center + radius, y_center - radius
    if start == 0 and extent == 360:
        canvas.create_oval(x0, y0, x1, y1, fill=color, outline="black", tags=tag)
    else:
        canvas.create_arc(x0, y0, x1, y1, start=start, extent=extent, fill=color, outline="black", tags=tag)

def clicked(event,tag,canvas,world_coordinates,world_coordinates_changed,arc_coordinates):
    if tag == "light_switch":
        if not hasattr(clicked, "count_light"):
            clicked.count_light = 0
        canvas.delete("light_switch")
        canvas.delete("light_bulb")
        if canvas.find_withtag("light_shine"):
            canvas.delete("light_shine")
        draw(canvas, world_coordinates_changed,tag=tag,world_coordinates_changed=world_coordinates,arc_coordinates=arc_coordinates)
        if clicked.count_light % 2 == 0:
            draw_arc(canvas, *arc_coordinates[1],tag="light_bulb")
            draw_arc(canvas, *arc_coordinates[2],tag="light_shine")
        else:
            draw_arc(canvas, *arc_coordinates[0],tag="light_bulb")
        clicked.count_light += 1

