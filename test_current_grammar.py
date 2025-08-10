#!/usr/bin/env python3
"""
Test the NLP parser with queries that match the current grammar
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nl_to_sql_package import NLToSQLParser

def test_current_grammar():
    """Test queries that should work with the current grammar"""
    
    parser = NLToSQLParser()
    
    # Queries that should work based on grammar analysis
    test_queries = [
        "Show all products",
        "List all products", 
        "What products are available",
        "How many phones",
        "How many laptops we have",
        "Show available products",
        "How many units of phones in store",
        "What is available",
        "Show low stock",
        "List all items",
        "How many tvs",
        "How many computers",
        "Show all items"
    ]
    
    print("🔍 Testing Current Grammar Capabilities")
    print("=" * 60)
    
    working_queries = []
    failed_queries = []
    
    for query in test_queries:
        try:
            print(f"\n📝 Testing: '{query}'")
            result = parser.parse_and_execute(query)
            
            if result['success'] and result['sql_queries']:
                sql = result['sql_queries'][0]
                print(f"✅ SUCCESS: {sql}")
                working_queries.append((query, sql))
            else:
                error_msg = '; '.join(result['errors']) if result['errors'] else 'No SQL generated'
                print(f"❌ FAILED: {error_msg}")
                failed_queries.append((query, error_msg))
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            failed_queries.append((query, str(e)))
    
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Queries: {len(test_queries)}")
    print(f"Working: {len(working_queries)}")
    print(f"Failed: {len(failed_queries)}")
    print(f"Success Rate: {len(working_queries)/len(test_queries)*100:.1f}%")
    
    if working_queries:
        print("\n✅ WORKING PATTERNS:")
        for query, sql in working_queries:
            print(f"   '{query}' → {sql}")
    
    if failed_queries:
        print("\n❌ FAILED PATTERNS:")
        for query, error in failed_queries[:5]:  # Show first 5
            print(f"   '{query}' → {error}")
    
    # Test a few variations to understand the pattern requirements
    print("\n🔍 TESTING VARIATIONS:")
    variations = [
        "Show me all products",  # Adding 'me'
        "show all products",     # lowercase
        "SHOW ALL PRODUCTS",     # uppercase
        "Show all product",      # singular
        "Display all products",  # different verb
    ]
    
    for query in variations:
        try:
            result = parser.parse_and_execute(query)
            if result['success']:
                print(f"✅ '{query}' → {result['sql_queries'][0]}")
            else:
                print(f"❌ '{query}' → Failed")
        except Exception as e:
            print(f"❌ '{query}' → Error: {str(e)}")

if __name__ == "__main__":
    test_current_grammar()
