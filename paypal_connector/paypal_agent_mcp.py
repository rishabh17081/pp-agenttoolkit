from fastmcp import FastMCP
from typing import Dict, List, Optional, Union, Any
import os
import requests

# Create the FastMCP server instance for MCP
mcp = FastMCP(name="PayPal MCP Connector")


# PayPal API Client class
class PayPalClient:
    def __init__(self, client_id: str, client_secret: str, sandbox: bool = True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox

        # Set the base URL based on environment
        if sandbox:
            self.base_url = "https://api-m.sandbox.paypal.com"
        else:
            self.base_url = "https://api-m.paypal.com"

        self.token = None

    def _get_auth_token(self) -> str:
        """Get OAuth token from PayPal."""
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US"
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(
            url,
            auth=(self.client_id, self.client_secret),
            headers=headers,
            data=data
        )

        if response.status_code == 200:
            self.token = response.json()["access_token"]
            return self.token
        else:
            raise Exception(f"Failed to get auth token: {response.text}")

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        if self.token is None:
            self._get_auth_token()

        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def request(self, method: str, endpoint: str, **kwargs):
        """Make a request to the PayPal API."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        # Merge headers with any provided in kwargs
        if "headers" in kwargs:
            headers = {**headers, **kwargs.pop("headers")}

        response = requests.request(method, url, headers=headers, **kwargs)

        if response.status_code in [200, 201, 204]:
            try:
                return response.json()
            except:
                return {"status": "success"}
        else:
            raise Exception(f"API request failed: {response.text}")


# Helper function to get PayPal client
def get_paypal_client():
    # move to env
    client_id = os.environ.get("PAYPAL_CLIENT_ID", "default - wont work")
    client_secret = os.environ.get("PAYPAL_CLIENT_SECRET", "default - wont work")
    return PayPalClient(client_id, client_secret, sandbox=True)


# Define functions for PayPal's Merchant Catalog Products API

@mcp.tool()
def create_product_in_paypal(
        name: str,
        type: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        image_url: Optional[str] = None,
        home_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a product in the PayPal catalog.

    Args:
        name: The product name
        type: The product type (PHYSICAL, DIGITAL, SERVICE)
        description: The product description
        category: The product category
        image_url: URL for the product image
        home_url: Home URL for the product

    Returns:
        Dict[str, Any]: The created product details
    """
    # Build the request payload
    payload = {
        "name": name,
        "type": type
    }

    if description:
        payload["description"] = description
    if category:
        payload["category"] = category
    if image_url:
        payload["image_url"] = image_url
    if home_url:
        payload["home_url"] = home_url

    # Get PayPal client and make the request
    client = get_paypal_client()
    endpoint = "/v1/catalogs/products"
    method = "POST"

    response = client.request(method, endpoint, json=payload)
    return response


@mcp.resource("config://app")
def list_products_from_paypal() -> Dict[str, Any]:
    """
    List products from the PayPal catalog. No arguments are required

    Returns:
        Dict[str, Any]: The list of products using specified pagination settings
    """
    # Set up query parameters
    params = {
        "page": 1,
        "page_size": 20,
        "total_required": str(True).lower()
    }

    # Get PayPal client and make the request
    client = get_paypal_client()
    endpoint = "/v1/catalogs/products"
    method = "GET"

    response = client.request(method, endpoint, params=params)
    return response


@mcp.resource(uri="resource://paypal/products/{product_id}", name="Show Product Details", mime_type="application/json")
def show_product_details_from_paypal(product_id: str) -> Dict[str, Any]:
    """
    Show details of a specific product.

    Args:
        product_id: The ID of the product

    Returns:
        Dict[str, Any]: The product details
    """
    # Get PayPal client and make the request
    client = get_paypal_client()
    endpoint = f"/v1/catalogs/products/{product_id}"
    method = "GET"

    response = client.request(method, endpoint)
    return response


@mcp.tool()
def update_products_to_paypal(
        product_id: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        image_url: Optional[str] = None,
        home_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Update a product in the PayPal catalog.

    Args:
        product_id: The ID of the product to update
        description: The updated product description
        category: The updated product category
        image_url: Updated URL for the product image
        home_url: Updated home URL for the product

    Returns:
        Dict[str, Any]: The updated product details
    """
    # Build the request payload with PATCH operations
    payload = []

    if description:
        payload.append({
            "op": "replace",
            "path": "/description",
            "value": description
        })
    if category:
        payload.append({
            "op": "replace",
            "path": "/category",
            "value": category
        })
    if image_url:
        payload.append({
            "op": "replace",
            "path": "/image_url",
            "value": image_url
        })
    if home_url:
        payload.append({
            "op": "replace",
            "path": "/home_url",
            "value": home_url
        })

    if not payload:
        raise ValueError("At least one field must be provided for update")

    # Get PayPal client and make the request
    client = get_paypal_client()
    endpoint = f"/v1/catalogs/products/{product_id}"
    method = "PATCH"

    response = client.request(method, endpoint, json=payload)
    return response


@mcp.tool(name="list_products", description="List products from PayPal")
def list_products_tool() -> Dict[str, Any]:
    """
    List products from the PayPal catalog.

    No Args

    Returns:
        Dict[str, Any]: The list of products
    """
    return list_products_from_paypal()


@mcp.tool(name="show_product_details", description="Show details of a specific product")
def show_product_details_tool(product_id: str) -> Dict[str, Any]:
    """
    Show details of a specific product.

    Args:
        product_id: The ID of the product

    Returns:
        Dict[str, Any]: The product details
    """
    return show_product_details_from_paypal(product_id)