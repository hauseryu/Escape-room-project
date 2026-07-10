
def compute_2d_coordinates(x, y, z, win_width,win_height):
    x_2d = (150*x)/z+(win_width/2)
    y_2d = (150*y)/z+(win_height/2)
    
    return (x_2d, y_2d)


