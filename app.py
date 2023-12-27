# app.py

import time
import uuid

from flask import Flask, g, request

from flask_chest import FlaskChestSQLite
from flask_chest.decorator import flask_chest
from flask_chest.exporter import FlaskChestExporterInfluxDB

app = Flask(__name__)

# Interface for FlaskChest with SQLite
chest = FlaskChestSQLite(app=app, db_uri="db.sqlite3")

influx_exporter = FlaskChestExporterInfluxDB(
    app,
    host="localhost",
    port=8086,
    username="my-user",
    password="my-password",
    dbname="influxdb-2.x",
)

influx_exporter.setup_periodic_task()

# chest.mount_exporter(exporter=exporter)

# Define tracked metrics
route_tracked_vars = {
    # 'REQUEST_METHOD': ['VARIABLE_NAME']
    "GET": ["user_id", "session_id", "total_time"],
    "POST": ["user_id", "data"],
}


def custom_request_id_generator():
    return str(uuid.uuid4())


@app.route("/", methods=["GET", "POST"])
@flask_chest(
    tracked_vars=route_tracked_vars,
    request_id_generator=custom_request_id_generator,
)
def index():
    if request.method == "GET":
        g.start = time.time()
        g.user_id = "123"
        g.session_id = "abc"
        time.sleep(0.1)
        g.total_time = time.time() - g.start
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
