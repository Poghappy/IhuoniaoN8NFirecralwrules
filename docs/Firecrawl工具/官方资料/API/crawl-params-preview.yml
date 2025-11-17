# Crawl Params Preview

## OpenAPI

````yaml v2-openapi POST /crawl/params-preview
paths:
  path: /crawl/params-preview
  method: post
  servers:
    - url: https://api.firecrawl.dev/v2
  request:
    security:
      - title: bearerAuth
        parameters:
          query: {}
          header:
            Authorization:
              type: http
              scheme: bearer
          cookie: {}
    parameters:
      path: {}
      query: {}
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              url:
                allOf:
                  - type: string
                    format: uri
                    description: The URL to crawl
              prompt:
                allOf:
                  - type: string
                    maxLength: 10000
                    description: Natural language prompt describing what you want to crawl
            required: true
            requiredProperties:
              - url
              - prompt
        examples:
          example:
            value:
              url: <string>
              prompt: <string>
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              success:
                allOf:
                  - type: boolean
                    example: true
              data:
                allOf:
                  - type: object
                    properties:
                      url:
                        type: string
                        format: uri
                        description: The URL to crawl
                      includePaths:
                        type: array
                        items:
                          type: string
                        description: URL patterns to include
                      excludePaths:
                        type: array
                        items:
                          type: string
                        description: URL patterns to exclude
                      maxDepth:
                        type: integer
                        description: Maximum crawl depth
                      maxDiscoveryDepth:
                        type: integer
                        description: Maximum discovery depth
                      crawlEntireDomain:
                        type: boolean
                        description: Whether to crawl the entire domain
                      allowExternalLinks:
                        type: boolean
                        description: Whether to allow external links
                      allowSubdomains:
                        type: boolean
                        description: Whether to allow subdomains
                      sitemap:
                        type: string
                        enum:
                          - skip
                          - include
                        description: Sitemap handling strategy
                      ignoreQueryParameters:
                        type: boolean
                        description: Whether to ignore query parameters
                      deduplicateSimilarURLs:
                        type: boolean
                        description: Whether to deduplicate similar URLs
                      delay:
                        type: number
                        description: Delay between requests in milliseconds
                      limit:
                        type: integer
                        description: Maximum number of pages to crawl
        examples:
          example:
            value:
              success: true
              data:
                url: <string>
                includePaths:
                  - <string>
                excludePaths:
                  - <string>
                maxDepth: 123
                maxDiscoveryDepth: 123
                crawlEntireDomain: true
                allowExternalLinks: true
                allowSubdomains: true
                sitemap: skip
                ignoreQueryParameters: true
                deduplicateSimilarURLs: true
                delay: 123
                limit: 123
        description: Successful response with generated crawl parameters
    '400':
      application/json:
        schemaArray:
          - type: object
            properties:
              success:
                allOf:
                  - type: boolean
                    example: false
              error:
                allOf:
                  - type: string
                    example: Invalid request parameters
        examples:
          example:
            value:
              success: false
              error: Invalid request parameters
        description: Bad request
    '401':
      application/json:
        schemaArray:
          - type: object
            properties:
              success:
                allOf:
                  - type: boolean
                    example: false
              error:
                allOf:
                  - type: string
                    example: Unauthorized
        examples:
          example:
            value:
              success: false
              error: Unauthorized
        description: Unauthorized
    '500':
      application/json:
        schemaArray:
          - type: object
            properties:
              success:
                allOf:
                  - type: boolean
                    example: false
              error:
                allOf:
                  - type: string
                    example: Failed to process natural language prompt
        examples:
          example:
            value:
              success: false
              error: Failed to process natural language prompt
        description: Server error
  deprecated: false
  type: path
components:
  schemas: {}

````