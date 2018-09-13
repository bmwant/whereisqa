# -*- coding: utf-8 -*-

"""Top-level package for whereisqa."""

__author__ = """Misha Behersky"""
__email__ = 'bmwant@gmail.com'
__version__ = '0.1.0'


import config
from . import views


def setup_routes(app):
    app.router.add_get('/', views.index)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=config.PROJECT_ROOT / 'static',
                          name='static')
    app.router.add_static('/node_modules/',
                          path=config.PROJECT_ROOT / 'node_modules',
                          name='node_modules')

