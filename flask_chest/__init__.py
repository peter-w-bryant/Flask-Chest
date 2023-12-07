from flask import Flask


class FlaskChest:
    def __init__(self, app: Flask, db_uri: str):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['flask_chest'] = self
        self.db_uri = db_uri

        # Initialize database connection
        self.init_db(app)

    def init_db(self, app):
        # Database initialization logic
        pass
