<!-- Import custom.css -->
<link rel="stylesheet" type="text/css" href="_static/custom.css">

# Sample Usage

## Example: Exporting SLIs to Multiple Targets
Suppose you have a Flask app that is serving an API, and you want to report on [Service Level Indicators](https://sre.google/sre-book/service-level-objectives/) (SLIs) to both an <u>InfluxDB 2.x instance</u> and <u>[SignalFX](https://www.splunk.com/en_us/about-splunk/acquisitions/signalfx.html)</u>. For this example, your SLIs are <b>total transactions</b> and <b>average response time of POST requests</b> to a single API endpoint. You want to track these SLIs for each request made to the API, and export them to both backends, so that you can <u>monitor and analyze the performance of your API in real-time</u>.<br>

<center>
<figure>
<img src="_static/flask_chest_simple_diagram.png" style="width:600px;"/>
<figcaption>Fig 1: Multi-target data flow diagram showing how data is exported from the view function of a Flask route to multiple backends using the `Flask-Chest` package.</figcaption>
</figure>
</center><br>

This example uses the following `FlaskChest` objects:
- `FlaskChestInfluxDB`, to establish a connection to an InfluxDB 2.x instance and write data points to a specified bucket.
- `FlaskChestCustomWriter`, to post data points to a SignalFX endpoint over HTTP.

As well as the `flask_chest` decorator to track global context variables and write data points to the specified backends.

## Imports
First you must import `FlaskChestInfluxDB`, `FlaskChestCustomWriter`, and the `flask_chest` decorator from the `flask-chest`package.

```python
from flask_chest import FlaskChestCustomWriter, FlaskChestInfluxDB
from flask_chest.decorator import flask_chest
```

Then you must initialize each chest object with their respective parameters.

## FlaskChestInfluxDB
Our `FlaskChestInfluxDB` will:
- Write data points to an InfluxDB 2.x database running on `http://localhost:8086` to the `my-bucket` bucket in the `my-org` organization with the provided authentication token.
- Include custom tags with each data point.
- Log all messages using the provided logger instance.

```python
chest_influxdb = FlaskChestInfluxDB(
    name="InfluxDB"
    url="http://localhost:8086",
    token=os.getenv("INFLUXDB_TOKEN"),
    org="my-org",
    bucket="my-bucket",
    custom_tags={"app": "your-app-name"},
    logger=logger,
)
```
## FlaskChestCustomWriter
Then we must initialize our `FlaskChestCustomWriter` object, which will post data points to a SignalFX endpoint listening on `http://localhost:3000`. To create an instance of `FlaskChestCustomWriter`, we must write a function that will return a data payload when passed the [context tuple list](interfaces.md#payload-generator-function).

Here is a simple <b>payload generator</b> that returns a dictionary mapping the index of each 3-tuple in the list of 3-tuples, to the 3-tuple itself.
```python
def cust_payload_generator(context_tuple_list: List[Tuple[str, str, str]]):
    payload = {}
    for i, context_tuple in enumerate(context_tuple_list):
        payload[i] = context_tuple
    return payload
```

Our `FlaskChestCustomWriter` will:
- Use the custom payload generator function to generate the payload for the POST request.
- Log all messages using the provided logger instance.
- Not verify the server's TLS certificate.
- Consider HTTP status codes `200` and `201` as success.

```python
chest_signalfx = FlaskChestCustomWriter(
    name="SignalFX",
    url="http://localhost:3000",
    payload_generator=cust_payload_generator,
    verify=False,
    success_status_codes=[200, 201],
    logger=logger,
)
```

## `flask_chest` Decorator
Now that the Flask Chest objects are initialized, we can apply our `flask_chest` decorator to our desired Flask route to start exporting. For this example app, lets use the following simple Flask index route,

```python
@app.route("/api-endpoint", methods=["GET", "POST"])
@flask_chest(
    chests=[chest_influxdb, chest_signalfx],
    tracked_vars={
        "GET": ["transaction"],
        "POST": ["transaction", "response_time"],
    },
)
def index():
    g.start = time.time()
    if request.method == "POST":
        g.transaction = 1
        g.response_time = time.time() - g.start
        return "Hello, World!"
    g.transaction = 1
    g.response_time = time.time() - g.start
    return "Hello, World!"
```

Another optional parameter we can provide the `flask_chest` decorator is a `request_id_generator`. This function will execute every time a request is made to the route. For this example, we will use the current date and time as a formatted string to distinguish requests made to the route.

```python
def custom_request_id_generator():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")
```

With our `FlaskChest` objects, our tracked variables dictionary, and our `request_id_generator` function initialized, we can now apply the `flask_chest` decorator to our index route like so,

```python
@app.route("/", methods=["GET", "POST"])
@flask_chest(
    chests=[chest_influxdb, chest_signalfx],
    tracked_vars={
        "GET": ["transaction"],
        "POST": ["transaction", "response_time"],
    },
    request_id_generator=custom_request_id_generator,
)
def index():
    g.start = time.time()
    if request.method == "POST":
        g.transaction = 1
        g.response_time = time.time() - g.start
        return "Hello, World!"
    g.transaction = 1
    g.response_time = time.time() - g.start
    return "Hello, World!"
```

With the `flask_chest` decorator applied to our route, the `Flask-Chest` package will automatically track and export the global context variables `g.transaction` and `g.response_time` to both the InfluxDB 2.x instance and the SignalFX endpoint every time the route is accessed.

From both databases, you can now monitor and analyze the performance of your API in real-time, and use the data to make informed decisions about the performance of your API. For transaction data, you can perform a sum aggregation to get the total number of transactions made to the API, and for response time data, you can perform an average aggregation to get the average response time of POST requests to the API.