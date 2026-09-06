
from pathlib import Path
import threading
import time
from tkinter import messagebox

from src.network.escape_server import EscapeServer
from src.network.escape_client import EscapeClient
from src.escape_room.room.room import Room
from src.escape_room.application import globals
from src.escape_room.application.start_screen import StartScreen
from src.escape_room.application.context_manager import ContextManager
from src.escape_room.actions.action import ActionManager
from src.llm.llm_client import LlmClient

IMAGE_DIR = ContextManager.get_image_path()

class EscapeApp():

    # create frame Objekt and drawing area (canvas)
    def __init__(self,master):

        # get context manager instance (singleton)
        self.context_manager = ContextManager()
        self.action_manager = ActionManager()
        self.context_manager.set_action_manager(self.action_manager)

        # create LLM client and pass it to context manager
        self.llm_client = LlmClient()
        self.context_manager.set_llm_client(self.llm_client)

        # create canvas frame
        self.room = Room(master, self)
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
            chat_queue=self.room.chat_queue,
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
        
    def return_to_start_screen(self):
        # delete canvas content completely
        self.room.canvas_area.delete("all")
        
        # seperate the network connection
        if hasattr(self.game_client, "disconnect"):
            self.game_client.disconnect()

        # actualise network search
        found_devices = self.game_client.get_devices_local_network()
        self.server = self.game_client.check_server_port(found_devices,globals.SERVER_PORT)
        
        self.show_start_screen()


