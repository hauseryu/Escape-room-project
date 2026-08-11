import os
import tkinter
import winsound

from escape_room import globals
from escape_room import graphics


class Key:
    def __init__(self, inventory):
        self.canvas = None
        self.object_owner = ""
        self.inventory = inventory
        package_dir = os.path.dirname(os.path.dirname(__file__))
        self.image_path = os.path.join(package_dir, "assets", "images", "key_transparent.png")
        self.sound_path = os.path.join(package_dir, "assets", "sounds", "grab_key.wav")

    def draw(self, canvas):
        self.canvas = canvas
        self.img = tkinter.PhotoImage(file=self.image_path)
        if self.inventory.objectInInventory("key",self.object_owner):
            objIndex = self.inventory.getObjectIndex("key",self.object_owner)
            (x1,y1) = self.inventory.getObjectCoordinates(objIndex)
        else:
            (x1, y1) = graphics.compute_2d_coordinates(
                6.5,
                0.78,
                3.0,
                globals.canvas_width,
                globals.canvas_height,
            )
        if self.inventory.objectIsSelected("key",self.object_owner):
            objIndex = self.inventory.getObjectIndex("key",self.object_owner)
            (x1,y1) = self.inventory.getObjectCoordinates(objIndex)
            select_rect = (x1-5,y1-5,
                           x1+57,y1-5,
                           x1+57,y1+45,
                           x1-5,y1+45
                           )
            self.selection = self.canvas.create_polygon(*select_rect,fill="blue",width=3)
        self.object_id = canvas.create_image(x1, y1, image=self.img, anchor="nw")
        tooltip_data = {"rect_id": None, "text_id": None}
        # bind event '<Enter>' (mouse moves over icon)
        self.canvas.tag_bind(
            self.object_id, 
            "<Enter>", 
            lambda event: self._show_tooltip(event, x1, y1, "owner: " + self.object_owner, tooltip_data)
        )        
        # bind event '<Leave>' (mouse moves away from icon)
        self.canvas.tag_bind(
            self.object_id,
            "<Leave>", 
            lambda event: self._hide_tooltip(event, tooltip_data)
        )        
        self.canvas.tag_bind(
            self.object_id,
            "<Button-1>", 
            lambda event: self.on_key_click(event, tooltip_data)
        )

    def on_key_click(self, event, tooltip_data):
        self._hide_tooltip(event, tooltip_data)
        self.canvas.delete(self.object_id)
        try:
            winsound.PlaySound(
                self.sound_path,
                winsound.SND_FILENAME | winsound.SND_ASYNC,
            )
        except Exception as e:
            print(f"Sound konnte nicht abgespielt werden: {e}")
        if not self.inventory.objectInInventory("key",self.object_owner):
            self.inventory.addObject("key",self.object_owner,self)
        else:
            self.inventory.selectObject("key",self.object_owner)
        self.draw(self.canvas)

    def _show_tooltip(self, event, x, y, text, tooltip_data):
        """draws text for a short wile on canvas."""
        # placement of text: e.g. 20 pixels above the icon
        text_id = tooltip_data["text_id"] = self.canvas.create_text(
            x, y - 20, 
            text=text, 
            font=("Arial", 10, "bold"), 
            fill="yellow", 
            anchor="w"
        )
        bbox = self.canvas.bbox(text_id)
        if bbox:
            # adjust to text size, create rectangle
            # care about order of drawing!
            rect_id = self.canvas.create_rectangle(
                bbox[0] - 4, bbox[1] - 2, 
                bbox[2] + 4, bbox[3] + 2, 
                fill="#4D2D97",      # 薄い黄色（お好みの色に変更してください）
                outline="#EE0707"    # 枠線の色
            )
            
            # 4. 重なり順の調整：背景の長方形をテキストの後ろ（下）に移動させる
            self.canvas.tag_lower(rect_id, text_id)
            
            # IDを保持
            tooltip_data["rect_id"] = rect_id
            tooltip_data["text_id"] = text_id        

    def _hide_tooltip(self, event, tooltip_data):
        """removes text immediately again, if mouse if moved."""
        if tooltip_data["rect_id"] is not None:
            self.canvas.delete(tooltip_data["rect_id"])
            tooltip_data["rect_id"] = None
            
        if tooltip_data["text_id"] is not None:
            self.canvas.delete(tooltip_data["text_id"])
            tooltip_data["text_id"] = None
