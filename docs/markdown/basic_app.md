# Basic Application
The following code snippet shows how to initialize a `FlaskChestInfluxDB` object in a Flask application. This object will write data points to an InfluxDB database running on `localhost:8086` with the provided authentication token when passed as an argument to the `flask_chest` decorator. The data points are written to the `my-bucket` bucket in the `my-org` organization, and custom tags are added to each data point.

```python
chest_influxdb = FlaskChestInfluxDB(
    url="http://localhost:8086",
    token=os.getenv("INFLUXDB_TOKEN"),
    org="my-org",
    bucket="my-bucket",
    custom_tags={"app": "your-app-name"},
    logger=logger,
)
```

```python
from typing import List, Tuple, Dict
def cust_payload_generator(context_tuple_list: List[Tuple[str, Any, str]]):
    """Generates a data payload for the custom writer.
    Args:
        context_tuple_list (List[Tuple[str, Any, str]]): A list of tuples of the form
        (variable_name, variable_value, request_id)
    """
    payload = {}
    for i, context_tuple in enumerate(context_tuple_list):
        payload[i] = context_tuple
    return payload

chest_custom_writer = FlaskChestCustomWriter(
    url="http://localhost:3000",
    headers=None,
    params=None,
    payload_generator=cust_payload_generator,
    verify=False,
    success_status_codes=[200, 201],
    logger=logger,
)
```

The following code snippet shows how to apply the `flask_chest` decorator to a Flask route. During a `GET` request, this decorator will write the variables `user_id`, `session_id`, and `total_time` to the configured chests after the route function is executed. The `request_id_generator` parameter is set to a custom function that returns a string representing the current date and time.

#### Sample Usage
The following code snippet shows how to initialize a `FlaskChestCustomWriter` object in a Flask application. This object logs all DEBUG messages using the provided logger instance, does not verify the server's TLS certificate, considers HTTP status codes `200` and `201` as success, does not send any headers or URL parameters with the POST request, does not use any proxies, uses a custom payload generator function, and writes data points to a custom writer running on `localhost:3000`. The data points are written to the custom writer using a custom payload generator function; in this case, the payload is a dictionary where the keys are integers and the values are tuples of the form `(variable_name, variable_value, request_id)`.

```python
def custom_request_id_generator():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S%f")

# Define tracked global context variables
route_tracked_vars = {
    "GET": ["user_id", "session_id", "total_time"],
    "POST": ["user_id", "data"],
}

@app.route("/", methods=["GET", "POST"])
@flask_chest(
    chests=[chest_influxdb, chest_custom_writer],
    tracked_vars=route_tracked_vars,
    request_id_generator=custom_request_id_generator,
    raise_exceptions=False,
)
def index():
    if request.method == "GET":
        g.start = time.time()
        g.user_id = "123"
        g.session_id = "abc"
        time.sleep(0.1)  # Simulate a delay
        g.total_time = time.time() - g.start
    return "Hello, World!"
```