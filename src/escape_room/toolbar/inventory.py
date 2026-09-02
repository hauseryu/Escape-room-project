
from pathlib import Path
from PIL import Image, ImageTk
from src.escape_room.application.context_manager import ContextManager

IMAGE_DIR = ContextManager.get_image_path()
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
        self.inventory = {} # dictionary of inventory objects (type,object owner, selection status)
        pass

    def draw(self,canvas):
        self.canvas = canvas
        self._draw_background(canvas)
        self._draw_header(canvas)
        self._draw_grid(canvas)
        for key,value in self.inventory.items():
            (_,object_ref,_) = value
            object_ref.draw(self.canvas)

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
        
    def addObject(self,object,object_owner,object_ref):
        dict_len = len(self.inventory)
        self.inventory.update({(object,object_owner): (dict_len,object_ref,"not selected")})

    def getObject(self,object,object_owner):
        return self.inventory[(object,object_owner)]
    
    def delObject(self,object,object_owner):
        del self.inventory[(object,object_owner)]
        # renumber all items
        index = 0
        for key,value in self.inventory.items():
            (_,object_ref,selection) = value
            self.inventory[key] = (index,object_ref,selection)
            index += 1

    def objectInInventory(self,object,object_owner):
        try:
            (_,_,_) = self.getObject(object,object_owner)
            return True
        except KeyError:
            return False

    def getObjectIndex(self,object,object_owner):
        (objIndex,_,_) = self.inventory[(object,object_owner)]
        return objIndex

    def getObjectCoordinates(self,object_index):
        return (28 + object_index*60, 80)

    def objectIsSelected(self,object,object_owner):
        try:
            (_,_,selection) = self.getObject(object,object_owner)
            if selection == "selected":
                return True
            else:
                return False
        except KeyError:
            return False
       
    def getSelectedObject(self):
        for obj in self.inventory:
            (_,_,selection) = self.inventory[obj]
            if selection == "selected":
                return obj
        return (None,None)

    def selectObject(self,object,object_owner):
        (index,obj_ref,_) = self.inventory[(object,object_owner)]
        self.inventory[(object,object_owner)] = (index,obj_ref,"selected")
      
    def remove_inventory_pictures(self):
        """remove old inventory on canvas """
        for obj,value in self.inventory.items():
            # remove current object images and selection
            (_,object_ref,selection) = value
            self.canvas.delete(object_ref.object_id)
            if selection == "selected":
                self.canvas.delete(object_ref.selection_id)

    def redraw_inventory(self):
        """redraw inventory on canvas """
        for obj,value in self.inventory.items():
            # remove current object images and selection
            (_,object_ref,_) = value
            object_ref.draw(self.canvas)
