# Contributing
Pull requests are welcome. Please open an issue first to discuss what you would like to change. If you would like to extend the available `FlaskChest` object backend interfaces, please implement the `FlaskChest` object [API spec](https://peter-w-bryant.github.io/Flask-Chest/chest_api_spec.html/) and run the available [test suite]() before opening a PR.

## How to Contribute
1. Open an issue to discuss the changes you would like to make (tag `enhancement`, `docs`, `bug`, and `refactor` accordingly).
2. Fork the repository on GitHub.
3. Clone your fork locally.
4. Install the development requirements:
    ```bash
    pip install -r requirements-dev.txt
    ```
5. Create a new branch for your feature or bug fix.
6. Make your changes and commit them to your branch.
7. Run the tests:
    ```bash
    pytest
    ```
8. Push your changes to your fork on GitHub.
9. Open a pull request to the `main` branch of the `peter-w-bryant/Flask-Chest` repository.

## Documentation
The documentation is built using [Sphinx](https://www.sphinx-doc.org/en/master/), and the [Furo](https://pradyunsg.me/furo/) theme. The documentation is written in [Markdown](https://www.markdownguide.org/) by way of the [myst_parser](https://myst-parser.readthedocs.io/en/latest/) extension, but it can include [reStructuredText](https://docutils.sourceforge.io/rst.html) (`.rst`) files. Updates to the documentation should be made in the `docs` directory on your feature branch, which will be built and deployed to the `gh-pages` branch of the repository when the PR is merged into `main`.