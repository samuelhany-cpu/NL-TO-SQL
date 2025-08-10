"""
Natural Language to SQL Parser Package

A comprehensive package for parsing natural language queries into SQL statements
with support for stock management operations, AST visualization, and error correction.

Author: Generated for Full-Stack Web Development
Version: 1.0.0
"""

from .core.parser import NLToSQLParser
from .core.ast_node import ASTNode
from .core.lexer import get_lexer
from .utils.sql_translator import SQLTranslator
from .utils.error_correction import ErrorCorrector
from .utils.visualization import ASTVisualizer
from .database.stock_manager import StockManager
from .api.web_api import NLToSQLAPI, create_flask_app

__version__ = "1.0.0"
__author__ = "NL-TO-SQL Team"

# Main API for easy access
def parse_query(query_text, db_connection=None):
    """
    Main entry point for parsing natural language queries.
    
    Args:
        query_text (str): Natural language query
        db_connection: Database connection (optional)
        
    Returns:
        dict: Parsing results with AST, SQL, and execution results
    """
    parser = NLToSQLParser()
    return parser.parse_and_execute(query_text, db_connection)

# Export main classes for advanced usage
__all__ = [
    'NLToSQLParser',
    'ASTNode', 
    'SQLTranslator',
    'ErrorCorrector',
    'ASTVisualizer',
    'StockManager',
    'NLToSQLAPI',
    'create_flask_app',
    'parse_query',
    'get_lexer'
]
