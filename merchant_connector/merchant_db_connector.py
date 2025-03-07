from fastmcp import FastMCP
from typing import Dict, List, Optional, Union, Any
import sqlite3
import os
import json

# Create the FastMCP server instance for Database MCP
mcp = FastMCP(name="E-commerce Database Connector")


class DatabaseConnector:
    """SQLite database connector for the e-commerce database."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the connector with the path to the database.

        Args:
            db_path: Path to the SQLite database. If None, uses default path.
        """
        if db_path is None:
            # Default path relative to the ecommerce site
            self.db_path = "/Users/rishabhsharma/PycharmProjects/ecommerce-site/scripts/db/ecommerce.db"
        else:
            self.db_path = db_path

        self.connection = None

    def connect(self) -> None:
        """Establish a connection to the database."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found at: {self.db_path}")

        self.connection = sqlite3.connect(self.db_path)
        # Configure SQLite connection to return rows as dictionaries
        self.connection.row_factory = sqlite3.Row

    def disconnect(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def _execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a query and return results as a list of dictionaries.

        Args:
            query: SQL query to execute
            params: Parameters for the query

        Returns:
            List of dictionaries with query results
        """
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute(query, params)

        # Convert SQLite rows to dictionaries
        results = [dict(row) for row in cursor.fetchall()]
        cursor.close()

        return results

    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Retrieve all users from the database.

        Returns:
            List of dictionaries containing user information
        """
        query = """
        SELECT id, username, email, first_name, last_name, 
               address, city, state, zip_code, country, phone,
               created_at, last_login
        FROM users
        ORDER BY id
        """

        return self._execute_query(query)

    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Retrieve all products from the database.

        Returns:
            List of dictionaries containing product information
        """
        query = """
        SELECT id, name, description, price, image,
               category, inventory, created_at, updated_at
        FROM products
        ORDER BY id
        """

        return self._execute_query(query)

    def get_all_cards(self) -> List[Dict[str, Any]]:
        """
        Retrieve all payment cards from the database.

        Returns:
            List of dictionaries containing card information with associated user details
        """
        query = """
        SELECT c.id, c.user_id, u.username, u.email,
               c.card_type, c.last_four, c.expiry_date,
               c.cardholder_name, c.is_default, c.created_at
        FROM cards c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.user_id, c.id
        """

        return self._execute_query(query)

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific user by ID.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            Dictionary with user information or None if not found
        """
        query = """
        SELECT id, username, email, first_name, last_name, 
               address, city, state, zip_code, country, phone,
               created_at, last_login
        FROM users
        WHERE id = ?
        """

        results = self._execute_query(query, (user_id,))
        return results[0] if results else None

    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific product by ID.

        Args:
            product_id: ID of the product to retrieve

        Returns:
            Dictionary with product information or None if not found
        """
        query = """
        SELECT id, name, description, price, image,
               category, inventory, created_at, updated_at
        FROM products
        WHERE id = ?
        """

        results = self._execute_query(query, (product_id,))
        return results[0] if results else None

    def get_cards_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve all payment cards for a specific user.

        Args:
            user_id: ID of the user

        Returns:
            List of dictionaries containing card information
        """
        query = """
        SELECT c.id, c.user_id, c.card_type, c.last_four,
               c.expiry_date, c.cardholder_name, c.is_default, c.created_at
        FROM cards c
        WHERE c.user_id = ?
        ORDER BY c.is_default DESC, c.id
        """

        return self._execute_query(query, (user_id,))

    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Retrieve all products in a specific category.

        Args:
            category: Product category to filter by

        Returns:
            List of dictionaries containing product information
        """
        query = """
        SELECT id, name, description, price, image,
               category, inventory, created_at, updated_at
        FROM products
        WHERE category = ?
        ORDER BY id
        """

        return self._execute_query(query, (category,))


# Helper function to get database connector
def get_db_connector():
    return DatabaseConnector()


# Define the MCP interface for database operations

@mcp.resource("config://database")
def get_database_info() -> Dict[str, Any]:
    """
    Get information about the connected database.

    Returns:
        Dict[str, Any]: Database information
    """
    connector = get_db_connector()
    try:
        connector.connect()

        # Get counts of each entity type
        user_count = len(connector.get_all_users())
        product_count = len(connector.get_all_products())
        card_count = len(connector.get_all_cards())

        return {
            "status": "connected",
            "database_path": connector.db_path,
            "counts": {
                "users": user_count,
                "products": product_count,
                "cards": card_count
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        connector.disconnect()


@mcp.resource("resource://ecommerce/users")
def getAllUsersFromDatabase() -> List[Dict[str, Any]]:
    """
    Retrieve all users from the database.

    Returns:
        List[Dict[str, Any]]: All users in the database
    """
    connector = get_db_connector()
    try:
        connector.connect()
        return connector.get_all_users()
    finally:
        connector.disconnect()


@mcp.resource("resource://ecommerce/products")
def getAllProductsFromDatabase() -> List[Dict[str, Any]]:
    """
    Retrieve all products from the database.

    Returns:
        List[Dict[str, Any]]: All products in the database
    """
    connector = get_db_connector()
    try:
        connector.connect()
        return connector.get_all_products()
    finally:
        connector.disconnect()


@mcp.resource("resource://ecommerce/cards")
def getAllCardsFromDatabase() -> List[Dict[str, Any]]:
    """
    Retrieve all payment cards from the database.

    Returns:
        List[Dict[str, Any]]: All cards in the database with associated user information
    """
    connector = get_db_connector()
    try:
        connector.connect()
        return connector.get_all_cards()
    finally:
        connector.disconnect()


@mcp.resource("resource://ecommerce/users/{user_id}")
def getUserByIdFromDataBase(user_id: int) -> Dict[str, Any]:
    """
    Retrieve a specific user by ID.

    Args:
        user_id: ID of the user to retrieve

    Returns:
        Dict[str, Any]: User details or error message if not found
    """
    connector = get_db_connector()
    try:
        connector.connect()
        user = connector.get_user_by_id(user_id)
        if user:
            return user
        else:
            return {"error": f"User with ID {user_id} not found"}
    finally:
        connector.disconnect()


@mcp.resource("resource://ecommerce/products/{product_id}")
def getProductById(product_id: int) -> Dict[str, Any]:
    """
    Retrieve a specific product by ID.

    Args:
        product_id: ID of the product to retrieve

    Returns:
        Dict[str, Any]: Product details or error message if not found
    """
    connector = get_db_connector()
    try:
        connector.connect()
        product = connector.get_product_by_id(product_id)
        if product:
            return product
        else:
            return {"error": f"Product with ID {product_id} not found"}
    finally:
        connector.disconnect()


@mcp.resource("resource://ecommerce/users/{user_id}/cards")
def getCardsByUserId(user_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve all payment cards for a specific user.

    Args:
        user_id: ID of the user

    Returns:
        List[Dict[str, Any]]: Cards associated with the user
    """
    connector = get_db_connector()
    try:
        connector.connect()
        # First check if user exists
        user = connector.get_user_by_id(user_id)
        if not user:
            return [{"error": f"User with ID {user_id} not found"}]

        return connector.get_cards_by_user_id(user_id)
    finally:
        connector.disconnect()


@mcp.resource("resource://ecommerce/products/category/{category}")
def getProductsByCategory(category: str) -> List[Dict[str, Any]]:
    """
    Retrieve all products in a specific category.

    Args:
        category: Product category to filter by

    Returns:
        List[Dict[str, Any]]: Products in the specified category
    """
    connector = get_db_connector()
    try:
        connector.connect()
        return connector.get_products_by_category(category)
    finally:
        connector.disconnect()


# Add MCP tools for the main functions that were requested
@mcp.tool(name="getAllUsersFromDatabase", description="Get all users from the ecommerce database")
def getAllUsersFromDatabase_tool() -> List[Dict[str, Any]]:
    """
    Retrieve all users from the database.

    Returns:
        List[Dict[str, Any]]: All users in the database
    """
    return getAllUsersFromDatabase()


@mcp.tool(name="getAllProductsFromDatabase", description="Get all products from the ecommerce database")
def getAllProductsFromDatabase_tool() -> List[Dict[str, Any]]:
    """
    Retrieve all products from the database.

    Returns:
        List[Dict[str, Any]]: All products in the database
    """
    return getAllProductsFromDatabase()


@mcp.tool(name="getAllCardsFromDatabase", description="Get all payment cards from the ecommerce database")
def getAllCardsFromDatabase_tool() -> List[Dict[str, Any]]:
    """
    Retrieve all payment cards from the database.

    Returns:
        List[Dict[str, Any]]: All cards in the database with associated user information
    """
    return getAllCardsFromDatabase()


if __name__ == "__main__":
    # This is a simple test to ensure the connector is working
    print("Testing Ecommerce Database Connector...")

    # Test database information
    db_info = get_database_info()
    print(f"Database Status: {db_info['status']}")

    if db_info['status'] == 'connected':
        print("Database counts:")
        for entity, count in db_info['counts'].items():
            print(f"  - {entity}: {count}")

        # Test getting users
        users = getAllUsersFromDatabase()
        if users:
            print(f"\nFound {len(users)} users, first user: {users[0]['username']}")
        else:
            print("\nNo users found")

        # Test getting products
        products = getAllProductsFromDatabase()
        if products:
            print(f"Found {len(products)} products, first product: {products[0]['name']}")
        else:
            print("No products found")

        # Test getting cards
        cards = getAllCardsFromDatabase()
        if cards:
            print(f"Found {len(cards)} payment cards")
        else:
            print("No payment cards found")

    print("\nTest complete.")


