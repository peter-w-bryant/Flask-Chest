import datetime
import sqlite3
import traceback

from flask import Flask

from .sqlite_utils import create_sqlite_table, sqlite_write


class FlaskChest:
    def __init__(self, app: Flask, type: str = "sqlite"):
        self.type = type    # Database type
        self.db_uri = None  # Database URI
        self.schemas = {}   # Database schemas

        # Register extension with app
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["flask_chest"] = self

        # Get database URI from app config
        self.db_uri = app.config.get("FLASKCHEST_DATABASE_URI", None)

        # Check if database URI is set
        if self.db_uri is None:
            raise ValueError("FLASKCHEST_DATABASE_URI is not set")

    def register_schema(self, schema_map):
        """
        The function `register_schema` creates storage location registers a schema map in the `schemas` dictionary if the
        database type is SQLite.

        :param schema_map: The `schema_map` parameter is a dictionary that contains information about
        the schema to be registered. It typically includes the following keys:
        """
        try:
            if schema_map["type"] == "sqlite" and self.type == "sqlite":
                # Create SQLite table from given schema
                create_sqlite_table(self.db_uri, schema_map)
                # Add schema to schemas dictionary
                self.schemas[schema_map["name"]] = schema_map

        except Exception:
            print(traceback.print_exc())

    def generic_db_write(
        self, schema_name, variable_name, variable_value, request_id=None
    ):
        """
        The function `generic_db_write` writes a variable value to a database, using the specified
        schema and variable name, and optionally associates it with a request ID.

        :param schema_name: The schema_name parameter refers to the name of the database schema or table
        where the data will be written
        :param variable_name: The variable_name parameter is the name of the variable that you want to
        write to the database
        :param variable_value: The `variable_value` parameter is the value that you want to write to the
        database. It can be any data type such as a string, integer, float, boolean, or even a complex
        data structure like a list or dictionary
        :param request_id: The `request_id` parameter is an optional parameter that represents the
        unique identifier for a specific request. It can be used to track and identify a specific
        request in the database
        """
        try:
            if self.type == "sqlite":
                sqlite_write(
                    self.db_uri, schema_name, variable_name, variable_value, request_id
                )
        except Exception:
            print(traceback.print_exc())