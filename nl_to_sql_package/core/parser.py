"""
Main parser implementation for Natural Language to SQL Parser

This module provides the high-level interface for parsing natural language
queries, handling error correction, and managing the parsing workflow.
"""

import re
from typing import List, Optional, Dict, Any, Union
from .lexer import get_lexer, get_vocabulary
from .grammar import get_parser
from .ast_node import ASTNode
from ..utils.error_correction import ErrorCorrector
from ..utils.sql_translator import SQLTranslator


class NLToSQLParser:
    """
    Main parser class that orchestrates the natural language to SQL conversion process.
    """
    
    def __init__(self):
        """Initialize the parser with all necessary components."""
        self.lexer = get_lexer()
        self.parser = get_parser()
        self.error_corrector = ErrorCorrector(get_vocabulary())
        self.sql_translator = SQLTranslator()
    
    def parse_query(self, query: str) -> Optional[ASTNode]:
        """
        Parse a single natural language query into an AST.
        
        Args:
            query: The input query string
            
        Returns:
            ASTNode: The root node of the parsed AST, or None if parsing failed
        """
        return self.parser.parse(query)
    
    def detect_compound_query(self, query: str) -> List[str]:
        """
        Detect if a query contains multiple sub-queries and split them.
        
        Args:
            query: The input query string
            
        Returns:
            List[str]: List of individual query parts
        """
        # Split on question marks followed by query starters
        query_parts = re.split(r'\\?\\s*(?=how|what|show|list|can)', query, flags=re.IGNORECASE)
        query_parts = [q.strip() for q in query_parts if q.strip()]
        
        return query_parts if len(query_parts) > 1 else [query]
    
    def parse_with_correction(self, query: str) -> tuple:
        """
        Parse a query with automatic error correction if needed.
        
        Args:
            query: The input query string
            
        Returns:
            tuple: (ast, corrected_query, suggestions)
        """
        # Try parsing the original query first
        ast = self.parse_query(query)
        
        if ast is not None:
            return ast, query, {}
        
        # If parsing failed, try error correction
        suggestions, corrected_query = self.error_corrector.suggest_corrections(query)
        
        if corrected_query:
            ast = self.parse_query(corrected_query)
            if ast is not None:
                return ast, corrected_query, suggestions
        
        # If still failed, return None
        return None, query, suggestions
    
    def parse_and_execute(self, query: str, db_connection=None) -> Dict[str, Any]:
        """
        Complete parsing and execution pipeline.
        
        Args:
            query: The input query string
            db_connection: Database connection for SQL execution (optional)
            
        Returns:
            Dict: Complete results including AST, SQL, and execution results
        """
        result = {
            'original_query': query,
            'query_parts': [],
            'corrections': {},
            'asts': [],
            'sql_queries': [],
            'execution_results': [],
            'errors': [],
            'success': False
        }
        
        try:
            # Detect if this is a compound query
            query_parts = self.detect_compound_query(query)
            result['query_parts'] = query_parts
            
            # Process each query part
            for i, query_part in enumerate(query_parts):
                part_result = {
                    'query_text': query_part,
                    'ast': None,
                    'corrected_query': None,
                    'suggestions': {},
                    'sql': None,
                    'execution_result': None,
                    'error': None
                }
                
                try:
                    # Parse with error correction
                    ast, corrected_query, suggestions = self.parse_with_correction(query_part)
                    
                    if ast is not None:
                        part_result['ast'] = ast
                        part_result['corrected_query'] = corrected_query
                        part_result['suggestions'] = suggestions
                        
                        # Generate SQL
                        sql = self.sql_translator.ast_to_sql(ast)
                        part_result['sql'] = sql
                        
                        # Execute if database connection provided
                        if db_connection and sql:
                            execution_result = self._execute_sql(db_connection, sql)
                            part_result['execution_result'] = execution_result
                        
                        # Store results
                        result['asts'].append(ast)
                        if isinstance(sql, list):
                            result['sql_queries'].extend(sql)
                        else:
                            result['sql_queries'].append(sql)
                        
                        if part_result['execution_result']:
                            result['execution_results'].append(part_result['execution_result'])
                        
                        if suggestions:
                            result['corrections'][f'query_{i+1}'] = suggestions
                        
                    else:
                        part_result['error'] = f"Could not parse query: {query_part}"
                        result['errors'].append(part_result['error'])
                
                except Exception as e:
                    part_result['error'] = str(e)
                    result['errors'].append(str(e))
                
                # Add this part's results to the main result
                if 'parts' not in result:
                    result['parts'] = []
                result['parts'].append(part_result)
            
            # Set success flag
            result['success'] = len(result['asts']) > 0
            
        except Exception as e:
            result['errors'].append(f"General parsing error: {str(e)}")
            result['success'] = False
        
        return result
    
    def _execute_sql(self, connection, sql: Union[str, List[str]]) -> List[Any]:
        """
        Execute SQL query/queries against the database.
        
        Args:
            connection: Database connection
            sql: SQL query string or list of queries
            
        Returns:
            List: Query execution results
        """
        if not connection:
            return []
        
        results = []
        cursor = connection.cursor()
        
        try:
            if isinstance(sql, list):
                for query in sql:
                    cursor.execute(query)
                    results.append(cursor.fetchall())
            else:
                cursor.execute(sql)
                results.append(cursor.fetchall())
        except Exception as e:
            results.append(f"SQL Error: {str(e)}")
        
        return results
    
    def get_ast_summary(self, ast: ASTNode) -> Dict[str, Any]:
        """
        Get a summary of an AST structure.
        
        Args:
            ast: The AST node to summarize
            
        Returns:
            Dict: AST summary information
        """
        return {
            'root_type': ast.type,
            'root_value': ast.value,
            'total_nodes': ast.get_node_count(),
            'node_types': list(set(node.type for node in self._get_all_nodes(ast))),
            'has_compound': len(ast.find_nodes_by_type("CompoundQuery")) > 0,
            'query_types': [node.type for node in ast.children if 'Query' in node.type]
        }
    
    def _get_all_nodes(self, node: ASTNode) -> List[ASTNode]:
        """Get all nodes in an AST recursively."""
        nodes = [node]
        for child in node.children:
            nodes.extend(self._get_all_nodes(child))
        return nodes
