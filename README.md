# Flask-Chest

![Flask-Chest Icon](flask_chest_README.png)

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)


## Introduction

Flask-Chest is a versatile Python package designed for Flask applications. It provides a decorator for Flask routes to track and record user-determined global context variables (`g.variables`) for each request. 

The package supports the dynamic tracking and storing of context variables in your configured `FlaskChest` object, an abstraction for your database; it also provides numerous exporters that will write your data to your database of choice, making it an ideal tool for simple monitoring and analytics in Flask web applications.

## Features

- Easy integration with Flask applications.
- Customizable tracking of `g.variables` based on request methods.
- Automatic or custom-defined request IDs for unique tracking of context variables initialized during the same request.
- Support for multiple database types (SQLite, MySQL, PostgreSQL, MongoDB, etc.).
- Exporters for writing data to your database of choice.

## How to Install

```bash
pip install flask-chest
```

## How to Use
Import and initialize Flask-Chest in your Flask application.
Define a schema and tracked metrics.
Apply the @flask_chest decorator to your routes.
Example:

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
chest = FlaskChestSQLite(app=app, db_uri="db.sqlite3")  # Instantiate the chest

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
This project is licensed under the MIT License - see the LICENSE file for details.
