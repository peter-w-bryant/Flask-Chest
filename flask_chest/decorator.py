# decorator.py

import uuid
from functools import wraps

from flask import current_app, g, request

from .db_utils import write_to_db


def flask_chest(schema, tracked_metrics):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if a custom request_id generator function is provided
            request_id_generator = schema.get('custom_request_id')
            if callable(request_id_generator):
                g.custom_request_id = request_id_generator()
            else:
                # Set a default unique identifier if no custom generator is provided
                g.custom_request_id = str(uuid.uuid4())

            response = func(*args, **kwargs)
            
            # Access Flask-Chest extension
            flask_chest = current_app.extensions.get('flask_chest')
            if flask_chest:
                request_id = getattr(g, 'custom_request_id', None)

                for method, variables in tracked_metrics.items():
                    if request.method == method.upper():
                        for var in variables:
                            if hasattr(g, var):
                                value = getattr(g, var)
                                write_to_db(schema, var, value, request_id)

            return response
        return wrapper
    return decorator
