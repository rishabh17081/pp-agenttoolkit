#!/usr/bin/env python3
"""
Simple script to run the PayPal MCP Connector server.
This script can be used to start the server locally for testing.
"""

from paypal_connector.paypal_agent_mcp import main

if __name__ == "__main__":
    print("Starting PayPal MCP Connector server...")
    main()
