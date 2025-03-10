"""Sphinx documentation configuration."""

import os
import sys
from datetime import datetime

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath('../..'))

# Project information
project = 'Python Project Template'
copyright = f'{datetime.now().year}, Your Company'
author = 'Your Name'
version = '0.1.0'
release = '0.1.0'

# Documentation generation configuration
extensions = [
    'sphinx.ext.autodoc',      # Automatic API documentation
    'sphinx.ext.napoleon',     # Support for Google style docstrings
    'sphinx.ext.viewcode',     # Add source code links
    'sphinx.ext.coverage',     # Documentation coverage check
    'sphinx.ext.githubpages',  # GitHub Pages support
]

# Theme settings
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Language settings
language = 'en'

# Source file settings
source_suffix = '.rst'
master_doc = 'index'

# Exclude patterns
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
