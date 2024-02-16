```{toctree}
:maxdepth: 3
:glob:
:hidden:
Overview<self>
Install<install.md>
APIs<interfaces.md>
Sample Usage<sample_usage.md>
Contributing<CONTRIBUTING.md>
```

<!-- Import custom.css -->
<link rel="stylesheet" type="text/css" href="_static/custom.css">

# Flask-Chest [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label&color=black)](https://github.com/peter-w-bryant/Flask-Chest) 
Flask-Chest is a <b>Python package</b> adding support for the automated tracking and exporting of [global context variables](https://flask.palletsprojects.com/en/2.3.x/appcontext/#storing-data) (`g.variables`) within the [request context](https://flask.palletsprojects.com/en/3.0.x/reqcontext/) of each client interaction. It provides a simple interface for making metrics, query parameters, and other context data available to a variety of backend targets, including databases, and custom HTTP endpoints.

<center>

![Flask-Chest Icon](/_static/flask_chest_README.png)

</center>

<p align="center">
    <a href="https://pypi.org/project/flask-chest/" style="text-decoration: none; border-bottom: none;"><img src="https://img.shields.io/pypi/v/flask-chest" alt="PyPI"/></a>
    <img src="https://github.com/peter-w-bryant/Flask-Chest/actions/workflows/tests.yml/badge.svg" alt="Tests"/>
    <img src="https://codecov.io/gh/peter-w-bryant/Flask-Chest/branch/main/graph/badge.svg" alt="codecov"/>
    <a href="https://github.com/peter-w-bryant/Flask-Chest/issues" style="text-decoration: none; border-bottom: none;"><img src="https://img.shields.io/github/issues/peter-w-bryant/Flask-Chest" alt="GitHub Issues"/></a>
    <a href="https://github.com/peter-w-bryant/Flask-Chest/blob/main/LICENSE" style="text-decoration: none; border-bottom: none;"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"/></a>
</p>


From the Flask documentation by Pallets Projects:

> The application context is a good place to store common data during a request or CLI command. Flask provides the `g` object for this purpose. It is a simple namespace object that has the same lifetime as an application context... The `g` name stands for “global”, but that is referring to the data being global within a context. The data on g is lost after the context ends, and it is not an appropriate place to store data between requests. Use the session or a database to store data across requests. [Source](https://flask.palletsprojects.com/en/2.0.x/appcontext/#storing-data)


## Features
- Implements multiple [`FlaskChest` objects](interfaces.md#flaskchest-objects), providing an <u>abstraction layer for different databases</u> (and other backends) using a simple/minimal interface.
- Provides the [`@flask_chest` decorator](interfaces.md#flask-chest-decorator) for view functions, <u>automatically exporting global context variables</u> to your configured targets.
- Customizable [request ID generation](interfaces.md#request-id-generator), enabling the <u>identification and aggregation of context data generated during the same request</u> context.
- Implements thread-safe data exporters, scheduled using [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler), to <u>cache context data and periodically export it</u>.

## Installation [![PyPI](https://img.shields.io/pypi/v/flask-chest)](https://pypi.org/project/flask-chest/)

```bash
pip install flask-chest
```

## Contributing
Pull requests are welcome. Please open an issue first to discuss what you would like to change. If you would like to extend the available `FlaskChest` object backend interfaces, please implement the `FlaskChest` object [API spec](chest_api_spec.md) and run the available [test suite](under_construction.md) before opening a PR. See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/peter-w-bryant/Flask-Chest/blob/main/LICENSE) file for details.