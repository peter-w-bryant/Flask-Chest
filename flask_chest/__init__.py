from flask import Flask


class FlaskChest:
    def __init__(self, app: Flask):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['flask_chest'] = self
        
        self.db_uri = app.config.get("FLASKCHEST_DATABASE_URI", None)
        
        if self.db_uri is None:
            raise ValueError("FLASKCHEST_DATABASE_URI is not set")
            
        # Initialize database connection
        self.init_db(app)

    def init_db(self, app):
        # Database initialization logic
        pass
