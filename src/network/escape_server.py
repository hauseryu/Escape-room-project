import socket
import threading
import queue
import json
import time
from src.escape_room.application.context_manager import ContextManager
from src.escape_room.objects import speech_data

PORT = 50000

# global player administration
# structure: { "player_name": outgoing_queue }
active_players = {}
players_lock = threading.Lock() # protects dictionary against competing access from different threads

class EscapeServer():

    def receive_messages(self,client_socket):
        """ read data from socket and return complete, single messages back to caller """
        data_buffer = ""
        
        while True:
            # 1. get new data, if delimiter is not in buffer
            if '\n' not in data_buffer:
                chunk = client_socket.recv(1024).decode('utf-8')
                if not chunk:
                    return # connection closed, finish generator
                data_buffer += chunk

            # 2. process all complete messages from the buffer
            while '\n' in data_buffer:
                message, data_buffer = data_buffer.split('\n', 1)
                if message.strip():
                    yield message  # return complete message to caller

    def client_receive_loop(self,client_socket, player_name, outgoing_queue):
        """ receives actions of player and processes escape room logic."""
        print(f"[SERVER] {player_name} has entered the room.")

        try:
            for message in self.receive_messages(client_socket):

                # 1. Validierung: Versuchen zu parsen
                try:
                    # we use JSON for structured game data
                    game_data = json.loads(message)
                except json.JSONDecodeError:
                    print(f"[SERVER] Invalid JSON format from {player_name}. Ignoring message.")
                    continue  # jump to next message
                
                action = game_data.get("action")
                
                # SCENARIO: passing over item ("send_inventory")
                if action == "send_inventory":
                    target = game_data.get("player_name")       # to whom?
                    inventory = game_data.get("inventory")           # what?
                    object_id = game_data.get("object_id")
                    owner =  game_data.get("owner")
                    
                    with players_lock:
                        if target in active_players:
                            # we put the event directly into the send queue of the target player!
                            payload = {"action": "inventory_received", 
                                       "from": player_name, 
                                       "inventory": inventory,
                                       "object_id": object_id,
                                       "owner": owner}
                            active_players[target]["queue"].put(json.dumps(payload))
                            
                            # confirmation to the sender
                            outgoing_queue.put(json.dumps({"event": "system", "msg": f"{inventory} passed over to {target} ."}))
                        else:
                            outgoing_queue.put(json.dumps({"event": "system", "msg": f"player {target} not found."}))

                # SCENARIO: calling server to generate chatbot message
                elif action == "send_chatbot_message":
                    player_name = game_data.get("player_name") # player to whom chatbot message is to be sent
                    message = game_data.get("message") # message to chatbot
                    first_message = game_data.get("first_message") # first message to chatbot?
                    player_role = game_data.get("player_role") # role of player (like Sherlock Holmes)
                    figure = game_data.get("figure") # dialog partner
                    story_index = game_data.get("story_index") # speech data, index to the story
                    print(f"[DEBUG] Server [action: {action}] received from player {player_name}, message: {message}")

                    # send message to chatbot client
                    chatbot_client = ContextManager().get_chatbot_client()
                    speech = speech_data.story_list[story_index]
                    chatbot_client._send_message(message,first_message,player_name,player_role,figure,speech,
                                                 speech_bubble=None,dialog=None,server_instance=self)

                # SCENARIO: passing over message to all players ("send_chat_message_simple")
                elif action == "send_chatbot_message_simple":
                    player_name = game_data.get("player_name") # player to whom chatbot message is to be sent
                    system_prompt = game_data.get("system_prompt") # system prompt for chatbot
                    user_prompt = game_data.get("user_prompt") # user prompt for chatbot
                    print(f"[DEBUG] Server [action: {action}] received from player {player_name}," \
                          f"system_prompt: {system_prompt}, user_prompt: {user_prompt}")

                    # send message to chatbot client
                    chatbot_client = ContextManager().get_chatbot_client()
                    chatbot_client._send_message_simple(system_prompt,user_prompt,player_name,server_instance=self)

                # SCENARIO: passing over message to all players ("chat_message")
                elif action == "chat_message":
                    sent_from = game_data.get("sent_from")
                    text = game_data.get("text")
                    print(f"[SERVER] Received chat message from {sent_from}:{text}")
                    payload = {"action": "chat_message", 
                                "sent_from": sent_from,
                                "text": text}
                    json_string = json.dumps(payload)                    
                    self.broadcast_message(json_string,sent_from)

                elif action == "update_player_list":
                    player_name = game_data.get("player_name")       # who changed?
                    role = game_data.get("role")                     # which role?
                    active_players[player_name]["role"] = role
                    self.broadcast_player_list()

        except (ConnectionResetError, BrokenPipeError, TimeoutError):
            # Fall B: Client-App wurde abrupt beendet (z.B. Task-Manager oder Absturz)
            print(f"connection to player {player_name} unexpectedly broken.")

        # player leaves the game
        print(f"[ROOM] {player_name} has left the game.")
        with players_lock:
            if player_name in active_players:
                del active_players[player_name]
        
        # terminate also the sending thread
        outgoing_queue.put("SHUTDOWN")
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        client_socket.close()
        print(f"[SERVER] connection to player {player_name} was closed.")

        # inform all players about the change
        self.broadcast_player_list()

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

    def client_send_update(self, action, parameter_container):
        # send message to client
        if action == "chatbot_answer":
            payload = {
                "action": action,
                "message": parameter_container["message"],
                "start_flag": parameter_container["start_flag"]
            }
            json_string = json.dumps(payload)
            player_name = parameter_container["player_name"]
            with players_lock:
                if player_name in active_players:
                    active_players[player_name]["queue"].put(json_string)
        elif action == "chatbot_answer_simple":
            payload = {
                "action": action,
                "message": parameter_container["message"]
            }
            json_string = json.dumps(payload)
            player_name = parameter_container["player_name"]
            with players_lock:
                if player_name in active_players:
                    active_players[player_name]["queue"].put(json_string)

    def handle_new_connection(self,client_socket, client_address):
        """ ask once for name and start threads."""
        try:
            # client must identify him/herself during first connection (e.g. "maria")
            client_socket.sendall("WELCOME: please send your registration data.".encode("utf-8"))
            reg_data = json.loads(client_socket.recv(1024).decode("utf-8"))
            player_name = reg_data.get("name", "").strip()
            icon_num = reg_data.get("icon", 1) # Standard-Icon 1, if nothing is passed
            role = reg_data.get("role", "") # standard: no role assigned
            
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
                    "icon": icon_num,
                    "role": role
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
                {"name": name, "icon": data["icon"], "role": data["role"]} 
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

    def broadcast_message(self,json_string,sent_from):
        """send message to all clients."""
        with players_lock:
            for data in active_players.values():
                if data["queue"] != active_players[sent_from]["queue"]: # don't send to player who wrote the message
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


