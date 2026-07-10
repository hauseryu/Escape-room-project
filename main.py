import tkinter
import escapeRoom
import globals

# create application and display window
root = tkinter.Tk()
escapeRoom = escapeRoom.EscapeApp(root)
root.geometry(f'{globals.canvas_width}x{globals.canvas_height}')
root.mainloop()
