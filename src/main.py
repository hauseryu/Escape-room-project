import tkinter
import sys

from escape_room import globals
from escape_room.escape_room import EscapeApp

def main():
    root = tkinter.Tk()
    
    root.title("Escape Room Game")

    try:
        app = EscapeApp(root)
    except RuntimeError:
        root.destroy()
        sys.exit()
    
    root.geometry(f"{globals.canvas_width}x{globals.canvas_height}")
    root.mainloop()

if __name__ == "__main__":
    main()
