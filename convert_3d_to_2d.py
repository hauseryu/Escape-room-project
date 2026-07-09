
def compute_2d_coordinates(x, y, z, win_height, win_width):
    x_2d = (50*x)/z+(win_width/2)
    y_2d = (50*y)/z+(win_height/2)
    
    return (x_2d, y_2d)


