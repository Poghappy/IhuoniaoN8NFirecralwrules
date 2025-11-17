#!/bin/bash

# MCP Tools Setup Script for Trae IDE
# This script helps set up MCP tools with proper configuration

echo "🔧 Setting up MCP Tools for Trae IDE..."

# Create .env.mcp file if it doesn't exist
if [ ! -f ".env.mcp" ]; then
    echo "Creating .env.mcp file..."
    cp .env.mcp.example .env.mcp
    echo "✅ Created .env.mcp file"
    echo "⚠️  Please edit .env.mcp and add your actual API keys"
else
    echo "✅ .env.mcp file already exists"
fi

# Create MCP configuration directory if it doesn't exist
mkdir -p .trae

# Install MCP packages globally
echo "📦 Installing MCP packages..."
npm install -g firecrawl-mcp
npm install -g @playwright/mcp
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-filesystem

echo "✅ MCP packages installed successfully"

# Test Firecrawl MCP server
echo "🧪 Testing Firecrawl MCP server..."
if [ -n "$FIRECRAWL_API_KEY" ] && [ "$FIRECRAWL_API_KEY" != "your_firecrawl_api_key_here" ]; then
    echo "Testing with your API key..."
    FIRECRAWL_API_KEY=$FIRECRAWL_API_KEY npx -y firecrawl-mcp --help
else
    echo "⚠️  Please set your FIRECRAWL_API_KEY in .env.mcp file first"
fi

echo ""
echo "🎉 MCP Tools setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env.mcp and add your actual API keys"
echo "2. Restart Trae IDE to load the new MCP configuration"
echo "3. Test the MCP tools in your IDE"
echo ""
echo "To get a Firecrawl API key:"
echo "- Visit: https://www.firecrawl.dev/app/api-keys"
echo "- Sign up with your Google email"
echo "- Generate your API key"
echo "- Add it to .env.mcp file"