import tkinter as tk

class IconPickerPopup:
    def __init__(self, parent, icon_image_path, icon_dateien, callback):
        # 1. Initialize the top-level popup window
        self.top = tk.Toplevel(parent)
        self.top.title("Select icon")
        
        # Make the popup modal
        self.top.transient(parent)
        self.top.grab_set()
        
        self.callback = callback
        self.loaded_icons = {}

        # title for popup
        label = tk.Label(self.top, text="Select a new icon:", font=("Arial", 12))
        label.pack(pady=10)

        # Create a container frame for the selection grid
        grid_frame = tk.Frame(self.top)
        grid_frame.pack(pady=10)

        # 2. Dynamically load and arrange icons in a grid layout
        for index, file_name in enumerate(icon_dateien):
            # Load image and keep it in memory
            img = tk.PhotoImage(file=icon_image_path.joinpath(file_name))
            self.loaded_icons[file_name] = img
            
            # Create a clickable label for each icon
            lbl = tk.Label(grid_frame, image=img, bd=2, relief="groove", cursor="hand2")
            
            # place icons next to each other (e.g. 4 per line)
            spalte = index % 4
            zeile = index // 4
            lbl.grid(row=zeile, column=spalte, padx=10, pady=10)
            
            # Bind click event using lambda to pass the selected icon name
            lbl.bind("<Button-1>", lambda event, d=file_name: self.on_icon_selected(d))

    def on_icon_selected(self, file_name):
        # Pass the selected icon back to the main application
        self.callback(file_name)
        # Close the popup window
        self.top.destroy()