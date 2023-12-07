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
