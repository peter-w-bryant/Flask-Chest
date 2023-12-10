# decorator.py

import uuid
from functools import wraps

from flask import current_app, g, request


def flask_chest(schema_name, tracked, request_id_generator=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            set_custom_request_id(request_id_generator)
            response = func(*args, **kwargs)
            write_tracked_variables(schema_name, tracked)
            return response

        return wrapper

    return decorator


def set_custom_request_id(request_id_generator):
    if callable(request_id_generator):
        g.custom_request_id = str(request_id_generator())
    else:
        g.custom_request_id = str(uuid.uuid4())

    # Check if the custom_request_id is too long
    if len(g.custom_request_id) > 255:
        g.custom_request_id = g.custom_request_id[:255]


def write_tracked_variables(schema_name, tracked):
    flask_chest = current_app.extensions.get("flask_chest")
    if flask_chest:
        request_id = getattr(g, "custom_request_id", None)
        for request_method, context_vars in tracked.items():
            if request.method == request_method.upper():
                for var in context_vars:
                    if hasattr(g, var):
                        value = getattr(g, var)
                        flask_chest.write(schema_name, var, value, request_id)
