"""
AST Node implementation for Natural Language to SQL Parser

This module contains the ASTNode class that represents nodes in the Abstract Syntax Tree
generated during parsing of natural language queries.
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Optional, Any


class ASTNode:
    """
    Represents a node in the Abstract Syntax Tree (AST) for natural language queries.
    
    Attributes:
        type (str): The type of the AST node (e.g., "QuantityQuery", "ProductType")
        value (Any): The value associated with the node (optional)
        children (List[ASTNode]): Child nodes of this node
    """
    
    def __init__(self, type_: str, value: Any = None, children: Optional[List['ASTNode']] = None):
        """
        Initialize an AST node.
        
        Args:
            type_: The type of the node
            value: The value associated with the node (optional)
            children: List of child nodes (optional)
        """
        self.type = type_
        self.value = value
        self.children = children or []

    def to_text_tree(self, indent: int = 0) -> str:
        """
        Generate a detailed text-based tree representation of the AST.
        
        Args:
            indent: Current indentation level
            
        Returns:
            str: Formatted text representation of the AST
        """
        prefix = "  " * indent
        
        # More detailed node representations with emojis
        if self.type == "QuantityQuery":
            result = f"{prefix}📊 Quantity Query\n"
        elif self.type == "CompoundQuery":
            result = f"{prefix}🔗 Compound Query (Multiple Questions)\n"
        elif self.type == "ListQuery":
            result = f"{prefix}📋 List Query\n"
        elif self.type == "AvailabilityQuery":
            result = f"{prefix}✅ Availability Query\n"
        elif self.type == "LowStockQuery":
            result = f"{prefix}⚠️ Low Stock Query\n"
        elif self.type == "ComparisonQuery":
            result = f"{prefix}🔢 Comparison Query\n"
        elif self.type == "ProductType":
            product_name = self.get_product_display_name(self.value)
            result = f"{prefix}🏷️ Product Type: {product_name}\n"
        elif self.type == "ItemID":
            result = f"{prefix}🆔 Specific Item: {self.value}\n"
        elif self.type == "Location":
            location_name = "Warehouse" if self.value.upper() == "STOCK" else "Store"
            result = f"{prefix}📍 Location: {location_name}\n"
        elif self.type == "Threshold":
            threshold_desc = "Out of Stock (0)" if self.value == 0 else f"Low Stock (≤ {self.value})"
            result = f"{prefix}🎯 Threshold: {threshold_desc}\n"
        elif self.type == "Operator":
            op_desc = "Less Than" if self.value == "less_than" else "Greater Than"
            result = f"{prefix}⚖️ Comparison: {op_desc}\n"
        elif self.type == "Value":
            result = f"{prefix}🔢 Value: {self.value}\n"
        elif self.type == "Target":
            target_desc = "All Products" if "all" in self.value else "Available Products"
            result = f"{prefix}🎯 Target: {target_desc}\n"
        elif self.type == "OriginalPhrase":
            result = f"{prefix}💬 Original Input: \"{self.value}\"\n"
        elif self.type == "QueryStyle":
            style_map = {
                "basic": "Direct Question",
                "conversational": "Conversational ('we have')",
                "polite_request": "Polite Request ('can you tell me')",
                "formal_request": "Formal Request ('I want to know')"
            }
            style_desc = style_map.get(self.value, self.value)
            result = f"{prefix}💭 Query Style: {style_desc}\n"
        else:
            # Fallback for any other types
            if self.value:
                result = f"{prefix}{self.type}: {self.value}\n"
            else:
                result = f"{prefix}{self.type}\n"
        
        # Add children with increased indentation
        for child in self.children:
            result += child.to_text_tree(indent + 1)
        
        return result
    
    def get_product_display_name(self, product_type: str) -> str:
        """
        Convert product type tokens to user-friendly names.
        
        Args:
            product_type: Raw product type token
            
        Returns:
            str: User-friendly product name
        """
        product_map = {
            "TVS": "Televisions (All)",
            "TV": "Television",
            "PHONES": "Mobile Phones (All)",
            "PHONE": "Mobile Phone",
            "MOBILES": "Mobile Phones (All)",
            "MOBILE": "Mobile Phone",
            "SMARTPHONE": "Smartphone",
            "LAPTOPS": "Laptops (All)",
            "LAPTOP": "Laptop",
            "COMPUTERS": "Computers/Laptops (All)",
            "COMPUTER": "Computer/Laptop",
            "TABLETS": "Tablets (All)",
            "TABLET": "Tablet",
            "DRIVES": "Storage Drives (All)",
            "DRIVE": "Storage Drive",
            "HARD_DRIVE": "Hard Drive",
            "ALL": "All Products"
        }
        return product_map.get(product_type.upper(), product_type)
    
    def to_dict(self) -> dict:
        """
        Convert AST node to dictionary representation for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the AST node
        """
        return {
            "type": self.type,
            "value": self.value,
            "children": [child.to_dict() for child in self.children]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ASTNode':
        """
        Create AST node from dictionary representation.
        
        Args:
            data: Dictionary containing node data
            
        Returns:
            ASTNode: Reconstructed AST node
        """
        children = [cls.from_dict(child) for child in data.get("children", [])]
        return cls(data["type"], data.get("value"), children)
    
    def find_nodes_by_type(self, node_type: str) -> List['ASTNode']:
        """
        Find all nodes of a specific type in the AST.
        
        Args:
            node_type: Type of nodes to find
            
        Returns:
            List[ASTNode]: List of matching nodes
        """
        result = []
        if self.type == node_type:
            result.append(self)
        
        for child in self.children:
            result.extend(child.find_nodes_by_type(node_type))
        
        return result
    
    def get_node_count(self) -> int:
        """
        Get the total number of nodes in the AST.
        
        Returns:
            int: Total node count
        """
        count = 1  # Count this node
        for child in self.children:
            count += child.get_node_count()
        return count
    
    def __str__(self) -> str:
        """String representation of the AST node."""
        if self.value:
            return f"{self.type}({self.value})"
        return self.type
    
    def __repr__(self) -> str:
        """Developer representation of the AST node."""
        return f"ASTNode(type='{self.type}', value={repr(self.value)}, children_count={len(self.children)})"
