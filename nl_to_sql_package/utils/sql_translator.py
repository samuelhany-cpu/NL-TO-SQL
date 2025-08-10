"""
SQL translator utility for Natural Language to SQL Parser

This module handles the conversion of AST nodes into SQL queries
for different types of natural language queries.
"""

from typing import Union, List, Optional
from ..core.ast_node import ASTNode


class SQLTranslator:
    """
    Translator that converts AST nodes into SQL queries.
    """
    
    def __init__(self):
        """Initialize the SQL translator."""
        self.product_mapping = {
            # TV mappings
            "TVS": "item_id LIKE 'TV%'",
            "TV": "item_id LIKE 'TV%'",
            
            # Phone/Mobile mappings
            "PHONES": "item_id LIKE 'PH%'",
            "PHONE": "item_id LIKE 'PH%'",
            "MOBILES": "item_id LIKE 'PH%'",
            "MOBILE": "item_id LIKE 'PH%'",
            "SMARTPHONE": "item_id LIKE 'PH%'",
            
            # Laptop/Computer mappings
            "LAPTOPS": "item_id LIKE 'LP%'",
            "LAPTOP": "item_id LIKE 'LP%'",
            "COMPUTERS": "item_id LIKE 'LP%'",
            "COMPUTER": "item_id LIKE 'LP%'",
            
            # Tablet mappings
            "TABLETS": "category = 'Tablets'",
            "TABLET": "category = 'Tablets'",
            
            # Storage/Drive mappings
            "DRIVES": "item_id LIKE 'HD%'",
            "DRIVE": "item_id LIKE 'HD%'",
            "HARD_DRIVE": "item_id LIKE 'HD%'",
            
            # All products
            "ALL": "1=1"  # Always true condition
        }
    
    def ast_to_sql(self, ast: ASTNode) -> Union[str, List[str], None]:
        """
        Convert an AST node to SQL query/queries.
        
        Args:
            ast: The root AST node
            
        Returns:
            Union[str, List[str], None]: SQL query string, list of queries, or None
        """
        if ast.type == "CompoundQuery":
            return self._handle_compound_query(ast)
        elif ast.type == "QuantityQuery":
            return self._handle_quantity_query(ast)
        elif ast.type == "ListQuery":
            return self._handle_list_query(ast)
        elif ast.type == "AvailabilityQuery":
            return self._handle_availability_query(ast)
        elif ast.type == "LowStockQuery":
            return self._handle_low_stock_query(ast)
        elif ast.type == "ComparisonQuery":
            return self._handle_comparison_query(ast)
        else:
            # Default fallback query
            return "SELECT item_id, name, quantity FROM stock;"
    
    def _handle_compound_query(self, ast: ASTNode) -> List[str]:
        """Handle compound queries with multiple sub-queries."""
        queries = []
        for child in ast.children:
            sql = self.ast_to_sql(child)
            if sql:
                if isinstance(sql, list):
                    queries.extend(sql)
                else:
                    queries.append(sql)
        return queries
    
    def _handle_quantity_query(self, ast: ASTNode) -> Optional[str]:
        """Handle quantity-based queries."""
        # Extract information from child nodes
        item_id = None
        product_type = None
        
        for child in ast.children:
            if child.type == "ItemID":
                item_id = child.value
            elif child.type == "ProductType":
                product_type = child.value
        
        # Build SQL query
        if item_id:
            # Specific item query
            return f"SELECT item_id, name, quantity FROM stock WHERE item_id = '{item_id}';"
        elif product_type:
            # Product type query
            condition = self._get_product_condition(product_type)
            return f"SELECT item_id, name, quantity FROM stock WHERE {condition};"
        else:
            # Default to all products
            return "SELECT item_id, name, quantity FROM stock;"
    
    def _handle_list_query(self, ast: ASTNode) -> str:
        """Handle list/show all queries."""
        return "SELECT item_id, name, quantity FROM stock ORDER BY name;"
    
    def _handle_availability_query(self, ast: ASTNode) -> str:
        """Handle availability queries."""
        return "SELECT item_id, name, quantity FROM stock WHERE quantity > 0 ORDER BY name;"
    
    def _handle_low_stock_query(self, ast: ASTNode) -> str:
        """Handle low stock queries."""
        threshold = 10  # default
        
        for child in ast.children:
            if child.type == "Threshold":
                threshold = child.value
        
        return f"SELECT item_id, name, quantity FROM stock WHERE quantity <= {threshold} ORDER BY quantity;"
    
    def _handle_comparison_query(self, ast: ASTNode) -> str:
        """Handle comparison queries (less than, greater than)."""
        operator = None
        value = None
        
        for child in ast.children:
            if child.type == "Operator":
                operator = child.value
            elif child.type == "Value":
                value = child.value
        
        if operator == "less_than":
            return f"SELECT item_id, name, quantity FROM stock WHERE quantity < {value} ORDER BY quantity;"
        elif operator == "greater_than":
            return f"SELECT item_id, name, quantity FROM stock WHERE quantity > {value} ORDER BY quantity DESC;"
        else:
            return "SELECT item_id, name, quantity FROM stock;"
    
    def _get_product_condition(self, product_type: str) -> str:
        """
        Get SQL condition for a product type.
        
        Args:
            product_type: The product type token
            
        Returns:
            str: SQL WHERE condition
        """
        return self.product_mapping.get(product_type.upper(), "1=1")
    
    def add_product_mapping(self, product_type: str, condition: str) -> None:
        """
        Add a new product type mapping.
        
        Args:
            product_type: The product type token
            condition: The SQL WHERE condition
        """
        self.product_mapping[product_type.upper()] = condition
    
    def get_supported_products(self) -> List[str]:
        """
        Get list of supported product types.
        
        Returns:
            List[str]: List of supported product type tokens
        """
        return list(self.product_mapping.keys())
    
    def validate_sql(self, sql: str) -> bool:
        """
        Basic SQL validation.
        
        Args:
            sql: SQL query string
            
        Returns:
            bool: True if SQL appears valid
        """
        if not sql or not sql.strip():
            return False
        
        sql_upper = sql.upper().strip()
        
        # Basic checks
        if not sql_upper.startswith('SELECT'):
            return False
        
        if 'FROM' not in sql_upper:
            return False
        
        # Check for basic SQL injection patterns
        dangerous_patterns = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'CREATE', 'ALTER', '--', ';--']
        for pattern in dangerous_patterns:
            if pattern in sql_upper:
                return False
        
        return True
