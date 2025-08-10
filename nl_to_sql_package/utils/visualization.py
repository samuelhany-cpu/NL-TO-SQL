"""
Visualization utility for Natural Language to SQL Parser

This module provides visualization capabilities for AST structures,
including both text-based and PNG image generation.
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Optional, Tuple
from ..core.ast_node import ASTNode


class ASTVisualizer:
    """
    Handles visualization of Abstract Syntax Trees (ASTs).
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        self.default_node_color = 'lightblue'
        self.default_node_size = 4000
        self.default_font_size = 8
        self.default_figure_size = (16, 10)
    
    def generate_text_tree(self, ast: ASTNode, show_emojis: bool = True) -> str:
        """
        Generate a text-based tree representation of the AST.
        
        Args:
            ast: The AST root node
            show_emojis: Whether to include emojis in the output
            
        Returns:
            str: Formatted text tree
        """
        if show_emojis:
            return ast.to_text_tree()
        else:
            return self._text_tree_no_emojis(ast)
    
    def _text_tree_no_emojis(self, ast: ASTNode, indent: int = 0) -> str:
        """Generate text tree without emojis."""
        prefix = "  " * indent
        
        if ast.type == "QuantityQuery":
            result = f"{prefix}Quantity Query\\n"
        elif ast.type == "CompoundQuery":
            result = f"{prefix}Compound Query (Multiple Questions)\\n"
        elif ast.type == "ProductType":
            product_name = ast.get_product_display_name(ast.value)
            result = f"{prefix}Product Type: {product_name}\\n"
        elif ast.type == "ItemID":
            result = f"{prefix}Specific Item: {ast.value}\\n"
        elif ast.type == "OriginalPhrase":
            result = f"{prefix}Original Input: \"{ast.value}\"\\n"
        else:
            if ast.value:
                result = f"{prefix}{ast.type}: {ast.value}\\n"
            else:
                result = f"{prefix}{ast.type}\\n"
        
        for child in ast.children:
            result += self._text_tree_no_emojis(child, indent + 1)
        
        return result
    
    def generate_png(self, ast: ASTNode, filename: str = "ast_tree.png", 
                    title: str = "Abstract Syntax Tree") -> str:
        """
        Generate a PNG image of the AST.
        
        Args:
            ast: The AST root node
            filename: Output filename
            title: Title for the visualization
            
        Returns:
            str: Path to the generated PNG file
        """
        G = nx.DiGraph()
        labels = {}
        pos_dict = {}
        
        def add_nodes(node: ASTNode, parent_id: Optional[str] = None, 
                     x: float = 0, y: float = 0, level: int = 0):
            node_id = str(id(node))
            
            # Create clean labels without emojis for PNG
            label = self._get_node_label(node)
            
            labels[node_id] = label
            G.add_node(node_id)
            pos_dict[node_id] = (x, y)
            
            if parent_id is not None:
                G.add_edge(parent_id, node_id)
            
            # Position children
            if node.children:
                child_width = 3.0 / len(node.children) if len(node.children) > 1 else 1.0
                start_x = x - (len(node.children) - 1) * child_width / 2
                
                for i, child in enumerate(node.children):
                    child_x = start_x + i * child_width
                    child_y = y - 2.0
                    add_nodes(child, parent_id=node_id, x=child_x, y=child_y, level=level + 1)
        
        add_nodes(ast)
        
        plt.figure(figsize=self.default_figure_size)
        plt.clf()
        
        # Draw the graph with enhanced styling (no emojis)
        nx.draw(G, pos_dict, labels=labels, node_color=self.default_node_color, 
                node_size=self.default_node_size, font_size=self.default_font_size, 
                font_weight='bold', arrows=True, arrowsize=20, edge_color='gray',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=self.default_node_color, alpha=0.8))
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def generate_compound_png(self, asts: List[ASTNode], query_parts: List[str], 
                             filename: str = "compound_ast_tree.png") -> str:
        """
        Generate a PNG image showing multiple ASTs for compound queries.
        
        Args:
            asts: List of AST root nodes
            query_parts: List of original query parts
            filename: Output filename
            
        Returns:
            str: Path to the generated PNG file
        """
        if not asts:
            return filename
        
        fig, axes = plt.subplots(1, len(asts), figsize=(8 * len(asts), 10))
        if len(asts) == 1:
            axes = [axes]  # Make it iterable for single query
        
        fig.suptitle("Compound Query AST - Natural Language to SQL Parser", 
                    fontsize=16, fontweight='bold')
        
        for idx, (ast, query_part) in enumerate(zip(asts, query_parts)):
            ax = axes[idx]
            
            G = nx.DiGraph()
            labels = {}
            pos_dict = {}
            
            def add_nodes(node: ASTNode, parent_id: Optional[str] = None, 
                         x: float = 0, y: float = 0, level: int = 0):
                node_id = str(id(node))
                
                # Create clean labels without emojis for PNG
                if node.type == "QuantityQuery":
                    label = f"Query {idx + 1}\\nQuantity Query"
                else:
                    label = self._get_node_label(node, query_index=idx + 1)
                
                labels[node_id] = label
                G.add_node(node_id)
                pos_dict[node_id] = (x, y)
                
                if parent_id is not None:
                    G.add_edge(parent_id, node_id)
                
                # Position children
                if node.children:
                    child_width = 2.0 / len(node.children) if len(node.children) > 1 else 1.0
                    start_x = x - (len(node.children) - 1) * child_width / 2
                    
                    for i, child in enumerate(node.children):
                        child_x = start_x + i * child_width
                        child_y = y - 1.5
                        add_nodes(child, parent_id=node_id, x=child_x, y=child_y, level=level + 1)
            
            add_nodes(ast)
            
            # Draw each AST in its subplot
            nx.draw(G, pos_dict, labels=labels, node_color=self.default_node_color, 
                    node_size=2500, font_size=7, font_weight='bold',
                    arrows=True, arrowsize=15, edge_color='gray',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=self.default_node_color, alpha=0.8),
                    ax=ax)
            
            # Truncate long query parts for title
            display_query = query_part[:30] + "..." if len(query_part) > 30 else query_part
            ax.set_title(f"Query {idx + 1}: \"{display_query}\"", fontsize=12, fontweight='bold', pad=10)
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _get_node_label(self, node: ASTNode, query_index: Optional[int] = None) -> str:
        """Get a clean label for a node (without emojis)."""
        if node.type == "QuantityQuery":
            prefix = f"Query {query_index}\\n" if query_index else ""
            return f"{prefix}Quantity Query"
        elif node.type == "OriginalPhrase":
            # Truncate long phrases for display
            phrase = str(node.value)[:25] + "..." if len(str(node.value)) > 25 else str(node.value)
            return f"Input:\\n\"{phrase}\""
        elif node.type == "QueryStyle":
            return f"Style:\\n{str(node.value)}"
        elif node.type == "ProductType":
            product_name = node.get_product_display_name(str(node.value))
            return f"Product:\\n{product_name}"
        elif node.type == "ItemID":
            return f"Item:\\n{str(node.value)}"
        elif node.type == "Location":
            location_name = "Warehouse" if str(node.value).upper() == "STOCK" else "Store"
            return f"Location:\\n{location_name}"
        else:
            return f"{node.type}\\n{str(node.value)}" if node.value else node.type
    
    def set_style_options(self, node_color: str = None, node_size: int = None, 
                         font_size: int = None, figure_size: Tuple[int, int] = None) -> None:
        """
        Set visualization style options.
        
        Args:
            node_color: Color for nodes
            node_size: Size of nodes
            font_size: Font size for labels
            figure_size: Figure size tuple (width, height)
        """
        if node_color:
            self.default_node_color = node_color
        if node_size:
            self.default_node_size = node_size
        if font_size:
            self.default_font_size = font_size
        if figure_size:
            self.default_figure_size = figure_size
    
    def get_ast_statistics(self, ast: ASTNode) -> dict:
        """
        Get statistics about an AST structure.
        
        Args:
            ast: The AST root node
            
        Returns:
            dict: Statistics about the AST
        """
        node_types = {}
        total_nodes = 0
        max_depth = 0
        
        def analyze_node(node: ASTNode, depth: int = 0):
            nonlocal total_nodes, max_depth
            total_nodes += 1
            max_depth = max(max_depth, depth)
            
            node_type = node.type
            node_types[node_type] = node_types.get(node_type, 0) + 1
            
            for child in node.children:
                analyze_node(child, depth + 1)
        
        analyze_node(ast)
        
        return {
            'total_nodes': total_nodes,
            'max_depth': max_depth,
            'node_types': node_types,
            'root_type': ast.type,
            'has_children': len(ast.children) > 0,
            'child_count': len(ast.children)
        }
