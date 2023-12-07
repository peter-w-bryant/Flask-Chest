# db_utils.py

import datetime
import sqlite3

from flask import current_app


def write_to_db(schema, variable_name, variable_value, request_id=None):
    flask_chest = current_app.extensions.get('flask_chest')
    if flask_chest:
        conn = sqlite3.connect(flask_chest.db_uri)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {schema['table_name']} (
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
        cursor.execute(f'''INSERT INTO {schema['table_name']} 
                            (request_id, date, time, variable_name, variable_value) 
                            VALUES (?, ?, ?, ?, ?)''', 
                            (request_id, date_str, time_str, variable_name, variable_value))

        conn.commit()
        conn.close()
