# Flask Chest Documentation

## Flask Chest [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label&color=black)](https://github.com/peter-w-bryant/Flask-Chest)
Flask Chest is a Python package adding support for the automated tracking and exporting of [global context variables](https://flask.palletsprojects.com/en/2.3.x/appcontext/#storing-data) (`g.variables`) for each request made to a Flask application.



<center>

![Flask-Chest Icon](/_static/flask_chest_README.png)

</center>

<center>

![PyPI](https://img.shields.io/pypi/v/flask-chest)
![Framework](https://img.shields.io/badge/framework-Flask-black.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</center>

From the Pallets Projects' Flask documentation:

> The application context is a good place to store common data during a request or CLI command. Flask provides the `g` object for this purpose. It is a simple namespace object that has the same lifetime as an application context... The `g` name stands for “global”, but that is referring to the data being global within a context. The data on g is lost after the context ends, and it is not an appropriate place to store data between requests. Use the session or a database to store data across requests. [Source](https://flask.palletsprojects.com/en/2.0.x/appcontext/#storing-data)


## Features
- Provides a decorator for Flask routes, automatically exporting specific global context variables to a predefined data store.
- Implements multiple `FlaskChest` objects, providing an abstraction layer for different databases (and other backends) using a common interface.
- Customizable request ID generation, ensuring unique identification of global context variables generated during the same request for better traceability and analysis of contextual data.
- Implements thread-safe data exporters, scheduled using [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler), to cache
global context variables and periodically export them to configured data stores.

## Installation

```bash
pip install flask-chest
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. View the [CONTRIBUTING](https://github.com/peter-w-bryant/Flask-Chest/blob/main/CONTRIBUTING.md) file for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/peter-w-bryant/Flask-Chest/blob/main/LICENSE) file for details.
