# PayPal MCP Connector

A Python package for interacting with PayPal's Merchant Catalog Products API, compliant with the Merchant Capability Protocol (MCP) for SmitheryAI deployment.

## Features

- Create products in PayPal catalog
- List products from PayPal catalog
- Show detailed product information
- Update existing products
- MCP-compliant API for SmitheryAI integration

## Installation

Clone the repository and install:

```bash
git clone https://github.com/rishabh17081/pp-agenttoolkit.git
cd pp-agenttoolkit
pip install -r requirements.txt
pip install -e .
```

## Usage

### Python API

```python
from paypal_connector.connector import MCPConnector

# Initialize the connector
connector = MCPConnector(client_id, client_secret, sandbox=True)

# Create a product
product = connector.create_product(
    name="Product Name",
    type="PHYSICAL",
    description="Product description"
)

# List products
products = connector.list_products()

# Get product details
product_details = connector.show_product_details(product_id="PROD-123456789")

# Update a product
updated_product = connector.update_product(
    product_id="PROD-123456789",
    description="Updated description"
)
```

### CLI Usage

Set up environment variables:
```bash
export PAYPAL_CLIENT_ID=your_client_id
export PAYPAL_CLIENT_SECRET=your_client_secret
```

Commands:
```bash
# Create a product
mcp-connector create_product --name "Product Name" --type PHYSICAL --description "Product description"

# List products
mcp-connector list_products

# Show product details
mcp-connector show_product_details --product_id PROD-123456789

# Update a product
mcp-connector update_product --product_id PROD-123456789 --description "Updated description"
```

## Running the Server

You can run the server using the console script:

```bash
export PAYPAL_CLIENT_ID=your_client_id
export PAYPAL_CLIENT_SECRET=your_client_secret
export HOST=0.0.0.0  # Optional, default is 127.0.0.1
export PORT=8000     # Optional, default is 8000

# Run using the console script
mcp-server

# Or run directly with Python
python -m paypal_connector.standalone_server
```

## Deploying to SmitheryAI

This package is designed to be easily deployed to SmitheryAI:

1. **Self-contained Server**: The `standalone_server.py` contains everything needed to run the service
2. **No Import Dependencies**: All code is contained within a single file to avoid import issues
3. **SmitheryAI Configuration**: The `smithery.yaml` is set up for automatic deployment

### Deployment Steps

1. Push your code to the GitHub repository:
   ```bash
   git push origin main
   ```

2. In the SmitheryAI dashboard:
   - Connect to your GitHub repository
   - Select the repository and branch
   - Set up the required environment variables:
     - `PAYPAL_CLIENT_ID`: Your PayPal API Client ID
     - `PAYPAL_CLIENT_SECRET`: Your PayPal API Client Secret

3. Deploy the agent using the SmitheryAI interface

## Available API Endpoints

- `/tools/call` - Tool invocation endpoint
- `/metadata` - Service metadata and tool discovery
- `/health` - Server health check

## License

MIT
