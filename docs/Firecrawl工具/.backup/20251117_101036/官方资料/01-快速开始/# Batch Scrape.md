# Batch Scrape

> Batch scrape multiple URLs

## Batch scraping multiple URLs

You can now batch scrape multiple URLs at the same time. It takes the starting URLs and optional parameters as arguments. The params argument allows you to specify additional options for the batch scrape job, such as the output formats.

### How it works

It is very similar to how the `/crawl` endpoint works. You can either start the batch and wait for completion, or start it and handle completion yourself.

* `batchScrape` (JS) / `batch_scrape` (Python): starts a batch job and waits for it to complete, returning the results.
* `startBatchScrape` (JS) / `start_batch_scrape` (Python): starts a batch job and returns the job ID so you can poll or use webhooks.

### Usage

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  start = firecrawl.start_batch_scrape([
      "https://firecrawl.dev",
      "https://docs.firecrawl.dev",
  ], formats=["markdown"])  # returns id

  job = firecrawl.batch_scrape([
      "https://firecrawl.dev",
      "https://docs.firecrawl.dev",
  ], formats=["markdown"], poll_interval=2, wait_timeout=120)

  print(job.status, job.completed, job.total)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  // Start a batch scrape job
  const { id } = await firecrawl.startBatchScrape([
    'https://firecrawl.dev',
    'https://docs.firecrawl.dev'
  ], {
    options: { formats: ['markdown'] },
  });

  // Wait for completion
  const job = await firecrawl.batchScrape([
    'https://firecrawl.dev',
    'https://docs.firecrawl.dev'
  ], { options: { formats: ['markdown'] }, pollInterval: 2, timeout: 120 });

  console.log(job.status, job.completed, job.total);
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

* Calling `batchScrape`/`batch_scrape` returns the full results when the batch completes.

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

\`

* Calling `startBatchScrape`/`start_batch_scrape` returns a job ID you can track via `getBatchScrapeStatus`/`get_batch_scrape_status`, using the API endpoint `/batch/scrape/{id}`, or webhooks. This endpoint is intended for in-progress checks or immediately after completion, **as batch jobs expire after 24 hours**.

```json
{
  "success": true,
  "id": "123-456-789",
  "url": "https://api.firecrawl.dev/v2/batch/scrape/123-456-789"
}
```

## Batch scrape with structured extraction

You can also use the batch scrape endpoint to extract structured data from the pages. This is useful if you want to get the same structured data from a list of URLs.

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR_API_KEY")

  # Scrape multiple websites:
  batch_scrape_result = firecrawl.batch_scrape(
      ['https://docs.firecrawl.dev', 'https://docs.firecrawl.dev/sdks/overview'], 
      formats=[{
          'type': 'json',
          'prompt': 'Extract the title and description from the page.',
          'schema': {
              'type': 'object',
              'properties': {
                  'title': {'type': 'string'},
                  'description': {'type': 'string'}
              },
              'required': ['title', 'description']
          }
      }]
  )
  print(batch_scrape_result)

  # Or, you can use the start method:
  batch_scrape_job = firecrawl.start_batch_scrape(
      ['https://docs.firecrawl.dev', 'https://docs.firecrawl.dev/sdks/overview'], 
      formats=[{
          'type': 'json',
          'prompt': 'Extract the title and description from the page.',
          'schema': {
              'type': 'object',
              'properties': {
                  'title': {'type': 'string'},
                  'description': {'type': 'string'}
              },
              'required': ['title', 'description']
          }
      }]
  )
  print(batch_scrape_job)

  # You can then use the job ID to check the status of the batch scrape:
  batch_scrape_status = firecrawl.get_batch_scrape_status(batch_scrape_job.id)
  print(batch_scrape_status)
  ```

  ```js Node
  import Firecrawl, { ScrapeResponse } from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({apiKey: "fc-YOUR_API_KEY"});

  // Define schema to extract contents into
  const schema = {
    type: "object",
    properties: {
      title: { type: "string" },
      description: { type: "string" }
    },
    required: ["title", "description"]
  };

  // Scrape multiple websites (synchronous):
  const batchScrapeResult = await firecrawl.batchScrape(['https://docs.firecrawl.dev', 'https://docs.firecrawl.dev/sdks/overview'], { 
    formats: [
      {
        type: "json",
        prompt: "Extract the title and description from the page.",
        schema: schema
      }
    ]
  });

  // Output all the results of the batch scrape:
  console.log(batchScrapeResult)

  // Or, you can use the start method:
  const batchScrapeJob = await firecrawl.startBatchScrape(['https://docs.firecrawl.dev', 'https://docs.firecrawl.dev/sdks/overview'], { 
    formats: [
      {
        type: "json",
        prompt: "Extract the title and description from the page.",
        schema: schema
      }
    ]
  });
  console.log(batchScrapeJob)

  // You can then use the job ID to check the status of the batch scrape:
  const batchScrapeStatus = await firecrawl.getBatchScrapeStatus(batchScrapeJob.id);
  console.log(batchScrapeStatus)
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/batch/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "urls": ["https://docs.firecrawl.dev", "https://docs.firecrawl.dev/sdks/overview"],
        "formats" : [{
          "type": "json",
          "prompt": "Extract the title and description from the page.",
          "schema": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string"
              },
              "description": {
                "type": "string"
              }
            },
            "required": [
              "title",
              "description"
            ]
          }
        }]
      }'
  ```
</CodeGroup>

### Response

* `batchScrape`/`batch_scrape` returns full results:

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
      "json": {
        "title": "Build a 'Chat with website' using Groq Llama 3 | Firecrawl",
        "description": "Learn how to use Firecrawl, Groq Llama 3, and Langchain to build a 'Chat with your website' bot."
      }
    },
    ...
  ]
}
```

* `startBatchScrape`/`start_batch_scrape` returns a job ID:

```json
{
  "success": true,
  "id": "123-456-789",
  "url": "https://api.firecrawl.dev/v2/batch/scrape/123-456-789"
}
```

## Batch scrape with webhooks

You can configure webhooks to receive real-time notifications as each URL in your batch is scraped. This allows you to process results immediately instead of waiting for the entire batch to complete.

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/batch/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "urls": [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
      ],
      "webhook": {
        "url": "https://your-domain.com/webhook",
        "metadata": {
          "any_key": "any_value"
        },
        "events": ["started", "page", "completed"]
      }
    }' 
```

For comprehensive webhook documentation including event types, payload structure, and implementation examples, see the [Webhooks documentation](/features/webhooks).

### Quick Reference

**Event Types:**

* `batch_scrape.started` - When the batch scrape begins
* `batch_scrape.page` - For each URL successfully scraped
* `batch_scrape.completed` - When all URLs are processed
* `batch_scrape.failed` - If the batch scrape encounters an error

**Basic Payload:**

```json
{
  "success": true,
  "type": "batch_scrape.page",
  "id": "batch-job-id",
  "data": [...], // Page data for 'page' events
  "metadata": {}, // Your custom metadata
  "error": null
}
```

<Note>
  For detailed webhook configuration, security best practices, and troubleshooting, visit the [Webhooks documentation](/features/webhooks).
</Note>
