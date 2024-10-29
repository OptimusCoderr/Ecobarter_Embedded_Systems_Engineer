import sqlite3

# Database path
DB_PATH = 'rvm.db'  # Use the correct path to your database

def drop_table_if_exists(table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if the table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print(f"Table '{table_name}' exists. Dropping the table.")
        cursor.execute(f"DROP TABLE {table_name};")
        print(f"Table '{table_name}' has been dropped.")
    else:
        print(f"Table '{table_name}' does not exist.")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()



