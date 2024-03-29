# Flask-Chest
Flask-Chest is a <b>Python package</b> adding support for the automated tracking and exporting of [global context variables](https://flask.palletsprojects.com/en/2.3.x/appcontext/#storing-data) (`g.variables`) within the [request context](https://flask.palletsprojects.com/en/3.0.x/reqcontext/) of each client interaction. It provides a simple interface for making metrics, query parameters, and other context data available to a variety of backend targets, including databases, and custom HTTP endpoints.

<div align="center">
    <img src="images/flask_chest_README.png" alt="logo"/>
</div>

<p align="center">
    <a href="https://pypi.org/project/flask-chest/" style="text-decoration: none; border-bottom: none;"><img src="https://img.shields.io/pypi/v/flask-chest" alt="PyPI"/></a>
    <img src="https://github.com/peter-w-bryant/Flask-Chest/actions/workflows/tests.yml/badge.svg" alt="Tests"/>
    <img src="https://codecov.io/gh/peter-w-bryant/Flask-Chest/branch/main/graph/badge.svg" alt="codecov"/>
    <a href="https://github.com/peter-w-bryant/Flask-Chest/issues" style="text-decoration: none; border-bottom: none;"><img src="https://img.shields.io/github/issues/peter-w-bryant/Flask-Chest" alt="GitHub Issues"/></a>
    <a href="https://github.com/peter-w-bryant/Flask-Chest/blob/main/LICENSE" style="text-decoration: none; border-bottom: none;"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"/></a>
</p>

- [Documentation](#documentation)
- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Documentation
Documentation for the Flask-Chest project can be found [here](https://peter-w-bryant.github.io/Flask-Chest/).

## Features
- Implements multiple `FlaskChest` objects, providing an <u>abstraction layer for different databases (and other backends)</u> using a simple/minimal interface.
- Provides the `@flask_chest` decorator for view functions, <u>automatically exporting global context variables</u> to your configured data store.
- Customizable request ID generation, enabling the <u>identification and aggregation of context data generated during the same request</u> context.
- Implements thread-safe data exporters, scheduled using [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler), to <u>cache context data and periodically export it</u>.

## Installation

```bash
pip install flask-chest
```

## Contributing
Pull requests are welcome. Please open an issue first to discuss what you would like to change. If you would like to extend the available `FlaskChest` object backend interfaces, please implement the `FlaskChest` object [API spec](chest_api_spec.md) and run the available [test suite](under_construction.md) before opening a PR. See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
