from PIL import Image, ImageTk
from src.escape_room.application.context_manager import ContextManager

# figures are persons, animals etc. drawn on the canvas
class Figure():

    def __init__(self, figure_name, image_path=None,x_coord=None,y_coord=None,width=None,height=None,
                 action_sequence_talk = None, action_sequence_generic = None):
        self.figure_name = figure_name
        self.image_path = image_path
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height
        self.foto_image = None
        self.image_id = None
        self.action_sequence_talk = action_sequence_talk
        self.action_sequence_generic = action_sequence_generic

    def draw_image(self, canvas):
        original_image = Image.open(self.image_path)
        self.image = original_image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        
        self.foto_image = ImageTk.PhotoImage(self.image, master=canvas)
        
        self.image_id = canvas.create_image(self.x_coord, self.y_coord, anchor="nw", image=self.foto_image)
        canvas.tag_bind(
            self.image_id,
            "<Button-1>",
            lambda e: self.figure_clicked(canvas, e) 
        )

    def remove_image(self, canvas):
        canvas.delete(self.image_id)

    def figure_clicked(self,canvas, event):
        print(f"[DEBUG]: figure {self.figure_name} clicked")
        top_left_x, top_left_y = canvas.coords(self.image_id) # get coordinates of the figure on the canvas
        # now get coordinates top left of the figure on the canvas
        img_w = self.image.width
        img_h = self.image.height
        # calculate, which pixel of the image was clicked
        pixel_x = int(event.x - top_left_x)
        pixel_y = int(event.y - top_left_y)
        # safeguard: check if pixel_x and pixel_y are within the image dimensions
        if not (0 <= pixel_x < img_w and 0 <= pixel_y < img_h):
            return
        
        # evaluate generic action sequence
        if self.action_sequence_generic!=None:            
            ContextManager().get_action_manager().execute_action_sequence(self.action_sequence_generic)

        # evaluate action sequence for talk
        if self.action_sequence_talk!=None:            
            ContextManager().get_action_manager().execute_action_sequence(self.action_sequence_talk)
