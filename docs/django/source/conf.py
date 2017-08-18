#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import django
import sphinx_rtd_theme


sys.path.insert(0, os.path.abspath('../../../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'doublegame.settings'
django.setup()

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'Code Game'
copyright = '2017, Group Sagualiazao'
author = 'Group Sagualiazao'

version = '0.1'
release = '0.1'

language = 'zh-cn'

exclude_patterns = [
    'doublegame.wsgi',
    'api.admin',
    'api.apps'
]

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}

htmlhelp_basename = 'CodeGamedoc'

latex_elements = {}

latex_documents = [
    (master_doc, 'CodeGame.tex', 'Code Game Documentation',
    'Group Sagualiazao', 'manual'),
]

man_pages = [
    (master_doc, 'codegame', 'Code Game Documentation',
    [author], 1)
]

texinfo_documents = [
    (master_doc, 'CodeGame', 'Code Game Documentation',
    author, 'CodeGame', 'One line description of project.',
    'Miscellaneous'),
]

intersphinx_mapping = {'https://docs.python.org/': None}
