# decorator.py

import uuid
from functools import wraps

from flask import current_app, g, request


def flask_chest(schema_name, tracked, request_id_generator=None):
    """
    The `flask_chest` function is a decorator that can be used to track and log variables in a Flask
    application.

    :param schema_name: The `schema_name` parameter is a string that represents the name of the database
    schema where the variables will be stored
    :param tracked: The `tracked` parameter is a dictionary that maps HTTP request methods to a list of
    variables that you want to track. For example, if you want to track the variables `var1` and `var2`
    for the `GET` and `POST` methods, you would pass `tracked={"
    :param request_id_generator: The `request_id_generator` parameter is an optional function that
    generates a custom request ID. This function is called to generate a unique identifier for each
    request. If no custom generator function is provided, a default unique identifier is generated using
    the `uuid.uuid4()` function
    :return: The decorator function "wrapper" is being returned.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if a custom request_id generator function is provided
            if callable(request_id_generator):
                g.custom_request_id = request_id_generator()
            else:
                # Set a default unique identifier if no custom generator is provided
                g.custom_request_id = str(uuid.uuid4())

            # Response is the return value of the decorated function
            response = func(*args, **kwargs)
            
            # Access Flask-Chest extension
            flask_chest = current_app.extensions.get("flask_chest")
            
            if flask_chest:
                # Get the custom request id value
                request_id = getattr(g, "custom_request_id", None)
                # Get each request method and variable list in the tracked dictionary
                for method, variables in tracked.items():
                    # If the current request method is in the tracked dictionary
                    if request.method == method.upper():
                        # For each variable in the tracked dictionary
                        for var in variables:
                            # If the variable is in the global context
                            if hasattr(g, var):
                                # Write the variable to the database
                                value = getattr(g, var)
                                # Write the variable to the database
                                flask_chest.generic_db_write(
                                    schema_name, var, value, request_id
                                )

            return response

        return wrapper

    return decorator
