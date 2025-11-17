# Firecrawl 快速开始指南

> **文档来源**: [Firecrawl 官方文档](https://docs.firecrawl.dev/introduction)
> **最后更新**: 2025-01-27
> **版本**: v2.0

![Firecrawl 将网站转换为 LLM 就绪数据](https://mintcdn.com/firecrawl/vlKm1oZYK3oSRVTM/images/turn-websites-into-llm-ready-data--firecrawl.png?fit=max&auto=format&n=vlKm1oZYK3oSRVTM&q=85&s=4e7b593752a4ff638c1d1dbfddb54a9a)

## 欢迎使用 Firecrawl

[Firecrawl](https://firecrawl.dev/?ref=github) 是一个 API 服务，它接收一个 URL，爬取它，并将其转换为干净的 Markdown。我们爬取所有可访问的子页面，并为每个页面提供干净的 Markdown。无需站点地图。

## 如何使用？

我们提供易于使用的 API 和托管版本。您可以在[这里](https://firecrawl.dev/playground)找到 Playground 和文档。如果您愿意，也可以自行托管后端。

查看以下资源以开始使用：

- **API**: [文档](https://docs.firecrawl.dev/api-reference/introduction)
- **SDKs**: [Python](https://docs.firecrawl.dev/sdks/python), [Node](https://docs.firecrawl.dev/sdks/node)
- **LLM 框架**: [Langchain (python)](https://python.langchain.com/docs/integrations/document_loaders/firecrawl/), [Langchain (js)](https://js.langchain.com/docs/integrations/document_loaders/web_loaders/firecrawl), [Llama Index](https://docs.llamaindex.ai/en/latest/examples/data_connectors/WebPageDemo/#using-firecrawl-reader), [Crew.ai](https://docs.crewai.com/), [Composio](https://composio.dev/tools/firecrawl/all), [PraisonAI](https://docs.praison.ai/firecrawl/), [Superinterface](https://superinterface.ai/docs/assistants/functions/firecrawl), [Vectorize](https://docs.vectorize.io/integrations/source-connectors/firecrawl)
- **低代码框架**: [Dify](https://dify.ai/blog/dify-ai-blog-integrated-with-firecrawl), [Langflow](https://docs.langflow.org/), [Flowise AI](https://docs.flowiseai.com/integrations/langchain/document-loaders/firecrawl), [Cargo](https://docs.getcargo.io/integration/firecrawl), [Pipedream](https://pipedream.com/apps/firecrawl/)
- **社区 SDKs**: [Go](https://docs.firecrawl.dev/sdks/go), [Rust](https://docs.firecrawl.dev/sdks/rust) (v1)
- **其他**: [Zapier](https://zapier.com/apps/firecrawl/integrations), [Pabbly Connect](https://www.pabbly.com/connect/integrations/firecrawl/)
- **自托管**: 要自托管，请参考[这里](https://docs.firecrawl.dev/contributing/self-host)的指南。

需要 SDK 或集成？请通过[提交 issue](https://github.com/firecrawl/firecrawl/issues) 告知我们。

### API 密钥

要使用 API，您需要在 [Firecrawl](https://firecrawl.dev/) 上注册并获取 API 密钥。

### 功能特性

- [**Scrape（抓取）**](#抓取): 抓取 URL 并以 LLM 就绪格式获取其内容（markdown、摘要、通过 [json 模式](#json-模式)的结构化数据、截图、html）
- [**Crawl（爬取）**](#爬取): 抓取网页的所有 URL 并以 LLM 就绪格式返回内容
- [**Map（映射）**](https://docs.firecrawl.dev/features/map): 输入网站并获取所有网站 URL - 极快
- [**Search（搜索）**](https://docs.firecrawl.dev/features/search): 搜索网络并从结果中获取完整内容
- [**Extract（提取）**](https://docs.firecrawl.dev/features/extract): 使用 AI 从单个页面、多个页面或整个网站获取结构化数据。

### 强大的功能

- **LLM 就绪格式**: markdown、摘要、结构化数据、截图、HTML、链接、元数据、图片
- **处理复杂情况**: 代理、反机器人机制、动态内容（js 渲染）、输出解析、编排
- **极速**: 几秒钟内获得结果 - 专为速度和高吞吐量用例而构建
- **可定制性**: 排除标签、使用自定义标头在身份验证墙后爬取、最大爬取深度等...
- **媒体解析**: pdfs、docx、图片
- **可靠性优先**: 旨在获取您需要的数据 - 无论有多困难
- **操作**: 在提取数据之前点击、滚动、输入、等待等

您可以在我们的[文档](https://docs.firecrawl.dev/api-reference/v2-introduction)中找到 Firecrawl 的所有功能以及如何使用它们。

## 安装 Firecrawl

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

## 抓取

要抓取单个 URL，请使用 `scrape` 方法。它接受 URL 作为参数，并以字典形式返回抓取的数据。

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  # 抓取网站:
  doc = firecrawl.scrape("https://firecrawl.dev", formats=["markdown", "html"])
  print(doc)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  // 抓取网站:
  const doc = await firecrawl.scrape('https://firecrawl.dev', { formats: ['markdown', 'html'] });
  console.log(doc);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://firecrawl.dev",
        "formats": ["markdown", "html"]
      }'
  ```
</CodeGroup>

### 响应

SDK 将直接返回数据对象。cURL 将完全按照下面显示的方式返回有效负载。

```json
{
  "success": true,
  "data": {
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

## 爬取

爬取功能允许您自动发现并提取 URL 及其所有可访问子页面的内容。使用我们的 SDK，只需调用 crawl 方法 - 这将提交爬取任务，等待其完成，并返回整个站点的完整结果。

### 使用方法

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  docs = firecrawl.crawl(url="https://docs.firecrawl.dev", limit=10)
  print(docs)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const docs = await firecrawl.crawl({ url: 'https://docs.firecrawl.dev', limit: 10 });
  console.log(docs);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/crawl \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://docs.firecrawl.dev",
        "limit": 10
      }'
  ```
</CodeGroup>

如果您直接使用我们的 API、cURL 或 SDK 上的 `start crawl` 函数，这将返回一个 `ID`，您可以使用它来检查爬取的状态。

```json
{
  "success": true,
  "id": "123-456-789",
  "url": "https://api.firecrawl.dev/v2/crawl/123-456-789"
}
```

### 获取爬取状态

用于检查爬取任务的状态并获取其结果。

<CodeGroup>
  ```python Python
  status = firecrawl.get_crawl_status("<crawl-id>")
  print(status)
  ```

  ```js Node
  const status = await firecrawl.getCrawlStatus('<crawl-id>');
  console.log(status);
  ```

  ```bash cURL
  curl -X GET https://api.firecrawl.dev/v2/crawl/<crawl-id> \
      -H 'Authorization: Bearer YOUR_API_KEY'
  ```
</CodeGroup>

#### 响应

响应将根据爬取的状态而不同。对于未完成或超过 10MB 的大型响应，会提供一个 `next` URL 参数。您必须请求此 URL 以检索下一个 10MB 的数据。如果 `next` 参数不存在，则表示爬取数据已结束。

**爬取中**:

```json
{
  "status": "scraping",
  "total": 36,
  "completed": 10,
  "creditsUsed": 10,
  "expiresAt": "2024-00-00T00:00:00.000Z",
  "next": "https://api.firecrawl.dev/v2/crawl/123-456-789?skip=10",
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

**已完成**:

```json
{
  "status": "completed",
  "total": 36,
  "completed": 36,
  "creditsUsed": 36,
  "expiresAt": "2024-00-00T00:00:00.000Z",
  "data": [
    ...
  ]
}
```

## JSON 模式

使用 JSON 模式，您可以轻松地从任何 URL 提取结构化数据。我们还支持 pydantic 模式，使您更容易使用。以下是使用方法：

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl
  from pydantic import BaseModel

  app = Firecrawl(api_key="fc-YOUR-API-KEY")

  class CompanyInfo(BaseModel):
      company_mission: str
      supports_sso: bool
      is_open_source: bool
      is_in_yc: bool

  result = app.scrape(
      'https://firecrawl.dev',
      formats=[{
        "type": "json",
        "schema": CompanyInfo.model_json_schema()
      }],
      only_main_content=False,
      timeout=120000
  )

  print(result)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const result = await firecrawl.scrape('https://firecrawl.dev', {
    formats: [{
      type: 'json',
      schema: {
        type: 'object',
        properties: {
          company_mission: { type: 'string' },
          supports_sso: { type: 'boolean' },
          is_open_source: { type: 'boolean' },
          is_in_yc: { type: 'boolean' }
        },
        required: ['company_mission', 'supports_sso', 'is_open_source', 'is_in_yc']
      }
    }],
    onlyMainContent: false,
    timeout: 120000
  });

  console.log(result);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://firecrawl.dev",
        "formats": [{
          "type": "json",
          "schema": {
            "type": "object",
            "properties": {
              "company_mission": { "type": "string" },
              "supports_sso": { "type": "boolean" },
              "is_open_source": { "type": "boolean" },
              "is_in_yc": { "type": "boolean" }
            },
            "required": ["company_mission", "supports_sso", "is_open_source", "is_in_yc"]
          }
        }],
        "onlyMainContent": false,
        "timeout": 120000
      }'
  ```
</CodeGroup>

**输出**:

```json
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
    }
  }
}
```

## 搜索

Firecrawl 的搜索 API 允许您执行网络搜索，并可选择在一次操作中抓取搜索结果。

- 选择特定的输出格式（markdown、HTML、链接、截图）
- 选择特定的来源（网络、新闻、图片）
- 使用可自定义的参数（位置等）搜索网络

有关详细信息，请参阅[搜索端点 API 参考](https://docs.firecrawl.dev/api-reference/endpoint/search)。

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  results = firecrawl.search(
      query="firecrawl",
      limit=3,
  )
  print(results)
  ```

  ```js Node
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const results = await firecrawl.search({
    query: 'firecrawl',
    limit: 3,
  });
  console.log(results);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/search \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "query": "firecrawl",
        "limit": 3
      }'
  ```
</CodeGroup>

### 响应

SDK 将直接返回数据对象。cURL 将返回完整的有效负载。

```json
{
  "success": true,
  "data": {
    "web": [
      {
        "url": "https://www.firecrawl.dev/",
        "title": "Firecrawl - The Web Data API for AI",
        "description": "The web crawling, scraping, and search API for AI. Built for scale. Firecrawl delivers the entire internet to AI agents and builders.",
        "position": 1
      },
      {
        "url": "https://github.com/mendableai/firecrawl",
        "title": "mendableai/firecrawl: Turn entire websites into LLM-ready ... - GitHub",
        "description": "Firecrawl is an API service that takes a URL, crawls it, and converts it into clean markdown or structured data.",
        "position": 2
      },
      ...
    ],
    "images": [
      {
        "title": "Quickstart | Firecrawl",
        "imageUrl": "https://mintlify.s3.us-west-1.amazonaws.com/firecrawl/logo/logo.png",
        "imageWidth": 5814,
        "imageHeight": 1200,
        "url": "https://docs.firecrawl.dev/",
        "position": 1
      },
      ...
    ],
    "news": [
      {
        "title": "Y Combinator startup Firecrawl is ready to pay $1M to hire three AI agents as employees",
        "url": "https://techcrunch.com/2025/05/17/y-combinator-startup-firecrawl-is-ready-to-pay-1m-to-hire-three-ai-agents-as-employees/",
        "snippet": "It's now placed three new ads on YC's job board for "AI agents only" and has set aside a $1 million budget total to make it happen.",
        "date": "3 months ago",
        "position": 1
      },
      ...
    ]
  }
}
```

### 无模式提取

现在您可以通过仅向端点传递 `prompt` 来提取数据，而无需模式。LLM 选择数据的结构。

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
  import Firecrawl from '@mendable/firecrawl-js';

  const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

  const result = await firecrawl.scrape('https://firecrawl.dev', {
    formats: [{
      type: 'json',
      prompt: 'Extract the company mission from the page.'
    }],
    onlyMainContent: false,
    timeout: 120000
  });

  console.log(result);
  ```

  ```bash cURL
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://firecrawl.dev",
        "formats": [{
          "type": "json",
          "prompt": "Extract the company mission from the page."
        }],
        "onlyMainContent": false,
        "timeout": 120000
      }'
  ```
</CodeGroup>

**输出**:

```json
{
  "success": true,
  "data": {
    "json": {
      "company_mission": "AI-powered web scraping and data extraction"
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
    }
  }
}
```

## 使用 Actions 与页面交互

Firecrawl 允许您在抓取网页内容之前对网页执行各种操作。这对于与动态内容交互、浏览页面或访问需要用户交互的内容特别有用。

以下是如何使用 actions 导航到 google.com、搜索 Firecrawl、点击第一个结果并截图的示例。

**重要提示**: 在执行其他操作之前/之后几乎总是使用 `wait` 操作，以便为页面加载留出足够的时间。

### 示例

<CodeGroup>
  ```python Python
  from firecrawl import Firecrawl

  firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

  doc = firecrawl.scrape(
      url="https://example.com/login",
      formats=["markdown"],
      actions=[
          {"type": "write", "text": "john@example.com"},
          {"type": "press", "key": "Tab"},
          {"type": "write", "text": "secret"},
          {"type": "click", "selector": 'button[type="submit"]'},
          {"type": "wait", "milliseconds": 1500},
          {"type": "screenshot", "fullPage": True},
      ],
  )

  print(doc.markdown, doc.screenshot)
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
          { "type": "screenshot", "fullPage": true }
        ]
      }'
  ```
</CodeGroup>

### 输出

```json
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

## 开源 vs 云服务

Firecrawl 在 [AGPL-3.0 许可证](https://github.com/mendableai/firecrawl/blob/main/LICENSE)下开源。

为了提供最佳产品，我们在开源产品旁边提供 Firecrawl 的托管版本。云解决方案使我们能够持续创新并为所有用户维护高质量、可持续的服务。

Firecrawl Cloud 可在 [firecrawl.dev](https://firecrawl.dev/) 获得，并提供开源版本中不可用的多种功能：

![Firecrawl Cloud vs Open Source](https://mintcdn.com/firecrawl/vlKm1oZYK3oSRVTM/images/open-source-cloud.png?fit=max&auto=format&n=vlKm1oZYK3oSRVTM&q=85&s=763a6e92c8605d06294ed7ed45df85d0)

## 贡献

我们喜欢贡献！请在提交 pull request 之前阅读我们的[贡献指南](https://github.com/mendableai/firecrawl/blob/main/CONTRIBUTING.md)。

---

**相关链接**:
- [Firecrawl 官网](https://firecrawl.dev/)
- [API 文档](https://docs.firecrawl.dev/api-reference/introduction)
- [GitHub 仓库](https://github.com/mendableai/firecrawl)
- [社区 Discord](https://discord.gg/gSmWdAkdwd)

