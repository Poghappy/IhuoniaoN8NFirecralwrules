# Firecrawl 集成说明文档

> 来源: https://docs.firecrawl.dev
> 抓取时间: 2024年

## 欢迎使用 Firecrawl

[Firecrawl](https://firecrawl.dev/?ref=github) 是一个API服务，它接收一个URL，爬取它，并将其转换为干净的markdown格式。我们爬取所有可访问的子页面，并为每个页面提供干净的markdown。无需站点地图。

## 如何使用？

我们通过托管版本提供易于使用的API。您可以在[这里](https://firecrawl.dev/playground)找到playground和文档。如果您愿意，也可以自托管后端。

查看以下资源开始使用：

- [x] **API**: [文档](https://docs.firecrawl.dev/api-reference/introduction)
- [x] **SDKs**: [Python](https://docs.firecrawl.dev/sdks/python), [Node](https://docs.firecrawl.dev/sdks/node)
- [x] **LLM框架**: [Langchain (python)](https://python.langchain.com/docs/integrations/document_loaders/firecrawl/), [Langchain (js)](https://js.langchain.com/docs/integrations/document_loaders/web_loaders/firecrawl), [Llama Index](https://docs.llamaindex.ai/en/latest/examples/data_connectors/WebPageDemo/#using-firecrawl-reader), [Crew.ai](https://docs.crewai.com/), [Composio](https://composio.dev/tools/firecrawl/all), [PraisonAI](https://docs.praison.ai/firecrawl/), [Superinterface](https://superinterface.ai/docs/assistants/functions/firecrawl), [Vectorize](https://docs.vectorize.io/integrations/source-connectors/firecrawl)
- [x] **低代码框架**: [Dify](https://dify.ai/blog/dify-ai-blog-integrated-with-firecrawl), [Langflow](https://docs.langflow.org/), [Flowise AI](https://docs.flowiseai.com/integrations/langchain/document-loaders/firecrawl), [Cargo](https://docs.getcargo.io/integration/firecrawl), [Pipedream](https://pipedream.com/apps/firecrawl/)
- [x] **社区SDKs**: [Go](https://docs.firecrawl.dev/sdks/go), [Rust](https://docs.firecrawl.dev/sdks/rust) (v1)
- [x] **其他**: [Zapier](https://zapier.com/apps/firecrawl/integrations), [Pabbly Connect](https://www.pabbly.com/connect/integrations/firecrawl/)

**自托管**: 要自托管，请参考[这里](https://docs.firecrawl.dev/contributing/self-host)的指南。

### API密钥

要使用API，您需要在[Firecrawl](https://firecrawl.dev/)上注册并获取API密钥。

### 功能特性

- [**Scrape**](https://docs.firecrawl.dev/introduction#scraping): 爬取URL并获取LLM就绪格式的内容（markdown、摘要、通过[json模式](https://docs.firecrawl.dev/introduction#json-mode)的结构化数据、截图、html）
- [**Crawl**](https://docs.firecrawl.dev/introduction#crawling): 爬取网页的所有URL并返回LLM就绪格式的内容
- [**Map**](https://docs.firecrawl.dev/features/map): 输入网站并获取所有网站URL - 极快
- [**Search**](https://docs.firecrawl.dev/features/search): 搜索网络并从结果中获取完整内容
- [**Extract**](https://docs.firecrawl.dev/features/extract): 使用AI从单页、多页或整个网站获取结构化数据

### 强大功能

- **LLM就绪格式**: markdown、摘要、结构化数据、截图、HTML、链接、元数据
- **处理复杂情况**: 代理、反机器人机制、动态内容（js渲染）、输出解析、编排
- **闪电般快速**: 在几秒钟内获得结果——为速度和高吞吐量用例而构建
- **可定制性**: 排除标签、使用自定义标头在认证墙后爬取、最大爬取深度等
- **媒体解析**: pdfs、docx、图像
- **可靠性优先**: 设计用于获取您需要的数据 - 无论多么困难
- **操作**: 在提取数据之前点击、滚动、输入、等待等

您可以在我们的[文档](https://docs.firecrawl.dev/api-reference/v2-introduction)中找到Firecrawl的所有功能以及如何使用它们。

## 安装 Firecrawl

### Python

```python
# pip install firecrawl-py
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")
```

### Node.js

```javascript
// npm install @mendable/firecrawl-js
import { Firecrawl } from '@mendable/firecrawl-js';

const firecrawl = new Firecrawl({ apiKey: 'fc-YOUR-API-KEY' });
```

## 爬取（Scraping）

要爬取单个URL，使用`scrape`方法。它将URL作为参数并返回爬取的数据作为字典。

### Python示例

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

# 爬取网站:
doc = firecrawl.scrape("https://firecrawl.dev", formats=["markdown", "html"])
print(doc)
```

### 响应格式

```json
{
  "success": true,
  "data" : {
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

## 爬取整站（Crawling）

爬取功能允许您自动发现并从URL及其所有可访问子页面提取内容。使用我们的SDK，只需调用crawl方法——这将提交爬取作业，等待其完成，并返回整个站点的完整结果。

### 使用方法

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

docs = firecrawl.crawl(url="https://docs.firecrawl.dev", limit=10)
print(docs)
```

如果您直接使用我们的API、cURL或SDK上的`start crawl`函数，这将返回一个`ID`，您可以使用它来检查爬取的状态。

```json
{
  "success": true,
  "id": "123-456-789",
  "url": "https://api.firecrawl.dev/v2/crawl/123-456-789"
}
```

### 获取爬取状态

用于检查爬取作业的状态并获取其结果。

```python
status = firecrawl.get_crawl_status("<crawl-id>")
print(status)
```

## JSON模式

使用JSON模式，您可以轻松从任何URL提取结构化数据。我们支持pydantic模式以使其更容易。以下是如何使用它：

```python
from firecrawl import Firecrawl
from pydantic import BaseModel

app = Firecrawl(api_key="fc-YOUR-API-KEY")

class JsonSchema(BaseModel):
    company_mission: str
    supports_sso: bool
    is_open_source: bool
    is_in_yc: bool

result = app.scrape(
    'https://firecrawl.dev',
    formats=[{
      "type": "json",
      "schema": JsonSchema
    }],
    only_main_content=False,
    timeout=120000
)

print(result)
```

输出：

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

## 搜索（Search）

Firecrawl的搜索API允许您执行网络搜索并可选择在一个操作中爬取搜索结果。

- 选择特定输出格式（markdown、HTML、链接、截图）
- 选择特定来源（网络、新闻、图像）
- 使用可定制参数搜索网络（位置等）

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

results = firecrawl.search(
    query="firecrawl",
    limit=3,
)
print(results)
```

### 搜索响应

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
      }
    ],
    "images": [
      {
        "title": "Quickstart | Firecrawl",
        "imageUrl": "https://mintlify.s3.us-west-1.amazonaws.com/firecrawl/logo/logo.png",
        "imageWidth": 5814,
        "imageHeight": 1200,
        "url": "https://docs.firecrawl.dev/",
        "position": 1
      }
    ],
    "news": [
      {
        "title": "Y Combinator startup Firecrawl is ready to pay $1M to hire three AI agents as employees",
        "url": "https://techcrunch.com/2025/05/17/y-combinator-startup-firecrawl-is-ready-to-pay-1m-to-hire-three-ai-agents-as-employees/",
        "snippet": "It's now placed three new ads on YC's job board for "AI agents only" and has set aside a $1 million budget total to make it happen.",
        "date": "3 months ago",
        "position": 1
      }
    ]
  }
}
```

## 无模式提取

您现在可以通过向端点传递`prompt`来在没有模式的情况下进行提取。LLM选择数据的结构。

```python
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

## 页面交互操作

Firecrawl允许您在爬取内容之前对网页执行各种操作。这对于与动态内容交互、浏览页面或访问需要用户交互的内容特别有用。

以下是如何使用操作导航到google.com、搜索Firecrawl、点击第一个结果并截图的示例。

重要的是，在执行其他操作之前/之后几乎总是使用`wait`操作，以给页面足够的时间加载。

```python
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-YOUR-API-KEY")

result = app.scrape(
    'https://google.com',
    formats=["screenshot"],
    actions=[
        {"type": "wait", "milliseconds": 3000},
        {"type": "write", "text": "firecrawl"},
        {"type": "press", "key": "Enter"},
        {"type": "wait", "milliseconds": 3000},
        {"type": "click", "selector": "h3"},
        {"type": "wait", "milliseconds": 3000},
        {"type": "screenshot"}
    ]
)

print(result)
```

## 开源 vs 云服务

### 开源版本
- 免费使用
- 需要自己托管和维护
- 基本功能
- 社区支持

### 云服务版本
- 托管服务，无需维护
- 高级功能和优化
- 专业支持
- 更好的性能和可靠性
- 付费使用

## 贡献

Firecrawl是开源项目，欢迎社区贡献。您可以：

- 报告问题和错误
- 提交功能请求
- 贡献代码
- 改进文档

访问我们的[GitHub仓库](https://github.com/firecrawl/firecrawl)了解更多信息。

## 总结

Firecrawl是一个强大的网页数据提取工具，提供：

1. **简单易用的API** - 只需几行代码即可开始使用
2. **多种输出格式** - Markdown、HTML、JSON、截图等
3. **智能爬取** - 自动处理JavaScript、反爬虫机制等
4. **结构化数据提取** - 使用AI提取特定数据
5. **高性能** - 快速、可靠的服务
6. **丰富的集成** - 支持多种框架和工具

无论您是构建AI应用、进行数据分析还是需要网页内容提取，Firecrawl都能为您提供强大而灵活的解决方案。