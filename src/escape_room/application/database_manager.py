import sqlite3
import json

class DatabaseManager:
    """data base class which manages connections"""
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
    def execute(self, query, params=()):
        """executes a SQL-Statement (INSERT, UPDATE, DELETE, CREATE)"""
        try: 
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            self.connection.rollback()
            print(self.db_path)
            print(f"Database error: {e}")
            raise e
     
    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        """return a single result"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def close(self):
        """closes connection"""
        self.connection.close()
    