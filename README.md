# Flask-Chest

<center>

![Flask-Chest Icon](/images/flask_chest_README.png)

</center>

<center>

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</center>

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Flask-Chest Interfaces](#flask-chest-interfaces)
  - [FlaskChestInfluxDB](#flaskchestinfluxdb)
    - [Default Parameter Values for FlaskChestInfluxDB](#default-parameter-values-for-flaskchestinfluxdb)
    - [Sample Usage](#sample-usage)
  - [FlaskChestCustomWriter](#flaskchestcustomwriter)
    - [Default Parameter Values for FlaskChestCustomWriter](#default-parameter-values-for-flaskchestcustomwriter)
    - [Payload Generator Function](#payload-generator-function)
    - [Sample Usage](#sample-usage-1)
- [The `flask_chest` Decorator](#the-flask_chest-decorator)
- [Contributing](#contributing)
- [License](#license)

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

## Flask-Chest Interfaces

### FlaskChestInfluxDB
The `FlaskChestInfluxDB` class is a Flask extension for storing key-value pairs in an InfluxDB database. It provides an interface to write data points to `InfluxDB 2.X` using the `influxdb-client` library.

#### Default Parameter Values for FlaskChestInfluxDB

| Parameter       | Default Value | Description                                                  |
|-----------------|---------------|--------------------------------------------------------------|
| url             | None          | The URL of the InfluxDB server.                              |
| token           | ""            | The InfluxDB authentication token.                           |
| org             | "my-org"      | The InfluxDB organization.                                   |
| bucket          | "my-bucket"   | The InfluxDB bucket.                                         |
| custom_tags     | {}            | Custom tags to be included with each data point.             |
| logger          | None          | Logger instance for logging messages.                        |

The `custom_tags` parameter is optional and can be used to add custom tags to each data point written to InfluxDB. The `logger` parameter is also optional and allows a user to provide a custom logger instance for logging messages

#### Sample Usage

The following code snippet shows how to initialize a `FlaskChestInfluxDB` object in a Flask application. This object will write data points to an InfluxDB database running on `localhost:8086` with the provided authentication token when passed as an argument to the [`flask_chest` decorator](#the-flask_chest-decorator). The data points are written to the `my-bucket` bucket in the `my-org` organization, and custom tags are added to each data point.

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

### FlaskChestCustomWriter
The `FlaskChestCustomWriter` class allows for writing key-value pairs to a custom backend by making HTTP POST requests with a custom payload.

#### Default Parameter Values for FlaskChestCustomWriter

| Parameter          | Default Value | Description                                                  |
|--------------------|---------------|--------------------------------------------------------------|
| url                | None          | The URL of the custom writer will POST data to.              |
| headers            | None          | HTTP headers to be sent with the POST request.               |
| params             | None          | URL parameters to be sent with the POST request.             |
| proxies            | None          | Proxy URLs to be used for the POST request.                  |
| payload_generator  | None          | A function that generates the payload for the POST request (see [Payload Generator Function](#payload-generator-function)). |
| verify             | False         | Whether to verify the server's TLS certificate.              |
| success_status_codes | [200]       | List of HTTP status codes considered as success.             |
| logger             | None          | Logger instance for logging messages.                        |


#### Payload Generator Function
When using the `FlaskChestCustomWriter` class, a `payload_generator` function must be provided. This function is used to generate the payload for the POST request every time the [`flask_chest` decorator](#the-flask_chest-decorator) is applied to a Flask route. This function must take a list of 3-tuples as an argument and it can return any payload (e.g. a string, a dictionary, etc.), as long as it is JSON serializable. The payload will be sent as the body of the POST request to the custom writer.

Each 3-tuple in the list represents a global context variable to be written to the provided endpoint. The first element of the tuple is a string representing the name of the variable, the second element is the value of the variable, and the third element is a string representing the unique ID of the request. Thus, each 3-tuple is an object of the form `(variable_name, variable_value, request_id)`. The order of the tuples in the list is the same as the order of the variables in the `tracked_vars` parameter of the [`flask_chest` decorator](#the-flask_chest-decorator).

#### Sample Usage
The following code snippet shows how to initialize a `FlaskChestCustomWriter` object in a Flask application. This object logs all DEBUG messages using the provided logger instance, does not verify the server's TLS certificate, considers HTTP status codes `200` and `201` as success, does not send any headers or URL parameters with the POST request, does not use any proxies, uses a custom payload generator function, and writes data points to a custom writer running on `localhost:3000`. The data points are written to the custom writer using a custom payload generator function; in this case, the payload is a dictionary where the keys are integers and the values are tuples of the form `(variable_name, variable_value, request_id)`.

```python
from typing import List, Tuple, Dict
def cust_payload_generator(context_tuple_list: List[Tuple[str, Any, str]]):
    """Generates a data payload for the custom writer.
    Args:
        context_tuple_list (List[Tuple[str, Any, str]]): A list of tuples of the form
        (variable_name, variable_value, request_id)

    Returns:
        Dict[int, Tuple[str, str, str]]: A dictionary of the form
        {0: (variable_name, variable_value, request_id), 1: (variable_name, variable_value, request_id), ...}
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

## The `flask_chest` Decorator
The `flask_chest` decorator is used to track and write specified variables to the configured backends (chests) after a Flask route function is executed.

### Default Parameter Values for `flask_chest` Decorator

| Parameter            | Default Value | Description                                                  |
|----------------------|---------------|--------------------------------------------------------------|
| chests               | None          | List of FlaskChest instances to write data to.               |
| tracked_vars         | None          | List of variables to track and write.                        |
| request_id_generator | `lambda: str(uuid.uuid4())` | A function that generates a unique request ID.               |
| raise_exceptions     | True          | Whether to raise exceptions if writing to a chest fails.     |

The `chests` parameter is a list of `FlaskChest` objects that the decorator will write to. The `tracked_vars` parameter is a list of strings representing the names of the variables to track and write to the chests. If this parameter is set to `None`, all variables in `g.variables` will be tracked and written to the chests.

The `request_id_generator` parameter is a function that should return a unique identifier for each request as a string. This ID is used to track and identify specific requests in the database, and can be used to trace the data back to the request that generated it. The default value for this parameter is a lambda function that returns a UUID4 string.

The `raise_exceptions` parameter is a boolean that determines whether exceptions should be raised if writing to a chest fails. If set to `False`, exceptions will not be raised, and the decorator will continue to execute the route function.

### Sample Usage
The following code snippet shows how to apply the `flask_chest` decorator to a Flask route. During a `GET` request, this decorator will write the variables `user_id`, `session_id`, and `total_time` to the configured chests after the route function is executed. The `request_id_generator` parameter is set to a custom function that returns a string representing the current date and time.

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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. View the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
