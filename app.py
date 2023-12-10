# app.py

import time
import uuid

from flask import Flask, g

from flask_chest import FlaskChestSQLite
from flask_chest.decorator import flask_chest

app = Flask(__name__)
chest = FlaskChestSQLite(app=app, db_uri="db.sqlite3")

def custom_request_id_generator():
    return str(uuid.uuid4())

# With default schema
chest.register_table(default_schema=True, table_name="metrics")

# Define tracked metrics
route_tracked_vars = {
    # 'REQUEST_METHOD': ['VARIABLE_NAME']
    "GET": ["user_id", "session_id", "total_time"],
    "POST": ["user_id", "data"],
}

@app.route("/", methods=["GET", "POST"])
@flask_chest(
    schema_name="metrics",
    tracked=route_tracked_vars,
    request_id_generator=custom_request_id_generator,
)
def index():
    g.start = time.time()
    g.user_id = "123"
    g.session_id = "abc"
    time.sleep(0.3)
    g.total_time = time.time() - g.start
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
