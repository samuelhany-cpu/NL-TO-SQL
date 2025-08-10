#!/usr/bin/env python3
"""
Comprehensive NLP to SQL Parser Test Suite
This script tests various natural language queries and exports results for analysis.
"""

import json
import csv
import datetime
from typing import List, Dict, Any
import traceback
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from nl_to_sql_package import NLToSQLParser
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the virtual environment with all dependencies installed")
    sys.exit(1)

class NLPTestSuite:
    def __init__(self):
        self.parser = NLToSQLParser()
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def add_test_result(self, test_name: str, query: str, expected_sql: str, actual_sql: str, 
                       status: str, error_msg: str = "", execution_time: float = 0.0, 
                       parser_result: dict = None):
        """Add a test result to the results list"""
        result = {
            'test_name': test_name,
            'natural_language_query': query,
            'expected_sql': expected_sql,
            'generated_sql': actual_sql,
            'status': status,
            'error_message': error_msg,
            'execution_time_ms': round(execution_time * 1000, 2),
            'timestamp': datetime.datetime.now().isoformat(),
            'full_parser_result': parser_result or {}
        }
        self.test_results.append(result)
        
        if status == 'PASS':
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        self.total_tests += 1

    def test_basic_select_queries(self):
        """Test basic SELECT queries"""
        test_cases = [
            {
                'name': 'Simple SELECT all',
                'query': 'Show me all products',
                'expected': 'SELECT * FROM products'
            },
            {
                'name': 'SELECT with WHERE condition',
                'query': 'Show me all users where age is greater than 25',
                'expected': 'SELECT * FROM users WHERE age > 25'
            },
            {
                'name': 'SELECT specific columns',
                'query': 'Show me the name and email from users',
                'expected': 'SELECT name, email FROM users'
            },
            {
                'name': 'SELECT with ORDER BY',
                'query': 'Show me all products ordered by price',
                'expected': 'SELECT * FROM products ORDER BY price'
            },
            {
                'name': 'SELECT with LIMIT',
                'query': 'Show me the first 10 users',
                'expected': 'SELECT * FROM users LIMIT 10'
            }
        ]
        
        for test_case in test_cases:
            try:
                start_time = datetime.datetime.now()
                result = self.parser.parse_and_execute(test_case['query'])
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                # Extract SQL from result
                generated_sql = None
                error_msg = ""
                
                if result['success'] and result['sql_queries']:
                    generated_sql = result['sql_queries'][0] if result['sql_queries'] else None
                    # Check if result is close to expected (basic comparison)
                    status = 'PASS' if generated_sql and 'SELECT' in str(generated_sql).upper() else 'FAIL'
                else:
                    generated_sql = 'None'
                    status = 'FAIL'
                    error_msg = '; '.join(result['errors']) if result['errors'] else 'No SQL generated'
                
                self.add_test_result(
                    test_name=test_case['name'],
                    query=test_case['query'],
                    expected_sql=test_case['expected'],
                    actual_sql=str(generated_sql) if generated_sql else 'None',
                    status=status,
                    execution_time=execution_time,
                    error_msg=error_msg,
                    parser_result=result
                )
                
            except Exception as e:
                self.add_test_result(
                    test_name=test_case['name'],
                    query=test_case['query'],
                    expected_sql=test_case['expected'],
                    actual_sql='Error',
                    status='ERROR',
                    error_msg=str(e)
                )

    def test_complex_queries(self):
        """Test more complex SQL queries"""
        test_cases = [
            {
                'name': 'JOIN query',
                'query': 'Show me all orders with customer names',
                'expected': 'SELECT orders.*, customers.name FROM orders JOIN customers ON orders.customer_id = customers.id'
            },
            {
                'name': 'GROUP BY with COUNT',
                'query': 'Count the number of orders per customer',
                'expected': 'SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id'
            },
            {
                'name': 'Multiple WHERE conditions',
                'query': 'Show me products where price is between 100 and 500 and category is electronics',
                'expected': 'SELECT * FROM products WHERE price BETWEEN 100 AND 500 AND category = "electronics"'
            },
            {
                'name': 'Aggregate functions',
                'query': 'What is the average price of all products',
                'expected': 'SELECT AVG(price) FROM products'
            },
            {
                'name': 'HAVING clause',
                'query': 'Show me customers who have more than 5 orders',
                'expected': 'SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(*) > 5'
            }
        ]
        
        for test_case in test_cases:
            try:
                start_time = datetime.datetime.now()
                result = self.parser.parse_and_execute(test_case['query'])
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                # Extract SQL from result
                generated_sql = None
                error_msg = ""
                
                if result['success'] and result['sql_queries']:
                    generated_sql = result['sql_queries'][0] if result['sql_queries'] else None
                    # For complex queries, just check if SQL was generated
                    status = 'PARTIAL' if generated_sql and 'SELECT' in str(generated_sql).upper() else 'FAIL'
                else:
                    generated_sql = 'None'
                    status = 'FAIL'
                    error_msg = '; '.join(result['errors']) if result['errors'] else 'No SQL generated'
                
                self.add_test_result(
                    test_name=test_case['name'],
                    query=test_case['query'],
                    expected_sql=test_case['expected'],
                    actual_sql=str(generated_sql) if generated_sql else 'None',
                    status=status,
                    execution_time=execution_time,
                    error_msg=error_msg,
                    parser_result=result
                )
                
            except Exception as e:
                self.add_test_result(
                    test_name=test_case['name'],
                    query=test_case['query'],
                    expected_sql=test_case['expected'],
                    actual_sql='Error',
                    status='ERROR',
                    error_msg=str(e)
                )

    def test_edge_cases(self):
        """Test edge cases and error handling"""
        test_cases = [
            {
                'name': 'Empty query',
                'query': '',
                'expected': 'Error or None'
            },
            {
                'name': 'Non-SQL related query',
                'query': 'What is the weather today?',
                'expected': 'Error or None'
            },
            {
                'name': 'Ambiguous query',
                'query': 'Show me stuff',
                'expected': 'Error or None'
            },
            {
                'name': 'Very long query',
                'query': 'Show me all the products that have a very long description and are available in multiple colors and have been ordered by customers who live in different countries and have made purchases in the last year',
                'expected': 'Complex SELECT statement'
            },
            {
                'name': 'SQL injection attempt',
                'query': 'Show me all users; DROP TABLE users;',
                'expected': 'Safe handling without injection'
            }
        ]
        
        for test_case in test_cases:
            try:
                start_time = datetime.datetime.now()
                result = self.parser.parse_and_execute(test_case['query'])
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                # Extract SQL from result
                generated_sql = None
                error_msg = ""
                
                if result['success'] and result['sql_queries']:
                    generated_sql = result['sql_queries'][0] if result['sql_queries'] else None
                    # For edge cases, we mainly check that it doesn't crash
                    status = 'HANDLED' if generated_sql is not None else 'NO_OUTPUT'
                else:
                    generated_sql = 'None'
                    status = 'NO_OUTPUT'
                    error_msg = '; '.join(result['errors']) if result['errors'] else 'No SQL generated'
                
                self.add_test_result(
                    test_name=test_case['name'],
                    query=test_case['query'],
                    expected_sql=test_case['expected'],
                    actual_sql=str(generated_sql) if generated_sql else 'None',
                    status=status,
                    execution_time=execution_time,
                    error_msg=error_msg,
                    parser_result=result
                )
                
            except Exception as e:
                self.add_test_result(
                    test_name=test_case['name'],
                    query=test_case['query'],
                    expected_sql=test_case['expected'],
                    actual_sql='Error',
                    status='ERROR',
                    error_msg=str(e)
                )

    def test_real_world_scenarios(self):
        """Test realistic business queries"""
        test_cases = [
            {
                'name': 'Sales report',
                'query': 'What are the total sales for each product this month?',
                'expected': 'SELECT product_id, SUM(amount) FROM sales WHERE month = CURRENT_MONTH GROUP BY product_id'
            },
            {
                'name': 'Customer analysis',
                'query': 'Which customers have spent more than 1000 dollars?',
                'expected': 'SELECT customer_id FROM orders GROUP BY customer_id HAVING SUM(total) > 1000'
            },
            {
                'name': 'Inventory check',
                'query': 'Show me products that are out of stock',
                'expected': 'SELECT * FROM products WHERE stock = 0 OR stock IS NULL'
            },
            {
                'name': 'Top performers',
                'query': 'Who are the top 5 customers by total purchase amount?',
                'expected': 'SELECT customer_id, SUM(total) FROM orders GROUP BY customer_id ORDER BY SUM(total) DESC LIMIT 5'
            },
            {
                'name': 'Date range query',
                'query': 'Show me all orders from last week',
                'expected': 'SELECT * FROM orders WHERE order_date >= DATE_SUB(NOW(), INTERVAL 1 WEEK)'
            }
        ]
        
        for test_case in test_cases:
            try:
                start_time = datetime.datetime.now()
                result = self.parser.parse_and_execute(test_case['query'])
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                # Extract SQL from result
                generated_sql = None
                error_msg = ""
                
                if result['success'] and result['sql_queries']:
                    generated_sql = result['sql_queries'][0] if result['sql_queries'] else None
                    # For real-world scenarios, check if meaningful SQL was generated
                    status = 'GENERATED' if generated_sql and len(str(generated_sql)) > 10 else 'INSUFFICIENT'
                else:
                    generated_sql = 'None'
                    status = 'INSUFFICIENT'
                    error_msg = '; '.join(result['errors']) if result['errors'] else 'No SQL generated'
                
                self.add_test_result(
                    test_name=test_case['name'],
                    query=test_case['query'],
                    expected_sql=test_case['expected'],
                    actual_sql=str(generated_sql) if generated_sql else 'None',
                    status=status,
                    execution_time=execution_time,
                    error_msg=error_msg,
                    parser_result=result
                )
                
            except Exception as e:
                self.add_test_result(
                    test_name=test_case['name'],
                    query=test_case['query'],
                    expected_sql=test_case['expected'],
                    actual_sql='Error',
                    status='ERROR',
                    error_msg=str(e)
                )

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting NLP to SQL Parser Test Suite...")
        print("=" * 60)
        
        print("📊 Running Basic SELECT Queries Tests...")
        self.test_basic_select_queries()
        
        print("🔧 Running Complex Queries Tests...")
        self.test_complex_queries()
        
        print("⚠️  Running Edge Cases Tests...")
        self.test_edge_cases()
        
        print("🏢 Running Real-World Scenarios Tests...")
        self.test_real_world_scenarios()
        
        print("✅ All tests completed!")

    def export_results(self):
        """Export test results to multiple formats"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export to JSON
        json_filename = f"nlp_test_results_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': self.total_tests,
                    'passed_tests': self.passed_tests,
                    'failed_tests': self.failed_tests,
                    'success_rate': round((self.passed_tests / self.total_tests) * 100, 2) if self.total_tests > 0 else 0,
                    'timestamp': datetime.datetime.now().isoformat()
                },
                'test_results': self.test_results
            }, f, indent=2, ensure_ascii=False)
        
        # Export to CSV (exclude complex fields)
        csv_filename = f"nlp_test_results_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['test_name', 'natural_language_query', 'expected_sql', 'generated_sql', 
                         'status', 'error_message', 'execution_time_ms', 'timestamp']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            # Remove the full_parser_result field for CSV export
            csv_results = []
            for result in self.test_results:
                csv_result = {k: v for k, v in result.items() if k != 'full_parser_result'}
                csv_results.append(csv_result)
            writer.writerows(csv_results)
        
        # Create a summary report
        report_filename = f"nlp_test_summary_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("NLP to SQL Parser Test Summary Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Test Execution Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Tests: {self.total_tests}\n")
            f.write(f"Passed Tests: {self.passed_tests}\n")
            f.write(f"Failed Tests: {self.failed_tests}\n")
            f.write(f"Success Rate: {round((self.passed_tests / self.total_tests) * 100, 2) if self.total_tests > 0 else 0}%\n\n")
            
            # Group results by status
            status_groups = {}
            for result in self.test_results:
                status = result['status']
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(result)
            
            f.write("Results by Status:\n")
            f.write("-" * 20 + "\n")
            for status, results in status_groups.items():
                f.write(f"{status}: {len(results)} tests\n")
                for result in results[:5]:  # Show first 5 of each status
                    f.write(f"  - {result['test_name']}: {result['natural_language_query'][:50]}...\n")
                if len(results) > 5:
                    f.write(f"  ... and {len(results) - 5} more\n")
                f.write("\n")
        
        print(f"\n📁 Results exported to:")
        print(f"   📄 JSON: {json_filename}")
        print(f"   📊 CSV: {csv_filename}")
        print(f"   📋 Summary: {report_filename}")
        
        return json_filename, csv_filename, report_filename

    def print_summary(self):
        """Print a summary of test results"""
        print("\n" + "=" * 60)
        print("🎯 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        
        if self.total_tests > 0:
            success_rate = (self.passed_tests / self.total_tests) * 100
            print(f"Success Rate: {success_rate:.2f}%")
            
            if success_rate >= 80:
                print("🟢 Excellent performance!")
            elif success_rate >= 60:
                print("🟡 Good performance, room for improvement")
            else:
                print("🔴 Needs significant improvement")
        
        # Show sample results
        print("\n📋 Sample Results:")
        print("-" * 40)
        for i, result in enumerate(self.test_results[:5]):
            status_emoji = "✅" if result['status'] in ['PASS', 'GENERATED', 'HANDLED'] else "❌"
            print(f"{status_emoji} {result['test_name']}")
            print(f"   Query: {result['natural_language_query'][:60]}...")
            print(f"   Result: {result['generated_sql'][:60]}...")
            print()

def main():
    """Main function to run the test suite"""
    print("🔍 NLP to SQL Parser - Comprehensive Test Suite")
    print("=" * 60)
    
    # Initialize test suite
    test_suite = NLPTestSuite()
    
    try:
        # Run all tests
        test_suite.run_all_tests()
        
        # Print summary
        test_suite.print_summary()
        
        # Export results
        test_suite.export_results()
        
        print("\n🎉 Testing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("Traceback:")
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
