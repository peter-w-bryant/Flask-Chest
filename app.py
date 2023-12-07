from flask import Flask, g

from flask_chest import FlaskChest
from flask_chest.decorator import flask_chest

app = Flask(__name__)
app.config['db_uri'] = 'db.sqlite'  # Updated configuration key
chest = FlaskChest(app, app.config['db_uri'])      # Using the updated configuration key

# Define the schema for the database
metric_schema = {
    'table_name': 'metrics',
    'fields': {
        'unique_id': 'unique_id',
        'date': 'date',
        'time': 'time',
        'variable_name': 'variable_name',
        'variable_value': 'variable_value'
    }
}

# Define which g.variables to track for each request method
tracked_metrics = {
    'GET': ['user_id', 'session_id'],
    'POST': ['user_id', 'data']
}

@app.route('/', methods=['GET', 'POST'])
@flask_chest(metric_schema, tracked_metrics)
def index():
    g.user_id = '12365'
    g.session_id = 'abcdef'
    # ... route logic ...
    return "Hello, World!"

if __name__ == '__main__':
    app.run()
