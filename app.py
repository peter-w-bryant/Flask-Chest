import os
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, g, request

# From flask-chest package
from flask_chest import FlaskChestSQLite, FlaskChestInfluxDB, FlaskChestCustomWriter
from flask_chest.decorator import flask_chest
# from flask_chest.exporter import FlaskChestExporterInfluxDB

app = Flask(__name__)

load_dotenv()

# chest_sqlite = FlaskChestSQLite(app=app, db_uri="db1.sqlite3")  # Instantiate the chest
# chest_influxdb = FlaskChestInfluxDB(
#     app=app,
#     https=False,
#     host="localhost",
#     port=8086,
#     token=os.getenv("INFLUXDB_TOKEN"),
#     org="my-org",
#     bucket="my-bucket",
# )

def cust_payload_generator(variable_name, variable_value, request_id):
    return {"variable_name": variable_name,
            "variable_value": variable_value,
            "request_id": request_id}

chest_signalfx = FlaskChestCustomWriter(
    app=app,
    https=False,
    host="localhost",
    port="3000",
    headers=None,
    payload_generator=cust_payload_generator,
    verify=False,
    success_status_codes = [200],
    debug=False,
)

# Define tracked global context variables
route_tracked_vars = {
    "GET": ["user_id", "session_id", "total_time"],
    "POST": ["user_id", "data"],
}

@app.route("/", methods=["GET", "POST"])
@flask_chest(
    chests=[chest_signalfx],
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
