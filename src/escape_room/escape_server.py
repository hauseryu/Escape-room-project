import socket
import threading
import queue
import json
import time

PORT = 50000

# global player administration
# structure: { "player_name": outgoing_queue }
active_players = {}
players_lock = threading.Lock() # protects dictionary against competing access from different threads

class EscapeServer():
    def client_receive_loop(self,client_socket, player_name, outgoing_queue):
        """ receives actions of player and processes escape room logic."""
        print(f"[ROOM] {player_name} has entered the room.")
        
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                    
                # we use JSON for structured game data
                game_data = json.loads(data.decode("utf-8"))
                action = game_data.get("action")
                
                # SCENARIO: passing over item ("send_inventory")
                if action == "send_inventory":
                    target = game_data.get("player_name")       # to whom?
                    inventory = game_data.get("inventory")           # what?
                    owner =  game_data.get("owner")
                    
                    with players_lock:
                        if target in active_players:
                            # we put the event directly into the send queue of the target player!
                            payload = {"action": "inventory_received", 
                                       "from": player_name, 
                                       "inventory": inventory,
                                       "owner": owner}
                            active_players[target]["queue"].put(json.dumps(payload))
                            
                            # confirmation to the sender
                            outgoing_queue.put(json.dumps({"event": "system", "msg": f"{inventory} passed over to {target} ."}))
                        else:
                            outgoing_queue.put(json.dumps({"event": "system", "msg": f"player {target} not found."}))
                            
            except json.JSONDecodeError:
                print(f"[FEHLER] invalid data format from {player_name}")
            except Exception as excp:
                break

        # player leaves the game
        print(f"[ROOM] {player_name} has left the game.")
        with players_lock:
            if player_name in active_players:
                del active_players[player_name]
        
        # terminate also the sending thread
        outgoing_queue.put("SHUTDOWN")
        client_socket.close()

    def client_send_loop(self,client_socket, outgoing_queue):
        """ take data from the queue of the player and to the player's PC."""
        while True:
            try:
                message = outgoing_queue.get()
                if message == "SHUTDOWN":
                    break
                print("[CLIENT]: send message: " + message)
                client_socket.sendall(message.encode("utf-8"))
            except Exception:
                break

    def handle_new_connection(self,client_socket, client_address):
        """ ask once for name and start threads."""
        try:
            # client must identify him/herself during first connection (e.g. "maria")
            client_socket.sendall("WELCOME: please send your registration data.".encode("utf-8"))
            reg_data = json.loads(client_socket.recv(1024).decode("utf-8"))
            player_name = reg_data.get("name", "").strip()
            icon_num = reg_data.get("icon", 1) # Standard-Icon 1, if nothing is passed
            
            player_queue = queue.Queue()
            
            with players_lock:
                # check if name is used already
                if player_name in active_players or not player_name:
                    client_socket.sendall("ERROR: name invalid or used already.".encode("utf-8"))
                    client_socket.close()
                    return
                # store player data in dictionary
                active_players[player_name] = {
                    "queue": player_queue,
                    "icon": icon_num
                }
            # send player list to all players (incl. new player)
            self.broadcast_player_list() 

            # start thread for the specific player
            t_recv = threading.Thread(target=EscapeServer.client_receive_loop, args=(self,client_socket, player_name, player_queue))
            t_send = threading.Thread(target=EscapeServer.client_send_loop, args=(self,client_socket, player_queue))
            
            t_recv.start()
            t_send.start()
            
        except (ConnectionResetError, ConnectionAbortedError) as e:
        # catch WinError 10053 (Aborted) and 10054 (Reset) with clean exception
            print(f"[INFO] port scan or aborted connection trial from {client_address}.")
            client_socket.close()            
        except Exception as e:
            print(f"error during connection setup: {e}")
            client_socket.close()

    def broadcast_player_list(self):
        """send current player list to all clients."""
        with players_lock:
            player_info_list = [
                {"name": name, "icon": data["icon"]} 
                for name, data in active_players.items()
            ]            
        payload = {
            "action": "player_list",
            "players": player_info_list
        }
        json_string = json.dumps(payload)
        
        with players_lock:
            for data in active_players.values():
                data["queue"].put(json_string)

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", PORT))
        server.listen()
        print(f"[START] escape room listening on port {PORT}...")
        
        while True:
            client_socket, client_address = server.accept()
            threading.Thread(target=EscapeServer.handle_new_connection, args=(self,client_socket, client_address)).start()


