import datetime
import json
import sqlite3
import traceback

from flask import Flask

from .sqlite_utils import create_sqlite_table, sqlite_write

SQLITE_DEFAULT_SCHEMA = {
    "name": "sqlite_default",
    "fields": {
        "variable_name": "TEXT",
        "variable_value": "TEXT",
    },
}


class FlaskChest:
    def __init__(self, app: Flask):
        self.app = app  # Flask app

        # Register extension with app
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["flask_chest"] = self


class FlaskChestSQLite(FlaskChest):
    def __init__(self, app: Flask, db_uri: str = "db.sqlite3"):
        super().__init__(app)
        self.db_uri = None  # Database URI
        self.tables = {}  # Database tables

        # Get database URI from app config
        self.db_uri = db_uri

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        return {
            "db_uri": self.db_uri,
            "tables": self.tables,
        }

    def register_table(self, schema=None, default_schema=True, table_name=None):
        try:
            # Configure default schema if selected
            if default_schema:
                schema = SQLITE_DEFAULT_SCHEMA
                # If table_name is specified, override default table name
                if table_name is not None:
                    schema["name"] = table_name

            # Create SQLite table from given schema, table_exists if table is created or already exists
            table_exists = create_sqlite_table(self.db_uri, schema)

            if not table_exists:
                raise Exception("Unable to register table!")

            # Add schema to schemas dictionary
            self.tables[schema["name"]] = schema

        except Exception:
            print(traceback.print_exc())
            raise Exception("Error occurred when registering table!")

    def write(self, schema_name, variable_name, variable_value, request_id=None):
        try:
            successful_write = sqlite_write(
                self.db_uri,
                self.tables[schema_name],
                variable_name,
                variable_value,
                request_id,
            )
            
            if not successful_write:
                raise Exception("Unable to write to database!")

        except Exception:
            print(traceback.print_exc())
