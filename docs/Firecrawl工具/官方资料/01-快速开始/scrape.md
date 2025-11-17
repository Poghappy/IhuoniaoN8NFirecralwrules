# Scrape

> Turn any url into clean data

Firecrawl converts web pages into markdown, ideal for LLM applications.

* It manages complexities: proxies, caching, rate limits, js-blocked content
* Handles dynamic content: dynamic websites, js-rendered sites, PDFs, images
* Outputs clean markdown, structured data, screenshots or html.

For details, see the [Scrape Endpoint API Reference](https://docs.firecrawl.dev/api-reference/endpoint/scrape).

## Scraping a URL with Firecrawl

### /scrape endpoint

Used to scrape a URL and get its content.

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

  # Scrape a website:
  doc = firecrawl.scrape("https://firecrawl.dev", formats=["markdown", "html"])
  print(doc)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  // Scrape a website:
  const doc = await firecrawl.scrape('https://firecrawl.dev', { formats: ['markdown', 'html'] });
  console.log(doc);
  ```

  ```bash cURL
  curl -s -X POST "https://api.firecrawl.dev/v2/scrape" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "url": "https://firecrawl.dev",
      "formats": ["markdown", "html"]
    }'
  ```
</CodeGroup>

For more details about the parameters, refer to the [API Reference](https://docs.firecrawl.dev/api-reference/endpoint/scrape).

### Response

SDKs will return the data object directly. cURL will return the payload exactly as shown below.

```json
{
  "success": true,
  "data" : {
    "markdown": "Launch Week I is here! [See our Day 2 Release 🚀](https://www.firecrawl.dev/blog/launch-week-i-day-2-doubled-rate-limits)[💥 Get 2 months free...",
    "html": "<!DOCTYPE html><html lang=\"en\" class=\"light\" style=\"color-scheme: light;\"><body class=\"__variable_36bd41 __variable_d7dc5d font-inter ...",
    "metadata": {
      "title": "Home - Firecrawl",
      "description": "Firecrawl crawls and converts any website into clean markdown.",
      "language": "en",
      "keywords": "Firecrawl,Markdown,Data,Mendable,Langchain",
      "robots": "follow, index",
      "ogTitle": "Firecrawl",
      "ogDescription": "Turn any website into LLM-ready data.",
      "ogUrl": "https://www.firecrawl.dev/",
      "ogImage": "https://www.firecrawl.dev/og.png?123",
      "ogLocaleAlternate": [],
      "ogSiteName": "Firecrawl",
      "sourceURL": "https://firecrawl.dev",
      "statusCode": 200
    }
  }
}
```

## Scrape Formats

You can now choose what formats you want your output in. You can specify multiple output formats. Supported formats are:

* Markdown (`markdown`)
* Summary (`summary`)
* HTML (`html`)
* Raw HTML (`rawHtml`) (with no modifications)
* Screenshot (`screenshot`, with options like `fullPage`, `quality`, `viewport`)
* Links (`links`)
* JSON (`json`) - structured output

Output keys will match the format you choose.

## Extract structured data

### /scrape (with json) endpoint

Used to extract structured data from scraped pages.

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl
  from pydantic import BaseModel
  app = Firecrawl(api_key="fc-YOUR-API-KEY")

  class JsonSchema(BaseModel):
      company_mission: str
      supports_sso: bool
      is_open_source: bool
      is_in_yc: bool

  result = app.scrape(
      'https://firecrawl.dev',
      formats=[{
        "type": "json",
        "schema": JsonSchema
      }],
      only_main_content=False,
      timeout=120000
  )

  print(result)
  ```

  ```js Node
  import FirecrawlApp from "@mendable/firecrawl-js";
  import { z } from "zod";

  const app = new FirecrawlApp({
    apiKey: "fc-YOUR_API_KEY"
  });

  // Define schema to extract contents into
  const schema = z.object({
    company_mission: z.string(),
    supports_sso: z.boolean(),
    is_open_source: z.boolean(),
    is_in_yc: z.boolean()
  });

  const result = await app.scrape("https://docs.firecrawl.dev/", {
    formats: [{
      type: "json",
      schema: schema
    }],
  });

  console.log(result);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://docs.firecrawl.dev/",
        "formats": [ {
          "type": "json",
          "schema": {
            "type": "object",
            "properties": {
              "company_mission": {
                        "type": "string"
              },
              "supports_sso": {
                        "type": "boolean"
              },
              "is_open_source": {
                        "type": "boolean"
              },
              "is_in_yc": {
                        "type": "boolean"
              }
            },
            "required": [
              "company_mission",
              "supports_sso",
              "is_open_source",
              "is_in_yc"
            ]
          }
        } ]
      }'
  ```
</CodeGroup>

Output:

```json JSON
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "AI-powered web scraping and data extraction",
        "supports_sso": true,
        "is_open_source": true,
        "is_in_yc": true
      },
      "metadata": {
        "title": "Firecrawl",
        "description": "AI-powered web scraping and data extraction",
        "robots": "follow, index",
        "ogTitle": "Firecrawl",
        "ogDescription": "AI-powered web scraping and data extraction",
        "ogUrl": "https://firecrawl.dev/",
        "ogImage": "https://firecrawl.dev/og.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Firecrawl",
        "sourceURL": "https://firecrawl.dev/"
      },
    }
}
```

### Extracting without schema

You can now extract without a schema by just passing a `prompt` to the endpoint. The llm chooses the structure of the data.

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  app = Firecrawl(api_key="fc-YOUR-API-KEY")

  result = app.scrape(
      'https://firecrawl.dev',
      formats=[{
        "type": "json",
        "prompt": "Extract the company mission from the page."
      }],
      only_main_content=False,
      timeout=120000
  )

  print(result)
  ```

  ```js Node
  import FirecrawlApp from "@mendable/firecrawl-js";

  const app = new FirecrawlApp({
    apiKey: "fc-YOUR_API_KEY"
  });

  const result = await app.scrape("https://docs.firecrawl.dev/", {
    formats: [{
      type: "json",
      prompt: "Extract the company mission from the page."
    }]
  });

  console.log(result);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://docs.firecrawl.dev/",
        "formats": [{
          "type": "json",
          "prompt": "Extract the company mission from the page."
        }]
      }'
  ```
</CodeGroup>

Output:

```json JSON
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "AI-powered web scraping and data extraction",
      },
      "metadata": {
        "title": "Firecrawl",
        "description": "AI-powered web scraping and data extraction",
        "robots": "follow, index",
        "ogTitle": "Firecrawl",
        "ogDescription": "AI-powered web scraping and data extraction",
        "ogUrl": "https://firecrawl.dev/",
        "ogImage": "https://firecrawl.dev/og.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Firecrawl",
        "sourceURL": "https://firecrawl.dev/"
      },
    }
}
```

### JSON format options

When using the `json` format, pass an object inside `formats` with the following parameters:

* `schema`: JSON Schema for the structured output.
* `prompt`: Optional prompt to help guide extraction when a schema is present or when you prefer light guidance.

## Interacting with the page with Actions

Firecrawl allows you to perform various actions on a web page before scraping its content. This is particularly useful for interacting with dynamic content, navigating through pages, or accessing content that requires user interaction.

Here is an example of how to use actions to navigate to google.com, search for Firecrawl, click on the first result, and take a screenshot.

It is important to almost always use the `wait` action before/after executing other actions to give enough time for the page to load.

### Example

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  doc = firecrawl.scrape('https://example.com/login', {
    formats=['markdown'],
    actions=[
      { type: 'write', text: 'john@example.com' },
      { type: 'press', key: 'Tab' },
      { type: 'write', text: 'secret' },
      { type: 'click', selector: 'button[type="submit"]' },
      { type: 'wait', milliseconds: 1500 },
      { type: 'screenshot', fullPage: true },
    ],
  });

  print(doc.markdown, doc.screenshot);
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const doc = await firecrawl.scrape('https://example.com/login', {
    formats: ['markdown'],
    actions: [
      { type: 'write', text: 'john@example.com' },
      { type: 'press', key: 'Tab' },
      { type: 'write', text: 'secret' },
      { type: 'click', selector: 'button[type="submit"]' },
      { type: 'wait', milliseconds: 1500 },
      { type: 'screenshot', fullPage: true },
    ],
  });

  console.log(doc.markdown, doc.screenshot);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://example.com/login",
        "formats": ["markdown"],
        "actions": [
          { "type": "write", "text": "john@example.com" },
          { "type": "press", "key": "Tab" },
          { "type": "write", "text": "secret" },
          { "type": "click", "selector": "button[type=\"submit\"]" },
          { "type": "wait", "milliseconds": 1500 },
          { "type": "screenshot", "fullPage": true },
        ],
    }'
  ```
</CodeGroup>

### Output

<CodeGroup>
  ```json JSON
  {
    "success": true,
    "data": {
      "markdown": "Our first Launch Week is over! [See the recap 🚀](blog/firecrawl-launch-week-1-recap)...",
      "actions": {
        "screenshots": [
          "https://alttmdsdujxrfnakrkyi.supabase.co/storage/v1/object/public/media/screenshot-75ef2d87-31e0-4349-a478-fb432a29e241.png"
        ],
        "scrapes": [
          {
            "url": "https://www.firecrawl.dev/",
            "html": "<html><body><h1>Firecrawl</h1></body></html>"
          }
        ]
      },
      "metadata": {
        "title": "Home - Firecrawl",
        "description": "Firecrawl crawls and converts any website into clean markdown.",
        "language": "en",
        "keywords": "Firecrawl,Markdown,Data,Mendable,Langchain",
        "robots": "follow, index",
        "ogTitle": "Firecrawl",
        "ogDescription": "Turn any website into LLM-ready data.",
        "ogUrl": "https://www.firecrawl.dev/",
        "ogImage": "https://www.firecrawl.dev/og.png?123",
        "ogLocaleAlternate": [],
        "ogSiteName": "Firecrawl",
        "sourceURL": "http://google.com",
        "statusCode": 200
      }
    }
  }
  ```
</CodeGroup>

For more details about the actions parameters, refer to the [API Reference](https://docs.firecrawl.dev/api-reference/endpoint/scrape).

## Location and Language

Specify country and preferred languages to get relevant content based on your target location and language preferences.

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

  doc = firecrawl.scrape('https://example.com',
      formats=['markdown'],
      location={
          'country': 'US',
          'languages': ['en']
      }
  )

  print(doc)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const doc = await firecrawl.scrape('https://example.com', {
    formats: ['markdown'],
    location: { country: 'US', languages: ['en'] },
  });

  console.log(doc.metadata);
  ```

  ```bash cURL
  curl -X POST "https://api.firecrawl.dev/v2/scrape" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "url": "https://example.com",
      "formats": ["markdown"],
      "location": { "country": "US", "languages": ["en"] }
    }'
  ```
</CodeGroup>

For more details about supported locations, refer to the [Proxies documentation](/features/proxies).

## Caching and maxAge

To make requests faster, Firecrawl serves results from cache by default when a recent copy is available.

* **Default freshness window**: `maxAge = 172800000` ms (2 days). If a cached page is newer than this, it’s returned instantly; otherwise, the page is scraped and then cached.
* **Performance**: This can speed up scrapes by up to 5x when data doesn’t need to be ultra-fresh.
* **Always fetch fresh**: Set `maxAge` to `0`.
* **Avoid storing**: Set `storeInCache` to `false` if you don’t want Firecrawl to cache/store results for this request.

Example (force fresh content):

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl
  firecrawl = Firecrawl(api_key='fc-YOUR_API_KEY')

  doc = firecrawl.scrape(url='https://example.com', maxAge=0, formats=['markdown'])
  print(doc)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const doc = await firecrawl.scrape('https://example.com', { maxAge: 0, formats: ['markdown'] });
  console.log(doc);
  ```

  ```bash cURL
  curl -s -X POST "https://api.firecrawl.dev/v2/scrape" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "url": "https://example.com",
      "maxAge": 0,
      "formats": ["markdown"]
    }'
  ```
</CodeGroup>

Example (use a 10-minute cache window):

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl
  firecrawl = Firecrawl(api_key='fc-YOUR_API_KEY')

  doc = firecrawl.scrape(url='https://example.com', maxAge=600000, formats=['markdown', 'html'])
  print(doc)
  ```

  ```js Node

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const doc = await firecrawl.scrape('https://example.com', { maxAge: 600000, formats: ['markdown', 'html'] });
  console.log(doc);
  ```

  ```bash cURL
  curl -s -X POST "https://api.firecrawl.dev/v2/scrape" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "url": "https://example.com",
      "maxAge": 600000,
      "formats": ["markdown", "html"]
    }'
  ```
</CodeGroup>

## Batch scraping multiple URLs

You can now batch scrape multiple URLs at the same time. It takes the starting URLs and optional parameters as arguments. The params argument allows you to specify additional options for the batch scrape job, such as the output formats.

### How it works

It is very similar to how the `/crawl` endpoint works. It submits a batch scrape job and returns a job ID to check the status of the batch scrape.

The sdk provides 2 methods, synchronous and asynchronous. The synchronous method will return the results of the batch scrape job, while the asynchronous method will return a job ID that you can use to check the status of the batch scrape.

### Usage

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  job = firecrawl.batch_scrape([
      "https://firecrawl.dev",
      "https://docs.firecrawl.dev",
  ], formats=["markdown"], poll_interval=2, wait_timeout=120)

  print(job)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const job = await firecrawl.batchScrape([
    'https://firecrawl.dev',
    'https://docs.firecrawl.dev',
  ], { options: { formats: ['markdown'] }, pollInterval: 2, timeout: 120 });

  console.log(job);
  ```

  ```bash cURL
  curl -s -X POST "https://api.firecrawl.dev/v2/batch/scrape" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "urls": ["https://firecrawl.dev", "https://docs.firecrawl.dev"],
      "formats": ["markdown"]
    }'
  ```
</CodeGroup>

### Response

If you’re using the sync methods from the SDKs, it will return the results of the batch scrape job. Otherwise, it will return a job ID that you can use to check the status of the batch scrape.

#### Synchronous

```json Completed
{
  "status": "completed",
  "total": 36,
  "completed": 36,
  "creditsUsed": 36,
  "expiresAt": "2024-00-00T00:00:00.000Z",
  "next": "https://api.firecrawl.dev/v2/batch/scrape/123-456-789?skip=26",
  "data": [
    {
      "markdown": "[Firecrawl Docs home page![light logo](https://mintlify.s3-us-west-1.amazonaws.com/firecrawl/logo/light.svg)!...",
      "html": "<!DOCTYPE html><html lang=\"en\" class=\"js-focus-visible lg:[--scroll-mt:9.5rem]\" data-js-focus-visible=\"\">...",
      "metadata": {
        "title": "Build a 'Chat with website' using Groq Llama 3 | Firecrawl",
        "language": "en",
        "sourceURL": "https://docs.firecrawl.dev/learn/rag-llama3",
        "description": "Learn how to use Firecrawl, Groq Llama 3, and Langchain to build a 'Chat with your website' bot.",
        "ogLocaleAlternate": [],
        "statusCode": 200
      }
    },
    ...
  ]
}
```

#### Asynchronous

You can then use the job ID to check the status of the batch scrape by calling the `/batch/scrape/{id}` endpoint. This endpoint is meant to be used while the job is still running or right after it has completed **as batch scrape jobs expire after 24 hours**.

```json
{
  "success": true,
  "id": "123-456-789",
  "url": "https://api.firecrawl.dev/v2/batch/scrape/123-456-789"
}
```

## Stealth Mode

For websites with advanced anti-bot protection, Firecrawl offers a stealth proxy mode that provides better success rates at scraping challenging sites.

Learn more about [Stealth Mode](/features/stealth-mode).
