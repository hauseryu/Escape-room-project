import os
import tkinter
from PIL import Image, ImageTk

from escape_room import globals
from escape_room import icon_picker_popup

class StartScreen:
    def __init__(self, canvas, start_callback, server):
        self.canvas = canvas
        self.start_callback = start_callback
        self.image_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "images",
        )
        self.image_path_start_screen = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "images",
            "start_screen_moon.png",
        )
        self.image = None
        self.display_image = None
        self.server_var = tkinter.IntVar() # 0 = off, 1 = on
        self.player_name = tkinter.StringVar()
        self.player_icon_number = tkinter.IntVar()
        self.server = server
        self.server_use_var = tkinter.IntVar() # 0 = off, 1 = on

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0,
            0,
            globals.canvas_width,
            globals.canvas_height,
            fill="#07111f",
            outline="",
        )
        self._draw_bitmap()
        self._draw_title()
        self._draw_server_checkbox()
        self._draw_server_playername()
        self._draw_start_button()
        self.canvas.tag_bind("start_button", "<Button-1>", self.start_callback)

    def _draw_bitmap(self):
        try:
            imagePil = Image.open(self.image_path_start_screen)
            imagePilResized = imagePil.resize((globals.canvas_width,globals.canvas_height),Image.LANCZOS)
            self.image = ImageTk.PhotoImage(imagePilResized)
            self.display_image = self.image
            self.canvas.create_image(
                0,
                0,
                image=self.display_image,
                anchor="nw",
            )
        except (RuntimeError, tkinter.TclError):
            self.canvas.create_rectangle(
                180,
                140,
                1420,
                940,
                fill="#14213a",
                outline="#44516a",
                width=3,
            )

    def _draw_title(self):
        center_x = globals.canvas_width / 2
        self.canvas.create_text(
            center_x + 4,
            284,
            text="ESCAPE ROOM",
            fill="#05070b",
            font=("Georgia", 68, "bold"),
        )
        self.canvas.create_text(
            center_x,
            280,
            text="ESCAPE ROOM",
            fill="#f1ead7",
            font=("Georgia", 68, "bold"),
        )

    def _draw_server_checkbox(self):
        server_start_checkbox = tkinter.Checkbutton(
            self.canvas.master,
            text="Start Server (Host)", 
            variable=self.server_var, 
            font=("Arial", 20),
            background = "#171a20",
            foreground= "#17b976"
        )
        self.canvas.create_window(795, 550, window=server_start_checkbox, anchor="nw")
        server_checkbox = tkinter.Checkbutton(
            self.canvas.master,
            text="Use Server (Host)" + self.server, 
            variable=self.server_use_var, 
            font=("Arial", 20),
            background = "#171a20",
            foreground= "#17b976"
        )
        if self.server == "":
            server_checkbox.config(state="disabled")
        self.canvas.create_window(795, 600, window=server_checkbox, anchor="nw")

    def _draw_server_playername(self):
        name_label = tkinter.Label(
            self.canvas.master,
            text="Enter player name:", 
            font=("Arial", 20),
            background = "#171a20",
            foreground= "#17b976"
            )
        self.canvas.create_window(795, 650, window=name_label, anchor="nw")
        name_entry = tkinter.Entry(
            self.canvas.master, 
            textvariable=self.player_name,
            font=("Arial", 20), 
            background = "#798191",
            foreground= "#17b976",            
            width=10)
        self.canvas.create_window(1050, 650, window=name_entry, anchor="nw")
        name_label = tkinter.Label(
            self.canvas.master,
            text="Select player icon:", 
            font=("Arial", 20),
            background = "#171a20",
            foreground= "#17b976"
            )
        self.canvas.create_window(795, 725, window=name_label, anchor="nw")
        self.canvas.tag_bind("pic_select", "<Button-1>", self.on_icon_click)
        self.canvas.tag_bind("pic_select", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("pic_select", "<Leave>", lambda e: self.canvas.config(cursor=""))
        # Liste aller verfügbaren Icons für das Popup
        self.available_icons = ["\\playerpic_wonder_woman.png", 
                                "\\playerpic_woman_thinking.png", 
                                "\\playerpic_woman_happy.png", 
                                "\\playerpic_spider_man.png",
                                "\\playerpic_running_man.png",
                                "\\playerpic_businessman.png",
                                ]
        # load & draw start icon
        self.player_icon = tkinter.PhotoImage(file=self.image_path + self.available_icons[1])
        self.current_icon = self.canvas.create_image(1050, 700, image=self.player_icon, tags="pic_select", anchor="nw")

    def on_icon_click(self, event):
        # open popup window and list of icons and pass the callback function
        main_window = self.canvas.winfo_toplevel()
        popup = icon_picker_popup.IconPickerPopup(main_window, 
                                          self.image_path, self.available_icons, self.update_main_icon)
        # define popup size
        p_width = 420
        p_height = 310
        # calculate left upper corner, so mouse is in the middle
        pos_x = event.x_root - (p_width // 2)
        pos_y = event.y_root - (p_height // 2)
        popup.top.geometry(f"{p_width}x{p_height}+{pos_x}+{pos_y}")

    def update_main_icon(self, gewaehltes_icon_pfad):
        print(f"Main window has received the selection: {gewaehltes_icon_pfad}")
        self.player_icon_number = self.available_icons.index(gewaehltes_icon_pfad)
        # Load new picture into main class (important for memory)
        self.aktuelles_bild = tkinter.PhotoImage(file=self.image_path + gewaehltes_icon_pfad)
        
        # Replace current picture on canvas with new picture
        self.canvas.itemconfig(self.current_icon, image=self.aktuelles_bild)

    def _draw_start_button(self):
        center_x = globals.canvas_width / 2
        button_half_width = 210
        self.canvas.create_rectangle(
            center_x - button_half_width,
            830,
            center_x + button_half_width,
            920,
            fill="#171a20",
            outline="#d6c28a",
            width=4,
            tags=("start_button",),
        )
        self.canvas.create_text(
            center_x,
            872,
            text="START GAME",
            fill="#090a0d",
            font=("Arial", 31, "bold"),
            tags=("start_button",),
        )
        self.canvas.create_text(
            center_x,
            872,
            text="START GAME",
            fill="#f3e8c4",
            font=("Arial", 31, "bold"),
            tags=("start_button",),
        )
