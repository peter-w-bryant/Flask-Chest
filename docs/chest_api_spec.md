# `FlaskChest` Object API Specification

## Class Definition and Interface
All `FlaskChest` objects must implement the following class interface:

```python
class SampleFlaskChest(FlaskChest):
    def __init__(self, name: str, logger: object, **kwargs) -> None:
        """
        Initialize the `FlaskChest` object.

        :param name: The name of the `FlaskChest` object (useful for logging).
        :param logger: Logger instance for logging messages.
        :param kwargs: Additional keyword arguments specific to the `FlaskChest` object.
        """
        pass

    def __str__(self) -> str:
        """
        Return a string representation of the `FlaskChest` object.

        :return: A string representation of the `FlaskChest` object.
        """
        pass

    def write(self, variables: List[Tuple[str, str, str]]) -> None:
        """
        Write the context variables to the backend.

        :param variables: A list of 3-tuples, each containing a global context variable of the form
                          `(variable_name, variable_value, request_id)`.
        """
        pass
```

### Logging
Your `FlaskChest` object should log all messages using the provided `logger` instance, and should not print to the console. If no `logger` instance is provided, the `FlaskChest` object should not log any messages. All log messages should be include `SampleFlaskChest(name=<chest_name>)` in the log message.

For an example implementation, see the [`FlaskChestCustomWriter`](https://github.com/peter-w-bryant/Flask-Chest/blob/main/flask-chest/flask_chest/chests/custom.py) class.