import re
import sqlite3
import difflib
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import ply.lex as lex
import ply.yacc as yacc

# =============================
# 1. LEXER
# =============================
tokens = (
    'I', 'WANT', 'TO', 'KNOW', 'HOW_MANY', 'UNITS', 'OF', 'ITEM', 'ITEMS', 'PRODUCT', 'PRODUCTS',
    'ID', 'IN', 'STORE', 'STOCK', 'THE', 'TVS', 'PHONES', 'LAPTOPS', 'DRIVES', 'SMARTPHONE',
    'LAPTOP', 'TV', 'PHONE', 'HARD', 'DRIVE', 'ALL', 'SHOW', 'LIST', 'WHAT', 'IS', 'ARE',
    'AVAILABLE', 'LOW', 'OUT', 'EMPTY', 'LESS', 'THAN', 'MORE', 'GREATER', 'NUMBER', 
    'MOBILES', 'MOBILE', 'COMPUTERS', 'COMPUTER', 'TABLETS', 'TABLET', 'WE', 'HAVE', 
    'DO', 'YOU', 'CAN', 'GET', 'TELL', 'ME', 'QUESTION_MARK', 'AND', 'ALSO', 'WORD'
)

t_ignore = ' \t'

def t_I(t):
    r'\bi\b'
    return t

def t_WANT(t):
    r'[Ww][Aa][Nn][Tt]'
    return t

def t_TO(t):
    r'[Tt][Oo]'
    return t

def t_KNOW(t):
    r'[Kk][Nn][Oo][Ww]'
    return t

def t_HOW_MANY(t):
    r'[Hh][Oo][Ww]\s+[Mm][Aa][Nn][Yy]'
    return t

def t_TVS(t):
    r'[Tt][Vv][Ss]?'
    return t

def t_TV(t):
    r'[Tt][Vv]'
    return t

def t_PHONES(t):
    r'[Pp][Hh][Oo][Nn][Ee][Ss]'
    return t

def t_PHONE(t):
    r'[Pp][Hh][Oo][Nn][Ee]'
    return t

def t_MOBILES(t):
    r'[Mm][Oo][Bb][Ii][Ll][Ee][Ss]'
    return t

def t_MOBILE(t):
    r'[Mm][Oo][Bb][Ii][Ll][Ee]'
    return t

def t_SMARTPHONE(t):
    r'[Ss][Mm][Aa][Rr][Tt][Pp][Hh][Oo][Nn][Ee]'
    return t

def t_LAPTOPS(t):
    r'[Ll][Aa][Pp][Tt][Oo][Pp][Ss]'
    return t

def t_LAPTOP(t):
    r'[Ll][Aa][Pp][Tt][Oo][Pp]'
    return t

def t_COMPUTERS(t):
    r'[Cc][Oo][Mm][Pp][Uu][Tt][Ee][Rr][Ss]'
    return t

def t_COMPUTER(t):
    r'[Cc][Oo][Mm][Pp][Uu][Tt][Ee][Rr]'
    return t

def t_TABLETS(t):
    r'[Tt][Aa][Bb][Ll][Ee][Tt][Ss]'
    return t

def t_TABLET(t):
    r'[Tt][Aa][Bb][Ll][Ee][Tt]'
    return t

def t_DRIVES(t):
    r'[Dd][Rr][Ii][Vv][Ee][Ss]'
    return t

def t_DRIVE(t):
    r'[Dd][Rr][Ii][Vv][Ee]'
    return t

def t_HARD(t):
    r'[Hh][Aa][Rr][Dd]'
    return t

def t_ITEMS(t):
    r'[Ii][Tt][Ee][Mm][Ss]'
    return t

def t_ITEM(t):
    r'[Ii][Tt][Ee][Mm]'
    return t

def t_PRODUCTS(t):
    r'[Pp][Rr][Oo][Dd][Uu][Cc][Tt][Ss]'
    return t

def t_PRODUCT(t):
    r'[Pp][Rr][Oo][Dd][Uu][Cc][Tt]'
    return t

def t_AVAILABLE(t):
    r'[Aa][Vv][Aa][Ii][Ll][Aa][Bb][Ll][Ee]'
    return t

def t_SHOW(t):
    r'[Ss][Hh][Oo][Ww]'
    return t

def t_LIST(t):
    r'[Ll][Ii][Ss][Tt]'
    return t

def t_ALL(t):
    r'[Aa][Ll][Ll]'
    return t

def t_WHAT(t):
    r'[Ww][Hh][Aa][Tt]'
    return t

def t_IS(t):
    r'[Ii][Ss]'
    return t

def t_ARE(t):
    r'[Aa][Rr][Ee]'
    return t

def t_LOW(t):
    r'[Ll][Oo][Ww]'
    return t

def t_OUT(t):
    r'[Oo][Uu][Tt]'
    return t

def t_EMPTY(t):
    r'[Ee][Mm][Pp][Tt][Yy]'
    return t

def t_LESS(t):
    r'[Ll][Ee][Ss][Ss]'
    return t

def t_THAN(t):
    r'[Tt][Hh][Aa][Nn]'
    return t

def t_MORE(t):
    r'[Mm][Oo][Rr][Ee]'
    return t

def t_GREATER(t):
    r'[Gg][Rr][Ee][Aa][Tt][Ee][Rr]'
    return t

def t_WE(t):
    r'[Ww][Ee]'
    return t

def t_HAVE(t):
    r'[Hh][Aa][Vv][Ee]'
    return t

def t_DO(t):
    r'[Dd][Oo]'
    return t

def t_YOU(t):
    r'[Yy][Oo][Uu]'
    return t

def t_CAN(t):
    r'[Cc][Aa][Nn]'
    return t

def t_GET(t):
    r'[Gg][Ee][Tt]'
    return t

def t_TELL(t):
    r'[Tt][Ee][Ll][Ll]'
    return t

def t_ME(t):
    r'[Mm][Ee]'
    return t

def t_QUESTION_MARK(t):
    r'\?'
    return t

def t_AND(t):
    r'[Aa][Nn][Dd]'
    return t

def t_ALSO(t):
    r'[Aa][Ll][Ss][Oo]'
    return t

def t_UNITS(t):
    r'[Uu][Nn][Ii][Tt][Ss]'
    return t

def t_OF(t):
    r'[Oo][Ff]'
    return t

def t_IN(t):
    r'[Ii][Nn]'
    return t

def t_THE(t):
    r'[Tt][Hh][Ee]'
    return t

def t_STORE(t):
    r'[Ss][Tt][Oo][Rr][Ee]'
    return t

def t_STOCK(t):
    r'[Ss][Tt][Oo][Cc][Kk]'
    return t

def t_ID(t):
    r'[A-Za-z]+-\d+'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_WORD(t):
    r'[A-Za-z]+'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' ignored.")
    t.lexer.skip(1)

lexer = lex.lex()

# =============================
# 2. PARSER (AST)
# =============================
class ASTNode:
    def __init__(self, type_, value=None, children=None):
        self.type = type_
        self.value = value
        self.children = children or []

    def to_text_tree(self, indent=0):
        """Generate a detailed text-based tree representation of the AST"""
        prefix = "  " * indent
        
        # More detailed node representations
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
    
    def get_product_display_name(self, product_type):
        """Convert product type tokens to user-friendly names"""
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
    
    def to_png(self, filename="ast_tree.png"):
        """Generate a PNG image of the AST using matplotlib and networkx"""
        G = nx.DiGraph()
        labels = {}
        pos_dict = {}
        
        def add_nodes(node, parent_id=None, x=0, y=0, level=0):
            node_id = str(id(node))  # Convert to string to fix the error
            
            # Create clean labels without emojis for PNG
            if node.type == "QuantityQuery":
                label = "Quantity Query"
            elif node.type == "OriginalPhrase":
                # Truncate long phrases for display
                phrase = str(node.value)[:25] + "..." if len(str(node.value)) > 25 else str(node.value)
                label = f"Input:\n\"{phrase}\""
            elif node.type == "QueryStyle":
                label = f"Style:\n{str(node.value)}"
            elif node.type == "ProductType":
                product_name = self.get_product_display_name(str(node.value))
                label = f"Product:\n{product_name}"
            elif node.type == "ItemID":
                label = f"Item:\n{str(node.value)}"
            elif node.type == "Location":
                location_name = "Warehouse" if str(node.value).upper() == "STOCK" else "Store"
                label = f"Location:\n{location_name}"
            else:
                label = f"{node.type}\n{str(node.value)}" if node.value else node.type
            
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
        
        add_nodes(self)
        
        plt.figure(figsize=(16, 10))
        plt.clf()
        
        # Draw the graph with enhanced styling (no emojis)
        nx.draw(G, pos_dict, labels=labels, node_color='lightblue', 
                node_size=4000, font_size=8, font_weight='bold',
                arrows=True, arrowsize=20, edge_color='gray',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
        
        plt.title("Enhanced Abstract Syntax Tree (AST) - Natural Language to SQL Parser", 
                 fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    @staticmethod
    def create_compound_png(asts, query_parts, filename="compound_ast_tree.png"):
        """Generate a PNG image showing multiple ASTs for compound queries"""
        import matplotlib.pyplot as plt
        import networkx as nx
        
        fig, axes = plt.subplots(1, len(asts), figsize=(8 * len(asts), 10))
        if len(asts) == 1:
            axes = [axes]  # Make it iterable for single query
        
        fig.suptitle("Enhanced Compound Query AST - Natural Language to SQL Parser", 
                    fontsize=16, fontweight='bold')
        
        for idx, (ast, query_part) in enumerate(zip(asts, query_parts)):
            ax = axes[idx]
            
            G = nx.DiGraph()
            labels = {}
            pos_dict = {}
            
            def add_nodes(node, parent_id=None, x=0, y=0, level=0):
                node_id = str(id(node))
                
                # Create clean labels without emojis for PNG
                if node.type == "QuantityQuery":
                    label = f"Query {idx + 1}\nQuantity Query"
                elif node.type == "OriginalPhrase":
                    phrase = str(node.value)[:20] + "..." if len(str(node.value)) > 20 else str(node.value)
                    label = f"Input:\n\"{phrase}\""
                elif node.type == "QueryStyle":
                    label = f"Style:\n{str(node.value)}"
                elif node.type == "ProductType":
                    product_map = {
                        "MOBILES": "Mobile Phones", "MOBILE": "Mobile Phone",
                        "PHONES": "Phones", "PHONE": "Phone",
                        "TVS": "Televisions", "TV": "Television",
                        "LAPTOPS": "Laptops", "LAPTOP": "Laptop",
                        "COMPUTERS": "Computers", "COMPUTER": "Computer",
                        "TABLETS": "Tablets", "TABLET": "Tablet"
                    }
                    product_name = product_map.get(str(node.value).upper(), str(node.value))
                    label = f"Product:\n{product_name}"
                elif node.type == "ItemID":
                    label = f"Item:\n{str(node.value)}"
                elif node.type == "Location":
                    location_name = "Warehouse" if str(node.value).upper() == "STOCK" else "Store"
                    label = f"Location:\n{location_name}"
                else:
                    label = f"{node.type}\n{str(node.value)}" if node.value else node.type
                
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
            nx.draw(G, pos_dict, labels=labels, node_color='lightblue', 
                    node_size=2500, font_size=7, font_weight='bold',
                    arrows=True, arrowsize=15, edge_color='gray',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8),
                    ax=ax)
            
            ax.set_title(f"Query {idx + 1}: \"{query_part}\"", fontsize=12, fontweight='bold', pad=10)
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename

def p_query(p):
    '''query : single_query
             | compound_query'''
    p[0] = p[1]

def p_single_query(p):
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

def p_compound_query(p):
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

def p_quantity_query(p):
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

def p_list_query(p):
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

def p_availability_query(p):
    '''availability_query : WHAT IS AVAILABLE
                          | WHAT products ARE AVAILABLE
                          | SHOW AVAILABLE products'''
    original_phrase = " ".join([str(token) for token in p[1:]])
    p[0] = ASTNode("AvailabilityQuery", children=[
        ASTNode("OriginalPhrase", original_phrase),
        ASTNode("Target", "available_products")
    ])

def p_low_stock_query(p):
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

def p_comparison_query(p):
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

def p_product_type(p):
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

def p_products(p):
    '''products : PRODUCTS
                | ITEMS'''
    p[0] = p[1]

def p_location(p):
    '''location : STORE
                | STOCK
                | THE STORE
                | THE STOCK'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_error(p):
    if p:
        print(f"Syntax error near '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# =============================
# 3. TRANSLATION: NL → SQL
# =============================
def ast_to_sql(ast):
    if ast.type == "CompoundQuery":
        # Handle multiple queries
        queries = []
        for child in ast.children:
            sql = ast_to_sql(child)
            if sql:
                queries.append(sql)
        return queries  # Return list of SQL queries
    
    elif ast.type == "QuantityQuery":
        # Check if it's a specific item ID or product type
        item_child = None
        product_child = None
        
        for child in ast.children:
            if child.type == "ItemID":
                item_child = child
            elif child.type == "ProductType":
                product_child = child
        
        if item_child:  # Specific item query
            item_id = item_child.value
            return f"SELECT item_id, name, quantity FROM stock WHERE item_id = '{item_id}';"
        elif product_child:  # Product type query
            product_type = product_child.value.upper()
            if product_type in ["TVS", "TV"]:
                return "SELECT item_id, name, quantity FROM stock WHERE item_id LIKE 'TV%';"
            elif product_type in ["PHONES", "PHONE", "MOBILES", "MOBILE", "SMARTPHONE"]:
                return "SELECT item_id, name, quantity FROM stock WHERE item_id LIKE 'PH%';"
            elif product_type in ["LAPTOPS", "LAPTOP", "COMPUTERS", "COMPUTER"]:
                return "SELECT item_id, name, quantity FROM stock WHERE item_id LIKE 'LP%';"
            elif product_type in ["TABLETS", "TABLET"]:
                return "SELECT item_id, name, quantity FROM stock WHERE category = 'Tablets';"
            elif product_type in ["DRIVES", "DRIVE", "HARD_DRIVE"]:
                return "SELECT item_id, name, quantity FROM stock WHERE item_id LIKE 'HD%';"
    
    elif ast.type == "ListQuery":
        return "SELECT item_id, name, quantity FROM stock ORDER BY name;"
    
    elif ast.type == "AvailabilityQuery":
        return "SELECT item_id, name, quantity FROM stock WHERE quantity > 0 ORDER BY name;"
    
    elif ast.type == "LowStockQuery":
        threshold = 0
        for child in ast.children:
            if child.type == "Threshold":
                threshold = child.value
        return f"SELECT item_id, name, quantity FROM stock WHERE quantity <= {threshold} ORDER BY quantity;"
    
    elif ast.type == "ComparisonQuery":
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
    
    return "SELECT item_id, name, quantity FROM stock;"

# =============================
# 4. SUGGESTIONS (FUZZY MATCH)
# =============================
def suggest(query, vocab):
    words = query.split()
    suggestions = {}
    corrected_query = query.lower()
    
    for w in words:
        close = difflib.get_close_matches(w.lower(), vocab, n=1, cutoff=0.6)
        if close and close[0] != w.lower():
            suggestions[w] = close[0]
            # Replace in corrected query
            corrected_query = corrected_query.replace(w.lower(), close[0])
    
    return suggestions, corrected_query if suggestions else None

# =============================
# 5. TEST DATABASE (SQLite)
# =============================
def init_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE stock (
        item_id TEXT PRIMARY KEY,
        name TEXT,
        quantity INTEGER,
        category TEXT,
        price REAL
    );
    """)
    test_data = [
        # TVs
        ("TV-1234", "Smart TV 42 inch", 15, "Electronics", 499.99),
        ("TV-5678", "4K Ultra HD TV 55 inch", 8, "Electronics", 799.99),
        ("TV-9999", "OLED TV 65 inch", 3, "Electronics", 1299.99),
        
        # Phones/Mobiles
        ("PH-5678", "Smartphone Galaxy S24", 42, "Electronics", 899.99),
        ("PH-1111", "iPhone 15 Pro", 25, "Electronics", 999.99),
        ("PH-2222", "Budget Android Phone", 60, "Electronics", 199.99),
        
        # Laptops/Computers 
        ("LP-2468", "Laptop Pro 15 inch", 8, "Computers", 1299.99),
        ("LP-3333", "Gaming Laptop RTX 4070", 5, "Computers", 1599.99),
        ("LP-4444", "Ultrabook 13 inch", 12, "Computers", 899.99),
        
        # Tablets
        ("TB-1111", "iPad Air 10.9 inch", 18, "Tablets", 599.99),
        ("TB-2222", "Android Tablet 11 inch", 22, "Tablets", 349.99),
        
        # Hard Drives
        ("HD-9999", "Hard Drive 1TB", 120, "Storage", 59.99),
        ("HD-5555", "SSD 500GB", 35, "Storage", 79.99),
        ("HD-6666", "External HDD 2TB", 0, "Storage", 99.99),  # Out of stock
        
        # Other items
        ("KB-1111", "Wireless Keyboard", 2, "Accessories", 49.99),  # Low stock
        ("MS-2222", "Gaming Mouse", 1, "Accessories", 69.99),      # Very low stock
        ("HD-7777", "USB Flash Drive 64GB", 150, "Storage", 19.99),
    ]
    cur.executemany("INSERT INTO stock VALUES (?, ?, ?, ?, ?);", test_data)
    conn.commit()
    return conn

# =============================
# 6. MAIN EXECUTION
# =============================
if __name__ == "__main__":
    conn = init_db()

    while True:
        query = input("\nEnter your NL query (or 'exit'): ")
        if query.lower() == "exit":
            break

        # Suggest corrections
        vocab = ["i", "want", "to", "know", "how", "many", "units", "of", "item", "items", "product", "products",
                "tvs", "tv", "phones", "phone", "mobiles", "mobile", "smartphone", "laptops", "laptop", 
                "computers", "computer", "tablets", "tablet", "drives", "drive", "hard",
                "in", "the", "store", "stock", "show", "list", "all", "what", "is", "are", "available",
                "low", "out", "empty", "less", "than", "more", "greater", "we", "have", "do", "you",
                "can", "get", "tell", "me", "and", "also"]
        suggestions, corrected_query = suggest(query, vocab)
        
        if suggestions:
            print("\n📝 Error Corrections Made:")
            for original, correction in suggestions.items():
                print(f"   '{original}' → '{correction}'")
            print(f"📄 Corrected Query: '{corrected_query}'")
            
            # Try parsing the corrected query if original fails
            original_query = query
            query = corrected_query

        # Check for multiple queries (split by question marks followed by new query words)
        import re
        
        # Split on question marks followed by query starters
        query_parts = re.split(r'\?\s*(?=how|what|show|list|can)', query, flags=re.IGNORECASE)
        query_parts = [q.strip() for q in query_parts if q.strip()]
        
        if len(query_parts) > 1:
            print(f"\n🔍 Detected {len(query_parts)} separate queries:")
            all_results = []
            all_asts = []
            
            for i, sub_query in enumerate(query_parts, 1):
                print(f"\n--- Query {i}: \"{sub_query}\" ---")
                
                # Parse each sub-query separately
                ast = parser.parse(sub_query)
                if ast:
                    all_asts.append(ast)  # Store AST for compound visualization
                    sql = ast_to_sql(ast)
                    cur = conn.cursor()
                    
                    if isinstance(sql, list):
                        for j, single_sql in enumerate(sql, 1):
                            print(f"🔍 Generated SQL {i}.{j}: {single_sql}")
                            try:
                                cur.execute(single_sql)
                                result = cur.fetchall()
                                print(f"📊 Result {i}.{j}: {result}")
                                all_results.append(result)
                            except sqlite3.Error as e:
                                print(f"❌ SQL Error {i}.{j}: {e}")
                    else:
                        print(f"🔍 Generated SQL {i}: {sql}")
                        try:
                            cur.execute(sql)
                            result = cur.fetchall()
                            print(f"📊 Result {i}: {result}")
                            all_results.append(result)
                        except sqlite3.Error as e:
                            print(f"❌ SQL Error {i}: {e}")
                    
                    # Display AST for each query
                    print(f"\n🌳 AST Structure {i}:")
                    print(ast.to_text_tree())
                else:
                    print(f"❌ Could not parse query {i}.")
            
            # Generate compound PNG if any queries succeeded
            if all_asts:
                try:
                    filename = ASTNode.create_compound_png(all_asts, query_parts, "compound_ast_tree.png")
                    print(f"\n🖼️  Compound AST diagram saved as: {filename}")
                    print(f"📊 Shows all {len(all_asts)} queries in side-by-side visualization!")
                except Exception as e:
                    print(f"⚠️  Could not generate compound PNG: {e}")
            
            continue  # Skip the single query processing below
        
        # Single query processing (existing logic)
        # Parse
        ast = parser.parse(query)
        if ast:
            sql = ast_to_sql(ast)
            cur = conn.cursor()
            
            # Handle both single SQL queries and lists of SQL queries
            if isinstance(sql, list):
                print(f"\n🔍 Generated {len(sql)} SQL queries:")
                for i, single_sql in enumerate(sql, 1):
                    print(f"   Query {i}: {single_sql}")
                    try:
                        cur.execute(single_sql)
                        result = cur.fetchall()
                        print(f"📊 Result {i}: {result}")
                    except sqlite3.Error as e:
                        print(f"❌ SQL Error {i}: {e}")
            else:
                print("\n🔍 Generated SQL:", sql)
                try:
                    cur.execute(sql)
                    result = cur.fetchall()
                    print("📊 Result:", result)
                except sqlite3.Error as e:
                    print("❌ SQL Error:", e)

            # Display AST as text tree
            print("\n🌳 AST Structure:")
            print(ast.to_text_tree())
            
            # Generate PNG image of AST
            try:
                filename = ast.to_png("ast_tree.png")
                print(f"🖼️  AST diagram saved as: {filename}")
            except Exception as e:
                print(f"⚠️  Could not generate PNG: {e}")
        else:
            print("❌ Could not parse query.")
