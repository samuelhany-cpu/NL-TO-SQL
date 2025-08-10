"""
Grammar parser implementation for Natural Language to SQL Parser

This module contains the grammar rules and parser logic for converting
tokenized natural language queries into Abstract Syntax Trees (ASTs).
"""

import ply.yacc as yacc
from typing import Any, Optional
from .ast_node import ASTNode
from .lexer import tokens  # Import tokens from lexer module


class NLGrammarParser:
    """
    Grammar parser that defines the syntax rules for natural language queries.
    """
    
    # Make tokens available to the parser
    tokens = tokens
    
    def __init__(self):
        """Initialize the parser."""
        self.parser = None
        self._build_parser()
    
    def _build_parser(self):
        """Build the PLY parser with our grammar rules."""
        self.parser = yacc.yacc(module=self)
    
    def parse(self, query: str) -> Optional[ASTNode]:
        """
        Parse a natural language query into an AST.
        
        Args:
            query: The input query string
            
        Returns:
            ASTNode: The root node of the parsed AST, or None if parsing failed
        """
        if not self.parser:
            self._build_parser()
        
        try:
            return self.parser.parse(query)
        except Exception as e:
            print(f"Parser error: {e}")
            return None
    
    # Grammar rules start here
    def p_query(self, p):
        '''query : single_query
                 | compound_query'''
        p[0] = p[1]

    def p_single_query(self, p):
        '''single_query : quantity_query
                        | quantity_query QUESTION_MARK
                        | list_query
                        | list_query QUESTION_MARK
                        | availability_query
                        | availability_query QUESTION_MARK
                        | low_stock_query
                        | low_stock_query QUESTION_MARK
                        | comparison_query
                        | comparison_query QUESTION_MARK'''
        p[0] = p[1]  # Return the main query, ignore question mark

    def p_compound_query(self, p):
        '''compound_query : single_query AND single_query
                          | single_query ALSO single_query
                          | single_query AND ALSO single_query
                          | single_query single_query
                          | quantity_query QUESTION_MARK quantity_query
                          | quantity_query QUESTION_MARK quantity_query QUESTION_MARK'''
        # Return a compound node with both queries
        if len(p) == 3:  # single_query single_query
            p[0] = ASTNode("CompoundQuery", children=[p[1], p[2]])
        elif len(p) == 4:  # single_query AND/ALSO single_query
            p[0] = ASTNode("CompoundQuery", children=[p[1], p[3]])
        elif len(p) == 5:  # quantity_query QUESTION_MARK quantity_query or single_query AND ALSO single_query
            if str(p[2]) == '?':  # question mark pattern
                p[0] = ASTNode("CompoundQuery", children=[p[1], p[3]])
            else:  # AND ALSO pattern
                p[0] = ASTNode("CompoundQuery", children=[p[1], p[4]])
        elif len(p) == 6:  # quantity_query QUESTION_MARK quantity_query QUESTION_MARK
            p[0] = ASTNode("CompoundQuery", children=[p[1], p[3]])

    def p_quantity_query(self, p):
        '''quantity_query : HOW_MANY product_type IN location
                          | HOW_MANY UNITS OF product_type IN location
                          | HOW_MANY product_type
                          | HOW_MANY product_type WE HAVE
                          | HOW_MANY product_type DO WE HAVE
                          | CAN YOU TELL ME HOW_MANY product_type WE HAVE
                          | I WANT TO KNOW HOW_MANY product_type IN location
                          | HOW_MANY ITEM ID IN location
                          | HOW_MANY UNITS OF ITEM ID IN location
                          | HOW_MANY ITEM ID WE HAVE
                          | HOW_MANY ITEM ID DO WE HAVE'''
        
        # Reconstruct the original phrase for context
        original_phrase = " ".join([str(token) for token in p[1:]])
        
        # Find product type or item ID in the rule
        product_type = None
        item_id = None
        location = "store"  # default
        query_style = "basic"
        
        # Determine query style
        phrase_lower = original_phrase.lower()
        if "we have" in phrase_lower:
            query_style = "conversational"
        elif "can you tell me" in phrase_lower:
            query_style = "polite_request"
        elif "i want to know" in phrase_lower:
            query_style = "formal_request"
        
        # Debug: print all tokens to see what we're getting
        print(f"Debug - Original phrase: '{original_phrase}'")
        print(f"Debug - Query style: {query_style}")
        print(f"Debug - Parsing tokens: {[str(token) for token in p[1:]]}")
        
        for i, token in enumerate(p[1:], 1):
            token_str = str(token).upper()
            if i < len(p) - 1:
                if token_str == "ITEM" and i + 1 < len(p):
                    # Check if next token looks like an ID
                    next_token = str(p[i + 1])
                    if "-" in next_token:  # Simple check for ID pattern
                        item_id = next_token
                elif token_str in ["TVS", "TV", "PHONES", "PHONE", "MOBILES", "MOBILE", 
                                   "SMARTPHONE", "LAPTOPS", "LAPTOP", 
                                   "COMPUTERS", "COMPUTER", "TABLETS", "TABLET", 
                                   "DRIVES", "DRIVE", "HARD"]:
                    product_type = token_str
                elif token_str in ["STORE", "STOCK"]:
                    location = token_str
        
        print(f"Debug - Found product_type: {product_type}, item_id: {item_id}, location: {location}")
        
        # Create more detailed AST nodes
        if item_id:
            p[0] = ASTNode("QuantityQuery", children=[
                ASTNode("OriginalPhrase", original_phrase),
                ASTNode("QueryStyle", query_style),
                ASTNode("ItemID", item_id),
                ASTNode("Location", location)
            ])
        elif product_type:
            p[0] = ASTNode("QuantityQuery", children=[
                ASTNode("OriginalPhrase", original_phrase),
                ASTNode("QueryStyle", query_style),
                ASTNode("ProductType", product_type),
                ASTNode("Location", location)
            ])
        else:
            # Fallback
            p[0] = ASTNode("QuantityQuery", children=[
                ASTNode("OriginalPhrase", original_phrase),
                ASTNode("QueryStyle", query_style),
                ASTNode("ProductType", "ALL"),
                ASTNode("Location", location)
            ])

    def p_list_query(self, p):
        '''list_query : SHOW ALL products
                      | LIST ALL products
                      | WHAT products ARE AVAILABLE
                      | SHOW ALL ITEMS
                      | LIST ALL ITEMS'''
        original_phrase = " ".join([str(token) for token in p[1:]])
        p[0] = ASTNode("ListQuery", children=[
            ASTNode("OriginalPhrase", original_phrase),
            ASTNode("Target", "all_products")
        ])

    def p_availability_query(self, p):
        '''availability_query : WHAT IS AVAILABLE
                              | WHAT products ARE AVAILABLE
                              | SHOW AVAILABLE products'''
        original_phrase = " ".join([str(token) for token in p[1:]])
        p[0] = ASTNode("AvailabilityQuery", children=[
            ASTNode("OriginalPhrase", original_phrase),
            ASTNode("Target", "available_products")
        ])

    def p_low_stock_query(self, p):
        '''low_stock_query : WHAT products ARE LOW
                           | SHOW LOW STOCK
                           | WHAT IS LOW IN STOCK
                           | WHAT products ARE OUT OF STOCK
                           | SHOW EMPTY products'''
        original_phrase = " ".join([str(token) for token in p[1:]])
        if "OUT" in [str(x) for x in p[1:]] or "EMPTY" in [str(x) for x in p[1:]]:
            p[0] = ASTNode("LowStockQuery", children=[
                ASTNode("OriginalPhrase", original_phrase),
                ASTNode("Threshold", 0)
            ])
        else:
            p[0] = ASTNode("LowStockQuery", children=[
                ASTNode("OriginalPhrase", original_phrase),
                ASTNode("Threshold", 10)  # Consider low stock as < 10
            ])

    def p_comparison_query(self, p):
        '''comparison_query : SHOW products LESS THAN NUMBER
                            | SHOW products MORE THAN NUMBER
                            | SHOW products GREATER THAN NUMBER'''
        original_phrase = " ".join([str(token) for token in p[1:]])
        operator = "less_than" if p[3] == "LESS" else "greater_than"
        p[0] = ASTNode("ComparisonQuery", children=[
            ASTNode("OriginalPhrase", original_phrase),
            ASTNode("Operator", operator),
            ASTNode("Value", p[5])
        ])

    def p_product_type(self, p):
        '''product_type : TVS
                        | TV
                        | PHONES
                        | PHONE
                        | MOBILES
                        | MOBILE
                        | SMARTPHONE
                        | LAPTOPS
                        | LAPTOP
                        | COMPUTERS
                        | COMPUTER
                        | TABLETS
                        | TABLET
                        | DRIVES
                        | HARD DRIVE
                        | products'''
        if len(p) == 2:
            p[0] = p[1]
        else:  # HARD DRIVE
            p[0] = "HARD_DRIVE"

    def p_products(self, p):
        '''products : PRODUCTS
                    | ITEMS'''
        p[0] = p[1]

    def p_location(self, p):
        '''location : STORE
                    | STOCK
                    | THE STORE
                    | THE STOCK'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_error(self, p):
        """Error handling for syntax errors."""
        if p:
            print(f"Syntax error near '{p.value}'")
        else:
            print("Syntax error at EOF")


def get_parser() -> NLGrammarParser:
    """
    Create and return a parser instance.
    
    Returns:
        NLGrammarParser: Configured parser instance
    """
    return NLGrammarParser()
