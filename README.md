# Flask-Chest

![Flask-Chest Icon](images/flask_chest_README.png)

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Introduction

Flask-Chest is a Python package for Flask applications, providing a decorator to track and record global context variables (`g.variables`) for each request. It interfaces with various databases to store and export these variables, serving as a tool for monitoring and analytics in Flask web applications.

## Features

- Tracks and records `g.variables` in Flask routes, allowing for the storage of contextual data in a configured database.
- Offers customizable request ID generation, ensuring unique identification of each request for better traceability and analysis of contextual data.
- Provides support for multiple databases, including SQLite, MySQL, PostgreSQL, and MongoDB, enabling flexibility in choosing the appropriate database for the application.
- Implements thread-safe data exporters, scheduled using AP Scheduler, to reliably and periodically export the recorded data, facilitating monitoring and analytics.

## Installation

```bash
pip install flask-chest
```

## Usage

1. Import and initialize Flask-Chest in your Flask application.
2. Import and initialize the desired exporter(s) for data export.
3. Define the variables to be tracked in the `@flask_chest` decorator. The tracked variables map should be a dictionary where each HTTP method (e.g., "GET", "POST") is a key, and the value is a list of strings representing the names of the variables to track.
4. Provide a request ID generator function that returns a unique string identifier for each request. If no custom generator is provided, a UUID4 string will be used by default.
5. Apply the `@flask_chest` decorator to Flask routes.

## List of Exporters
- FlaskChestExporterInfluxDB: Exports data to an InfluxDB database.

_Coming soon_:
- FlaskChestExporterMongoDB: Exports data to a MongoDB database.
- FlaskChestExporterMySQL: Exports data to a MySQL database.
- FlaskChestExporterPostgreSQL: Exports data to a PostgreSQL database.

### Example:
This code snippet showcases a Flask application that leverages Flask-Chest, utilizing a local SQLite database for caching and an InfluxDB database for exporting. It demonstrates the implementation of tracked variables and a custom request ID generator.

```python
import os
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, g, request

# From flask-chest package
from flask_chest import FlaskChestSQLite
from flask_chest.decorator import flask_chest
from flask_chest.exporter import FlaskChestExporterInfluxDB

load_dotenv()
app = Flask(__name__)

# Instantiate the chest
chest = FlaskChestSQLite(app=app, db_uri="db.sqlite3")  

# Instantiate the Influx exporter and set it to run every 1 minute
influx_exporter = FlaskChestExporterInfluxDB(
    chest=chest,
    token=os.getenv("INFLUXDB_TOKEN"),
    interval_minutes=1,
)

# Define tracked global context variables
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

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
