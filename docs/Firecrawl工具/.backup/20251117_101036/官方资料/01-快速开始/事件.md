# Overview

> Real-time notifications for your Firecrawl operations

Webhooks allow you to receive real-time notifications about your Firecrawl operations as they progress. Instead of polling for status updates, Firecrawl will automatically send HTTP POST requests to your specified endpoint when events occur.

## Supported Operations

Webhooks are supported for most major Firecrawl operations:

* **Crawl** - Get notified as pages are crawled and when crawls complete
* **Batch scrape** - Receive updates for each URL scraped in a batch
* **Extract** - Receive updates when extract jobs start, complete, or fail

## Quick Setup

Configure webhooks by adding a `webhook` object to your request:

```json JSON
{
  "webhook": {
    "url": "https://your-domain.com/webhook",
    "metadata": {
      "any_key": "any_value"
    },
    "events": ["started", "page", "completed", "failed"]
  }
} 
```

### Configuration Options

| Field      | Type   | Required | Description                                   |
| ---------- | ------ | -------- | --------------------------------------------- |
| `url`      | string | ✅        | Your webhook endpoint URL                     |
| `headers`  | object | ❌        | Custom headers to include in webhook requests |
| `metadata` | object | ❌        | Custom data included in all webhook payloads  |
| `events`   | array  | ❌        | Event types to receive (default: all events)  |

## Basic Usage Examples

### Crawl with Webhook

```bash cURL
curl -X POST https://api.firecrawl.dev/v2/crawl \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev",
      "limit": 100,
      "webhook": {
        "url": "https://your-domain.com/webhook",
        "metadata": {
          "any_key": "any_value"
        },
        "events": ["started", "page", "completed"]
      }
    }'
```

### Batch Scrape with Webhook

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

## Handling Webhooks

Here's a simple example of handling webhooks in your application:

<CodeGroup>
  ```js Node/Express
  import crypto from 'crypto';
  import express from 'express';

  const app = express();

  // Use raw body parser for signature verification
  app.use('/webhook/firecrawl', express.raw({ type: 'application/json' }));

  app.post('/webhook/firecrawl', (req, res) => {
    const signature = req.get('X-Firecrawl-Signature');
    const webhookSecret = process.env.FIRECRAWL_WEBHOOK_SECRET;
    
    if (!signature || !webhookSecret) {
      return res.status(401).send('Unauthorized');
    }
    
    // Extract hash from signature header
    const [algorithm, hash] = signature.split('=');
    if (algorithm !== 'sha256') {
      return res.status(401).send('Invalid signature algorithm');
    }
    
    // Compute expected signature
    const expectedSignature = crypto
      .createHmac('sha256', webhookSecret)
      .update(req.body)
      .digest('hex');
    
    // Verify signature using timing-safe comparison
    if (!crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(expectedSignature, 'hex'))) {
      return res.status(401).send('Invalid signature');
    }
    
    // Parse and process verified webhook
    const event = JSON.parse(req.body);
    console.log('Verified Firecrawl webhook:', event);
    
    res.status(200).send('ok');
  });

  app.listen(3000, () => console.log('Listening on 3000'));
  ```

  ```python Python/Flask
  import hmac
  import hashlib
  from flask import Flask, request, abort

  app = Flask(__name__)

  WEBHOOK_SECRET = 'your-webhook-secret-here'  # Get from Firecrawl dashboard

  @app.post('/webhook/firecrawl')
  def webhook():
      signature = request.headers.get('X-Firecrawl-Signature')
      
      if not signature:
          abort(401, 'Missing signature header')
      
      # Extract hash from signature header
      try:
          algorithm, hash_value = signature.split('=', 1)
          if algorithm != 'sha256':
              abort(401, 'Invalid signature algorithm')
      except ValueError:
          abort(401, 'Invalid signature format')
      
      # Compute expected signature
      expected_signature = hmac.new(
          WEBHOOK_SECRET.encode('utf-8'),
          request.data,
          hashlib.sha256
      ).hexdigest()
      
      # Verify signature using timing-safe comparison
      if not hmac.compare_digest(hash_value, expected_signature):
          abort(401, 'Invalid signature')
      
      # Parse and process verified webhook
      event = request.get_json(force=True)
      print('Verified Firecrawl webhook:', event)
      
      return 'ok', 200

  if __name__ == '__main__':
      app.run(port=3000)
  ```
</CodeGroup>

### Best Practices

1. **Respond quickly** – Always return a `2xx` status code within 30 seconds
2. **Process asynchronously** – For heavy processing, queue the work and respond immediately
3. **Validate authenticity** – Always verify the webhook signature (see [Security](/webhooks/security))
