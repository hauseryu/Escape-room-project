
from pathlib import Path
import threading
import time
from tkinter import messagebox

from escape_room.escape_server import EscapeServer
from escape_room.escape_client import EscapeClient
from escape_room.room import Room
from escape_room import globals
from escape_room.start_screen import StartScreen

IMAGE_DIR = Path(__file__).resolve().parent / "assets" / "images"

class EscapeApp():

    # create frame Objekt and drawing area (canvas)
    def __init__(self,master):

        # create canvas frame
        self.room = Room(master)
        self.init_network()
        # initialization complete!
        # create room and inventory bar
        self.room.init_room(self.game_client)
        # show the start screen => start screen will then call the start_game function
        self.show_start_screen()
        
    # set up network, server and connection to other players
    def init_network(self):
        self.start_server = None
        self.player_name = None
        self.player_icon_number = None
        self.escape_server = EscapeServer()

        # create client network object and configure it
        # we pass the GUI queue so it can be written to by the network object
        self.game_client = EscapeClient(
            server_ip="127.0.0.1", 
            port=globals.SERVER_PORT, 
            player_name="", 
            player_icon_number=1, # set some default icon number
            network_queue=self.room.network_queue,
            gui_master=self.room.master
        )
        # now retrieve list of local devices
        found_devices = self.game_client.get_devices_local_network()
        self.server = self.game_client.check_server_port(found_devices,globals.SERVER_PORT)
        if self.server == None:
            print("no game server running.")
        else:
            print("server running on device: ",self.server)

    # show start screen
    def show_start_screen(self):
        self.start_screen = StartScreen(self.room.canvas_area, self.start_game,self.server)
        self.start_screen.draw()

    # start_game is called from start screen after user
    # has entered name, selected his icon and decided on server startup
    def start_game(self, event=None):
        self.room.canvas_area.delete("all")
        # get values from start screen fields
        self.player_name = self.start_screen.player_name.get()
        self.start_server = self.start_screen.server_var.get()
        self.player_icon_number = self.start_screen.player_icon_number
        # check if we have to start the server
        if self.start_server == 1:
            threading.Thread(target=self.escape_server.start_server, daemon=True).start()
        time.sleep(0.2) # give server object some time to start up....

        # start client connection
        if self.start_screen.server_use_var.get() == 1:
            self.game_client.server_ip = self.server    
        else:
            self.game_client.server_ip = "127.0.0.1"
        self.game_client.player_name = self.player_name
        self.game_client.player_icon_number = self.player_icon_number
        if self.game_client.connect_and_start():
            print("client network connection started successfully.")
        else:
            print("Game could not be started due to failing connection.")
            messagebox.showerror("error", "connection to server failed.")
            raise RuntimeError("server connection failed")

        # pass over player data to the room object
        self.room.update_player_data(self.player_name,self.player_icon_number)
        # pass over control to room object => create and show room 
        self.room.draw_room()



