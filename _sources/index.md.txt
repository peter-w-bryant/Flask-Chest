```{toctree}
:maxdepth: 2
:hidden:
Overview<self>
Install<install.md>
Interfaces<interfaces.md>
Basic Application<basic_app.md>
```

# Flask-Chest [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label&color=black)](https://github.com/peter-w-bryant/Flask-Chest)
Flask-Chest is a <b>Python package</b> adding support for the automated tracking and exporting of [global context variables](https://flask.palletsprojects.com/en/2.3.x/appcontext/#storing-data) (`g.variables`) within the [request context](https://flask.palletsprojects.com/en/3.0.x/reqcontext/) of each client interaction.

<center>

![Flask-Chest Icon](/_static/flask_chest_README.png)

</center>

<center>

[![Framework](https://img.shields.io/badge/framework-Flask-black.svg)](https://flask.palletsprojects.com/en/3.0.x/)
[![PyPI](https://img.shields.io/pypi/v/flask-chest)](https://pypi.org/project/flask-chest/)
![Tests](https://github.com/peter-w-bryant/Flask-Chest/actions/workflows/tests.yml/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/peter-w-bryant/Flask-Chest/blob/main/LICENSE)
![codecov](https://codecov.io/gh/peter-w-bryant/Flask-Chest/branch/main/graph/badge.svg)
[![GitHub Issues](https://img.shields.io/github/issues/peter-w-bryant/Flask-Chest)](https://github.com/peter-w-bryant/Flask-Chest/issues)

</center>

From the Flask documentation by Pallets Projects:

> The application context is a good place to store common data during a request or CLI command. Flask provides the `g` object for this purpose. It is a simple namespace object that has the same lifetime as an application context... The `g` name stands for “global”, but that is referring to the data being global within a context. The data on g is lost after the context ends, and it is not an appropriate place to store data between requests. Use the session or a database to store data across requests. [Source](https://flask.palletsprojects.com/en/2.0.x/appcontext/#storing-data)


## Features
- Implements multiple `FlaskChest` objects, providing an <u>abstraction layer for different databases (and other backends)</u> using a simple/minimal interface.
- Provides the `@flask_chest` decorator for view functions, <u>automatically exporting global context variables</u> to your configured data store.
- Customizable request ID generation, enabling the <u>identification and aggregation of context data generated during the same request</u> context.
- Implements thread-safe data exporters, scheduled using [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler), to <u>cache context data and periodically export it</u>.

## Installation [![PyPI](https://img.shields.io/pypi/v/flask-chest)](https://pypi.org/project/flask-chest/)

```bash
pip install flask-chest
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. View the [CONTRIBUTING](https://github.com/peter-w-bryant/Flask-Chest/blob/main/CONTRIBUTING.md) file for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/peter-w-bryant/Flask-Chest/blob/main/LICENSE) file for details.
