# Flask-Chest

<center>

![Flask-Chest Icon](/images/flask_chest_README.png)

</center>

<center>

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Version](https://img.shields.io/badge/version-0.0.10-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</center>

## Table of Contents
- [Introduction](#introduction)
- [Documentation](#documentation)
- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Flask-Chest is a Python package for Flask applications, providing a decorator to track and record global context variables (`g.variables`) for each request. It interfaces with various databases to store and export these variables, serving as a tool for monitoring and analytics in Flask web applications.

## Documentation
Documentation for the Flask-Chest project can be found [here](https://peter-w-bryant.github.io/Flask-Chest/).

## Features

- Tracks and records `g.variables` in Flask routes, allowing for the storage of contextual data in a configured database.
- Offers customizable request ID generation, ensuring unique identification of each request for better traceability and analysis of contextual data.
- Provides support for multiple databases, including SQLite, MySQL, PostgreSQL, and MongoDB, enabling flexibility in choosing the appropriate database for the application.
- Implements thread-safe data exporters, scheduled using AP Scheduler, to reliably and periodically export the recorded data, facilitating monitoring and analytics.

## Installation

```bash
pip install flask-chest
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. View the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
