# Map

> Input a website and get all the urls on the website - extremely fast

## Introducing /map

The easiest way to go from a single url to a map of the entire website. This is extremely useful for:

* When you need to prompt the end-user to choose which links to scrape
* Need to quickly know the links on a website
* Need to scrape pages of a website that are related to a specific topic (use the `search` parameter)
* Only need to scrape specific pages of a website

## Mapping

### /map endpoint

Used to map a URL and get urls of the website. This returns most links present on the website.

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

### Usage

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")
  res = firecrawl.map(url="https://firecrawl.dev", limit=50, sitemap="include")
  print(res)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const res = await firecrawl.map('https://firecrawl.dev', { limit: 50, sitemap: 'include' });
  console.log(res);
  ```
</CodeGroup>

### Response

SDKs will return the data object directly. cURL will return the payload exactly as shown below.

```json
{
  "success": true,
  "links": [
    {
      "url": "https://docs.firecrawl.dev/features/scrape",
      "title": "Scrape | Firecrawl",
      "description": "Turn any url into clean data"
    },
    {
      "url": "https://www.firecrawl.dev/blog/5_easy_ways_to_access_glm_4_5",
      "title": "5 Easy Ways to Access GLM-4.5",
      "description": "Discover how to access GLM-4.5 models locally, through chat applications, via the official API, and using the LLM marketplaces API for seamless integration i..."
    },
    {
      "url": "https://www.firecrawl.dev/playground",
      "title": "Playground - Firecrawl",
      "description": "Preview the API response and get the code snippets for the API"
    },
    {
      "url": "https://www.firecrawl.dev/?testId=2a7e0542-077b-4eff-bec7-0130395570d6",
      "title": "Firecrawl - The Web Data API for AI",
      "description": "The web crawling, scraping, and search API for AI. Built for scale. Firecrawl delivers the entire internet to AI agents and builders. Clean, structured, and ..."
    },
    {
      "url": "https://www.firecrawl.dev/?testId=af391f07-ca0e-40d3-8ff2-b1ecf2e3fcde",
      "title": "Firecrawl - The Web Data API for AI",
      "description": "The web crawling, scraping, and search API for AI. Built for scale. Firecrawl delivers the entire internet to AI agents and builders. Clean, structured, and ..."
    },
    ...
  ]
}
```

<Warning>
  Title and description are not always present as it depends on the website.
</Warning>

#### Map with search

Map with `search` param allows you to search for specific urls inside a website.

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/map \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "url": "https://firecrawl.dev",
    "search": "docs"
  }'
```

Response will be an ordered list from the most relevant to the least relevant.

```json
{
  "status": "success",
  "links": [
    {
      "url": "https://docs.firecrawl.dev",
      "title": "Firecrawl Docs",
      "description": "Firecrawl documentation"
    },
    {
      "url": "https://docs.firecrawl.dev/sdks/python",
      "title": "Firecrawl Python SDK",
      "description": "Firecrawl Python SDK documentation"
    },
    ...
  ]
}
```

## Location and Language

Specify country and preferred languages to get relevant content based on your target location and language preferences, similar to the scrape endpoint.

### How it works

When you specify the location settings, Firecrawl will use an appropriate proxy if available and emulate the corresponding language and timezone settings. By default, the location is set to 'US' if not specified.

### Usage

To use the location and language settings, include the `location` object in your request body with the following properties:

* `country`: ISO 3166-1 alpha-2 country code (e.g., 'US', 'AU', 'DE', 'JP'). Defaults to 'US'.
* `languages`: An array of preferred languages and locales for the request in order of priority. Defaults to the language of the specified location.

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  res = firecrawl.map('https://example.com',
      location={
          'country': 'US',
          'languages': ['en']
      }
  )

  print(res)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const res = await firecrawl.map('https://example.com', {
    location: { country: 'US', languages: ['en'] },
  });

  console.log(res.metadata);
  ```

  ```bash cURL
  curl -X POST "https://api.firecrawl.dev/v2/map" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "url": "https://example.com",
      "location": { "country": "US", "languages": ["en"] }
    }'
  ```
</CodeGroup>

For more details about supported locations, refer to the [Proxies documentation](/features/proxies).

## Considerations

This endpoint prioritizes speed, so it may not capture all website links. We are working on improvements. Feedback and suggestions are very welcome.
