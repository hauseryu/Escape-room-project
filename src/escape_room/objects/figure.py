from PIL import Image, ImageTk
from src.escape_room.application.context_manager import ContextManager

# figures are persons, animals etc. drawn on the canvas
class Figure():

    def __init__(self, figure_name, image_path=None,x_coord=None,y_coord=None,width=None,height=None,
                 action_sequence_talk = None):
        self.figure_name = figure_name
        self.image_path = image_path
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height
        self.foto_image = None
        self.image_id = None
        self.action_sequence_talk = action_sequence_talk

    def draw_image(self, canvas):
        image = Image.open(self.image_path)
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        
        self.foto_image = ImageTk.PhotoImage(image, master=canvas)
        
        self.image_id = canvas.create_image(self.x_coord, self.y_coord, anchor="nw", image=self.foto_image)
        canvas.tag_bind(
            self.image_id,
            "<Button-1>",
            lambda e: self.figure_clicked(canvas) 
        )

    def figure_clicked(self,canvas):
        print(f"[DEBUG]: figure {self.figure_name} clicked")
        ContextManager().get_action_manager().execute_action_sequence(self.action_sequence_talk)
        pass
