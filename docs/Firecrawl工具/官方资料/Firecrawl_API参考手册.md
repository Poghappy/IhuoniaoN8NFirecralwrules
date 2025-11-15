# Firecrawl API 参考手册

> 基于官方文档整理的完整API参考
> 更新时间: 2024年

## 目录

1. [快速开始](#快速开始)
2. [认证](#认证)
3. [API端点](#api端点)
4. [Scrape API](#scrape-api)
5. [Crawl API](#crawl-api)
6. [Map API](#map-api)
7. [Search API](#search-api)
8. [Extract API](#extract-api)
9. [错误处理](#错误处理)
10. [SDK使用](#sdk使用)
11. [最佳实践](#最佳实践)

## 快速开始

### 基础URL
```
https://api.firecrawl.dev
```

### 认证
所有API请求都需要在请求头中包含API密钥：

```bash
Authorization: Bearer fc-YOUR-API-KEY
```

### 基本请求示例

```bash
curl -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer fc-YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown"]
  }'
```

## API端点

### 核心端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/v2/scrape` | POST | 爬取单个URL |
| `/v2/crawl` | POST | 开始爬取作业 |
| `/v2/crawl/{id}` | GET | 获取爬取状态 |
| `/v2/map` | POST | 获取网站地图 |
| `/v2/search` | POST | 搜索网络内容 |
| `/v2/extract` | POST | 提取结构化数据 |

## Scrape API

### 端点
```
POST /v2/scrape
```

### 请求参数

```json
{
  "url": "string",                    // 必需：要爬取的URL
  "formats": ["markdown", "html"],   // 可选：输出格式
  "onlyMainContent": true,           // 可选：只提取主要内容
  "includeTags": ["title", "meta"],  // 可选：包含的HTML标签
  "excludeTags": ["nav", "footer"],  // 可选：排除的HTML标签
  "waitFor": 2000,                   // 可选：等待时间(毫秒)
  "timeout": 30000,                  // 可选：超时时间(毫秒)
  "actions": [],                     // 可选：页面操作
  "location": {                      // 可选：地理位置
    "country": "US"
  },
  "mobile": false,                   // 可选：移动端视图
  "skipTlsVerification": false       // 可选：跳过TLS验证
}
```

### 输出格式选项

#### 基本格式
- `markdown` - Markdown格式
- `html` - 清理后的HTML
- `rawHtml` - 原始HTML
- `screenshot` - 页面截图
- `links` - 页面链接

#### JSON模式
```json
{
  "type": "json",
  "prompt": "提取产品信息",
  "schema": {
    "type": "object",
    "properties": {
      "name": {"type": "string"},
      "price": {"type": "number"}
    }
  }
}
```

### 响应格式

```json
{
  "success": true,
  "data": {
    "markdown": "页面内容...",
    "html": "<html>...",
    "metadata": {
      "title": "页面标题",
      "description": "页面描述",
      "language": "en",
      "sourceURL": "https://example.com",
      "statusCode": 200
    },
    "llm": {
      "tokenCount": 1500
    }
  }
}
```

### 页面操作

支持的操作类型：

```json
[
  {"type": "wait", "milliseconds": 3000},
  {"type": "click", "selector": ".button"},
  {"type": "write", "text": "搜索内容"},
  {"type": "press", "key": "Enter"},
  {"type": "scroll", "direction": "down"},
  {"type": "screenshot"},
  {"type": "executeJavascript", "script": "console.log('test');"}
]
```

## Crawl API

### 开始爬取
```
POST /v2/crawl
```

### 请求参数

```json
{
  "url": "https://example.com",
  "limit": 100,                      // 最大页面数
  "maxDepth": 3,                     // 最大深度
  "allowExternalLinks": false,       // 允许外部链接
  "includePaths": ["/blog/*"],       // 包含路径
  "excludePaths": ["/admin/*"],      // 排除路径
  "scrapeOptions": {                 // 爬取选项
    "formats": ["markdown"],
    "onlyMainContent": true
  },
  "webhook": "https://your-webhook.com", // 完成回调
  "deduplicateSimilarURLs": true     // 去重相似URL
}
```

### 响应

```json
{
  "success": true,
  "id": "crawl-123-456-789",
  "url": "https://api.firecrawl.dev/v2/crawl/crawl-123-456-789"
}
```

### 获取爬取状态
```
GET /v2/crawl/{id}
```

### 状态响应

```json
{
  "success": true,
  "status": "completed",
  "total": 25,
  "completed": 25,
  "creditsUsed": 25,
  "expiresAt": "2024-12-31T23:59:59Z",
  "data": [
    {
      "markdown": "页面内容...",
      "metadata": {
        "title": "页面标题",
        "sourceURL": "https://example.com/page1"
      }
    }
  ]
}
```

### 爬取状态
- `scraping` - 爬取中
- `completed` - 已完成
- `failed` - 失败
- `cancelled` - 已取消

## Map API

### 端点
```
POST /v2/map
```

### 请求参数

```json
{
  "url": "https://example.com",
  "search": "blog",                  // 搜索过滤
  "limit": 1000,                    // 最大URL数量
  "includeSubdomains": false,       // 包含子域名
  "ignoreSitemap": false            // 忽略站点地图
}
```

### 响应

```json
{
  "success": true,
  "links": [
    "https://example.com/",
    "https://example.com/about",
    "https://example.com/blog",
    "https://example.com/contact"
  ]
}
```

## Search API

### 端点
```
POST /v2/search
```

### 请求参数

```json
{
  "query": "firecrawl API",
  "limit": 10,
  "sources": ["web", "news", "images"],
  "location": "US",
  "scrapeOptions": {
    "formats": ["markdown"]
  }
}
```

### 响应

```json
{
  "success": true,
  "data": {
    "web": [
      {
        "url": "https://example.com",
        "title": "页面标题",
        "description": "页面描述",
        "position": 1,
        "markdown": "页面内容..."
      }
    ],
    "news": [...],
    "images": [...]
  }
}
```

## Extract API

### 端点
```
POST /v2/extract
```

### 请求参数

```json
{
  "urls": [
    "https://example.com/product1",
    "https://example.com/product2"
  ],
  "prompt": "提取产品名称、价格和描述",
  "schema": {
    "type": "object",
    "properties": {
      "products": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"},
            "description": {"type": "string"}
          }
        }
      }
    }
  }
}
```

### 响应

```json
{
  "success": true,
  "data": {
    "products": [
      {
        "name": "产品A",
        "price": 99.99,
        "description": "产品描述"
      }
    ]
  }
}
```

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "error": "错误描述",
  "details": {
    "code": "INVALID_URL",
    "message": "提供的URL无效"
  }
}
```

### 常见错误代码

| 代码 | 描述 | 解决方案 |
|------|------|----------|
| `INVALID_URL` | URL格式无效 | 检查URL格式 |
| `RATE_LIMIT_EXCEEDED` | 超出速率限制 | 减少请求频率 |
| `INSUFFICIENT_CREDITS` | 积分不足 | 充值或升级套餐 |
| `TIMEOUT` | 请求超时 | 增加超时时间 |
| `BLOCKED_URL` | URL被阻止 | 检查robots.txt |

### HTTP状态码

- `200` - 成功
- `400` - 请求错误
- `401` - 认证失败
- `403` - 权限不足
- `429` - 速率限制
- `500` - 服务器错误

## SDK使用

### Python SDK

```python
from firecrawl import Firecrawl

# 初始化
app = Firecrawl(api_key="fc-YOUR-API-KEY")

# 爬取单页
result = app.scrape(
    url="https://example.com",
    formats=["markdown", "html"]
)

# 爬取整站
result = app.crawl(
    url="https://example.com",
    limit=10,
    scrape_options={
        "formats": ["markdown"]
    }
)

# 搜索
result = app.search(
    query="firecrawl",
    limit=5
)

# 获取网站地图
result = app.map(url="https://example.com")
```

### Node.js SDK

```javascript
import { Firecrawl } from '@mendable/firecrawl-js';

// 初始化
const app = new Firecrawl({ apiKey: 'fc-YOUR-API-KEY' });

// 爬取单页
const result = await app.scrape({
  url: 'https://example.com',
  formats: ['markdown', 'html']
});

// 爬取整站
const crawlResult = await app.crawl({
  url: 'https://example.com',
  limit: 10,
  scrapeOptions: {
    formats: ['markdown']
  }
});

// 搜索
const searchResult = await app.search({
  query: 'firecrawl',
  limit: 5
});
```

## 最佳实践

### 1. 性能优化

- 使用`onlyMainContent: true`减少不必要内容
- 合理设置`limit`和`maxDepth`
- 使用`excludeTags`排除无关元素
- 启用`deduplicateSimilarURLs`去重

### 2. 错误处理

```python
try:
    result = app.scrape(url)
except Exception as e:
    if "rate limit" in str(e).lower():
        # 处理速率限制
        time.sleep(60)
        result = app.scrape(url)
    else:
        # 其他错误处理
        print(f"错误: {e}")
```

### 3. 批量处理

```python
# 使用crawl而不是多次scrape
result = app.crawl(
    url="https://example.com",
    limit=100,
    scrape_options={
        "formats": ["markdown"]
    }
)
```

### 4. 内容过滤

```python
# 只爬取特定路径
result = app.crawl(
    url="https://example.com",
    include_paths=["/blog/*", "/news/*"],
    exclude_paths=["/admin/*", "/login/*"]
)
```

### 5. 监控和调试

```python
# 检查爬取状态
status = app.get_crawl_status(crawl_id)
print(f"进度: {status['completed']}/{status['total']}")
print(f"使用积分: {status['creditsUsed']}")
```

## 配额和限制

### 免费套餐
- 500次请求/月
- 基础功能
- 社区支持

### 付费套餐
- Hobby: $20/月，2000次请求
- Standard: $100/月，10000次请求
- Scale: $500/月，50000次请求
- 企业版: 自定义

### 速率限制
- 免费: 2请求/分钟
- Hobby: 10请求/分钟
- Standard: 50请求/分钟
- Scale: 200请求/分钟

## 集成示例

### 与Langchain集成

```python
from langchain.document_loaders import FirecrawlLoader

loader = FirecrawlLoader(
    api_key="fc-YOUR-API-KEY",
    url="https://example.com",
    mode="scrape"
)
docs = loader.load()
```

### 与Webhook集成

```python
# 设置webhook接收爬取完成通知
result = app.crawl(
    url="https://example.com",
    webhook="https://your-domain.com/webhook"
)
```

### Webhook处理示例

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    if data['status'] == 'completed':
        # 处理完成的爬取结果
        process_crawl_results(data['data'])
    return 'OK'
```

## 总结

Firecrawl API提供了强大而灵活的网页数据提取能力：

1. **多种API端点** - 满足不同的数据提取需求
2. **丰富的配置选项** - 精确控制爬取行为
3. **多种输出格式** - 适应不同的使用场景
4. **智能处理** - 自动处理复杂的网页结构
5. **可靠的服务** - 高可用性和性能保证

通过合理使用这些API，您可以高效地从网络中提取所需的数据，为您的应用提供强大的数据支持。