from PIL import Image, ImageTk

# figures are persons, animals etc. drawn on the canvas
class Figure():

    def __init__(self, figure_name, image_path=None,x_coord=None,y_coord=None,width=None,height=None):
        self.figure_name = figure_name
        self.image_path = image_path
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height
        self.foto_image = None
        self.image_id = None

    def draw_image(self, canvas):
        image = Image.open(self.image_path)
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        
        self.foto_image = ImageTk.PhotoImage(image, master=canvas)
        
        self.image_id = canvas.create_image(self.x_coord, self.y_coord, anchor="nw", image=self.foto_image)
        canvas.tag_bind(
            self.image_id,
            "<Button-1>",
            lambda e: self.speech_bubble.show_bubble(canvas) 
        )
