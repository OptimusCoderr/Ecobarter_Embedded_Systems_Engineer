import sqlite3
import uuid
import random
from datetime import datetime

# Function to create the SQLite database and table
def create_table():
    conn = sqlite3.connect('/home/daniel/MyApps/Ecobarter/New_RVM_Code/rvm.db')  # Connect to the SQLite database (or create it)
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rvm (
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

# Function to insert 20 random records into the rvm table
def insert_random_data():
    conn = sqlite3.connect('/home/daniel/MyApps/Ecobarter/New_RVM_Code/rvm.db')
    cursor = conn.cursor()
    
    # Generate and insert 20 random entries
    for _ in range(20):
        can_count = random.randint(0, 100)
        can_weight = random.randint(0, 500)
        bottle_count = random.randint(0, 100)
        bottle_weight = random.randint(0, 500)
        machine_name = f"machine_{random.randint(1, 10)}"
        created = datetime.now().isoformat()
        modified = datetime.now().isoformat()
        session_id = uuid.uuid4().hex  # Generate unique session ID
        
        cursor.execute('''
            INSERT INTO rvm (can_count, can_weight, bottle_count, bottle_weight, machine_name, created, modified, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (can_count, can_weight, bottle_count, bottle_weight, machine_name, created, modified, session_id))
        
    conn.commit()
    conn.close()
    print("20 random records inserted into the database.")

# Run the functions
create_table()  # Ensure table exists
insert_random_data()  # Insert random data
