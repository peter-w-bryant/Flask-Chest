# decorator.py

import uuid
from functools import wraps

from flask import current_app, g, request


def flask_chest(schema_name, tracked, request_id_generator=None):
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
            flask_chest = current_app.extensions.get('flask_chest')
            
            if flask_chest:
                # Get the custom request id value
                request_id = getattr(g, 'custom_request_id', None)

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
                                flask_chest.generic_db_write(schema_name, var, value, request_id)

            return response
        return wrapper
    return decorator
