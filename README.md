# Flask-Chest

![Flask-Chest Icon](flask_chest.png)

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)


## Introduction

Flask-Chest is a versatile Python package designed for Flask applications. It provides a decorator for Flask routes to track and record specific global variables (`g.variables`) for each request. The package supports dynamic tracking and stores metrics in a SQLite database, making it an ideal tool for monitoring and analytics in Flask web applications.

## Features

- Easy integration with Flask applications.
- Customizable tracking of `g.variables` based on request methods.
- Automatic or custom-defined request IDs for unique tracking.
- Efficient storage of metrics in a SQLite database with a user-defined schema.

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
# app.py

import time
import uuid
from datetime import datetime

from flask import Flask, g

from flask_chest import FlaskChest
from flask_chest.decorator import flask_chest

app = Flask(__name__)
app.config['db_uri'] = 'db.sqlite3'
chest = FlaskChest(app, app.config['db_uri'])

# Function to compute a unique request ID (e.g., current epoch time)
# def custom_request_id_generator():
#     return str(int(time.time()))

# def custom_request_id_generator():
#     return str(uuid.uuid4())

def custom_request_id_generator():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S%f")

# Define the schema for the database
db_schema = {
    'table_name': 'metrics',
    'fields': {
        'unique_id': 'unique_id',
        'request_id': 'request_id',
        'date': 'date',
        'time': 'time',
        'variable_name': 'variable_name',
        'variable_value': 'variable_value'
    },
    # 'custom_request_id': custom_request_id_generator  # Function to generate custom request ID
}

# Define tracked metrics
tracked_metrics = {
    'GET': ['user_id', 'session_id'],
    'POST': ['user_id', 'data']
}

@app.route('/', methods=['GET', 'POST'])
@flask_chest(db_schema, tracked_metrics)
def index():
    g.user_id = '123'
    g.session_id = 'abc'
    return "Hello, World!"

if __name__ == '__main__':
    app.run()
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.