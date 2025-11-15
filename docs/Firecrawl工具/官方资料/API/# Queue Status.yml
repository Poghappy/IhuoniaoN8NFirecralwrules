# Queue Status

## OpenAPI

````yaml v2-openapi GET /team/queue-status
paths:
  path: /team/queue-status
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
      path: {}
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
                    example: true
              jobsInQueue:
                allOf:
                  - type: number
                    description: Number of jobs currently in your queue
              activeJobsInQueue:
                allOf:
                  - type: number
                    description: Number of jobs currently active
              waitingJobsInQueue:
                allOf:
                  - type: number
                    description: Number of jobs currently waiting
              maxConcurrency:
                allOf:
                  - type: number
                    description: >-
                      Maximum number of concurrent active jobs based on your
                      plan
              mostRecentSuccess:
                allOf:
                  - type: string
                    format: date-time
                    description: Timestamp of the most recent successful job
                    nullable: true
        examples:
          example:
            value:
              success: true
              jobsInQueue: 123
              activeJobsInQueue: 123
              waitingJobsInQueue: 123
              maxConcurrency: 123
              mostRecentSuccess: '2023-11-07T05:31:56Z'
        description: Successful response
  deprecated: false
  type: path
components:
  schemas: {}

````