import os
import tkinter
import winsound
from PIL import Image, ImageTk, ImageOps

from src.escape_room.application import globals
from src.escape_room.gui_utilities import graphics
from src.escape_room.application.context_manager import ContextManager

class InventoryItem:
    # normal constructor should not be called directly => see below create method
    def __init__(self, name, room_data, index, image, inventory, 
                 room_state, unique_id="", shift_coordinates=(0, 0, 0), room_placement=False, sound=None, 
            resize_room = None, resize_inventory = None):
        (x,y,z) = room_data[name][index][0] # get object coordinates (first element in list)
        unique_id = room_data[name][index][1] # unique identifier for the key
        room_placement = True
        # key
        if name=="key":
            image = "key_transparent.png"
            shift_coordinates = (x-6.5,y-0.78,z-3.0)    
        # revolver
        if name=="revolver":
            image = "revolver.png"
            shift_coordinates = (x-6.5,y-0.78,z-3.0)    
        # magnifier        
        if name == "magnifier":
            image = "magnifier.png"
            shift_coordinates = (x-6.5,y-0.78,z-3.0)   
        # water glass
        if name == "water_glass":
            image = "water_glass.png"
            shift_coordinates = (x-5.0,y-1.0,z-3.0)           
        # poker
        if name == "poker":
            image = "poker.png"
            shift_coordinates = (x-4,y-0,z-3.0)
        # diamond
        if name == "diamond":
            image = "diamond.png"
            shift_coordinates = (x-3.78,y-0.37,z-3.5)

        # set attributes
        self.canvas = None
        self.object_owner = ""
        self.name = name
        self.inventory = inventory
        self.object_id = None
        self.selection_id = None
        self.unique_id = unique_id
        self.shift_coordinates = shift_coordinates
        self.room_placement = room_placement
        self.room_state = room_state
        self.resize_room_tuple = resize_room if resize_room else None
        self.resize_inventory_tuple = resize_inventory if resize_inventory else None
        self.image_path = ContextManager.get_image_path().joinpath(image)
        self.sound_path = ContextManager.get_sound_path().joinpath(sound) if sound else None

    # class method create has to be used to create objects, if based on preconditions
    @classmethod
    def create(cls, name, room_data, index, image, inventory, 
                room_state, unique_id="", shift_coordinates=(0, 0, 0), room_placement=False, sound=None, 
        resize_room = None, resize_inventory = None):
        unique_id = room_data[name][index][1] # unique identifier for the object
        try:
            role_assign = room_data[name][index][2] # availability of object for role?
            if ContextManager().get_room().role != role_assign:
                return None # role mismatch => object not relevant for player!
        except:
            pass
        if room_state.object_is_removed(name,unique_id):
            return None
        return cls(name, room_data, index, image, inventory, room_state, unique_id, 
                    shift_coordinates, room_placement, sound, resize_room, resize_inventory)

    def draw(self, canvas):

        # part 1: check preconditions (in some cases inventory item may be hidden)
        if self.name == "key": # key may be hidden in safe
            draw_key = True
            for safe in ContextManager().get_room().safe: # look for associated safe
                if (self.unique_id == safe.key.unique_id and safe.state == 1): # safe is open
                    break
                elif (self.unique_id == safe.key.unique_id and safe.state == 0): # safe is closed
                    draw_key = False
                    break
            if not draw_key:
                return # key is hidden => do not draw it!

        if self.name == "diamond":
            draw_diamond = True            
            for index, cassette in enumerate(ContextManager().get_room().metal_cassette): 
                unique_id = ContextManager().get_room().room_data["metal_cassette"][index][1]
                if (self.unique_id == cassette.diamond.unique_id and self.room_state.get_state_object("metal_cassette",unique_id) == "opened"): 
                    break
                else: 
                    draw_diamond = False
                    break
            if not draw_diamond:
                return # key is hidden => do not draw it!

            # for index, cassette in enumerate(ContextManager().get_room().metal_cassette):
            #     unique_id = ContextManager().get_room().room_data["metal_cassette"][index][1]
            #     if self.unique_id == unique_id and self.room_state.get_state_object("metal_cassette",unique_id) == "opened":
            #         break
            #     else:
            #         draw_diamond = False
            #         break
            # if not draw_diamond:
            #     return

        # part 2: actually draw the inventory item
        self.canvas = canvas
        img = Image.open(self.image_path)
        if self.resize_room_tuple is not None:
            img = ImageOps.contain(img, self.resize_room_tuple)
        self.img = ImageTk.PhotoImage(img, master=canvas)
        
        if self.inventory.objectInInventory(self.name,self.object_owner):
            objIndex = self.inventory.getObjectIndex(self.name,self.object_owner)
            (x1,y1) = self.inventory.getObjectCoordinates(objIndex)
            if self.resize_inventory_tuple is not None:
                img = ImageOps.contain(img, self.resize_inventory_tuple)
            self.img = ImageTk.PhotoImage(img, master=canvas)
        elif self.room_placement == True:
            (x1, y1) = graphics.compute_2d_coordinates(
                6.5,
                0.78,
                3.0,
                globals.canvas_width,
                globals.canvas_height,
                self.shift_coordinates
            )
        if self.inventory.objectIsSelected(self.name, self.object_owner):
            objIndex = self.inventory.getObjectIndex(self.name, self.object_owner)
            (x1,y1) = self.inventory.getObjectCoordinates(objIndex)
            select_rect = (x1-5,y1-5,
                           x1+57,y1-5,
                           x1+57,y1+45,
                           x1-5,y1+45
                           )
            self.selection_id = self.canvas.create_polygon(*select_rect,fill="blue",width=3)
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
        if self.sound_path is not None:
            try:
                winsound.PlaySound(
                    self.sound_path,
                    winsound.SND_FILENAME | winsound.SND_ASYNC,
                )
            except Exception as e:
                print(f"Sound konnte nicht abgespielt werden: {e}")
        
        if not self.inventory.objectInInventory(self.name, self.object_owner) and \
               self.room_placement == True:
            self.inventory.addObject(self.name, self.object_owner, self)
            self.room_state.remove(self.name, self.unique_id)
            self.room_placement = False
            ContextManager().get_room().removeObject(self)
        else:
            self.inventory.selectObject(self.name, self.object_owner)
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
