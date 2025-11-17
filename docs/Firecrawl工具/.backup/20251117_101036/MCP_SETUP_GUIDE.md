# MCP Tools Configuration for Trae IDE

This document provides comprehensive setup instructions for MCP (Model Context Protocol) tools in Trae IDE.

## 🚀 Quick Start

1. **Get Firecrawl API Key**
   - Visit: https://www.firecrawl.dev/app/api-keys
   - Sign up with your Google email
   - Generate your API key

2. **Configure MCP Tools**
   ```bash
   # Run the setup script
   ./setup-mcp.sh
   
   # Edit the environment file with your API keys
   nano .env.mcp
   ```

3. **Restart Trae IDE** to load the new MCP configuration

## 📋 Available MCP Tools

### 1. Firecrawl MCP Server
- **Purpose**: Web scraping, crawling, and data extraction
- **Features**: 
  - Scrape single URLs
  - Crawl entire websites
  - Search and extract structured data
  - Batch processing with rate limiting
- **Configuration**: See `.trae/mcp.json`

### 2. Playwright MCP
- **Purpose**: Browser automation and testing
- **Features**:
  - Automated browser actions
  - Screenshot capture
  - Form interaction
  - Page navigation

### 3. Sequential Thinking MCP
- **Purpose**: Complex problem-solving and analysis
- **Features**:
  - Multi-step reasoning
  - Task decomposition
  - Decision tree analysis

### 4. Fetch MCP
- **Purpose**: HTTP requests and web API integration
- **Features**:
  - REST API calls
  - Data retrieval
  - Web service integration

### 5. Filesystem MCP
- **Purpose**: File system operations
- **Features**:
  - File reading/writing
  - Directory operations
  - Path management

## ⚙️ Configuration Files

### `.trae/mcp.json`
Main MCP server configuration file defining all available MCP tools.

### `.env.mcp`
Environment variables for MCP tools (API keys, settings, etc.)

### `.env.mcp.example`
Template file showing all available configuration options.

## 🔧 Advanced Configuration

### Firecrawl Retry Settings
```bash
FIRECRAWL_RETRY_MAX_ATTEMPTS=3
FIRECRAWL_RETRY_INITIAL_DELAY=1000
FIRECRAWL_RETRY_MAX_DELAY=10000
FIRECRAWL_RETRY_BACKOFF_FACTOR=2
```

### Credit Monitoring
```bash
FIRECRAWL_CREDIT_WARNING_THRESHOLD=1000
FIRECRAWL_CREDIT_CRITICAL_THRESHOLD=100
```

### Custom API URL (for self-hosted)
```bash
FIRECRAWL_API_URL=https://firecrawl.your-domain.com
```

## 🧪 Testing MCP Tools

After configuration, test your MCP tools:

```bash
# Test Firecrawl MCP
npx -y firecrawl-mcp --help

# Test with your API key
FIRECRAWL_API_KEY=your_key_here npx -y firecrawl-mcp
```

## 🔒 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Add `.env.mcp` to `.gitignore`**
4. **Rotate API keys regularly**
5. **Use least-privilege API keys** when possible

## 📚 MCP Tool Usage Examples

### Web Scraping with Firecrawl
```json
{
  "name": "firecrawl_scrape",
  "arguments": {
    "url": "https://example.com",
    "formats": ["markdown"],
    "onlyMainContent": true,
    "timeout": 30000
  }
}
```

### Batch Processing
```json
{
  "name": "firecrawl_batch_scrape",
  "arguments": {
    "urls": ["https://site1.com", "https://site2.com"],
    "options": {
      "formats": ["markdown"],
      "onlyMainContent": true
    }
  }
}
```

### Deep Research
```json
{
  "name": "firecrawl_deep_research",
  "arguments": {
    "query": "How does carbon capture technology work?",
    "maxDepth": 3,
    "timeLimit": 120,
    "maxUrls": 50
  }
}
```

## 🆘 Troubleshooting

### Common Issues

1. **MCP Server not starting**
   - Check API key configuration
   - Verify network connectivity
   - Review MCP server logs

2. **Rate limiting errors**
   - Adjust retry configuration
   - Monitor credit usage
   - Implement exponential backoff

3. **Authentication failures**
   - Verify API key validity
   - Check environment variable setup
   - Ensure proper header formatting

### Debug Mode
Enable debug logging by setting:
```bash
export MCP_DEBUG=true
```

## 📞 Support

For MCP-related issues:
1. Check official MCP documentation
2. Review tool-specific error logs
3. Test with minimal configuration
4. Contact tool providers for API issues

## 🔗 Useful Links

- [Firecrawl Documentation](https://docs.firecrawl.dev/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Trae IDE Documentation](https://trae.ai/docs)
- [Firecrawl MCP Server GitHub](https://github.com/mendableai/firecrawl-mcp-server)