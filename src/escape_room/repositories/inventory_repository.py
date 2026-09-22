import json
from src.escape_room.application.database_manager import DatabaseManager

class InventoryRepository():
    def __init__(self, db_path="src/escape_room/assets/mydata.db"):
        self.db = DatabaseManager(db_path)
        self._init_db()
    
    def _init_db(self):
        """Create a table if it doesn't exist yet"""
        query ="""
        CREATE table IF NOT EXISTS inventory (
            object TEXT NOT NULL,
            object_owner TEXT NOT NULL,
            item_index INTEGER NOT NULL,
            PRIMARY KEY (object, object_owner)
        )
        """
        self.db.execute(query)
        
    def load_inventory(self):
        """loads inventory converts them into a python dict"""
        query = "SELECT object, object_owner, item_index FROM inventory"
        result  = self.db.fetch_all(query)
        #result = {}
        
        # for row in rows:
        #     room_name = row["room_name"]
        #     result[room_name] = json.loads(row["state_json"])
        # result = json.loads(result)
        return result
        
    def save_inventory(self, inventory):
        """Updates the inventory"""
        try:
            self.db.execute("DELETE FROM inventory") # empty the table 
            
            for (object, object_owner), (index, _, _) in inventory.inventory.items():    
                data_to_insert = [
                    (object, object_owner, index)
                ]
            
            self.db.cursor.executemany(
                "INSERT INTO inventory (object, object_owner, item_index) VALUES (?,?,?)",
                data_to_insert
            )
            self.db.connection.commit()
        except Exception as e:
            self.db.connection.rollback() 
            raise e
