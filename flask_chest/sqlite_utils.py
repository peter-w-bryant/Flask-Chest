import datetime
import sqlite3
import traceback

from icecream import ic


def sqlite_write(db_uri, schema, variable_name, variable_value, request_id):
    try:
        conn = sqlite3.connect(db_uri)
        cursor = conn.cursor()
        
        # Get table name and fields from schema dictionary
        table_name = schema["name"]
        fields = schema["fields"]
        
        # Create table if not exists
        field_definitions = "unique_id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT, "
        field_definitions += ", ".join([f"{field} {data_type}" for field, data_type in fields.items()])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})")
        
        # Create placeholders for the field values
        placeholders = ", ".join(["?" for _ in fields])
        
        # Insert a new record
        field_names = ", ".join(fields.keys())
        
        field_values = [request_id, variable_name, variable_value]
        cursor.execute(f"INSERT INTO {table_name} (request_id, {field_names}) VALUES (?, {placeholders})", field_values)
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(traceback.print_exc())
        return False


def create_sqlite_table(db_uri, schema_map):
    """
    Create a SQLite table based on the provided schema map.

    Args:
        db_uri (str): The URI of the SQLite database.
        schema_map (dict): A dictionary containing the schema information for the table.

    Returns:
        bool: True if the table is created successfully, False otherwise.
    """
    try:
        # Connect to database
        conn = sqlite3.connect(db_uri)
        cursor = conn.cursor()

        # Get table name and fields from schema map
        table_name = schema_map["name"]
        fields = schema_map["fields"]

        # Create field definitions (e.g. "unique_id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT, field1 DATATYPE, field2 DATATYPE, ...")
        field_definitions = "unique_id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT, " + ", ".join(
            [f"{field} {data_type}" for field, data_type in fields.items()]
        )

        # Create table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})")

        # Commit and close connection
        conn.commit()
        conn.close()
        return True

    # Except if connection fails
    except Exception as e:
        print(traceback.print_exc())

    return False
