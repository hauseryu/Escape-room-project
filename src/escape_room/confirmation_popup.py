from escape_room.graphics import compute_2d_coordinates
from tkinter import messagebox  # Required import for native dialog popups
import tkinter

# Styling Constants matching your furniture palette
BACKGROUND_COLOR = "#2e2e2e"    # Dark Charcoal
TEXT_COLOR = "#ffffff"          # White
BUTTON_BG = "#6F4520"           # WOOD_MIDTONE (Rich Brown)
BUTTON_FG = "#ffffff"           # White
BUTTON_ACTIVE_BG = "#7A4A22"    # WOOD_HIGHLIGHT (Brighter Brown)

class ConfirmationPopup:
    def __init__(self, parent_window, title, message, mouse_x, mouse_y, show_confirmation=True):
        self.result = False  # Default decision

        # 1. Create a modal TopLevel window
        self.top = tkinter.Toplevel(parent_window)
        self.top.title(title)

        # Apply the dark background to the main popup window frame
        self.top.configure(bg=BACKGROUND_COLOR)

        # define popup size and align with mouse coordinates
        p_width = 300
        p_height = 250

        # determine upper left corner, so mouse position is in the middle
        pos_x = mouse_x - (p_width // 2)
        pos_y = mouse_y - (p_height // 2)

        # apply geometry
        self.top.geometry(f"{p_width}x{p_height}+{pos_x}+{pos_y}")
        self.top.resizable(False, False)
        
        self.show_confirmation = show_confirmation

        # Center the popup exactly over your mouse or parent window
        self.top.transient(parent_window)
        self.top.grab_set()

        # 2. Add the question label
        # 2. Add the question label with custom text and background colors
        msg_label = tkinter.Label(
            self.top, 
            text=message, 
            font=("Arial", 10, "bold"), 
            wraplength=260, 
            pady=20,
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        msg_label.pack()

        # 3. Container frame for the English buttons
        button_frame = tkinter.Frame(self.top, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        # "Yes" Button with theme styling and hover/active states
        if self.show_confirmation:
            yes_btn = tkinter.Button(
                button_frame, 
                text="Yes", 
                width=10, 
                font=("Arial", 9, "bold"),
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                activebackground=BUTTON_ACTIVE_BG,
                activeforeground=BUTTON_FG,
                bd=1,
                relief="raised",
                cursor="hand2",
                command=self._on_yes
            )
            yes_btn.pack(side="left", padx=10)

            # "No" Button with theme styling
            no_btn = tkinter.Button(
                button_frame, 
                text="No", 
                width=10, 
                font=("Arial", 9, "bold"),
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                activebackground=BUTTON_ACTIVE_BG,
                activeforeground=BUTTON_FG,
                bd=1,
                relief="raised",
                cursor="hand2",
                command=self._on_no
            )
            no_btn.pack(side="left", padx=10)
        else:
            # If no confirmation is needed, just show an "OK" button
            ok_btn = tkinter.Button(
                button_frame, 
                text="OK", 
                width=10, 
                font=("Arial", 9, "bold"),
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                activebackground=BUTTON_ACTIVE_BG,
                activeforeground=BUTTON_FG,
                bd=1,
                relief="raised",
                cursor="hand2",
                command=self._on_yes  # Treat OK as a positive response
            )
            ok_btn.pack(side="left", padx=10)

        # Wait here until the popup is closed
        parent_window.wait_window(self.top)

    def _on_yes(self):
        self.result = True
        self.top.destroy()

    def _on_no(self):
        self.result = False
        self.top.destroy() 