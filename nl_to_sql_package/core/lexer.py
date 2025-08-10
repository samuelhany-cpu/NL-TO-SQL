"""
Lexer implementation for Natural Language to SQL Parser

This module contains the lexical analyzer that tokenizes natural language queries
into tokens that can be parsed by the grammar rules.
"""

import ply.lex as lex
from typing import Any


# Token definitions - these represent all the words/patterns our lexer can recognize
tokens = (
    'I', 'WANT', 'TO', 'KNOW', 'HOW_MANY', 'UNITS', 'OF', 'ITEM', 'ITEMS', 'PRODUCT', 'PRODUCTS',
    'ID', 'IN', 'STORE', 'STOCK', 'THE', 'TVS', 'PHONES', 'LAPTOPS', 'DRIVES', 'SMARTPHONE',
    'LAPTOP', 'TV', 'PHONE', 'HARD', 'DRIVE', 'ALL', 'SHOW', 'LIST', 'WHAT', 'IS', 'ARE',
    'AVAILABLE', 'LOW', 'OUT', 'EMPTY', 'LESS', 'THAN', 'MORE', 'GREATER', 'NUMBER', 
    'MOBILES', 'MOBILE', 'COMPUTERS', 'COMPUTER', 'TABLETS', 'TABLET', 'WE', 'HAVE', 
    'DO', 'YOU', 'CAN', 'GET', 'TELL', 'ME', 'QUESTION_MARK', 'AND', 'ALSO', 'WORD'
)

# Ignored characters (whitespace and tabs)
t_ignore = ' \t'


# Lexer rule functions - these define how to recognize each token
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
    """Error handling for illegal characters."""
    print(f"Illegal character '{t.value[0]}' ignored.")
    t.lexer.skip(1)


def get_lexer() -> Any:
    """
    Create and return a lexer instance.
    
    Returns:
        PLY lexer object configured with our token rules
    """
    return lex.lex()


def get_vocabulary() -> list:
    """
    Get the vocabulary of recognized words for error correction.
    
    Returns:
        list: List of recognized words
    """
    return [
        "i", "want", "to", "know", "how", "many", "units", "of", "item", "items", 
        "product", "products", "tvs", "tv", "phones", "phone", "mobiles", "mobile", 
        "smartphone", "laptops", "laptop", "computers", "computer", "tablets", "tablet", 
        "drives", "drive", "hard", "in", "the", "store", "stock", "show", "list", "all", 
        "what", "is", "are", "available", "low", "out", "empty", "less", "than", "more", 
        "greater", "we", "have", "do", "you", "can", "get", "tell", "me", "and", "also"
    ]


def tokenize_query(query: str) -> list:
    """
    Tokenize a query string into a list of tokens.
    
    Args:
        query: The input query string
        
    Returns:
        list: List of token objects
    """
    lexer = get_lexer()
    lexer.input(query)
    
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    
    return tokens
