import sqlite3
import json
from src.escape_room.application.database_manager import DatabaseManager

class RoomStateRepository(DatabaseManager):
    def __init__(self, db_path="src/escape_room/assets/mydata.db"):
        super().__init__(db_path)
        self._init_db()
    
    def _init_db(self):
        """Create a table if it doesn't exist yet"""
        query ="""
        CREATE  TABLE IF NOT EXISTS room_states (
            room_name TEXT PRIMARY KEY,
            state_json TEXT NOT NULL
        )
        """
        self.execute(query)
        
            
    def load_all_rooms(self):
        """loads all rooms and converts them into a python dict"""
        self.cursor.execute("""
                        SELECT room_name, state_json FROM room_states
                        """)
        rows = self.cursor.fetchall()
        result = {}
        for row in rows:
            room_name = row["room_name"]
            result[room_name] = json.loads("state_json")
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
