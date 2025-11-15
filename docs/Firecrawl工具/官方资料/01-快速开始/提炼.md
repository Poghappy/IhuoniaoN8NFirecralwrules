# Extract

> Extract structured data from pages using LLMs

The `/extract` endpoint simplifies collecting structured data from any number of URLs or entire domains. Provide a list of URLs, optionally with wildcards (e.g., `example.com/*`), and a prompt or schema describing the information you want. Firecrawl handles the details of crawling, parsing, and collating large or small datasets.

<Info>Extract is billed differently than other endpoints. See the [Extract pricing](https://www.firecrawl.dev/extract#pricing) for details.</Info>

## Using `/extract`

You can extract structured data from one or multiple URLs, including wildcards:

* **Single Page**\
  Example: `https://firecrawl.dev/some-page`
* **Multiple Pages / Full Domain**\
  Example: `https://firecrawl.dev/*`

When you use `/*`, Firecrawl will automatically crawl and parse all URLs it can discover in that domain, then extract the requested data. This feature is experimental; email [help@firecrawl.com](mailto:help@firecrawl.com) if you have issues.

### Example Usage

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  schema = {
      "type": "object",
      "properties": {"description": {"type": "string"}},
      "required": ["description"],
  }

  res = firecrawl.extract(
      urls=["https://docs.firecrawl.dev"],
      prompt="Extract the page description",
      schema=schema,
  )

  print(res.data["description"])
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const schema = {
    type: 'object',
    properties: {
      title: { type: 'string' }
    },
    required: ['title']
  };

  const res = await firecrawl.extract({
    urls: ['https://docs.firecrawl.dev'],
    prompt: 'Extract the page title',
    schema,
    scrapeOptions: { formats: [{ type: 'json', prompt: 'Extract', schema }] }
  });

  console.log(res.status || res.success, res.data);
  ```

  ```bash cURL
  curl -s -X POST "https://api.firecrawl.dev/v2/extract" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "urls": ["https://docs.firecrawl.dev"],
      "prompt": "Extract the page title",
      "schema": {
        "type": "object",
        "properties": {"title": {"type": "string"}},
        "required": ["title"]
      },
      "scrapeOptions": {
        "formats": [{"type": "json", "prompt": "Extract", "schema": {"type": "object"}}]
      }
    }'
  ```
</CodeGroup>

**Key Parameters:**

* **urls**: An array of one or more URLs. Supports wildcards (`/*`) for broader crawling.
* **prompt** (Optional unless no schema): A natural language prompt describing the data you want or specifying how you want that data structured.
* **schema** (Optional unless no prompt): A more rigid structure if you already know the JSON layout.
* **enableWebSearch** (Optional): When `true`, extraction can follow links outside the specified domain.

See [API Reference](https://docs.firecrawl.dev/api-reference/endpoint/extract) for more details.

### Response (sdks)

```json JSON
{
  "success": true,
  "data": {
    "company_mission": "Firecrawl is the easiest way to extract data from the web. Developers use us to reliably convert URLs into LLM-ready markdown or structured data with a single API call.",
    "supports_sso": false,
    "is_open_source": true,
    "is_in_yc": true
  }
}
```

## Job status and completion

When you submit an extraction job—either directly via the API or through the starter methods—you'll receive a Job ID. You can use this ID to:

* Get Job Status: Send a request to the /extract/{ID} endpoint to see if the job is still running or has finished.
* Wait for results: If you use the default `extract` method (Python/Node), the SDK waits and returns final results.
* Start then poll: If you use the start methods—`start_extract` (Python) or `startExtract` (Node)—the SDK returns a Job ID immediately. Use `get_extract_status` (Python) or `getExtractStatus` (Node) to check progress.

<Note>
  This endpoint only works for jobs in progress or recently completed (within 24
  hours).
</Note>

Below are code examples for checking an extraction job's status using Python, Node.js, and cURL:

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(
      api_key="fc-YOUR_API_KEY"
  )

  # Start an extraction job first
  extract_job = firecrawl.start_extract([
      'https://docs.firecrawl.dev/*', 
      'https://firecrawl.dev/'
  ], prompt="Extract the company mission and features from these pages.")

  # Get the status of the extraction job
  job_status = firecrawl.get_extract_status(extract_job.id)

  print(job_status)
  # Example output:
  # id=None
  # status='completed'
  # expires_at=datetime.datetime(...)
  # success=True
  # data=[{ ... }]
  # error=None
  # warning=None
  # sources=None
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const started = await firecrawl.startExtract({
    urls: ['https://docs.firecrawl.dev'],
    prompt: 'Extract title',
    schema: { type: 'object', properties: { title: { type: 'string' } }, required: ['title'] },
  });

  if (started.id) {
    const done = await firecrawl.getExtractStatus(started.id);
    console.log(done.status, done.data);
  }
  ```

  ```bash cURL
  curl -s -X GET "https://api.firecrawl.dev/v2/extract/<jobId>" \
    -H "Authorization: Bearer $FIRECRAWL_API_KEY"
  ```
</CodeGroup>

### Possible States

* **completed**: The extraction finished successfully.
* **processing**: Firecrawl is still processing your request.
* **failed**: An error occurred; data was not fully extracted.
* **cancelled**: The job was cancelled by the user.

#### Pending Example

```json JSON
{
  "success": true,
  "data": [],
  "status": "processing",
  "expiresAt": "2025-01-08T20:58:12.000Z"
}
```

#### Completed Example

```json JSON
{
  "success": true,
  "data": {
      "company_mission": "Firecrawl is the easiest way to extract data from the web. Developers use us to reliably convert URLs into LLM-ready markdown or structured data with a single API call.",
      "supports_sso": false,
      "is_open_source": true,
      "is_in_yc": true
    },
  "status": "completed",
  "expiresAt": "2025-01-08T20:58:12.000Z"
}
```

## Extracting without a Schema

If you prefer not to define a strict structure, you can simply provide a `prompt`. The underlying model will choose a structure for you, which can be useful for more exploratory or flexible requests.

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  # Initialize the FirecrawlApp with your API key
  firecrawl = Firecrawl(api_key='your_api_key')

  data = firecrawl.extract([
    'https://docs.firecrawl.dev/',
    'https://firecrawl.dev/'
  ], prompt="Extract Firecrawl's mission from the page.")
  print(data)
  ```

  ```js Node
  import Firecrawl from "@mendable/firecrawl-js";

  const firecrawl = new Firecrawl({
  apiKey: "fc-YOUR_API_KEY"
  });

  const scrapeResult = await firecrawl.extract([
  'https://docs.firecrawl.dev/',
  'https://firecrawl.dev/'
  ], {
  prompt: "Extract Firecrawl's mission from the page."
  });

  console.log(scrapeResult);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/extract \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "urls": [
          "https://docs.firecrawl.dev/",
          "https://firecrawl.dev/"
        ],
        "prompt": "Extract Firecrawl'\''s mission from the page."
      }'
  ```
</CodeGroup>

```json JSON
{
  "success": true,
  "data": {
    "company_mission": "Turn websites into LLM-ready data. Power your AI apps with clean data crawled from any website."
  }
}
```

## Improving Results with Web Search

Setting `enableWebSearch = true` in your request will expand the crawl beyond the provided URL set. This can capture supporting or related information from linked pages.

Here's an example that extracts information about dash cams, enriching the results with data from related pages:

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  # Initialize the FirecrawlApp with your API key

  firecrawl = Firecrawl(api_key='your_api_key')

  data = firecrawl.extract([
  'https://nextbase.com/dash-cams/622gw-dash-cam'
  ], prompt="Extract details about the best dash cams including prices, features, pros/cons and reviews.", enable_web_search=True)
  print(data)
  ```

  ```js Node
  import Firecrawl from "@mendable/firecrawl-js";

  const firecrawl = new Firecrawl({
  apiKey: "fc-YOUR_API_KEY"
  });

  const scrapeResult = await firecrawl.extract([
  'https://nextbase.com/dash-cams/622gw-dash-cam'
  ], {
  prompt: "Extract details about the best dash cams including prices, features, pros/cons and reviews.",
  enableWebSearch: true // Enable web search for better context
  });

  console.log(scrapeResult);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/extract \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "urls": ["https://nextbase.com/dash-cams/622gw-dash-cam"],
        "prompt": "Extract details about the best dash cams including prices, features, pros/cons, and reviews.",
        "enableWebSearch": true
      }'
  ```
</CodeGroup>

### Example Response with Web Search

```json JSON
{
  "success": true,
  "data": {
    "dash_cams": [
      {
        "name": "Nextbase 622GW",
        "price": "$399.99",
        "features": [
          "4K video recording",
          "Image stabilization",
          "Alexa built-in",
          "What3Words integration"
        ],
        /* Information below enriched with other websites like 
        https://www.techradar.com/best/best-dash-cam found 
        via enableWebSearch parameter */
        "pros": [
          "Excellent video quality",
          "Great night vision",
          "Built-in GPS"
        ],
        "cons": ["Premium price point", "App can be finicky"]
      }
    ],
  }

```

The response includes additional context gathered from related pages, providing more comprehensive and accurate information.

## Extracting without URLs

The `/extract` endpoint now supports extracting structured data using a prompt without needing specific URLs. This is useful for research or when exact URLs are unknown. Currently in Alpha.

<CodeGroup>
  ```python Python
  from pydantic import BaseModel

  class ExtractSchema(BaseModel):
      company_mission: str


  # Define the prompt for extraction
  prompt = 'Extract the company mission from Firecrawl\'s website.'

  # Perform the extraction
  scrape_result = firecrawl.extract(prompt=prompt, schema=ExtractSchema)

  print(scrape_result)
  ```

  ```js Node
  import { z } from "zod";

  // Define schema to extract contents into
  const schema = z.object({
    company_mission: z.string(),
  });

  const scrapeResult = await firecrawl.extract([], {
    prompt: "Extract the company mission from Firecrawl's website.",
    schema: schema
  });

  console.log(scrapeResult);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/extract \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "urls": [],
        "prompt": "Extract the company mission from the Firecrawl's website.",
        "schema": {
          "type": "object",
          "properties": {
            "company_mission": {
              "type": "string"
            }
          },
          "required": ["company_mission"]
        }
      }'
  ```
</CodeGroup>

## Known Limitations (Beta)

1. **Large-Scale Site Coverage**\
   Full coverage of massive sites (e.g., "all products on Amazon") in a single request is not yet supported.

2. **Complex Logical Queries**\
   Requests like "find every post from 2025" may not reliably return all expected data. More advanced query capabilities are in progress.

3. **Occasional Inconsistencies**\
   Results might differ across runs, particularly for very large or dynamic sites. Usually it captures core details, but some variation is possible.

4. **Beta State**\
   Since `/extract` is still in Beta, features and performance will continue to evolve. We welcome bug reports and feedback to help us improve.

## Using FIRE-1

FIRE-1 is an AI agent that enhances Firecrawl's scraping capabilities. It can controls browser actions and navigates complex website structures to enable comprehensive data extraction beyond traditional scraping methods.

You can leverage the FIRE-1 agent with the `/extract` endpoint for complex extraction tasks that require navigation across multiple pages or interaction with elements.

**Example (cURL):**

```bash
curl -X POST https://api.firecrawl.dev/v2/extract \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "urls": ["https://example-forum.com/topic/123"],
      "prompt": "Extract all user comments from this forum thread.",
      "schema": {
        "type": "object",
        "properties": {
          "comments": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "author": {"type": "string"},
                "comment_text": {"type": "string"}
              },
              "required": ["author", "comment_text"]
            }
          }
        },
        "required": ["comments"]
      },
      "agent": {
        "model": "FIRE-1"
      }
    }'
```

> FIRE-1 is already live and available under preview.

## Billing and Usage Tracking

You can check our the pricing for /extract on the [Extract landing page pricing page](https://www.firecrawl.dev/extract#pricing) and monitor usage via the [Extract page on the dashboard](https://www.firecrawl.dev/app/extract).

Have feedback or need help? Email [help@firecrawl.com](mailto:help@firecrawl.com).
