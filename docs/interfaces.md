````{note}
Last updated : 2024-2-15
````

# APIs [![GitHub Issues](https://img.shields.io/github/issues/peter-w-bryant/Flask-Chest)](https://github.com/peter-w-bryant/Flask-Chest/issues)

## FlaskChest Objects
`FlaskChest` objects are <u>an abstraction layer for different databases</u> (and other backends). Once initialized, they can be passed as arguments to the [`flask_chest` decorator](#flask-chest-decorator) to write data to their respective backends.

The following `FlaskChest` objects are currently implemented:
- [`FlaskChestCustomWriter`](#flaskchestcustomwriter)
- [`FlaskChestInfluxDB`](#flaskchestinfluxdb)
- `FlaskChestPrometheus`
- `FlaskChestSQLite`
- `FlaskChestMySQL`

### FlaskChestCustomWriter
The `FlaskChestCustomWriter` class provides an interface to write context data to any backend that can accept HTTP POST requests. [Example usage](https://peter-w-bryant.github.io/Flask-Chest/basic_app.html#flaskchestcustomwriter).

| Parameter (*=required)           | Data Type     | Default Value | Description                                                  |
|--------------------|---------------|---------------|--------------------------------------------------------------|
| `url`*                | `str`          | `None`          | The URL the custom writer will POST data to.                 |
| `payload_generator`*  | `func`         | `None`          | A function that generates the payload for the POST request (see [Payload Generator Function](#payload-generator-function)). |
| `name`               | `str`          | `<your_url>`           | The name of the custom writer (useful for logging).          |
| `headers`            | `dict`          | `None`          | HTTP headers to be sent with the POST request.               |
| `params`             | `dict`          | `None`          | URL parameters to be sent with the POST request.             |
| `proxies`            | `dict`          | `None`          | Proxy URLs to be used for the POST request.                  |
| `verify`             | `bool`       | `False`         | Whether to verify the server's TLS certificate.              |
| `success_status_codes` | `list[int]`  | `[200]`         | List of HTTP status codes that indicate a successful POST request. |
| `logger`             | `object`        | `None`          | Logger instance for logging messages.                        |


#### Payload Generator Function
```python
def payload_generator(context_tuple_list: List[Tuple[str, str, str]]) -> dict|list|str|int|float|bool|None:
```
When using the `FlaskChestCustomWriter` class, a payload generator function must be provided, but <i>can be named anything</i>. This function is used to <b>generate the JSON body for the POST request</b> every time the `flask_chest` decorator is applied to a Flask route. [Example usage](https://peter-w-bryant.github.io/Flask-Chest/basic_app.html#flaskchestcustomwriter).

This function must implement the following interface:
- It must take a list of 3-tuples as an argument. Each 3-tuple is a global context variable of the form `(variable_name, variable_value, request_id)`. The order of the tuples in the list is the same as the order of the variables in the `tracked_vars` parameter of the [`flask_chest`](#the-flask_chest-decorator) decorator.
- It must return a [JSON serializable payload](https://learnpython.com/blog/object-serialization-in-python/) (e.g. `dict`, `list`, `str`, `int`, `float`, `bool`, and `None`).

### FlaskChestInfluxDB
The `FlaskChestInfluxDB` class provides an interface to write data points to instances of [InfluxDB 2.X](https://docs.influxdata.com/influxdb/v2/) using the [influxdb-client](https://github.com/influxdata/influxdb-client-python) library. [Example usage](https://peter-w-bryant.github.io/Flask-Chest/basic_app.html#flaskchestinfluxdb).

| Parameter (*=required)           | Data Type     | Default Value | Description                                                  |
|----------------------------------|---------------|---------------|--------------------------------------------------------------|
| `url`*                             | `str`         | `None`        | The URL of the InfluxDB server.                              |
| `token`*                           | `str`         | `""`          | The InfluxDB authentication token.                           |
| `org`*                             | `str`         | `"my-org"`    | The InfluxDB organization.                                   |
| `bucket`*                          | `str`         | `"my-bucket"` | The InfluxDB bucket.                                         |
| `custom_tags`                      | `dict`        | `{}`          | Custom tags to be included with each data point.             |
| `logger`                           | `object`      | `None`        | Logger instance for logging messages.                        |

#### Specifying Custom Tags

The `custom_tags` parameter is optional and can be used to add custom tags to each data point written to InfluxDB; each key-value pair in the dictionary should be of the form `{"tag_name": "tag_value"}`. [Example usage](https://peter-w-bryant.github.io/Flask-Chest/basic_app.html#flaskchestinfluxdb).

---

## `flask_chest` Decorator
The `flask_chest` decorator is used to track and write specified context variables to the target specified in the `chests` parameter. It can be applied to any Flask route, and will write data points to the specified backends every time the route is accessed. Each `FlaskChest` object passed to the `chests` parameter will receive the same data points. [Example usage](https://peter-w-bryant.github.io/Flask-Chest/basic_app.html#the-flask-chest-decorator).

| Parameter (*=required)           | Data Type     | Default Value                  | Description                                                  |
|----------------------------------|---------------|--------------------------------|--------------------------------------------------------------|
| chests*                          | `list[FlaskChest]` | `None`                    | List of `FlaskChest` objects to write data to.              |
| tracked_vars*                    | `dict`        | `None`                         | Dictionary mapping HTTP methods to lists of tracked variables. |
| request_id_generator             | `func`        | `lambda: str(uuid.uuid4())`    | A function that generates a unique request ID.               |
| raise_exceptions                 | `bool`        | `True`                         | Whether to raise exceptions if writing to a chest fails.     |


The `chests` parameter is a list of `FlaskChest` objects that the decorator will write to. The `tracked_vars` parameter is a dictionary specifying which global context variables to write to the chests per request method. If this parameter is set to `None`, all variables in `g.variables` will be tracked and written to the chests.

### Request ID Generator
The `request_id_generator` parameter is a function that should <u>return a unique identifier for each request as a string</u>. This ID is used to track and identify specific requests in the database, and can be used to trace the data back to the request that generated it. The default value for this parameter is a lambda function that returns a [UUID4](https://docs.python.org/3/library/uuid.html) string. [Example usage](https://peter-w-bryant.github.io/Flask-Chest/basic_app.html#the-flask-chest-decorator).


### Exception Handling
The `raise_exceptions` parameter is a <u>boolean that determines whether exceptions should be raised if writing to a chest fails</u>. If set to `False`, exceptions will not be raised, and the decorator will continue to execute the view function even if writing to a chest fails. If set to `True`, exceptions will be raised if writing to a chest fails, and the view function will not be executed.