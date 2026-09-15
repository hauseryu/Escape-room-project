import sqlite3
import json

class RoomStateRepository:
    def __init__(self, db_path="src/escape_room/assets/mydata.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor() # tool to execute sql commands
        self._init_db() # initialise 
    
    def _init_db(self):
        """Create a table if it doesn't exist yet"""
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS room_states (
                            room_name TEXT PRIMARY KEY,
                            state_json TEXT NOT NULL    
                        )
        """)
        self.connection.commit() # commit changes
            
    def load_all_rooms(self):
        """loads all rooms and converts them into a python dict"""
        self.cursor.execute("""
                        SELECT room_name, state_json FROM room_states
                        """)
        rows = self.cursor.fetchall()
        result = {}
        for row_id, json_data in rows:
            result[row_id] = json.loads(json_data)
        return result
        
    def save_all_rooms(self, room_state):
        """Stores und updates the room states"""
        try:
            self.cursor.execute("DELETE FROM room_states") # empty the table 
            
            data_to_insert = [
                (room_name, json.dumps(state))
                for room_name, state in room_state.items()
            ]
            
            self.cursor.executemany(
                "INSERT INTO room_states (room_name, state_json) VALUES (?,?)",
                data_to_insert
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback() 
            raise e
        
    def close(self):
        self.connection.close()
        
# # 1. Create a connection to the database (or create it if it doesn't exist)
# connection = sqlite3.connect("src/escape_room/assets/mydata.db")
# cursor = connection.cursor()

# # 2. Create a table 
# ret = cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         age INTEGER
#     )
# """
# )

# # delete all existing records in the table
# cursor.execute("DELETE FROM users")

# ret = cursor.execute(
#     "INSERT INTO users (name, age) VALUES (?, ?)", ("Anna", 28)
# )

# # save changes
# connection.commit()

# ret = cursor.execute("SELECT id, name, age FROM users")

# alle_users = cursor.fetchall()

# for users in alle_users:
#     print(f"ID: {users[0]} | Name: {users[1]} | Age: {users[2]}")


# connection.close()
