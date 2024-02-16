# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Flask-Chest"
copyright = "2024, Peter Bryant"
author = "Peter Bryant"
release = "0.0.11"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.extlinks",
    'sphinx.ext.autodoc',
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "myst_parser",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = "Flask-Chest"
html_static_path = ["_static"]
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/peter-w-bryant/Flask-Chest",
    "source_branch": "main",
    "source_directory": "docs/",
        "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/peter-w-bryant/Flask-Chest",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
    ],
}

# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-extlinks-extension
html_favicon = "_static/favicon.ico"

html_css_files = [
    '_static/custom.css',
]

html_theme_options = {
    "navigation_with_keys": True,
}