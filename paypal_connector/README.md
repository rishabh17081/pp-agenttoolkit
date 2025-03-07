# PayPal MCP Connector

A Python package for interacting with PayPal's Merchant Commerce Platform (MCP).

## Features

- Create products in PayPal catalog
- List products from PayPal catalog
- Show detailed product information
- Update existing products

## Installation

```bash
pip install mcp-connector-pkg
```

## Usage

```python
from paypal_connector.connector import MCPConnector

# Initialize the connector
connector = MCPConnector(client_id, client_secret, sandbox=True)

# Create a product
product = connector.create_product(
    name="Product Name",
    type="PHYSICAL",
    description="Product description",
    category="ELECTRONICS",
    image_url="https://example.com/image.jpg",
    home_url="https://example.com/product"
)

# List products
products = connector.list_products()

# Get product details
product_details = connector.show_product_details(product_id="PROD-123456789")

# Update a product
updated_product = connector.update_product(
    product_id="PROD-123456789",
    description="Updated description",
    category="UPDATED_CATEGORY",
    image_url="https://example.com/new-image.jpg",
    home_url="https://example.com/updated-product"
)
```

## CLI Usage

```bash
# Set up environment variables
export PAYPAL_CLIENT_ID=your_client_id
export PAYPAL_CLIENT_SECRET=your_client_secret

# Create a product
python -m paypal_connector.cli create_product --name "Product Name" --type PHYSICAL --description "Product description"

# List products
python -m paypal_connector.cli list_products

# Show product details
python -m paypal_connector.cli show_product_details --product_id PROD-123456789

# Update a product
python -m paypal_connector.cli update_product --product_id PROD-123456789 --description "Updated description"
```

## License

MIT
