from src.escape_room.application import globals
from PIL import Image, ImageDraw, ImageTk
import numpy as np

# Ermittelt den Ordner, in dem diese escape_room.py Datei liegt

# Fügt diesen Ordner zu den Python-Suchpfaden hinzu, falls er noch nicht drin ist


# convert 3D coordinates to 2D coordinates
def compute_2d_coordinates(x, y, z, win_width,win_height,shift_coordinates = (0,0,0)):
    x+=shift_coordinates[0]
    y+=shift_coordinates[1]
    z+=shift_coordinates[2]
    y = -2*y+3
    x_2d = 1.6*((300*(x-4))/(z+1))+(win_width/2)
    y_2d = 0.953*((300*(y))/(z+1))+(win_height/2)+98
    
    return (x_2d, y_2d)

# convert from world to pixel coordinates
# passed argument world_coordinates: list of polygons, each polygon = list of points, each point = (x,y,z)
def convert_polygon_coordinates(world_coordinates, shift_coordinates = (0,0,0)):
    coordinates = []
    
    # iterate through the list of polygons and convert each point to 2D coordinates
    for polygon in world_coordinates:
        poly = []            
        for index,point in enumerate(polygon):
            if index == 0:
                poly.append(point)
            else:
                (x,y,z) = point
                (coord_x,coord_y) = compute_2d_coordinates(x,y,z,globals.canvas_width,globals.canvas_height,
                                                           shift_coordinates)
                poly.append([coord_x])
                poly.append([coord_y])
        coordinates.append(poly)

    # return list of polygons with 2D coordinates
    return coordinates

# determine coordinate shift for each room + objects
def shift_coordinates(world_coord_source,world_coord_target):
    (x_source,y_source,z_source) = world_coord_source
    (x_target,y_target,z_target) = world_coord_target
    return (x_target-x_source,y_target-y_source,z_source-z_target)
    
    # draw an object using world coordinates
def draw(canvas,world_coordinates,tag=None,object=None,arc_coordinates=None,
         shift_coordinates = (0,0,0)): 
    coordinates = convert_polygon_coordinates(world_coordinates,shift_coordinates)
    # draw the polygons on the canvas
    for polygon in coordinates:
        canvas.create_polygon(polygon[1:],width=1,fill=polygon[0],outline="black",tags=tag)
        if tag != None:
            canvas.tag_bind(tag,"<Button-1>",
                            lambda event: clicked(event, tag, object, canvas, world_coordinates,arc_coordinates))

def draw_textured_polygon(canvas, polygon, texture_path, fallback_fill="#8B4513", shift_coordinates=(0,0,0),
                          tag=None, object=None):

    coordinates = convert_polygon_coordinates([polygon], shift_coordinates)[0]
    points = _flatten_points(coordinates[1:])

    # 1. Ermittle die Bounding Box des Polygons (Min/Max Werte für X und Y)
    x_coords = points[0::2]  # Alle X-Werte (gerade Indizes)
    y_coords = points[1::2]  # Alle Y-Werte (ungerade Indizes)

    min_x, max_x = int(min(x_coords)), int(max(x_coords))
    min_y, max_y = int(min(y_coords)), int(max(y_coords))

    # Berechne die Breite und Höhe des Polygons
    poly_width = max_x - min_x
    poly_height = max_y - min_y

    # Sicherheitsprüfung für ungültige Dimensionen
    if poly_width <= 0 or poly_height <= 0:
        return

    # 2. Fallback-Polygon zeichnen (falls die Textur fehlschlägt)
    canvas.create_polygon(points, width=1, fill=fallback_fill, outline="black", tags=tag)

    # 3. Textur laden
    texture = Image.open(texture_path).convert("RGBA")
    tw, th = texture.size

    # 4. Punkte lokal verschieben (relativ zur Bounding Box)
    local_points = []
    for i in range(0, len(points), 2):
        local_points.append(points[i] - min_x)      # Lokales X
        local_points.append(points[i+1] - min_y)    # Lokales Y

    # WICHTIG: Für die perspektivische Transformation benötigen wir exakt 4 Eckpunkte!
    if len(local_points) == 8:  # Ein Viereck (4 Paare = 8 Werte)
        # Zielkoordinaten im lokalen System [(x0,y0), (x1,y1), (x2,y2), (x3,y3)]
        # Reihenfolge: oben_links, oben_rechts, unten_rechts, unten_links
        dst_pts = [(local_points[i], local_points[i+1]) for i in range(0, 8, 2)]
        
        # SCHRITT 1: Die Textur zuerst auf die benötigte Box-Größe kacheln
        # Dadurch haben wir genug Ziegel und sie werden nicht riesengroß gestreckt!
        tiled_texture = _tile_texture(texture, poly_width, poly_height)
        tw, th = tiled_texture.size
        
        # Quellkoordinaten der flachen, gekachelten Textur (vollständiges Rechteck)
        src_pts = [(0, th), (0, 0), (tw, 0), (tw, th)]
        
        # --- Korrigierte Matrix-Berechnung für PIL (Rückwärts-Transformation) ---
        matrix = []
        # Bei PIL.Image.PERSPECTIVE mappen wir von den ZIEL-Punkten (dst) zu den QUELL-Punkten (src)
        for (X, Y), (x, y) in zip(dst_pts, src_pts):
            matrix.append([X, Y, 1, 0, 0, 0, -x*X, -x*Y])
            matrix.append([0, 0, 0, X, Y, 1, -y*X, -y*Y])
        
        A = np.array(matrix, dtype=float)
        B = np.array([pt for pair in src_pts for pt in pair], dtype=float)
        
        # Berechne die 8 Koeffizienten via NumPy
        coeffs = np.linalg.solve(A, B)
        
        # SCHRITT 2: Die gekachelte Textur jetzt perspektivisch in das Polygon verzerren
        textured_polygon = tiled_texture.transform(
            (poly_width, poly_height), 
            Image.PERSPECTIVE, 
            coeffs, 
            Image.BICUBIC
        )
    else:
        # Fallback für Dreiecke oder komplexe Polygone (altes Kachel-Verfahren)
        tiled_texture = _tile_texture(texture, poly_width, poly_height)
        mask = Image.new("L", (poly_width, poly_height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.polygon(local_points, fill=255)
        
        textured_polygon = Image.new("RGBA", (poly_width, poly_height), (0, 0, 0, 0))
        textured_polygon.paste(tiled_texture, (0, 0), mask)

    try:
        image = ImageTk.PhotoImage(textured_polygon, master=canvas)
    except (RuntimeError, AttributeError):
        return

    # 5. Das Texturbild exakt an den korrekten Koordinaten einfügen
    canvas.create_image(min_x, min_y, anchor="nw", image=image, tags=tag)

    # 6. Konturlinie (Rahmen) oben drüber legen
    canvas.create_polygon(points, width=1, fill="", outline="black", tags=tag)

    # 7. Klick-Event sauber binden
    if tag is not None:
        canvas.tag_bind(tag, "<Button-1>",
                        lambda event: clicked(event, tag, object, canvas, polygon))

    # Referenz behalten (Garbage Collector Schutz)
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

def draw_arc(canvas, x, y, z, radius, color, start, extent, tag=None, shift_coordinates = (0,0,0)):
    x_center, y_center = compute_2d_coordinates(x, y, z, globals.canvas_width, globals.canvas_height,
                                                shift_coordinates)
    radius = radius*165
    (x0, y0) = x_center - radius, y_center + radius
    (x1, y1) = x_center + radius, y_center - radius
    if start == 0 and extent == 360:
        canvas.create_oval(x0, y0, x1, y1, fill=color, outline="black", tags=tag)
    else:
        canvas.create_arc(x0, y0, x1, y1, start=start, extent=extent, fill=color, outline="black", tags=tag)

def clicked(event,tag,object,canvas,world_coordinates,arc_coordinates=None):
    if tag == "light_switch" or tag[0:6] == "letter":
        object.clicked(event,tag,object,canvas,world_coordinates,arc_coordinates)
    if tag == "safe" or tag == "wardrobe" or tag == "bench" or tag == "chair" or tag == "table":
        object.clicked(event,tag,object,canvas,world_coordinates)


