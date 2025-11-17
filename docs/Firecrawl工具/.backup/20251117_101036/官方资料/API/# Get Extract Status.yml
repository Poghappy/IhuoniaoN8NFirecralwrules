# Get Extract Status

## OpenAPI

````yaml v2-openapi GET /extract/{id}
paths:
  path: /extract/{id}
  method: get
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
      path:
        id:
          schema:
            - type: string
              required: true
              description: The ID of the extract job
              format: uuid
      query: {}
      header: {}
      cookie: {}
    body: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              success:
                allOf:
                  - type: boolean
              data:
                allOf:
                  - type: object
              status:
                allOf:
                  - type: string
                    enum:
                      - completed
                      - processing
                      - failed
                      - cancelled
                    description: The current status of the extract job
              expiresAt:
                allOf:
                  - type: string
                    format: date-time
              tokensUsed:
                allOf:
                  - type: integer
                    description: >-
                      The number of tokens used by the extract job. Only
                      available if the job is completed.
            refIdentifier: '#/components/schemas/ExtractStatusResponse'
        examples:
          example:
            value:
              success: true
              data: {}
              status: completed
              expiresAt: '2023-11-07T05:31:56Z'
              tokensUsed: 123
        description: Successful response
  deprecated: false
  type: path
components:
  schemas: {}

````