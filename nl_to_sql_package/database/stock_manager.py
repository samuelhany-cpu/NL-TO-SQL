"""
Stock management database utilities

This module provides database setup, management, and query execution
for the stock management system.
"""

import sqlite3
from typing import List, Tuple, Optional, Dict, Any
import os


class StockManager:
    """
    Manages stock database operations and provides sample data.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize the stock manager.
        
        Args:
            db_path: Path to SQLite database file (default: in-memory)
        """
        self.db_path = db_path
        self.connection = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    def initialize_database(self) -> None:
        """Create the stock table and populate with sample data."""
        if not self.connection:
            self._connect()
        
        cursor = self.connection.cursor()
        
        # Create the stock table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            item_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            category TEXT NOT NULL,
            price REAL NOT NULL DEFAULT 0.0,
            supplier TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Check if table is empty and populate with sample data
        cursor.execute("SELECT COUNT(*) FROM stock")
        if cursor.fetchone()[0] == 0:
            self._populate_sample_data()
        
        self.connection.commit()
    
    def _populate_sample_data(self) -> None:
        """Populate the database with sample stock data."""
        sample_data = [
            # TVs
            ("TV-1234", "Smart TV 42 inch", 15, "Electronics", 499.99, "Samsung Corp"),
            ("TV-5678", "4K Ultra HD TV 55 inch", 8, "Electronics", 799.99, "LG Electronics"),
            ("TV-9999", "OLED TV 65 inch", 3, "Electronics", 1299.99, "Sony Corp"),
            
            # Phones/Mobiles
            ("PH-5678", "Smartphone Galaxy S24", 42, "Electronics", 899.99, "Samsung Corp"),
            ("PH-1111", "iPhone 15 Pro", 25, "Electronics", 999.99, "Apple Inc"),
            ("PH-2222", "Budget Android Phone", 60, "Electronics", 199.99, "Xiaomi Corp"),
            
            # Laptops/Computers 
            ("LP-2468", "Laptop Pro 15 inch", 8, "Computers", 1299.99, "Dell Technologies"),
            ("LP-3333", "Gaming Laptop RTX 4070", 5, "Computers", 1599.99, "MSI Gaming"),
            ("LP-4444", "Ultrabook 13 inch", 12, "Computers", 899.99, "HP Inc"),
            
            # Tablets
            ("TB-1111", "iPad Air 10.9 inch", 18, "Tablets", 599.99, "Apple Inc"),
            ("TB-2222", "Android Tablet 11 inch", 22, "Tablets", 349.99, "Samsung Corp"),
            
            # Hard Drives/Storage
            ("HD-9999", "Hard Drive 1TB", 120, "Storage", 59.99, "Western Digital"),
            ("HD-5555", "SSD 500GB", 35, "Storage", 79.99, "Samsung Corp"),
            ("HD-6666", "External HDD 2TB", 0, "Storage", 99.99, "Seagate Tech"),  # Out of stock
            ("HD-7777", "USB Flash Drive 64GB", 150, "Storage", 19.99, "SanDisk Corp"),
            
            # Accessories
            ("KB-1111", "Wireless Keyboard", 2, "Accessories", 49.99, "Logitech"),  # Low stock
            ("MS-2222", "Gaming Mouse", 1, "Accessories", 69.99, "Razer Inc"),      # Very low stock
        ]
        
        cursor = self.connection.cursor()
        cursor.executemany("""
        INSERT INTO stock (item_id, name, quantity, category, price, supplier) 
        VALUES (?, ?, ?, ?, ?, ?);
        """, sample_data)
    
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results.
        
        Args:
            sql: SQL query string
            
        Returns:
            List[Dict]: Query results as list of dictionaries
        """
        if not self.connection:
            self._connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            
            # Convert rows to dictionaries
            columns = [description[0] for description in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        except sqlite3.Error as e:
            print(f"SQL execution error: {e}")
            return []
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Get all products in the database."""
        return self.execute_query("SELECT * FROM stock ORDER BY name")
    
    def get_product_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a product by its ID.
        
        Args:
            item_id: Product item ID
            
        Returns:
            Dict containing product data or None if not found
        """
        results = self.execute_query(f"SELECT * FROM stock WHERE item_id = '{item_id}'")
        return results[0] if results else None
    
    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all products in a specific category.
        
        Args:
            category: Product category
            
        Returns:
            List of products in the category
        """
        return self.execute_query(f"SELECT * FROM stock WHERE category = '{category}' ORDER BY name")
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict[str, Any]]:
        """
        Get products with low stock.
        
        Args:
            threshold: Stock threshold (default: 10)
            
        Returns:
            List of low stock products
        """
        return self.execute_query(f"SELECT * FROM stock WHERE quantity <= {threshold} ORDER BY quantity")
    
    def get_out_of_stock_products(self) -> List[Dict[str, Any]]:
        """Get products that are out of stock."""
        return self.execute_query("SELECT * FROM stock WHERE quantity = 0 ORDER BY name")
    
    def update_stock_quantity(self, item_id: str, new_quantity: int) -> bool:
        """
        Update the stock quantity for a product.
        
        Args:
            item_id: Product item ID
            new_quantity: New quantity value
            
        Returns:
            bool: True if update was successful
        """
        if not self.connection:
            self._connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
            UPDATE stock SET quantity = ?, last_updated = CURRENT_TIMESTAMP 
            WHERE item_id = ?
            """, (new_quantity, item_id))
            
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Update error: {e}")
            return False
    
    def add_product(self, item_id: str, name: str, quantity: int, 
                   category: str, price: float, supplier: str = None) -> bool:
        """
        Add a new product to the database.
        
        Args:
            item_id: Product item ID
            name: Product name
            quantity: Initial quantity
            category: Product category
            price: Product price
            supplier: Supplier name (optional)
            
        Returns:
            bool: True if addition was successful
        """
        if not self.connection:
            self._connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
            INSERT INTO stock (item_id, name, quantity, category, price, supplier) 
            VALUES (?, ?, ?, ?, ?, ?)
            """, (item_id, name, quantity, category, price, supplier))
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Insert error: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the database.
        
        Returns:
            Dict containing database statistics
        """
        stats = {}
        
        # Total products
        result = self.execute_query("SELECT COUNT(*) as count FROM stock")
        stats['total_products'] = result[0]['count'] if result else 0
        
        # Total quantity
        result = self.execute_query("SELECT SUM(quantity) as total FROM stock")
        stats['total_quantity'] = result[0]['total'] if result and result[0]['total'] else 0
        
        # Categories
        result = self.execute_query("SELECT category, COUNT(*) as count FROM stock GROUP BY category")
        stats['categories'] = {row['category']: row['count'] for row in result}
        
        # Low stock count
        result = self.execute_query("SELECT COUNT(*) as count FROM stock WHERE quantity <= 10")
        stats['low_stock_count'] = result[0]['count'] if result else 0
        
        # Out of stock count
        result = self.execute_query("SELECT COUNT(*) as count FROM stock WHERE quantity = 0")
        stats['out_of_stock_count'] = result[0]['count'] if result else 0
        
        # Average price
        result = self.execute_query("SELECT AVG(price) as avg_price FROM stock")
        stats['average_price'] = round(result[0]['avg_price'], 2) if result and result[0]['avg_price'] else 0.0
        
        return stats
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def create_sample_database(db_path: str = "sample_stock.db") -> StockManager:
    """
    Create a sample database file for testing.
    
    Args:
        db_path: Path for the database file
        
    Returns:
        StockManager: Initialized stock manager
    """
    # Remove existing file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    manager = StockManager(db_path)
    manager.initialize_database()
    
    return manager
