#!/bin/bash

# Install local FastMCP package
echo "Installing local FastMCP package..."
pip install -e ./local_fastmcp

# Install the MCP connector package
echo "Installing MCP Connector package..."
pip install -e .

echo "Installation complete."
