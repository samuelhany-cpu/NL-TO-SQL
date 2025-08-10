"""
API module for Natural Language to SQL Parser

This module provides REST API endpoints and web integration utilities
for the natural language to SQL parser system.
"""

from typing import Dict, Any, Optional, List
import json
from datetime import datetime
from ..core.parser import NLToSQLParser
from ..database.stock_manager import StockManager
from ..utils.visualization import ASTVisualizer


class NLToSQLAPI:
    """
    API interface for the Natural Language to SQL Parser system.
    """
    
    def __init__(self, db_manager: Optional[StockManager] = None):
        """
        Initialize the API.
        
        Args:
            db_manager: Stock manager instance (optional)
        """
        self.parser = NLToSQLParser()
        self.db_manager = db_manager or StockManager()
        self.visualizer = ASTVisualizer()
        
        # Initialize database if not already done
        if self.db_manager:
            self.db_manager.initialize_database()
    
    def parse_query_api(self, query: str, execute_sql: bool = True, 
                       generate_visualization: bool = False) -> Dict[str, Any]:
        """
        Main API endpoint for parsing natural language queries.
        
        Args:
            query: Natural language query string
            execute_sql: Whether to execute generated SQL
            generate_visualization: Whether to generate AST visualization
            
        Returns:
            Dict: API response with parsing results
        """
        try:
            # Parse the query
            connection = self.db_manager.connection if execute_sql else None
            result = self.parser.parse_and_execute(query, connection)
            
            # Create API response
            api_response = {
                'status': 'success' if result['success'] else 'error',
                'timestamp': datetime.now().isoformat(),
                'query': {
                    'original': result['original_query'],
                    'parts': result['query_parts'],
                    'corrections': result['corrections']
                },
                'parsing': {
                    'ast_count': len(result['asts']),
                    'sql_count': len(result['sql_queries']),
                    'has_compound_query': len(result['query_parts']) > 1
                },
                'sql_queries': result['sql_queries'],
                'execution_results': result['execution_results'] if execute_sql else [],
                'errors': result['errors']
            }
            
            # Add AST information
            if result['asts']:
                api_response['ast_info'] = []
                for i, ast in enumerate(result['asts']):
                    ast_info = self.parser.get_ast_summary(ast)
                    ast_info['ast_dict'] = ast.to_dict()  # Serializable AST
                    if generate_visualization:
                        ast_info['text_tree'] = self.visualizer.generate_text_tree(ast, show_emojis=False)
                    api_response['ast_info'].append(ast_info)
            
            # Generate visualization files if requested
            if generate_visualization and result['asts']:
                visualization_files = []
                
                if len(result['asts']) == 1:
                    # Single query visualization
                    filename = f"ast_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    self.visualizer.generate_png(result['asts'][0], filename)
                    visualization_files.append(filename)
                else:
                    # Compound query visualization
                    filename = f"compound_ast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    self.visualizer.generate_compound_png(result['asts'], result['query_parts'], filename)
                    visualization_files.append(filename)
                
                api_response['visualization_files'] = visualization_files
            
            return api_response
            
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'query': {'original': query}
            }
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get information about the database.
        
        Returns:
            Dict: Database information and statistics
        """
        try:
            stats = self.db_manager.get_database_stats()
            
            return {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'database_stats': stats,
                'connection_status': 'connected' if self.db_manager.connection else 'disconnected'
            }
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def get_vocabulary(self) -> Dict[str, Any]:
        """
        Get the parser vocabulary for error correction.
        
        Returns:
            Dict: Vocabulary information
        """
        try:
            vocab = self.parser.error_corrector.vocabulary
            vocab_stats = self.parser.error_corrector.get_vocabulary_stats()
            
            return {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'vocabulary': vocab,
                'statistics': vocab_stats
            }
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def get_supported_queries(self) -> Dict[str, Any]:
        """
        Get information about supported query types and examples.
        
        Returns:
            Dict: Supported query information
        """
        try:
            query_examples = {
                'quantity_queries': [
                    "How many TVs do we have?",
                    "How many units of item TV-1234 in the store?",
                    "How many mobiles we have?",
                    "Can you tell me how many laptops we have?"
                ],
                'list_queries': [
                    "Show all products",
                    "List all items",
                    "What products are available?"
                ],
                'availability_queries': [
                    "What is available?",
                    "Show available products"
                ],
                'low_stock_queries': [
                    "What products are low?",
                    "Show low stock",
                    "What products are out of stock?"
                ],
                'comparison_queries': [
                    "Show products less than 10",
                    "Show products more than 50"
                ],
                'compound_queries': [
                    "How many TVs we have ? How many phones we have ?",
                    "Show all products and also show low stock"
                ]
            }
            
            supported_products = self.parser.sql_translator.get_supported_products()
            
            return {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'query_types': list(query_examples.keys()),
                'examples': query_examples,
                'supported_products': supported_products
            }
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Validate a query without executing it.
        
        Args:
            query: Natural language query to validate
            
        Returns:
            Dict: Validation results
        """
        try:
            # Try parsing without execution
            result = self.parser.parse_and_execute(query, db_connection=None)
            
            validation_result = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'is_valid': result['success'],
                'parse_errors': result['errors'],
                'corrections_suggested': bool(result['corrections']),
                'corrections': result['corrections'],
                'query_type': None,
                'sql_generated': len(result['sql_queries']) > 0
            }
            
            # Determine query type
            if result['asts']:
                query_types = []
                for ast in result['asts']:
                    if ast.type in ['QuantityQuery', 'ListQuery', 'AvailabilityQuery', 
                                   'LowStockQuery', 'ComparisonQuery', 'CompoundQuery']:
                        query_types.append(ast.type)
                validation_result['query_type'] = query_types
            
            return validation_result
            
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'query': query,
                'is_valid': False
            }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Health check endpoint.
        
        Returns:
            Dict: System health status
        """
        try:
            # Check database connection
            db_status = 'connected' if self.db_manager.connection else 'disconnected'
            
            # Try a simple query
            test_result = self.db_manager.execute_query("SELECT COUNT(*) as count FROM stock")
            db_working = len(test_result) > 0 and 'count' in test_result[0]
            
            return {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'components': {
                    'parser': 'operational',
                    'database': db_status,
                    'database_queries': 'operational' if db_working else 'error',
                    'error_corrector': 'operational',
                    'sql_translator': 'operational',
                    'visualizer': 'operational'
                }
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }


def create_flask_app(db_manager: Optional[StockManager] = None):
    """
    Create a Flask application with API endpoints.
    
    Args:
        db_manager: Stock manager instance (optional)
        
    Returns:
        Flask app instance
    """
    try:
        from flask import Flask, request, jsonify
        from flask_cors import CORS
    except ImportError:
        raise ImportError("Flask and Flask-CORS are required for web API. Install with: pip install flask flask-cors")
    
    app = Flask(__name__)
    CORS(app)  # Enable CORS for web frontend
    
    api = NLToSQLAPI(db_manager)
    
    @app.route('/api/parse', methods=['POST'])
    def parse_query():
        """Parse a natural language query."""
        data = request.get_json()
        query = data.get('query', '')
        execute_sql = data.get('execute_sql', True)
        generate_visualization = data.get('generate_visualization', False)
        
        result = api.parse_query_api(query, execute_sql, generate_visualization)
        return jsonify(result)
    
    @app.route('/api/validate', methods=['POST'])
    def validate_query():
        """Validate a query without executing it."""
        data = request.get_json()
        query = data.get('query', '')
        
        result = api.validate_query(query)
        return jsonify(result)
    
    @app.route('/api/database/info', methods=['GET'])
    def database_info():
        """Get database information."""
        result = api.get_database_info()
        return jsonify(result)
    
    @app.route('/api/vocabulary', methods=['GET'])
    def vocabulary():
        """Get parser vocabulary."""
        result = api.get_vocabulary()
        return jsonify(result)
    
    @app.route('/api/queries/supported', methods=['GET'])
    def supported_queries():
        """Get supported query types and examples."""
        result = api.get_supported_queries()
        return jsonify(result)
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        result = api.health_check()
        return jsonify(result)
    
    return app
