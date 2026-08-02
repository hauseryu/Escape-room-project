import tkinter as tk

class PlayerPanel(tk.Frame):
    """A subarea container to display game player statuses horizontally."""
    def __init__(self, parent_widget, image_path):
        # Initialize as a Tkinter Frame without hardcoded size limits
        super().__init__(parent_widget, bd=2, relief="groove", padx=10, pady=10)
        
        self.image_path = image_path
        self.loaded_icons = {}  # Cache to hold active photo references

        # --- Section 1: Current Player Profile ---
        # CHANGED: Added side="left" and fill="y", changed pady to padx for side-by-side spacing
        self.current_player_frame = tk.LabelFrame(self, text=" You (Current Player) ", padx=10, pady=10)
        self.current_player_frame.pack(side="left", fill="y", padx=(0, 15))

        # Placeholder label for the current player's icon
        self.current_icon_label = tk.Label(self.current_player_frame)
        self.current_icon_label.pack(side="left", padx=(0, 10))

        # Label for the current player's name
        self.current_name_label = tk.Label(self.current_player_frame, text="", font=("Arial", 11, "bold"))
        self.current_name_label.pack(side="left")

        # --- Section 2: Other Active Players ---
        # CHANGED: Added side="left" and fill="y" to place it right next to Section 1
        self.others_frame = tk.LabelFrame(self, text=" Other Active Players ", padx=10, pady=10)
        self.others_frame.pack(side="left", fill="y")

        # Dynamic container where other players will be drawn horizontally
        self.players_list_frame = tk.Frame(self.others_frame)
        self.players_list_frame.pack(fill="both", expand=True)
        
    def update_current_player(self, player_name, icon_name):
        """Updates the local profile display of the active user."""
        full_path = f"{self.image_path}/{icon_name}"
        img = tk.PhotoImage(file=full_path)
        
        # Keep photo reference alive in memory
        self.loaded_icons["current_player"] = img
        
        self.current_icon_label.config(image=img)
        self.current_name_label.config(text=player_name)

    def update_players_list(self, players_data_list):
        """Clears and redraws the list of other active players horizontally."""
        # 1. Clear previous widget elements
        for child in self.players_list_frame.winfo_children():
            child.destroy()

        # 2. Rebuild the list with new data aligned side-by-side
        for index, player in enumerate(players_data_list):
            # CHANGED: Pack individual player cards horizontally inside the list frame
            player_card_frame = tk.Frame(self.players_list_frame, pady=4, padx=10)
            player_card_frame.pack(side="left", fill="y")  # <-- Aligns items next to each other

            # Load specific player icon
            full_path = f"{self.image_path}/{player['icon']}"
            img = tk.PhotoImage(file=full_path)
            
            # Keep active unique key reference to prevent Garbage Collection
            cache_key = f"other_{index}_{player['name']}"
            self.loaded_icons[cache_key] = img

            # Render player icon and player name stacked vertically or side-by-side
            # Let's stack icon over text for a clean horizontal profile look:
            icon_lbl = tk.Label(player_card_frame, image=img)
            icon_lbl.pack(side="top")

            name_lbl = tk.Label(player_card_frame, text=player["name"], font=("Arial", 10))
            name_lbl.pack(side="top", pady=(2, 0))