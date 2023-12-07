from functools import wraps

from flask import current_app, g, request

from .db_utils import write_to_db  # Import the function


def flask_chest(schema, tracked_metrics):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            
            # Access Flask-Chest extension
            flask_chest = current_app.extensions.get('flask_chest')
            if flask_chest:
                for method, variables in tracked_metrics.items():
                    if request.method == method.upper():
                        for var in variables:
                            if hasattr(g, var):
                                value = getattr(g, var)
                                write_to_db(schema, var, value)  # Call the function directly

            return response
        return wrapper
    return decorator
