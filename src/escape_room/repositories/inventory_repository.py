import json
from src.escape_room.application.database_manager import DatabaseManager
from src.escape_room.application.context_manager import ContextManager

function_put_in_inventory = None

def set_function_put_in_inventory(function):
    global function_put_in_inventory  
    function_put_in_inventory = function
    pass
        
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
            unique_id TEXT NOT NULL,
            PRIMARY KEY (object, object_owner)
        )
        """
        self.db.execute(query)
        
    def load_inventory(self):
        """loads inventory converts them into a python dict"""
        query = "SELECT object, object_owner, item_index, unique_id FROM inventory"
        rows  = self.db.fetch_all(query)
        #result = {}
        
        # for row in rows:
        #     room_name = row["room_name"]
        #     result[room_name] = json.loads(row["state_json"])
        # result = json.loads(result)
        action_manager = ContextManager().get_action_manager()        
        for object, object_owner, item_index, unique_id in rows:
            print(f"Object {object}, object_owner {object_owner}, index {item_index}, unique_id {unique_id}")
            function_put_in_inventory(action_manager, object, unique_id, object_owner)
    
        
        # return json.loads(result)
        
    def save_inventory(self, inventory):
        """Updates the inventory"""
        try:
            self.db.execute("DELETE FROM inventory") # empty the table 
            
            for (object, object_owner), (index, object_ref, _) in inventory.inventory.items():    
                data_to_insert = [
                    (object, object_owner, index, object_ref.unique_id)
                ]
            
            self.db.cursor.executemany(
                "INSERT INTO inventory (object, object_owner, item_index, unique_id) VALUES (?,?,?,?)",
                data_to_insert
            )
            self.db.connection.commit()
        except Exception as e:
            self.db.connection.rollback() 
            raise e
