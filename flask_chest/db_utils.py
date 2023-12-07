import datetime
import sqlite3

from flask import current_app


def write_to_db(schema, variable_name, variable_value):
    flask_chest = current_app.extensions.get("flask_chest")
    if flask_chest:
        conn = sqlite3.connect(flask_chest.db_uri)
        cursor = conn.cursor()

        # Ensure the table exists based on the provided schema
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {schema['table_name']} (
                {schema['fields']['unique_id']} INTEGER PRIMARY KEY AUTOINCREMENT, 
                {schema['fields']['date']} TEXT, 
                {schema['fields']['time']} TEXT, 
                {schema['fields']['variable_name']} TEXT, 
                {schema['fields']['variable_value']} TEXT)"""
        )

        # Get current date and time
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Insert a new record
        cursor.execute(
            f"""INSERT INTO {schema['table_name']} 
                            ({schema['fields']['date']}, 
                            {schema['fields']['time']}, 
                            {schema['fields']['variable_name']}, 
                            {schema['fields']['variable_value']}) 
                            VALUES (?, ?, ?, ?)""",
            (date_str, time_str, variable_name, variable_value),
        )

        conn.commit()
        conn.close()
