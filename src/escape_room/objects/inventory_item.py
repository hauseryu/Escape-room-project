import os
import tkinter
import winsound
from PIL import Image, ImageTk, ImageOps

from src.escape_room.application import globals
from src.escape_room.gui_utilities import graphics
from src.escape_room.application.context_manager import ContextManager

class InventoryItem:
    # normal constructor should not be called directly => see below create method
    def __init__(self, name, room_data, index, inventory, 
                 room_state, unique_id="", shift_coordinates=(0, 0, 0), room_placement=False, sound=None, 
                 resize_room = None, resize_inventory = None, unique_identifier = None, object_owner = None,
                 resize_inventory_flag = False):
        # determine image & shift coordinates based on object name
        if room_data != None and index != None:
            (x,y,z) = room_data[name][index]["coord"] # get object coordinates (first element in list)
        else:
            (x,y,z) = (0,0,0)
                    
        map_name_to_attributes = {
            "key": ("key_transparent.png", (x-6.5, y-0.78, z-3.0),(40, 80)),
            "revolver": ("revolver.png", (x-6.5, y-0.78, z-3.0),(40, 80)),
            "magnifier": ("magnifier.png", (x-6.5, y-0.78, z-3.0),(40, 80)),
            "water_glass": ("water_glass.png", (x-5.0, y-1.0, z-3.0),(40, 80)),
            "poker": ("poker.png", (x-4, y-0, z-3.0),(40, 80)),
            "diamond": ("diamond.png", (x-3.78, y-0.37, z-3.5),(40, 80)),
            "coin": ("gold_coin.png", (x-0.5, y-1.25, z-5.0),(40, 80))
        }
        image = map_name_to_attributes[name][0]

        # evaluate room data, if given
        if room_data != None and index != None:
            unique_id = room_data[name][index]["unique_id"] # unique identifier for the key
            room_placement = True
            shift_coordinates = map_name_to_attributes[name][1]
            self.object_owner = ""
            try:
                self.check_action_draw = room_data[name][index]["check_action_draw"] # get action that checks preconditions for drawing
            except:
                self.check_action_draw = None
            try:
                self.allow_transfer = room_data[name][index]["allow_transfer"] # get action that checks preconditions for drawing
            except:
                self.allow_transfer = False

        else: # in case magnifier is not created from room data
            self.object_owner = object_owner
            self.check_action_draw = None
            self.allow_transfer = False

        # set attributes
        self.canvas = None
        self.name = name
        self.inventory = inventory
        self.selection_id = None
        self.unique_id = unique_id
        self.shift_coordinates = shift_coordinates
        self.room_placement = room_placement
        self.room_state = room_state
        self.resize_room_tuple = resize_room if resize_room else None
        self.resize_inventory_tuple = resize_inventory if resize_inventory else None
        if resize_inventory_flag:
            self.resize_inventory_tuple = map_name_to_attributes[name][2]
        self.image_path = ContextManager.get_image_path().joinpath(image)
        self.sound_path = ContextManager.get_sound_path().joinpath(sound) if sound else None

    # class method create has to be used to create objects, if based on preconditions
    @classmethod
    def create(cls, name, room_data, index, inventory, 
                room_state, unique_id="", shift_coordinates=(0, 0, 0), room_placement=False, sound=None, 
                resize_room = None, resize_inventory = None):
        unique_id = room_data[name][index]["unique_id"] # unique identifier for the object
        try:
            role_assign = room_data[name][index]["role"] # availability of object for role?
            if ContextManager().get_room().role != role_assign:
                return None # role mismatch => object not relevant for player!
        except:
            pass
        if room_state.object_is_removed(name,unique_id):
            return None
        # check action?
        try:
            check_action = room_data[name][index]["check_action"] # get action that checks preconditions
        except:
            check_action = None
        if check_action != None:
            create_allowed = ContextManager().get_action_manager().execute_action_sequence(check_action)
            if not create_allowed:
                return None
        # ok, object can be created
        return cls(name, room_data, index, inventory, room_state, unique_id, 
                    shift_coordinates, room_placement, sound, resize_room, resize_inventory)

    def draw(self, canvas):

        # part 1: check preconditions (in some cases inventory item may be hidden)
        # check draw action
        if self.check_action_draw != None and \
                not self.inventory.objectInInventory(self.name,self.unique_id,self.object_owner):
            draw_allowed = ContextManager().get_action_manager().execute_action_sequence(self.check_action_draw)
            if not draw_allowed:
                return None

        # part 2: actually draw the inventory item
        self.canvas = canvas
        img = Image.open(self.image_path)
        if self.resize_room_tuple is not None:
            img = ImageOps.contain(img, self.resize_room_tuple)
        self.img = ImageTk.PhotoImage(img, master=canvas)
        
        if self.inventory.objectInInventory(self.name,self.unique_id,self.object_owner):
            objIndex = self.inventory.getObjectIndex(self.name,self.unique_id,self.object_owner)
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
        if self.inventory.objectIsSelected(self.name, self.unique_id, self.object_owner):
            objIndex = self.inventory.getObjectIndex(self.name, self.unique_id, self.object_owner)
            (x1,y1) = self.inventory.getObjectCoordinates(objIndex)
            select_rect = (x1-5,y1-5,
                           x1+57,y1-5,
                           x1+57,y1+45,
                           x1-5,y1+45
                           )
            self.selection_id = self.canvas.create_polygon(*select_rect,fill="blue",width=3)
        self.obj_id = canvas.create_image(x1, y1, image=self.img, anchor="nw", tags=self.name)
        tooltip_data = {"rect_id": None, "text_id": None}
        # bind event '<Enter>' (mouse moves over icon)
        self.canvas.tag_bind(
            self.obj_id, 
            "<Enter>", 
            lambda event: self._show_tooltip(event, x1, y1, 
                                             "owner: " + self.object_owner + "(" + self.unique_id + ")", tooltip_data)
        )        
        # bind event '<Leave>' (mouse moves away from icon)
        self.canvas.tag_bind(
            self.obj_id,
            "<Leave>", 
            lambda event: self._hide_tooltip(event, tooltip_data)
        )        
        self.canvas.tag_bind(
            self.obj_id,
            "<Button-1>", 
            lambda event: self.on_key_click(event, tooltip_data)
        )

    def on_key_click(self, event, tooltip_data):
        self._hide_tooltip(event, tooltip_data)
        self.canvas.delete(self.obj_id)
        if self.sound_path is not None:
            try:
                winsound.PlaySound(
                    self.sound_path,
                    winsound.SND_FILENAME | winsound.SND_ASYNC,
                )
            except Exception as e:
                print(f"[DEBUG] Sound could not be played: {e}")
        
        if not self.inventory.objectInInventory(self.name, self.unique_id,self.object_owner) and \
               self.room_placement == True:
            self.inventory.addObject(self.name, self.unique_id, self.object_owner, self)
            self.room_state.remove(self.name, self.unique_id)
            self.room_placement = False
            ContextManager().get_room().removeObject(self)
        else:
            self.inventory.selectObject(self.name, self.unique_id, self.object_owner)
        self.draw(self.canvas)

    def _show_tooltip(self, event, x, y, text, tooltip_data):
        """draws text for a short wile on canvas."""

        # 1. create top level window
        popup = tooltip_data["popup_window"] = tkinter.Toplevel(self.canvas.winfo_toplevel())
        
        # 2. change window to frame-less, so it looks like a tooltip
        popup.wm_overrideredirect(True)
        
        # 3. configure window like a normal rectangle object
        popup.configure(
            bg="#4D2D97", 
            highlightbackground="#EE0707", 
            highlightthickness=1
        )

        # 4. insert text label
        label = tkinter.Label(
            popup, 
            text=text, 
            font=("Arial", 10, "bold"), 
            fg="yellow", 
            bg="#4D2D97", 
            padx=4, pady=2
        )
        label.pack()

        # 5. calculate position on screen (not canvas!) 
        # winfo_rootx/y is absolute screen position of canvas origin
        root_x = self.canvas.winfo_rootx() + x
        root_y = self.canvas.winfo_rooty() + (y - 20)

        int_x = int(root_x)
        int_y = int(root_y)

        # place window onto calculated position 
        popup.wm_geometry(f"+{int_x}+{int_y}")

        # 6. make sure it's on top
        popup.lift()        

    def _hide_tooltip(self, event, tooltip_data):
        """removes text immediately again, if mouse if moved."""
        if "popup_window" in tooltip_data and tooltip_data["popup_window"]:
            tooltip_data["popup_window"].destroy()
            tooltip_data["popup_window"] = None


