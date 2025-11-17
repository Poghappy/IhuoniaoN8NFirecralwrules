# Search

> Search the web and get full content from results

Firecrawl's search API allows you to perform web searches and optionally scrape the search results in one operation.

* Choose specific output formats (markdown, HTML, links, screenshots)
* Search the web with customizable parameters (location, etc.)
* Optionally retrieve content from search results in various formats
* Control the number of results and set timeouts

For details, see the [Search Endpoint API Reference](https://docs.firecrawl.dev/api-reference/endpoint/search).

## Performing a Search with Firecrawl

### /search endpoint

Used to perform web searches and optionally retrieve content from the results.

### Installation

<CodeGroup>
  ```python Python
  # pip install firecrawl-py

  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")
  ```

  ```js Node
  # npm install @mendable/firecrawl-js

  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });
  ```
</CodeGroup>

### Basic Usage

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  results = firecrawl.search(
      query="firecrawl",
      limit=3,
  )
  print(results)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const results = await firecrawl.search('firecrawl', {
    limit: 3,
    scrapeOptions: { formats: ['markdown'] }
  });
  console.log(results);
  ```

  ```bash
  curl -s -X POST "https://api.firecrawl.dev/v2/search" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "query": "firecrawl",
      "limit": 3
    }'
  ```
</CodeGroup>

### Response

SDKs will return the data object directly. cURL will return the complete payload.

```json JSON
{
  "success": true,
  "data": {
    "web": [
      {
        "url": "https://www.firecrawl.dev/",
        "title": "Firecrawl - The Web Data API for AI",
        "description": "The web crawling, scraping, and search API for AI. Built for scale. Firecrawl delivers the entire internet to AI agents and builders.",
        "position": 1
      },
      {
        "url": "https://github.com/mendableai/firecrawl",
        "title": "mendableai/firecrawl: Turn entire websites into LLM-ready ... - GitHub",
        "description": "Firecrawl is an API service that takes a URL, crawls it, and converts it into clean markdown or structured data.",
        "position": 2
      },
      ...
    ],
    "images": [
      {
        "title": "Quickstart | Firecrawl",
        "imageUrl": "https://mintlify.s3.us-west-1.amazonaws.com/firecrawl/logo/logo.png",
        "imageWidth": 5814,
        "imageHeight": 1200,
        "url": "https://docs.firecrawl.dev/",
        "position": 1
      },
      ...
    ],
    "news": [
      {
        "title": "Y Combinator startup Firecrawl is ready to pay $1M to hire three AI agents as employees",
        "url": "https://techcrunch.com/2025/05/17/y-combinator-startup-firecrawl-is-ready-to-pay-1m-to-hire-three-ai-agents-as-employees/",
        "snippet": "It's now placed three new ads on YC's job board for “AI agents only” and has set aside a $1 million budget total to make it happen.",
        "date": "3 months ago",
        "position": 1
      },
      ...
    ]
  }
}
```

## Search result types

In addition to regular web results, Search supports specialized result types via the `sources` parameter:

* `web`: standard web results (default)
* `news`: news-focused results
* `images`: image search results

## Search Categories

Filter search results by specific categories using the `categories` parameter:

* `github`: Search within GitHub repositories, code, issues, and documentation
* `research`: Search academic and research websites (arXiv, Nature, IEEE, PubMed, etc.)

### GitHub Category Search

Search specifically within GitHub repositories:

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -d '{
    "query": "web scraping python",
    "categories": ["github"],
    "limit": 10
  }'
```

### Research Category Search

Search academic and research websites:

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -d '{
    "query": "machine learning transformers",
    "categories": ["research"],
    "limit": 10
  }'
```

### Mixed Category Search

Combine multiple categories in one search:

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -d '{
    "query": "neural networks",
    "categories": ["github", "research"],
    "limit": 15
  }'
```

### Category Response Format

Each search result includes a `category` field indicating its source:

```json
{
  "success": true,
  "data": {
    "web": [
      {
        "url": "https://github.com/example/neural-network",
        "title": "Neural Network Implementation",
        "description": "A PyTorch implementation of neural networks",
        "category": "github"
      },
      {
        "url": "https://arxiv.org/abs/2024.12345",
        "title": "Advances in Neural Network Architecture",
        "description": "Research paper on neural network improvements",
        "category": "research"
      }
    ]
  }
}
```

Examples:

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -d '{
    "query": "openai",
    "sources": ["news"],
    "limit": 5
  }'
```

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -d '{
    "query": "jupiter",
    "sources": ["images"],
    "limit": 8
  }'
```

### HD Image Search with Size Filtering

Use Google Images operators to find high-resolution images:

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -d '{
    "query": "sunset imagesize:1920x1080",
    "sources": ["images"],
    "limit": 5
  }'
```

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -d '{
    "query": "mountain wallpaper larger:2560x1440",
    "sources": ["images"],
    "limit": 8
  }'
```

**Common HD resolutions:**

* `imagesize:1920x1080` - Full HD (1080p)
* `imagesize:2560x1440` - QHD (1440p)
* `imagesize:3840x2160` - 4K UHD
* `larger:1920x1080` - HD and above
* `larger:2560x1440` - QHD and above

## Search with Content Scraping

Search and retrieve content from the search results in one operation.

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR_API_KEY")

  # Search and scrape content
  results = firecrawl.search(
      "firecrawl web scraping",
      limit=3,
      scrape_options={
          "formats": ["markdown", "links"]
      }
  )
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const results = await firecrawl.search('firecrawl', {
    limit: 3,
    scrapeOptions: { formats: ['markdown'] }
  });
  console.log(results);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/search \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer fc-YOUR_API_KEY" \
    -d '{
      "query": "firecrawl web scraping",
      "limit": 3,
      "scrapeOptions": {
        "formats": ["markdown", "links"]
      }
    }'
  ```
</CodeGroup>

Every option in scrape endpoint is supported by this search endpoint through the `scrapeOptions` parameter.

### Response with Scraped Content

```json
{
  "success": true,
  "data": [
    {
      "title": "Firecrawl - The Ultimate Web Scraping API",
      "description": "Firecrawl is a powerful web scraping API that turns any website into clean, structured data for AI and analysis.",
      "url": "https://firecrawl.dev/",
      "markdown": "# Firecrawl\n\nThe Ultimate Web Scraping API\n\n## Turn any website into clean, structured data\n\nFirecrawl makes it easy to extract data from websites for AI applications, market research, content aggregation, and more...",
      "links": [
        "https://firecrawl.dev/pricing",
        "https://firecrawl.dev/docs",
        "https://firecrawl.dev/guides"
      ],
      "metadata": {
        "title": "Firecrawl - The Ultimate Web Scraping API",
        "description": "Firecrawl is a powerful web scraping API that turns any website into clean, structured data for AI and analysis.",
        "sourceURL": "https://firecrawl.dev/",
        "statusCode": 200
      }
    }
  ]
}
```

## Advanced Search Options

Firecrawl's search API supports various parameters to customize your search:

### Location Customization

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR_API_KEY")

  # Search with location settings (Germany)
  search_result = firecrawl.search(
      "web scraping tools",
      limit=5,
      location="Germany"
  )

  # Process the results
  for result in search_result.data:
      print(f"Title: {result['title']}")
      print(f"URL: {result['url']}")
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  // Search with location settings (Germany)
  const results = await firecrawl.search('web scraping tools', {
    limit: 5,
    location: "Germany"
  });

  // Process the results
  console.log(results);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/search \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer fc-YOUR_API_KEY" \
    -d '{
      "query": "web scraping tools",
      "limit": 5,
      "location": "Germany"
    }'
  ```
</CodeGroup>

### Time-Based Search

Use the `tbs` parameter to filter results by time:

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  results = firecrawl.search(
      query="firecrawl",
      limit=5,
      tbs="qdr:d",
  )
  print(len(results.get('web', [])))
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const results = await firecrawl.search('firecrawl', {
    limit: 5,
    tbs: 'qdr:d', // past day
  });

  console.log(results.web);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/search \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer fc-YOUR_API_KEY" \
    -d '{
      "query": "latest web scraping techniques",
      "limit": 5,
      "tbs": "qdr:w"
    }'
  ```
</CodeGroup>

Common `tbs` values:

* `qdr:h` - Past hour
* `qdr:d` - Past 24 hours
* `qdr:w` - Past week
* `qdr:m` - Past month
* `qdr:y` - Past year

For more precise time filtering, you can specify exact date ranges using the custom date range format:

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  # Initialize the client with your API key
  firecrawl = Firecrawl(api_key="fc-YOUR_API_KEY")

  # Search for results from December 2024
  search_result = firecrawl.search(
      "firecrawl updates",
      limit=10,
      tbs="cdr:1,cd_min:12/1/2024,cd_max:12/31/2024"
  )
  ```

  ```js JavaScript
  import Firecrawl from '@mendable/firecrawl-js';

  // Initialize the client with your API key
  const firecrawl = new Firecrawl({apiKey: "fc-YOUR_API_KEY"});

  // Search for results from December 2024
  firecrawl.search("firecrawl updates", {
    limit: 10,
    tbs: "cdr:1,cd_min:12/1/2024,cd_max:12/31/2024"
  })
  .then(searchResult => {
    console.log(searchResult.data);
  });
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/search \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer fc-YOUR_API_KEY" \
    -d '{
      "query": "firecrawl updates",
      "limit": 10,
      "tbs": "cdr:1,cd_min:12/1/2024,cd_max:12/31/2024"
    }'
  ```
</CodeGroup>

### Custom Timeout

Set a custom timeout for search operations:

<CodeGroup>
  ```python Python
  from firecrawl import FirecrawlApp

  # Initialize the client with your API key
  app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

  # Set a 30-second timeout
  search_result = app.search(
      "complex search query",
      limit=10,
      timeout=30000  # 30 seconds in milliseconds
  )
  ```

  ```js JavaScript
  import FirecrawlApp from '@mendable/firecrawl-js';

  // Initialize the client with your API key
  const app = new FirecrawlApp({apiKey: "fc-YOUR_API_KEY"});

  // Set a 30-second timeout
  app.search("complex search query", {
    limit: 10,
    timeout: 30000  // 30 seconds in milliseconds
  })
  .then(searchResult => {
    // Process results
    console.log(searchResult.data);
  });
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/search \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer fc-YOUR_API_KEY" \
    -d '{
      "query": "complex search query",
      "limit": 10,
      "timeout": 30000
    }'
  ```
</CodeGroup>

## Cost Implications

The cost of using this endpoint is 1 credit per search result. There is no additional charge for basic scrapes of each search result.

However, be aware of these cost factors:

* **PDF parsing**: 1 credit per PDF page (can significantly increase costs for multi-page PDFs)
* **Stealth proxy mode**: +4 additional credits per search result
* ***JSON mode***: +4 additional credits per search result

To control costs:

* Set `parsers: []` if you don't need PDF content
* Use `proxy: "basic"` instead of `"stealth"` when possible
* Limit the number of search results with the `limit` parameter

## Advanced Scraping Options

For more details about the scraping options, refer to the [Scrape Feature documentation](https://docs.firecrawl.dev/features/scrape). Everything except for the FIRE-1 Agent and Change-Tracking features are supported by this Search endpoint.
