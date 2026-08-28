import sqlite3

# 1. Create a connection to the database (or create it if it doesn't exist)
connection = sqlite3.connect("src/escape_room/assets/mydata.db")
cursor = connection.cursor()

# 2. Create a table 
ret = cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
"""
)

# delete all existing records in the table
cursor.execute("DELETE FROM users")

ret = cursor.execute(
    "INSERT INTO users (name, age) VALUES (?, ?)", ("Anna", 28)
)

# save changes
connection.commit()

ret = cursor.execute("SELECT id, name, age FROM users")

alle_users = cursor.fetchall()

for users in alle_users:
    print(f"ID: {users[0]} | Name: {users[1]} | Age: {users[2]}")


connection.close()
