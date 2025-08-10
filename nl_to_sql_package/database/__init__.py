"""
Database module for Natural Language to SQL Parser

Contains database management utilities and stock management system.
"""

from .stock_manager import StockManager, create_sample_database

__all__ = [
    'StockManager',
    'create_sample_database'
]
