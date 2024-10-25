import sqlite3
import uuid

# Function to create the SQLite database and table
def create_table():
    conn = sqlite3.connect('ebuka.db')  # Connect to the SQLite database (or create it)
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS ebuka (
                can_count INTEGER,
                can_weight INTEGER,
                bottle_count INTEGER,
                bottle_weight INTEGER,
                machine_name TEXT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT PRIMARY KEY
            )
        ''')
        
    conn.commit()
    conn.close()

# Function to check if session_id exists
def session_id_exists(session_id):
    conn = sqlite3.connect('ebuka.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM ebuka WHERE session_id = ?', (session_id,))
    exists = cursor.fetchone()[0] > 0
    
    conn.close()
    return exists  # Return True or False



# Function to create a unique session ID
def create_session_id():
    session_id = uuid.uuid4().hex
    # Check for uniqueness of session ID
    while session_id_exists(session_id):
        print("Session ID already exists. Generating a new one...")
        session_id = uuid.uuid4().hex
    
    return session_id

# Function to insert values into the database
def insert_values(can_count, can_weight, bottle_count, bottle_weight ,created,modified,session_id):
    create_table()
    
    machine_name = "rvm3"  # CHANGE AS YOU WISH
    
    # Insert the data into the table
    conn = sqlite3.connect('ebuka.db')
    cursor = conn.cursor()
    
    # Insert the data
    cursor.execute('''
        INSERT INTO ebuka (can_count, can_weight, bottle_count, bottle_weight, machine_name,created,modified,session_id)
        VALUES (?, ?, ?, ?, ?, ?,?,?)
    ''', (can_count, can_weight, bottle_count, bottle_weight, machine_name,created,modified,session_id))
    
    conn.commit()
    conn.close()

    print("Data inserted successfully with session ID:", session_id)