# Stealth Mode

> Use stealth proxies for sites with advanced anti-bot solutions

Firecrawl provides different proxy types to help you scrape websites with varying levels of anti-bot protection. The proxy type can be specified using the `proxy` parameter.

### Proxy Types

Firecrawl supports three types of proxies:

* **basic**: Proxies for scraping sites with none to basic anti-bot solutions. Fast and usually works.
* **stealth**: Stealth proxies for scraping sites with advanced anti-bot solutions. Slower, but more reliable on certain sites.
* **auto**: Firecrawl will automatically retry scraping with stealth proxies if the basic proxy fails. If the retry with stealth is successful, 5 credits will be billed for the scrape. If the first attempt with basic is successful, only the regular cost will be billed.

If you do not specify a proxy, Firecrawl will default to basic.

### Using Stealth Mode

When scraping websites with advanced anti-bot protection, you can use the stealth proxy mode to improve your success rate.

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key='fc-YOUR-API-KEY')

  # Choose proxy strategy: 'basic' | 'stealth' | 'auto'
  doc = firecrawl.scrape('https://example.com', formats=['markdown'], proxy='auto')

  print(doc.warning or 'ok')
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  // Choose proxy strategy: 'basic' | 'stealth' | 'auto'
  const doc = await firecrawl.scrape('https://example.com', {
    formats: ['markdown'],
    proxy: 'auto'
  });

  console.log(doc.warning || 'ok');
  ```

  ```bash cURL

  // Choose proxy strategy: 'basic' | 'stealth' | 'auto'
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer fc-YOUR-API-KEY' \
      -d '{
        "url": "https://example.com",
        "proxy": "auto"
      }'

  ```
</CodeGroup>

**Note:** Stealth proxy requests cost 5 credits per request when used.

## Using Stealth as a Retry Mechanism

A common pattern is to first try scraping with the default proxy settings, and then retry with stealth mode if you encounter specific error status codes (401, 403, or 500) in the `metadata.statusCode` field of the response. These status codes can be indicative of the website blocking your request.

<CodeGroup>
  ```python Python
  # pip install firecrawl-py

  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="YOUR_API_KEY")

  # First try with basic proxy
  try:
      content = firecrawl.scrape("https://example.com")
      
      # Check if we got an error status code
      status_code = content.get("metadata", {}).get("statusCode")
      if status_code in [401, 403, 500]:
          print(f"Got status code {status_code}, retrying with stealth proxy")
          # Retry with stealth proxy
          content = firecrawl.scrape("https://example.com", proxy="stealth")
      
      print(content["markdown"])
  except Exception as e:
      print(f"Error: {e}")
      # Retry with stealth proxy on exception
      try:
          content = firecrawl.scrape("https://example.com", proxy="stealth")
          print(content["markdown"])
      except Exception as e:
          print(f"Stealth proxy also failed: {e}")
  ```

  ```js Node
  // npm install @mendable/firecrawl-js

  import { Firecrawl } from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: 'YOUR_API_KEY' });

  // Function to scrape with retry logic
  async function scrapeWithRetry(url) {
    try {
      // First try with default proxy
      const content = await firecrawl.scrape(url);
      
      // Check if we got an error status code
      const statusCode = content?.metadata?.statusCode;
      if ([401, 403, 500].includes(statusCode)) {
        console.log(`Got status code ${statusCode}, retrying with stealth proxy`);
        // Retry with stealth proxy
        return await firecrawl.scrape(url, {
          proxy: 'stealth'
        });
      }
      
      return content;
    } catch (error) {
      console.error(`Error: ${error.message}`);
      // Retry with stealth proxy on exception
      try {
        return await firecrawl.scrape(url, {
          proxy: 'stealth'
        });
      } catch (retryError) {
        console.error(`Stealth proxy also failed: ${retryError.message}`);
        throw retryError;
      }
    }
  }

  // Usage
  const content = await scrapeWithRetry('https://example.com');
  console.log(content.markdown);
  ```

  ```bash cURL
  # First try with default proxy
  RESPONSE=$(curl -s -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://example.com"
      }')

  # Extract status code from response
  STATUS_CODE=$(echo $RESPONSE | jq -r '.data.metadata.statusCode')

  # Check if status code indicates we should retry with stealth
  if [[ "$STATUS_CODE" == "401" || "$STATUS_CODE" == "403" || "$STATUS_CODE" == "500" ]]; then
      echo "Got status code $STATUS_CODE, retrying with stealth proxy"
      
      # Retry with stealth proxy
      curl -X POST https://api.firecrawl.dev/v2/scrape \
          -H 'Content-Type: application/json' \
          -H 'Authorization: Bearer YOUR_API_KEY' \
          -d '{
            "url": "https://example.com",
            "proxy": "stealth"
          }'
  else
      # Output the original response
      echo $RESPONSE
  fi
  ```
</CodeGroup>

This approach allows you to optimize your credit usage by only using stealth mode when necessary.
