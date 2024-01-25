> &#128204; Last updated : 2024-1-24 
# Interfaces [![GitHub Issues](https://img.shields.io/github/issues/peter-w-bryant/Flask-Chest)](https://github.com/peter-w-bryant/Flask-Chest/issues)

- [Flask Chests](#flask-chests)
  - [FlaskChestCustomWriter](#flaskchestcustomwriter)
    - [Payload Generator Function](#payload-generator-function)
  - [FlaskChestInfluxDB](#flaskchestinfluxdb)
- [The flask_chest Decorator](#the-flask_chest-decorator)

---

## Flask Chests
`FlaskChest` objects are <u>an abstraction layer for different databases</u> (and other backends). Once initialized, they can be passed as arguments to the [`flask_chest` decorator](#the-flask-chest-decorator) to write data to their respective backends.

At the time of writing, the following `FlaskChest` objects are implemented:
- [`FlaskChestCustomWriter`](#flaskchestcustomwriter)
- [`FlaskChestInfluxDB`](#flaskchestinfluxdb)
- [`FlaskChestPrometheus`](#flaskchestprometheus)
- `FlaskChestSQLite`
- `FlaskChestMySQL`

### FlaskChestCustomWriter
The `FlaskChestCustomWriter` class allows for writing to a custom backend by making HTTP POST requests with a custom payload. 

| Parameter (*=required)           | Default Value | Description                                                  |
|--------------------|---------------|--------------------------------------------------------------|
| url*                | None         | The URL the custom writer will POST data to.                 |
| payload_generator*  | None         | A function that generates the payload for the POST request (see [Payload Generator Function](#payload-generator-function)). |
| name               | url           | The name of the custom writer (useful for logging).          |
| headers            | None          | HTTP headers to be sent with the POST request.               |
| params             | None          | URL parameters to be sent with the POST request.             |
| proxies            | None          | Proxy URLs to be used for the POST request.                  |
| verify             | False         | Whether to verify the server's TLS certificate.              |
| success_status_codes | [200]       | List of HTTP status codes considered as success.             |
| logger             | None          | Logger instance for logging INFO, DEBUG, and ERROR messages. |

#### Payload Generator Function
```python
def payload_generator(variables: List[Tuple[str, Any, str]]) -> Any:
```
When using the `FlaskChestCustomWriter` class, a payload generator function must be provided, but <i>can be named anything</i>. This function is used to <b>generate the JSON body for the POST request</b> every time the `flask_chest` decorator is applied to a Flask route.

This function must implement the following interface:
- It must take a list of 3-tuples as an argument. Each 3-tuple is a global context variable of the form `(variable_name, variable_value, request_id)`. The order of the tuples in the list is the same as the order of the variables in the `tracked_vars` parameter of the [`flask_chest`](#the-flask_chest-decorator) decorator.
- It must return a JSON serializable payload (e.g. a string, a dictionary, etc.).

## FlaskChestInfluxDB
The `FlaskChestInfluxDB` class allows for writing to an InfluxDB database. It provides an interface to write data points to instances of `InfluxDB 2.X` using the `influxdb-client` library.

| Parameter       | Default Value | Description                                                  |
|-----------------|---------------|--------------------------------------------------------------|
| url*             | None          | The URL of the InfluxDB server.                              |
| token*           | ""            | The InfluxDB authentication token.                           |
| org*             | "my-org"      | The InfluxDB organization.                                   |
| bucket*          | "my-bucket"   | The InfluxDB bucket.                                         |
| custom_tags     | {}            | Custom tags to be included with each data point.             |
| logger          | None          | Logger instance for logging messages.                        |

The `custom_tags` parameter is optional and can be used to add custom tags to each data point written to InfluxDB. The `logger` parameter is also optional and allows a user to provide a custom logger instance for logging messages.

---

## The flask_chest Decorator
The `flask_chest` decorator is used to track and write specified variables to the configured backends (chests) after a Flask route function is executed.

| Parameter            | Default Value | Description                                                  |
|----------------------|---------------|--------------------------------------------------------------|
| chests*               | None          | List of FlaskChest instances to write data to.               |
| tracked_vars*         | None          | Dictionary mapping HTTP methods to lists of tracked variables. |
| request_id_generator | `lambda: str(uuid.uuid4())` | A function that generates a unique request ID.               |
| raise_exceptions     | True          | Whether to raise exceptions if writing to a chest fails.     |

The `chests` parameter is a list of `FlaskChest` objects that the decorator will write to. The `tracked_vars` parameter is a dictionary specifying which global context variables to write to the chests per request method. If this parameter is set to `None`, all variables in `g.variables` will be tracked and written to the chests.

The `request_id_generator` parameter is a function that should return a unique identifier for each request as a string. This ID is used to track and identify specific requests in the database, and can be used to trace the data back to the request that generated it. The default value for this parameter is a lambda function that returns a [UUID4](https://docs.python.org/3/library/uuid.html) string.

The `raise_exceptions` parameter is a boolean that determines whether exceptions should be raised if writing to a chest fails. If set to `False`, exceptions will not be raised, and the decorator will continue to execute the route function.