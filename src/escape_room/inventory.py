
from pathlib import Path

from PIL import Image, ImageTk


IMAGE_DIR = Path(__file__).resolve().parent / "assets" / "images"
INVENTORY_TEXTURE = IMAGE_DIR / "inventory_wood.jpg"
INVENTORY_ICON = IMAGE_DIR / "inventory_rucksack.png"


class Inventory():
    WIDTH = 350
    HEIGHT = 200
    HEADER_HEIGHT = 58
    GRID_X = 20
    GRID_Y = 70
    GRID_WIDTH = 310
    GRID_HEIGHT = 125
    ICON_SIZE = 55
    COLUMNS = 5
    ROWS = 2

    def __init__(self):
        self.canvas = None
        self.inventory = []
        pass

    def draw(self,canvas):
        self.canvas = canvas
        self._draw_background(canvas)
        self._draw_header(canvas)
        self._draw_grid(canvas)

    def _draw_background(self, canvas):
        canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill="black")

        try:
            texture = Image.open(INVENTORY_TEXTURE).convert("RGB")
            texture = texture.resize((self.WIDTH, self.HEIGHT))
            self.background_image = ImageTk.PhotoImage(texture, master=canvas)
        except (RuntimeError, AttributeError):
            return

        canvas.create_image(0, 0, anchor="nw", image=self.background_image)

    def _draw_header(self, canvas):
        canvas.create_text(
            150,
            30,
            text="Inventory",
            fill="white",
            font=("Arial", 16, "bold"),
        )

        try:
            icon = Image.open(INVENTORY_ICON).convert("RGBA")
            icon = icon.resize((self.ICON_SIZE, self.ICON_SIZE))
            self.icon_image = ImageTk.PhotoImage(icon, master=canvas)
        except (RuntimeError, AttributeError):
            return

        canvas.create_image(35, 10, anchor="nw", image=self.icon_image)

    def _draw_grid(self, canvas):
        cell_width = self.GRID_WIDTH / self.COLUMNS
        cell_height = self.GRID_HEIGHT / self.ROWS

        for column in range(self.COLUMNS + 1):
            x = self.GRID_X + column * cell_width
            canvas.create_line(x, self.GRID_Y, x, self.GRID_Y + self.GRID_HEIGHT, fill="black", width=2)

        for row in range(self.ROWS + 1):
            y = self.GRID_Y + row * cell_height
            canvas.create_line(self.GRID_X, y, self.GRID_X + self.GRID_WIDTH, y, fill="black", width=2)
        
    def addObject(self,object):
        self.inventory.append(object)

    def objectInInventory(self,object):
        return (object in self.inventory)
    

