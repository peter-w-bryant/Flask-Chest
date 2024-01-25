# Flask-Chest
Flask Chest is a Python package adding support for the automated tracking and exporting of [global context variables](https://flask.palletsprojects.com/en/2.3.x/appcontext/#storing-data) (`g.variables`) for each request made to a Flask application.

<center>

![Flask-Chest Icon](/images/flask_chest_README.png)

</center>

<center>

[![PyPI](https://img.shields.io/pypi/v/flask-chest)](https://pypi.org/project/flask-chest/)
[![Framework](https://img.shields.io/badge/framework-Flask-black.svg)](https://flask.palletsprojects.com/en/3.0.x/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/peter-w-bryant/Flask-Chest/blob/main/LICENSE)

</center>

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
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. View the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
