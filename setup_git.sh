#!/bin/bash

# Change to the mcp_connector_pkg directory
cd /Users/rishabhsharma/PycharmProjects/mcp-connector/mcp_connector_pkg

# Initialize git repository
echo "Initializing Git repository..."
git init

# Add all files
echo "Adding files to Git..."
git add .

# Make initial commit
echo "Making initial commit..."
git commit -m "Initial commit: PayPal MCP Connector package"

# Add remote
echo "Adding remote repository..."
git remote add origin git@github.com:rishabh17081/pp-agenttoolkit.git

# Verify remote
echo "Verifying remote repository..."
git remote -v

echo "Git repository set up successfully with remote tracking!"

# Setup branch
echo "Setting up main branch tracking..."
git branch -M main

echo "Git setup complete. You can now push with: git push -u origin main"
