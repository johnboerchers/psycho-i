# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Psycho-i"
copyright = "2022, Trevor Fush, John Boerchers, Sydney Rzepka"
author = "Trevor Fush, John Boerchers, Sydney Rzepka"
release = "0.0.1"

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))
sys.path.insert(0, os.path.abspath("../src/pgen"))
sys.path.insert(0, os.path.abspath("../plotting"))
autodoc_mock_imports = ["numba"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
