import os
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, g, request

# From flask-chest package
from flask_chest import FlaskChestSQLite
from flask_chest.decorator import flask_chest
from flask_chest.exporter import FlaskChestExporterInfluxDB


app = Flask(__name__)
chest1 = FlaskChestSQLite(app=app, db_uri="db1.sqlite3")  # Instantiate the chest
chest2 = FlaskChestSQLite(app=app, db_uri="db2.sqlite3")  # Instantiate the chest

# load_dotenv()
# Instantiate the Influx exporter and set it to run every 1 minute
# influx_exporter = FlaskChestExporterInfluxDB(
#     chest=chest,
#     token=os.getenv("INFLUXDB_TOKEN"),
#     interval_minutes=1,
# )

# Define tracked global context variables
route_tracked_vars = {
    "GET": ["user_id", "session_id", "total_time"],
    "POST": ["user_id", "data"],
}


def custom_request_id_generator():
    return str(uuid.uuid4())


@app.route("/", methods=["GET", "POST"])
@flask_chest(
    chests=[chest1, chest2],
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
