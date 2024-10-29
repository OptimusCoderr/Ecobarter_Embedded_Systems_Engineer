import requests
import sqlite3
import os

# API Endpoints
API_URL_STORE = "https://app.ecobarter.africa/api/rvms/store"
API_URL_ALL = "https://app.ecobarter.africa/api/rvms"

# Database path
DB_PATH = '/home/daniel/MyApps/Ecobarter/New_RVM_Code/rvm.db'

# Function to check for an internet connection
def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        print("No internet connection.")
        return False

# Function to retrieve all session IDs from the API
def get_all_session_ids_from_api():
    try:
        response = requests.get(API_URL_ALL)
        if response.status_code == 200:
            records = response.json()
            return {record['session_id'] for record in records}  # Return a set of session_ids
        print(f"Failed to retrieve session IDs. Status Code: {response.status_code}, Response: {response.text}")
        return set()
    except Exception as e:
        print(f"Exception occurred while retrieving session IDs: {e}")
        return set()

# Function to get the last session ID from the local database
def get_last_session_id_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id FROM rvm ORDER BY created DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# Function to send all records from the local database to the API
def send_all_records_to_api():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rvm")
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to dictionary format for the API
    records = [
        {
            "can_count": row[0],
            "can_weight": row[1],
            "bottle_count": row[2],
            "bottle_weight": row[3],
            "machine_name": row[4],
            "created": row[5],
            "modified": row[6],
            "session_id": row[7]
        }
        for row in rows
    ]

    # Send data to API
    try:
        response = requests.post(API_URL_STORE, json=records)
        if response.status_code == 200:
            print("Data successfully posted to the server.")
            return True
        else:
            print(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"Exception occurred while sending data: {e}")
        return False

# Function to drop the rvm table
def drop_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS rvm")
    conn.commit()
    conn.close()
    print("Table 'rvm' dropped successfully.")

# Main function to check and update records
def main():
    if not check_internet_connection():
        print("Aborting process due to lack of internet connection.")
        return  # Exit the function if no internet connection

    # Get the last session ID from the local database and all session IDs from the API
    last_db_session_id = get_last_session_id_from_db()
    all_api_session_ids = get_all_session_ids_from_api()

    # Check if the last DB session ID exists in the API session IDs
    if last_db_session_id and last_db_session_id in all_api_session_ids:
        print("No new data to update.")
        drop_table()
    else:
        print("New data detected. Updating records.")
        if send_all_records_to_api():
            drop_table()

if __name__ == "__main__":
    main()
