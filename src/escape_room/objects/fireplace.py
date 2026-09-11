from PIL import Image, ImageTk, ImageOps

class Fireplace():
    def __init__(self, shift_coordinates=(0, 0, 0)):
        self.shift_coordinates = shift_coordinates
        self.fireplace_coordinates = [
            ["#4A3429",(3.2, 0, 4),(4.8, 0, 4),(4.8, 1.05, 4),(3.2, 1.05, 4)], # bottom of the fireplace (back)
            ["#4C382E",(3.55, 1.34, 4),(4.45, 1.34, 4),(4.45, 2.20, 4),(3.55, 2.20, 4)], # bottom of the chimney (back)
            ["#49362C",(3.42, 2.20, 4),(4.58, 2.20, 4),(4.58, 2.35, 4),(3.42, 2.35, 4)], # upper chimney (back)
            ["#5A4032",(3.2, 0, 3.55),(3.2, 0, 4),(3.2, 1.05, 4),(3.2, 1.05, 3.55)], # bottom of the fireplace (left side)
            ["#4A3429",(4.8, 0, 4),(4.8, 0, 3.55),(4.8, 1.05, 3.55),(4.8, 1.05, 4)], # bottom of the fireplace (right side)
            ["#5B4335",(3.55, 1.34, 3.52),(3.55, 1.34, 4),(3.55, 2.20, 4),(3.55, 2.20, 3.52)], # lower chimney (left side)
            ["#4C382E",(4.45, 1.34, 4),(4.45, 1.34, 3.52),(4.45, 2.20, 3.52),(4.45, 2.20, 4)], # lower chimney (right side)
            ["#684A39",(3.55, 2.20, 3.52),(4.45, 2.20, 3.52),(4.45, 2.20, 4),(3.55, 2.20, 4)], # lower chimney (top side)
            ["#765542",(3.55, 1.34, 3.52),(4.45, 1.34, 3.52),(4.45, 2.20, 3.52),(3.55, 2.20, 3.52)],# lower chimney (front side)
            ["#987158",(3.48, 2.10, 3.50),(4.52, 2.10, 3.50),(4.52, 2.23, 3.50),(3.48, 2.23, 3.50)], # chimney decorative strip
            ["#594033",(3.42, 2.20, 3.47),(3.42, 2.20, 4),(3.42, 2.35, 4),(3.42, 2.35, 3.47)], # chimney head (left side)
            ["#49362C",(4.58, 2.20, 4),(4.58, 2.20, 3.47),(4.58, 2.35, 3.47),(4.58, 2.35, 4)], # chimney head (right side)
            ["#84634D",(3.42, 2.35, 3.47),(4.58, 2.35, 3.47),(4.58, 2.35, 4),(3.42, 2.35, 4)], # chimney head (top side)
            ["#654939",(3.42, 2.20, 3.47),(4.58, 2.20, 3.47),(4.58, 2.35, 3.47),(3.42, 2.35, 3.47)], # chimney head (front side)
            ["#765544",(3.2, 1.05, 3.55),(4.8, 1.05, 3.55),(4.8, 1.05, 4),(3.2, 1.05, 4)], # lower part of the fireplace (top side)
            ["#694A38",(3.2, 0, 3.55),(4.8, 0, 3.55),(4.8, 1.05, 3.55),(3.2, 1.05, 3.55)], # front of the fireplace
            ["#181412",(3.55, 0.18, 3.53),(4.45, 0.18, 3.53),(4.45, 0.86, 3.53),(3.55, 0.86, 3.53)], # black fireplace opening 
            ["#241B17",(3.64, 0.27, 3.50),(4.36, 0.27, 3.50),(4.36, 0.76, 3.50),(3.64, 0.76, 3.50)], # dark back wall of the fireplace
            ["#3B2920",(3.48, 0.08, 3.54),(4.52, 0.08, 3.54),(4.42, 0.23, 3.54),(3.58, 0.23, 3.54)], # fire pit of the fireplace
            ["#85614A",(3.30, 0.04, 3.51),(3.55, 0.04, 3.51),(3.55, 1.00, 3.51),(3.30, 1.00, 3.51)], # left pillar
            ["#765440",(4.45, 0.04, 3.51),(4.70, 0.04, 3.51),(4.70, 1.00, 3.51),(4.45, 1.00, 3.51)], # right pillar
            ["#A0785A",(3.34, 0.32, 3.49),(3.50, 0.32, 3.49),(3.50, 0.48, 3.49),(3.34, 0.48, 3.49)], # left decorative element
            ["#946C51",(4.50, 0.32, 3.49),(4.66, 0.32, 3.49),(4.66, 0.48, 3.49),(4.50, 0.48, 3.49)], # right decorative element
            ["#8C684F",(3.24, 0.86, 3.50),(4.76, 0.86, 3.50),(4.76, 1.10, 3.50),(3.24, 1.10, 3.50)], # decorative frieze (base)
            ["#A27A5B",(3.36, 0.91, 3.48),(4.64, 0.91, 3.48),(4.64, 1.04, 3.48),(3.36, 1.04, 3.48)], # decorative frieze (inner strip)
            ["#745340",(3.05, 1.21, 3.82),(4.95, 1.21, 3.82),(4.95, 1.34, 3.82),(3.05, 1.34, 3.82)], # mantelpiece (back part)
            ["#A98468",(3.05, 1.34, 3.40),(4.95, 1.34, 3.40),(4.95, 1.34, 3.82),(3.05, 1.34, 3.82)], # mantelpiece (top side)
            ["#654838",(3.10, 1.10, 3.43),(4.90, 1.10, 3.43),(4.90, 1.21, 3.43),(3.10, 1.21, 3.43)], # mantelpiece (bottom part)
            ["#92705A",(3.05, 1.21, 3.40),(4.95, 1.21, 3.40),(4.95, 1.34, 3.40),(3.05, 1.34, 3.40)], # mantelpiece (front part)
        ]
        self.fire_coordinate = (3.55, 0.8, 3.9)

    def draw_fire(self, canvas, x_pos, y_pos):
        # Load the fire image
        fire_image_path = "src/escape_room/assets/images/fire.png"
        fire_image = Image.open(fire_image_path)
        resized_image = ImageOps.contain(fire_image, (90, 90))  # Resize while maintaining aspect ratio
        self.fire_image_tk = ImageTk.PhotoImage(resized_image)
        # Draw the fire image on the canvas
        self.fire_image_id = canvas.create_image(x_pos, y_pos, image=self.fire_image_tk, anchor="nw")
