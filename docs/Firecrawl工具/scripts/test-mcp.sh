#!/bin/bash

# MCP Tools Test Script
# This script tests the MCP tools configuration

echo "🧪 Testing MCP Tools Configuration..."
echo ""

# Test 1: Check if MCP packages are installed
echo "1. Checking MCP packages installation..."
npm list -g firecrawl-mcp @playwright/mcp @modelcontextprotocol/server-sequential-thinking @modelcontextprotocol/server-fetch @modelcontextprotocol/server-filesystem

if [ $? -eq 0 ]; then
    echo "✅ All MCP packages are installed"
else
    echo "❌ Some MCP packages are missing"
fi

echo ""

# Test 2: Test Firecrawl MCP server (without API key)
echo "2. Testing Firecrawl MCP server..."
echo "Note: This will show help information if the server is properly installed"
npx -y firecrawl-mcp --help

if [ $? -eq 0 ]; then
    echo "✅ Firecrawl MCP server is working"
else
    echo "❌ Firecrawl MCP server has issues"
fi

echo ""

# Test 3: Check MCP configuration file
echo "3. Checking MCP configuration..."
if [ -f ".trae/mcp.json" ]; then
    echo "✅ MCP configuration file exists"
    echo "Configuration preview:"
    cat .trae/mcp.json | head -10
else
    echo "❌ MCP configuration file missing"
fi

echo ""

# Test 4: Check environment file
echo "4. Checking environment configuration..."
if [ -f ".env.mcp" ]; then
    echo "✅ Environment file exists"
    echo "Please ensure your FIRECRAWL_API_KEY is set in .env.mcp"
else
    echo "⚠️  Environment file not found. Copy from .env.mcp.example:"
    echo "cp .env.mcp.example .env.mcp"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Get your Firecrawl API key from: https://www.firecrawl.dev/app/api-keys"
echo "2. Add the API key to your .env.mcp file"
echo "3. Restart Trae IDE to load the new configuration"
echo "4. Test the MCP tools in your IDE"
echo ""
echo "📚 For detailed instructions, see: MCP_SETUP_GUIDE.md"