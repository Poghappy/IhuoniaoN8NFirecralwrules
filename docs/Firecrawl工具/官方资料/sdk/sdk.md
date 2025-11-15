# Overview

> Firecrawl SDKs are wrappers around the Firecrawl API to help you easily extract data from websites.

## Official SDKs

<CardGroup cols={2}>
  <Card title="Python SDK" icon="python" href="python">
    Explore the Python SDK for Firecrawl.
  </Card>

  <Card title="Node SDK" icon="node" href="node">
    Explore the Node SDK for Firecrawl.
  </Card>
</CardGroup>

## Community SDKs (v1 only)

<CardGroup cols={2}>
  <Card title="Go SDK" icon="golang" href="go">
    Explore the Go SDK for Firecrawl.
  </Card>

  <Card title="Rust SDK" icon="rust" href="rust">
    Explore the Rust SDK for Firecrawl.
  </Card>
</CardGroup>
# Python

> Firecrawl Python SDK is a wrapper around the Firecrawl API to help you easily turn websites into markdown.

## Installation

To install the Firecrawl Python SDK, you can use pip:

```python Python
# pip install firecrawl-py

from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")
```

## Usage

1. Get an API key from [firecrawl.dev](https://firecrawl.dev)
2. Set the API key as an environment variable named `FIRECRAWL_API_KEY` or pass it as a parameter to the `Firecrawl` class.

Here's an example of how to use the SDK:

```python Python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_status = firecrawl.scrape(
  'https://firecrawl.dev', 
  formats=['markdown', 'html']
)
print(scrape_status)

# Crawl a website:
crawl_status = firecrawl.crawl(
  'https://firecrawl.dev', 
  limit=100, 
  scrape_options={
    'formats': ['markdown', 'html']
  }
)
print(crawl_status)
```

### Scraping a URL

To scrape a single URL, use the `scrape` method. It takes the URL as a parameter and returns the scraped document.

```python Python
# Scrape a website:
scrape_result = firecrawl.scrape('firecrawl.dev', formats=['markdown', 'html'])
print(scrape_result)
```

### Crawl a Website

To crawl a website, use the `crawl` method. It takes the starting URL and optional options as arguments. The options allow you to specify additional settings for the crawl job, such as the maximum number of pages to crawl, allowed domains, and the output format. See [Pagination](#pagination) for auto/manual pagination and limiting.

```python Python
job = firecrawl.crawl(url="https://docs.firecrawl.dev", limit=5, poll_interval=1, timeout=120)
print(job)
```

### Start a Crawl

<Tip>Prefer non-blocking? Check out the [Async Class](#async-class) section below.</Tip>

Start a job without waiting using `start_crawl`. It returns a job `ID` you can use to check status. Use `crawl` when you want a waiter that blocks until completion. See [Pagination](#pagination) for paging behavior and limits.

```python Python
job = firecrawl.start_crawl(url="https://docs.firecrawl.dev", limit=10)
print(job)
```

### Checking Crawl Status

To check the status of a crawl job, use the `get_crawl_status` method. It takes the job ID as a parameter and returns the current status of the crawl job.

```python Python
status = firecrawl.get_crawl_status("<crawl-id>")
print(status)
```

### Cancelling a Crawl

To cancel an crawl job, use the `cancel_crawl` method. It takes the job ID of the `start_crawl` as a parameter and returns the cancellation status.

```python Python
ok = firecrawl.cancel_crawl("<crawl-id>")
print("Cancelled:", ok)
```

### Map a Website

Use `map` to generate a list of URLs from a website. The options let you customize the mapping process, including excluding subdomains or utilizing the sitemap.

```python Python
res = firecrawl.map(url="https://firecrawl.dev", limit=10)
print(res)
```

{/* ### Extracting Structured Data from Websites

  To extract structured data from websites, use the `extract` method. It takes the URLs to extract data from, a prompt, and a schema as arguments. The schema is a Pydantic model that defines the structure of the extracted data.

  <ExtractPythonShort /> */}

### Crawling a Website with WebSockets

To crawl a website with WebSockets, start the job with `start_crawl` and subscribe using the `watcher` helper. Create a watcher with the job ID and attach handlers (e.g., for page, completed, failed) before calling `start()`.

```python Python
import asyncio
from firecrawl import AsyncFirecrawl

async def main():
    firecrawl = AsyncFirecrawl(api_key="fc-YOUR-API-KEY")

    # Start a crawl first
    started = await firecrawl.start_crawl("https://firecrawl.dev", limit=5)

    # Watch updates (snapshots) until terminal status
    async for snapshot in firecrawl.watcher(started.id, kind="crawl", poll_interval=2, timeout=120):
        if snapshot.status == "completed":
            print("DONE", snapshot.status)
            for doc in snapshot.data:
                print("DOC", doc.metadata.sourceURL if doc.metadata else None)
        elif snapshot.status == "failed":
            print("ERR", snapshot.status)
        else:
            print("STATUS", snapshot.status, snapshot.completed, "/", snapshot.total)

asyncio.run(main())
```

### Pagination

Firecrawl endpoints for crawl and batch return a `next` URL when more data is available. The Python SDK auto-paginates by default and aggregates all documents; in that case `next` will be `None`. You can disable auto-pagination or set limits.

#### Crawl

Use the waiter method `crawl` for the simplest experience, or start a job and page manually.

##### Simple crawl (auto-pagination, default)

* See the default flow in [Crawl a Website](#crawl-a-website).

##### Manual crawl with pagination control (single page)

* Start a job, then fetch one page at a time with `auto_paginate=False`.

```python Python
crawl_job = client.start_crawl("https://example.com", limit=100)

status = client.get_crawl_status(crawl_job.id, pagination_config=PaginationConfig(auto_paginate=False))
print("crawl single page:", status.status, "docs:", len(status.data), "next:", status.next)
```

##### Manual crawl with limits (auto-pagination + early stop)

* Keep auto-pagination on but stop early with `max_pages`, `max_results`, or `max_wait_time`.

```python Python
status = client.get_crawl_status(
    crawl_job.id,
    pagination_config=PaginationConfig(max_pages=2, max_results=50, max_wait_time=15),
)
print("crawl limited:", status.status, "docs:", len(status.data), "next:", status.next)
```

#### Batch Scrape

Use the waiter method `batch_scrape`, or start a job and page manually.

##### Simple batch scrape (auto-pagination, default)

* See the default flow in [Batch Scrape](/features/batch-scrape).

##### Manual batch scrape with pagination control (single page)

* Start a job, then fetch one page at a time with `auto_paginate=False`.

```python Python
batch_job = client.start_batch_scrape(urls)
status = client.get_batch_scrape_status(batch_job.id, pagination_config=PaginationConfig(auto_paginate=False))
print("batch single page:", status.status, "docs:", len(status.data), "next:", status.next)
```

##### Manual batch scrape with limits (auto-pagination + early stop)

* Keep auto-pagination on but stop early with `max_pages`, `max_results`, or `max_wait_time`.

```python Python
status = client.get_batch_scrape_status(
    batch_job.id,
    pagination_config=PaginationConfig(max_pages=2, max_results=100, max_wait_time=20),
)
print("batch limited:", status.status, "docs:", len(status.data), "next:", status.next)
```

## Error Handling

The SDK handles errors returned by the Firecrawl API and raises appropriate exceptions. If an error occurs during a request, an exception will be raised with a descriptive error message.

## Async Class

For async operations, use the `AsyncFirecrawl` class. Its methods mirror `Firecrawl`, but they don't block the main thread.

```python Python
import asyncio
from firecrawl import AsyncFirecrawl

async def main():
    firecrawl = AsyncFirecrawl(api_key="fc-YOUR-API-KEY")

    # Scrape
    doc = await firecrawl.scrape("https://firecrawl.dev", formats=["markdown"])  # type: ignore[arg-type]
    print(doc.get("markdown"))

    # Search
    results = await firecrawl.search("firecrawl", limit=2)
    print(results.get("web", []))

    # Crawl (start + status)
    started = await firecrawl.start_crawl("https://docs.firecrawl.dev", limit=3)
    status = await firecrawl.get_crawl_status(started.id)
    print(status.status)

    # Batch scrape (wait)
    job = await firecrawl.batch_scrape([
        "https://firecrawl.dev",
        "https://docs.firecrawl.dev",
    ], formats=["markdown"], poll_interval=1, timeout=60)
    print(job.status, job.completed, job.total)

asyncio.run(main())
```
# Node

> Firecrawl Node SDK is a wrapper around the Firecrawl API to help you easily turn websites into markdown.

## Installation

To install the Firecrawl Node SDK, you can use npm:

```js Node
# npm install @mendable/firecrawl-js

import Firecrawl from '@mendable/firecrawl-js';

const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });
```

## Usage

1. Get an API key from [firecrawl.dev](https://firecrawl.dev)
2. Set the API key as an environment variable named `FIRECRAWL_API_KEY` or pass it as a parameter to the `FirecrawlApp` class.

Here's an example of how to use the SDK with error handling:

```js Node
import Firecrawl from '@mendable/firecrawl-js';

const firecrawl = new Firecrawl({apiKey: "fc-YOUR_API_KEY"});

// Scrape a website
const scrapeResponse = await firecrawl.scrape('https://firecrawl.dev', {
  formats: ['markdown', 'html'],
});

console.log(scrapeResponse)

// Crawl a website
const crawlResponse = await firecrawl.crawl('https://firecrawl.dev', {
  limit: 100,
  scrapeOptions: {
    formats: ['markdown', 'html'],
  }
});

console.log(crawlResponse)
```

### Scraping a URL

To scrape a single URL with error handling, use the `scrapeUrl` method. It takes the URL as a parameter and returns the scraped data as a dictionary.

```js Node
// Scrape a website:
const scrapeResult = await firecrawl.scrape('firecrawl.dev', { formats: ['markdown', 'html'] });

console.log(scrapeResult)
```

### Crawling a Website

To crawl a website with error handling, use the `crawlUrl` method. It takes the starting URL and optional parameters as arguments. The `params` argument allows you to specify additional options for the crawl job, such as the maximum number of pages to crawl, allowed domains, and the output format. See [Pagination](#pagination) for auto/ manual pagination and limiting.

```js Node
const job = await firecrawl.crawl('https://docs.firecrawl.dev', { limit: 5, pollInterval: 1, timeout: 120 });
console.log(job.status);
```

### Start a Crawl

Start a job without waiting using `startCrawl`. It returns a job `ID` you can use to check status. Use `crawl` when you want a waiter that blocks until completion. See [Pagination](#pagination) for paging behavior and limits.

```js Node
const { id } = await firecrawl.startCrawl('https://docs.firecrawl.dev', { limit: 10 });
console.log(id);
```

### Checking Crawl Status

To check the status of a crawl job with error handling, use the `checkCrawlStatus` method. It takes the `ID` as a parameter and returns the current status of the crawl job.

```js Node
const status = await firecrawl.getCrawlStatus("<crawl-id>");
console.log(status);
```

### Cancelling a Crawl

To cancel an crawl job, use the `cancelCrawl` method. It takes the job ID of the `startCrawl` as a parameter and returns the cancellation status.

```js Node
const ok = await firecrawl.cancelCrawl("<crawl-id>");
console.log("Cancelled:", ok);
```

### Mapping a Website

To map a website with error handling, use the `mapUrl` method. It takes the starting URL as a parameter and returns the mapped data as a dictionary.

```js Node
const res = await firecrawl.map('https://firecrawl.dev', { limit: 10 });
console.log(res.links);
```

{/* ### Extracting Structured Data from Websites

  To extract structured data from websites with error handling, use the `extractUrl` method. It takes the starting URL as a parameter and returns the extracted data as a dictionary.

  <ExtractNodeShort /> */}

### Crawling a Website with WebSockets

To crawl a website with WebSockets, use the `crawlUrlAndWatch` method. It takes the starting URL and optional parameters as arguments. The `params` argument allows you to specify additional options for the crawl job, such as the maximum number of pages to crawl, allowed domains, and the output format.

```js Node
import Firecrawl from '@mendable/firecrawl-js';

const firecrawl = new Firecrawl({ apiKey: 'fc-YOUR-API-KEY' });

// Start a crawl and then watch it
const { id } = await firecrawl.startCrawl('https://mendable.ai', {
  excludePaths: ['blog/*'],
  limit: 5,
});

const watcher = firecrawl.watcher(id, { kind: 'crawl', pollInterval: 2, timeout: 120 });

watcher.on('document', (doc) => {
  console.log('DOC', doc);
});

watcher.on('error', (err) => {
  console.error('ERR', err?.error || err);
});

watcher.on('done', (state) => {
  console.log('DONE', state.status);
});

// Begin watching (WS with HTTP fallback)
await watcher.start();
```

### Pagination

Firecrawl endpoints for crawl and batch return a `next` URL when more data is available. The Node SDK auto-paginates by default and aggregates all documents; in that case `next` will be `null`. You can disable auto-pagination or set limits.

#### Crawl

Use the waiter method `crawl` for the simplest experience, or start a job and page manually.

##### Simple crawl (auto-pagination, default)

* See the default flow in [Crawling a Website](#crawling-a-website).

##### Manual crawl with pagination control (single page)

* Start a job, then fetch one page at a time with `autoPaginate: false`.

```js Node
const crawlStart = await firecrawl.startCrawl('https://docs.firecrawl.dev', { limit: 5 });
const crawlJobId = crawlStart.id;

const crawlSingle = await firecrawl.getCrawlStatus(crawlJobId, { autoPaginate: false });
console.log('crawl single page:', crawlSingle.status, 'docs:', crawlSingle.data.length, 'next:', crawlSingle.next);
```

##### Manual crawl with limits (auto-pagination + early stop)

* Keep auto-pagination on but stop early with `maxPages`, `maxResults`, or `maxWaitTime`.

```js Node
const crawlLimited = await firecrawl.getCrawlStatus(crawlJobId, {
  autoPaginate: true,
  maxPages: 2,
  maxResults: 50,
  maxWaitTime: 15,
});
console.log('crawl limited:', crawlLimited.status, 'docs:', crawlLimited.data.length, 'next:', crawlLimited.next);
```

#### Batch Scrape

Use the waiter method `batchScrape`, or start a job and page manually.

##### Simple batch scrape (auto-pagination, default)

* See the default flow in [Batch Scrape](/features/batch-scrape).

##### Manual batch scrape with pagination control (single page)

* Start a job, then fetch one page at a time with `autoPaginate: false`.

```js Node
const batchStart = await firecrawl.startBatchScrape([
  'https://docs.firecrawl.dev',
  'https://firecrawl.dev',
], { options: { formats: ['markdown'] } });
const batchJobId = batchStart.id;

const batchSingle = await firecrawl.getBatchScrapeStatus(batchJobId, { autoPaginate: false });
console.log('batch single page:', batchSingle.status, 'docs:', batchSingle.data.length, 'next:', batchSingle.next);
```

##### Manual batch scrape with limits (auto-pagination + early stop)

* Keep auto-pagination on but stop early with `maxPages`, `maxResults`, or `maxWaitTime`.

```js Node
const batchLimited = await firecrawl.getBatchScrapeStatus(batchJobId, {
  autoPaginate: true,
  maxPages: 2,
  maxResults: 100,
  maxWaitTime: 20,
});
console.log('batch limited:', batchLimited.status, 'docs:', batchLimited.data.length, 'next:', batchLimited.next);
```

## Error Handling

The SDK handles errors returned by the Firecrawl API and raises appropriate exceptions. If an error occurs during a request, an exception will be raised with a descriptive error message. The examples above demonstrate how to handle these errors using `try/catch` blocks.
# Go

> Firecrawl Go SDK is a wrapper around the Firecrawl API to help you easily turn websites into markdown.

<Warning>
  This SDK currently uses the **v1** version of the Firecrawl API, which is not the most recent (v2 is available). Some features and improvements may only be available in v2.
</Warning>

## Installation

To install the Firecrawl Go SDK, you can use go get:

```bash Go
go get github.com/mendableai/firecrawl-go
```

## Usage

1. Get an API key from [firecrawl.dev](https://firecrawl.dev)
2. Set the `API key` as a parameter to the `FirecrawlApp` struct.
3. Set the `API URL` and/or pass it as a parameter to the `FirecrawlApp` struct. Defaults to `https://api.firecrawl.dev`.
4. Set the `version` and/or pass it as a parameter to the `FirecrawlApp` struct. Defaults to `v1`.

Here's an example of how to use the SDK with error handling:

```go Go
import (
	"fmt"
	"log"
	"github.com/google/uuid"
	"github.com/mendableai/firecrawl-go"
)

func ptr[T any](v T) *T {
	return &v
}

func main() {
	// Initialize the FirecrawlApp with your API key
	apiKey := "fc-YOUR_API_KEY"
	apiUrl := "https://api.firecrawl.dev"
	version := "v1"

	app, err := firecrawl.NewFirecrawlApp(apiKey, apiUrl, version)
	if err != nil {
		log.Fatalf("Failed to initialize FirecrawlApp: %v", err)
	}

  // Scrape a website
  scrapeStatus, err := app.ScrapeUrl("https://firecrawl.dev", firecrawl.ScrapeParams{
    Formats: []string{"markdown", "html"},
  })
  if err != nil {
    log.Fatalf("Failed to send scrape request: %v", err)
  }

  fmt.Println(scrapeStatus)

	// Crawl a website
  idempotencyKey := uuid.New().String() // optional idempotency key
  crawlParams := &firecrawl.CrawlParams{
		ExcludePaths: []string{"blog/*"},
		MaxDepth:     ptr(2),
	}

	crawlStatus, err := app.CrawlUrl("https://firecrawl.dev", crawlParams, &idempotencyKey)
	if err != nil {
		log.Fatalf("Failed to send crawl request: %v", err)
	}

	fmt.Println(crawlStatus) 
}
```

### Scraping a URL

To scrape a single URL with error handling, use the `ScrapeURL` method. It takes the URL as a parameter and returns the scraped data as a dictionary.

```go Go
// Scrape a website
scrapeResult, err := app.ScrapeUrl("https://firecrawl.dev", map[string]any{
  "formats": []string{"markdown", "html"},
})
if err != nil {
  log.Fatalf("Failed to scrape URL: %v", err)
}

fmt.Println(scrapeResult)
```

### Crawling a Website

To crawl a website, use the `CrawlUrl` method. It takes the starting URL and optional parameters as arguments. The `params` argument allows you to specify additional options for the crawl job, such as the maximum number of pages to crawl, allowed domains, and the output format.

```go Go
crawlStatus, err := app.CrawlUrl("https://firecrawl.dev", map[string]any{
  "limit": 100,
  "scrapeOptions": map[string]any{
    "formats": []string{"markdown", "html"},
  },
})
if err != nil {
  log.Fatalf("Failed to send crawl request: %v", err)
}

fmt.Println(crawlStatus) 
```

### Checking Crawl Status

To check the status of a crawl job, use the `CheckCrawlStatus` method. It takes the job ID as a parameter and returns the current status of the crawl job.

```go Go
// Get crawl status
crawlStatus, err := app.CheckCrawlStatus("<crawl_id>")

if err != nil {
  log.Fatalf("Failed to get crawl status: %v", err)
}

fmt.Println(crawlStatus)
```

### Map a Website

Use `MapUrl` to generate a list of URLs from a website. The `params` argument let you customize the mapping process, including options to exclude subdomains or to utilize the sitemap.

```go Go
// Map a website
mapResult, err := app.MapUrl("https://firecrawl.dev", nil)
if err != nil {
  log.Fatalf("Failed to map URL: %v", err)
}

fmt.Println(mapResult)
```

## Error Handling

The SDK handles errors returned by the Firecrawl API and raises appropriate exceptions. If an error occurs during a request, an exception will be raised with a descriptive error message.
# Rust

> Firecrawl Rust SDK is a library to help you easily scrape and crawl websites, and output the data in a format ready for use with language models (LLMs).

<Warning>
  This SDK currently uses the **v1** version of the Firecrawl API, which is not the most recent (v2 is available). Some features and improvements may only be available in v2.
</Warning>

## Installation

To install the Firecrawl Rust SDK, add the following to your `Cargo.toml`:

```yaml Rust
# Add this to your Cargo.toml
[dependencies]
firecrawl = "^1.0"
tokio = { version = "^1", features = ["full"] }
```

## Usage

First, you need to obtain an API key from [firecrawl.dev](https://firecrawl.dev). Then, you need to initialize the `FirecrawlApp`. From there, you can access functions like `FirecrawlApp::scrape_url`, which let you use our API.

Here's an example of how to use the SDK in Rust:

```rust Rust
use firecrawl::{crawl::{CrawlOptions, CrawlScrapeOptions, CrawlScrapeFormats}, FirecrawlApp, scrape::{ScrapeOptions, ScrapeFormats}};

#[tokio::main]
async fn main() {
    // Initialize the FirecrawlApp with the API key
    let app = FirecrawlApp::new("fc-YOUR_API_KEY").expect("Failed to initialize FirecrawlApp");

    // Scrape a URL
    let options = ScrapeOptions {
        formats vec! [ ScrapeFormats::Markdown, ScrapeFormats::HTML ].into(),
        ..Default::default()
    };

    let scrape_result = app.scrape_url("https://firecrawl.dev", options).await;

    match scrape_result {
        Ok(data) => println!("Scrape Result:\n{}", data.markdown.unwrap()),
        Err(e) => eprintln!("Map failed: {}", e),
    }

    // Crawl a website
    let crawl_options = CrawlOptions {
        scrape_options: CrawlScrapeOptions {
            formats: vec![ CrawlScrapeFormats::Markdown, CrawlScrapeFormats::HTML ].into(),
            ..Default::default()
        }.into(),
        limit: 100.into(),
        ..Default::default()
    };

    let crawl_result = app
        .crawl_url("https://mendable.ai", crawl_options)
        .await;

    match crawl_result {
        Ok(data) => println!("Crawl Result (used {} credits):\n{:#?}", data.credits_used, data.data),
        Err(e) => eprintln!("Crawl failed: {}", e),
    }
}
```

### Scraping a URL

To scrape a single URL, use the `scrape_url` method. It takes the URL as a parameter and returns the scraped data as a `Document`.

```rust Rust
let options = ScrapeOptions {
    formats vec! [ ScrapeFormats::Markdown, ScrapeFormats::HTML ].into(),
    ..Default::default()
};

let scrape_result = app.scrape_url("https://firecrawl.dev", options).await;

match scrape_result {
    Ok(data) => println!("Scrape Result:\n{}", data.markdown.unwrap()),
    Err(e) => eprintln!("Map failed: {}", e),
}
```

### Scraping with Extract

With Extract, you can easily extract structured data from any URL. You need to specify your schema in the JSON Schema format, using the `serde_json::json!` macro.

```rust Rust
let json_schema = json!({
    "type": "object",
    "properties": {
        "top": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "points": {"type": "number"},
                    "by": {"type": "string"},
                    "commentsURL": {"type": "string"}
                },
                "required": ["title", "points", "by", "commentsURL"]
            },
            "minItems": 5,
            "maxItems": 5,
            "description": "Top 5 stories on Hacker News"
        }
    },
    "required": ["top"]
});

let llm_extraction_options = ScrapeOptions {
    formats: vec![ ScrapeFormats::Json ].into(),
    jsonOptions: ExtractOptions {
        schema: json_schema.into(),
        ..Default::default()
    }.into(),
    ..Default::default()
};

let llm_extraction_result = app
    .scrape_url("https://news.ycombinator.com", llm_extraction_options)
    .await;

match llm_extraction_result {
    Ok(data) => println!("LLM Extraction Result:\n{:#?}", data.extract.unwrap()),
    Err(e) => eprintln!("LLM Extraction failed: {}", e),
}
```

### Crawling a Website

To crawl a website, use the `crawl_url` method. This will wait for the crawl to complete, which may take a long time based on your starting URL and your options.

```rust Rust
let crawl_options = CrawlOptions {
    scrape_options: CrawlScrapeOptions {
        formats: vec![ CrawlScrapeFormats::Markdown, CrawlScrapeFormats::HTML ].into(),
        ..Default::default()
    }.into(),
    limit: 100.into(),
    ..Default::default()
};

let crawl_result = app
    .crawl_url("https://mendable.ai", crawl_options)
    .await;

match crawl_result {
    Ok(data) => println!("Crawl Result (used {} credits):\n{:#?}", data.credits_used, data.data),
    Err(e) => eprintln!("Crawl failed: {}", e),
}
```

#### Crawling asynchronously

To crawl without waiting for the result, use the `crawl_url_async` method. It takes the same parameters, but it returns a `CrawlAsyncRespone` struct, containing the crawl's ID. You can use that ID with the `check_crawl_status` method to check the status at any time. Do note that completed crawls are deleted after 24 hours.

```rust Rust
let crawl_id = app.crawl_url_async("https://mendable.ai", None).await?.id;

// ... later ...

let status = app.check_crawl_status(crawl_id).await?;

if status.status == CrawlStatusTypes::Completed {
    println!("Crawl is done: {:#?}", status.data);
} else {
    // ... wait some more ...
}
```

### Map a URL

Map all associated links from a starting URL.

```rust Rust
let map_result = app.map_url("https://firecrawl.dev", None).await;

match map_result {
    Ok(data) => println!("Mapped URLs: {:#?}", data),
    Err(e) => eprintln!("Map failed: {}", e),
}
```

## Error Handling

The SDK handles errors returned by the Firecrawl API and by our dependencies, and combines them into the `FirecrawlError` enum, implementing `Error`, `Debug` and `Display`. All of our methods return a `Result<T, FirecrawlError>`.
