import datetime
import sqlite3


def sqlite_write(db_uri, schema_name, variable_name, variable_value, request_id):
    conn = sqlite3.connect(db_uri)
    cursor = conn.cursor()
    # Create table if not exists
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {schema_name} (
                        unique_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        request_id TEXT, 
                        date TEXT, 
                        time TEXT, 
                        variable_name TEXT, 
                        variable_value TEXT)''')
    # Get current date and time
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    # Insert a new record
    cursor.execute(f'''INSERT INTO {schema_name} 
                        (request_id, date, time, variable_name, variable_value) 
                        VALUES (?, ?, ?, ?, ?)''', 
                        (request_id, date_str, time_str, variable_name, variable_value))
    conn.commit()
    conn.close()

def create_sqlite_table(db_uri, schema_map):
    # Database initialization logic
    conn = sqlite3.connect(db_uri)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {schema_map['name']} (
                        unique_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        request_id TEXT, 
                        date TEXT, 
                        time TEXT, 
                        variable_name TEXT, 
                        variable_value TEXT)''')
    
    conn.commit()
    conn.close()