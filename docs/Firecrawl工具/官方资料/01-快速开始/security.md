# Security

> Verify webhook authenticity and implement security best practices

Webhook security is critical to ensure that requests to your endpoint are actually coming from Firecrawl and haven't been tampered with. This page covers how to verify webhook authenticity and implement security best practices.

## Why Webhook Security Matters

Without proper verification, attackers could:

* Send fake webhook requests to trigger unwanted actions
* Modify payload data to manipulate your application
* Overload your webhook endpoint with requests

## How Firecrawl Signs Webhooks

Firecrawl signs every webhook request using **HMAC-SHA256** encryption with your account's secret key. This creates a unique signature for each request that proves:

1. The request came from Firecrawl
2. The payload hasn't been modified

## Finding Your Secret Key

Your webhook secret is available under the [Advanced tab](https://www.firecrawl.dev/app/settings?tab=advanced) of your account settings. Each account has a unique secret that's used to sign all webhook requests.

<Warning>
  Keep your webhook secret secure and never expose it publicly. If you believe
  your secret has been compromised, regenerate it immediately from your account
  settings.
</Warning>

## Signature Verification

### How Signatures Work

Each webhook request includes an `X-Firecrawl-Signature` header with this format:

```
X-Firecrawl-Signature: sha256=abc123def456...
```

The signature is computed as follows:

1. Take the raw request body (JSON string)
2. Create HMAC-SHA256 hash using your secret key
3. Convert to hexadecimal string
4. Prefix with `sha256=`

### Implementation Examples

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

### Step-by-Step Verification

1. **Extract the signature** from the `X-Firecrawl-Signature` header
2. **Get the raw request body** as received (don't parse it first)
3. **Compute HMAC-SHA256** using your secret key and the raw body
4. **Compare signatures** using a timing-safe comparison function
5. **Only process** the webhook if signatures match

## Security Best Practices

### Always Validate Signatures

Never trust a webhook request without signature verification:

```javascript
// ❌ BAD - No verification
app.post('/webhook', (req, res) => {
  processWebhook(req.body); // Dangerous!
  res.status(200).send('OK');
});

// ✅ GOOD - Verified first
app.post('/webhook', (req, res) => {
  if (!verifySignature(req)) {
    return res.status(401).send('Unauthorized');
  }
  processWebhook(req.body);
  res.status(200).send('OK');
});
```

### Use Timing-Safe Comparisons

Standard string comparison can leak timing information. Use dedicated functions:

* **Node.js**: `crypto.timingSafeEqual()`
* **Python**: `hmac.compare_digest()`
* **Other languages**: Look for "constant-time" or "timing-safe" comparison functions

### Require HTTPS

Always use HTTPS endpoints for webhooks:

```json
{
  "url": "https://your-app.com/webhook" // ✅ Secure
}
```

```json
{
  "url": "http://your-app.com/webhook" // ❌ Insecure
}
```
