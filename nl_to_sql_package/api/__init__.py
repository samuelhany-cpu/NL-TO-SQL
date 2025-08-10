"""
API module for Natural Language to SQL Parser

Provides web API and integration utilities for full-stack applications.
"""

from .web_api import NLToSQLAPI, create_flask_app

__all__ = [
    'NLToSQLAPI',
    'create_flask_app'
]
