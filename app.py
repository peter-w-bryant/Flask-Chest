import os
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, g, request

from flask_chest import FlaskChestSQLite
from flask_chest.decorator import flask_chest
from flask_chest.exporter import FlaskChestExporterInfluxDB  # Import the exporter class

app = Flask(__name__)
load_dotenv()
influxdb_token = os.getenv("INFLUXDB_TOKEN")

# Interface for FlaskChest with SQLite
chest = FlaskChestSQLite(app=app, db_uri="db.sqlite3")

# Instantiate the Influx exporter and set it to run every 1 minute
influx_exporter = FlaskChestExporterInfluxDB(
    app=app,
    token=influxdb_token,
    interval_minutes=1,  # Export data every 1 minute
)

# Define tracked metrics
route_tracked_vars = {
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
        time.sleep(0.1)  # Simulate a delay
        g.total_time = time.time() - g.start
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
