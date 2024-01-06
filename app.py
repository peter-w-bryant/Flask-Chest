import logging
import os
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, g, request

# From flask-chest package
from flask_chest import FlaskChestCustomWriter, FlaskChestInfluxDB, FlaskChestSQLite
from flask_chest.decorator import flask_chest

# from flask_chest.exporter import FlaskChestExporterInfluxDB

app = Flask(__name__)

load_dotenv()

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and set the log file path
log_file = "app.log"
file_handler = logging.FileHandler(log_file)

# Create a log formatter and set the format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# chest_sqlite = FlaskChestSQLite(app=app, db_uri="db1.sqlite3")  # Instantiate the chest
chest_influxdb = FlaskChestInfluxDB(
    app=app,
    https=False,
    host="localhost",
    port=8086,
    token=os.getenv("INFLUXDB_TOKEN"),
    org="my-org",
    bucket="my-bucket",
    custom_tags={"app": "tokentrust"},
    logger=logger,
)


def cust_payload_generator(context_tuple_list):
    payload = {}
    for i, context_tuple in enumerate(context_tuple_list):
        payload[i] = context_tuple
    return payload


chest_signalfx = FlaskChestCustomWriter(
    app=app,
    https=False,
    host="localhost",
    port="3000",
    headers=None,
    payload_generator=cust_payload_generator,
    verify=False,
    success_status_codes=[200],
    debug=False,
)

# Define tracked global context variables
route_tracked_vars = {
    "GET": ["user_id", "session_id", "total_time"],
    "POST": ["user_id", "data"],
}


@app.route("/", methods=["GET", "POST"])
@flask_chest(
    chests=[chest_influxdb, chest_signalfx],
    tracked_vars=route_tracked_vars,
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
