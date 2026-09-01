import socket
import threading
import json
import scapy.all as scapy

class EscapeClient:
    def __init__(self, server_ip, port, player_name, player_icon_number, network_queue, chat_queue, gui_master):
        self.server_ip = server_ip
        self.port = port
        self.player_name = player_name
        self.player_icon_number = player_icon_number
        self.network_queue = network_queue  # Waiting queue in main app
        self.chat_queue = chat_queue # for incoming chat messages
        self.client_socket = None
        self.gui_master = gui_master

    def connect_and_start(self):
        """build up connection & start background reception thread."""
        try:
            # 1. create TCP sockets and connect
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[CLIENT] Connect to {self.server_ip}:{self.port}...")
            self.client_socket.connect((self.server_ip, self.port))
            
            # 2. get welcome text from server 
            welcome_msg = self.client_socket.recv(1024).decode("utf-8")
            print(f"[CLIENT] Server answers: {welcome_msg}")
            
            # 3. register own player name & get player list
            reg_payload = {
                "name": self.player_name,
                "icon": self.player_icon_number
            }
            self.client_socket.sendall(json.dumps(reg_payload).encode("utf-8"))
            print(f"[CLIENT] Registered successfully as '{self.player_name}'.")

            # 4. create background thread for permanent reception thread 
            recv_thread = threading.Thread(target=self._receive_loop, daemon=True)
            recv_thread.start()
            return True
            
        except Exception as e:
            print(f"❌ [CLIENT] Connection error: {e}")
            if self.client_socket:
                self.client_socket.close()
            return False

    def receive_action(self, action_data):
        """process incoming initial actions like player list."""
        action_type = action_data.get("action")
        
        if action_type == "player_list":
            players = action_data.get("players", [])
            print(f"[NETWORK] player list updated: {players}")
            
            # transfer player list to GUI
            payload = {
                "event": "player_list", 
                "players": players
            }
            self.network_queue.put(payload)

        if action_type == "send_inventory":
            inventory = action_data.get("inventory")
            print(f"[NETWORK] send_inventory for {inventory}")


    def _receive_loop(self):
        """runs asynchronously in background. Receives data and puts it into the GUI queue."""
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    print("[CLIENT] Verbindung vom Server geschlossen.")
                    # put specific event into queue, so GUI gets knowledge about it
                    self.network_queue.put({"event": "system", "msg": "lost connection."})
                    break
                
                # decode JSON package
                game_event = json.loads(data.decode("utf-8"))
                # transmit event to GUI
                self.network_queue.put(game_event)
                # fire event for the canvas master window
                self.gui_master.event_generate("<<NetworkEvent>>", when="tail")
                
            except Exception:
                break
        
        if self.client_socket:
            self.client_socket.close()

    def send_action(self, action_type, player=None, inventory=None, owner=None, json_payload = None):
        """ useful method to send actions to the sever via the GUI class."""
        if not self.client_socket:
            print("⚠️ No active server connection.")
            return
            
        if action_type == "chat_message":
            payload = json_payload
        else:
            payload = {
                "action": action_type,
                "player_name": player,
                "inventory": inventory,
                "owner": owner
            }

        try:
            json_string = json.dumps(payload)
            self.client_socket.sendall(json_string.encode("utf-8"))
        except Exception as e:
            print(f"error during sending: {e}")

# functions to retrieve all computer IP addresses in local network
    def get_own_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def scan_network(self,ip_range):
        print(f"Scan network range: {ip_range} ...")
        
        # create ARP request for whole IP area
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        
        # send package and collect answers (timeout after 2 seconds)
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        
        devices = []
        for element in answered_list:
            device_info = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            devices.append(device_info)
        return devices

    def get_devices_local_network(self):
        # 1. get own IP address 
        own_ip = self.get_own_ip()
        # 2. convert e.g.  192.168.178.45 into -> 192.168.178.0/24
        network_prefix = ".".join(own_ip.split(".")[:-1]) + ".0/24"

        # 3. do scan
        found_devices = self.scan_network(network_prefix)

        # 4. show result
        print("\nfound computers in local network:")
        print("IP address\t\tMAC address")
        print("-" * 50)
        for device in found_devices:
            print(f"{device['ip']}\t\t{device['mac']}")
        return found_devices

    def check_port(self,ip, port):
        # create TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set a short timeout, so script does not wait forever (e.g. 1 second)
        s.settimeout(1.0)
        
        # try to connect
        result = s.connect_ex((ip, port))
        s.close()
        
        # result of 0 means: port is open and accepting
        if result == 0:
            return True
        else:
            return False

    def check_server_port(self,found_devices,port):
        for device in found_devices:
            found = self.check_port(device['ip'],port)
            if found:
                return device['ip']
        return ""