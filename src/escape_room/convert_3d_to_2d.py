from . import globals

# convert 3D coordinates to 2D coordinates
def compute_2d_coordinates(x, y, z, win_width,win_height):
    y = -2*y+3
    x_2d = (250*(x-4))/(z+1)+(win_width/2)
    y_2d = (250*(y))/(z+1)+(win_height/2)
    
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
