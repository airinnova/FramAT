#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Configuration file for the Sphinx documentation builder.
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------
import os
import sys

from framat.stdfun import DEFAULT_MODEL_FILENAME
from framat.__version__ import __version__


sys.path.insert(0, os.path.abspath('../../src/lib/framat'))
sys.setrecursionlimit(1500)

NAME = 'FramAT'
NAME_LONG = 'Frame Analysis Tool'
NAME_LC = NAME.lower()
NAME_CLI = NAME_LC
COPYRIGHT = '2019, A. Dettmann'
AUTHOR = 'Aaron Dettmann'
LICENCE_NAME = "Apache-2.0"
DESCR_SHORT = "Frame Analysis Tool"

# -- Project information -----------------------------------------------------
project = NAME
author = AUTHOR
copyright = COPYRIGHT

# version: The short X.Y version
# release: The full version, including alpha/beta/rc tags
version = __version__

# ====================================
# ######### AUTOMATE THINGS ##########
# ====================================
os.system('bash ./dev_doc/gen_auto_doc.sh')
os.system('bash ./_gen_help_page.sh')
os.system('python ./user_guide/make_example.py')

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    # 'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]

# Paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Source file parsers
# source_parsers = {
#         '.md': 'recommonmark.parser.CommonMarkParser',
#         }

# The suffix(es) of source filenames.
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

rst_prolog = f"""
.. |name| replace:: {NAME}
.. |name_long| replace:: {NAME_LONG}
.. |name_cli| replace:: ``{NAME_CLI}``
.. |eb| replace:: Euler-Bernoulli
.. |std_model_filename| replace:: ``{DEFAULT_MODEL_FILENAME}``
.. |std_model_filename_unformatted| replace:: {DEFAULT_MODEL_FILENAME}
.. |name_bold| replace:: **{NAME}**
.. |dof| replace:: d.o.f.
.. |dof_long| replace:: degrees of freedom
.. _FEM: https://en.wikipedia.org/wiki/Finite_element_method
.. _JSON: https://json.org/
.. _FE: https://en.wikipedia.org/wiki/Finite_element_method
.. _aeroelasticity: https://en.wikipedia.org/wiki/Aeroelasticity
.. _CPACS: https://www.cpacs.de/
.. _DLR: https://www.dlr.de/
.. _Airinnova: http://airinnova.se/
.. _Airinnova AB: http://airinnova.se/
.. _PyPI: https://pypi.org/project/framat/
.. |pypi_long| replace:: Python Package Index
.. _pip: https://pip.pypa.io/en/stable/
.. |author1| replace:: {AUTHOR}
.. |license| replace:: {LICENCE_NAME}
"""

numfig = True

# -- Options for HTML output -------------------------------------------------

# html_theme = 'classic'
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'canonical_url': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
}

# Paths that contain custom static files (such as style sheets) relative to this directory.
html_static_path = ['_static']

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = f'{NAME}_doc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': '',

    # Latex figure (float) alignment
    'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, f'{NAME}.tex', f'{NAME} Documentation', f'{AUTHOR}', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, f'{NAME_LC}', f'{NAME} Documentation', [AUTHOR], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, f'{NAME}', f'{NAME} Documentation', AUTHOR, f'{NAME}', f'{DESCR_SHORT}', 'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = NAME

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
