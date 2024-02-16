# `FlaskChest` Object API Specification
All `FlaskChest` objects must implement the following interface:

```python
class YourFlaskChest(FlaskChest):
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