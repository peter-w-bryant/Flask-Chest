# decorator.py

import uuid
from functools import wraps
from typing import Callable, List, Optional
from icecream import ic

from flask import current_app, g, request

from flask_chest import FlaskChest, FlaskChestSQLite


def flask_chest(
    chests: List[FlaskChest],
    tracked_vars: List[str],
    request_id_generator
):
    """
    The `flask_chest` function is a decorator that tracks specified variables and writes them to a table
    in a database after the decorated function is executed.

    :param table_name: The name of the table where the tracked variables will be stored
    :param tracked_vars: The "tracked_vars" parameter is a list of variables that you want to track and store in a
    database table. These variables can be any values that you want to keep track of during the
    execution of the decorated function
    :param request_id_generator: The `request_id_generator` parameter is a function that generates a
    unique request ID for each request. This can be useful for tracking and logging purposes. If no
    `request_id_generator` is provided, the default request ID generator will be used
    :return: The function `decorator` is being returned.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            set_custom_request_id(request_id_generator)
            response = func(*args, **kwargs)
            write_tracked_variables(chests, tracked_vars)
            return response

        return wrapper

    return decorator

def write_tracked_variables(chests: List[FlaskChest], tracked_vars: List[str]) -> None:
    # Write tracked variables to each chest
    for chest in chests:

        request_id = getattr(g, "custom_request_id", None)
        
        # Write tracked variables to database
        for request_method, context_vars in tracked_vars.items():
            if request.method == request_method.upper():
                
                # For each global context var in the list of tracked vars
                for var_name in context_vars:
                    if hasattr(g, var_name):
                        value = getattr(g, var_name)
                        chest.write(var_name, value, request_id)

def set_custom_request_id(request_id_generator: Optional[Callable[[], str]]):
    """
    The function `set_custom_request_id` sets a custom request ID by either using a provided request ID
    generator function or generating a random UUID, and then truncates the ID if it exceeds 255
    characters.

    :param request_id_generator: The `request_id_generator` parameter is a function that generates a
    custom request ID. It should return a unique identifier for each request. If a custom request ID
    generator is not provided, a random UUID (Universally Unique Identifier) will be used instead
    """
    if callable(request_id_generator):
        g.custom_request_id = str(request_id_generator())
    else:
        g.custom_request_id = str(uuid.uuid4())

    # Check if the custom_request_id is too long
    if len(g.custom_request_id) > 255:
        g.custom_request_id = g.custom_request_id[:255]