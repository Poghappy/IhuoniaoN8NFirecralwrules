# Firecrawl SDK 使用指南

> 全面的SDK使用教程和最佳实践
> 更新时间: 2024年

## 目录

1. [支持的SDK](#支持的sdk)
2. [Python SDK](#python-sdk)
3. [Node.js SDK](#nodejs-sdk)
4. [Go SDK](#go-sdk)
5. [Rust SDK](#rust-sdk)
6. [cURL示例](#curl示例)
7. [框架集成](#框架集成)
8. [最佳实践](#最佳实践)
9. [故障排除](#故障排除)

## 支持的SDK

### 官方SDK
- **Python** - `firecrawl-py`
- **Node.js** - `@mendable/firecrawl-js`

### 社区SDK
- **Go** - `firecrawl-go`
- **Rust** - `firecrawl-rust`

### 框架集成
- **Langchain** (Python/JavaScript)
- **LlamaIndex**
- **Crew.ai**
- **Dify**
- **Langflow**

## Python SDK

### 安装

```bash
pip install firecrawl-py
```

### 基本使用

```python
from firecrawl import Firecrawl

# 初始化客户端
app = Firecrawl(api_key="fc-YOUR-API-KEY")

# 基本爬取
result = app.scrape("https://example.com")
print(result['data']['markdown'])
```

### 详细配置

```python
from firecrawl import Firecrawl
from pydantic import BaseModel
import json

# 初始化
app = Firecrawl(
    api_key="fc-YOUR-API-KEY",
    base_url="https://api.firecrawl.dev"  # 可选，自定义API端点
)

# 高级爬取配置
result = app.scrape(
    url="https://example.com",
    formats=["markdown", "html", "screenshot"],
    only_main_content=True,
    include_tags=["title", "meta", "article"],
    exclude_tags=["nav", "footer", "aside"],
    wait_for=3000,
    timeout=30000,
    mobile=False,
    actions=[
        {"type": "wait", "milliseconds": 2000},
        {"type": "click", "selector": ".load-more"},
        {"type": "wait", "milliseconds": 2000}
    ]
)

print(f"标题: {result['data']['metadata']['title']}")
print(f"内容长度: {len(result['data']['markdown'])}")
```

### JSON模式提取

```python
# 使用Pydantic模式
class ProductInfo(BaseModel):
    name: str
    price: float
    description: str
    in_stock: bool

result = app.scrape(
    url="https://example.com/product",
    formats=[{
        "type": "json",
        "schema": ProductInfo
    }]
)

product = result['data']['json']
print(f"产品: {product['name']}, 价格: ${product['price']}")
```

### 无模式提取

```python
# 使用自然语言提示
result = app.scrape(
    url="https://example.com",
    formats=[{
        "type": "json",
        "prompt": "提取页面中的联系信息，包括电话、邮箱和地址"
    }]
)

contact_info = result['data']['json']
print(json.dumps(contact_info, indent=2, ensure_ascii=False))
```

### 爬取整站

```python
# 同步爬取（推荐用于小型网站）
result = app.crawl(
    url="https://example.com",
    limit=50,
    max_depth=3,
    include_paths=["/blog/*", "/news/*"],
    exclude_paths=["/admin/*", "/login/*"],
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    },
    allow_external_links=False,
    deduplicate_similar_urls=True
)

print(f"爬取了 {len(result['data'])} 个页面")
for page in result['data']:
    print(f"- {page['metadata']['title']}: {page['metadata']['sourceURL']}")
```

### 异步爬取

```python
import time

# 启动爬取作业
crawl_result = app.start_crawl(
    url="https://example.com",
    limit=100,
    scrape_options={
        "formats": ["markdown"]
    }
)

crawl_id = crawl_result['id']
print(f"爬取作业ID: {crawl_id}")

# 检查状态
while True:
    status = app.get_crawl_status(crawl_id)
    print(f"状态: {status['status']}, 进度: {status['completed']}/{status['total']}")
    
    if status['status'] == 'completed':
        print("爬取完成！")
        for page in status['data']:
            print(f"- {page['metadata']['title']}")
        break
    elif status['status'] == 'failed':
        print("爬取失败")
        break
    
    time.sleep(10)  # 等待10秒后再检查
```

### 搜索功能

```python
# 基本搜索
result = app.search(
    query="firecrawl API tutorial",
    limit=10,
    sources=["web", "news"]
)

print(f"找到 {len(result['data']['web'])} 个网页结果")
for item in result['data']['web']:
    print(f"- {item['title']}: {item['url']}")

# 搜索并爬取内容
result = app.search(
    query="Python web scraping",
    limit=5,
    scrape_options={
        "formats": ["markdown"]
    }
)

for item in result['data']['web']:
    if 'markdown' in item:
        print(f"\n=== {item['title']} ===")
        print(item['markdown'][:500] + "...")
```

### 获取网站地图

```python
# 快速获取所有URL
result = app.map(
    url="https://example.com",
    search="blog",  # 过滤包含"blog"的URL
    limit=1000,
    include_subdomains=False
)

print(f"发现 {len(result['links'])} 个链接")
for link in result['links'][:10]:  # 显示前10个
    print(f"- {link}")
```

### 批量提取

```python
# 从多个URL提取结构化数据
urls = [
    "https://example.com/product1",
    "https://example.com/product2",
    "https://example.com/product3"
]

result = app.extract(
    urls=urls,
    prompt="提取每个产品的名称、价格、评分和主要特性",
    schema={
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "number"},
                        "rating": {"type": "number"},
                        "features": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
)

products = result['data']['products']
for product in products:
    print(f"产品: {product['name']}, 价格: ${product['price']}, 评分: {product['rating']}")
```

### 错误处理

```python
from firecrawl import Firecrawl
from firecrawl.exceptions import FirecrawlError
import time

app = Firecrawl(api_key="fc-YOUR-API-KEY")

def safe_scrape(url, max_retries=3):
    """安全爬取，包含重试机制"""
    for attempt in range(max_retries):
        try:
            result = app.scrape(url)
            return result
        except FirecrawlError as e:
            if "rate limit" in str(e).lower():
                print(f"遇到速率限制，等待60秒后重试... (尝试 {attempt + 1}/{max_retries})")
                time.sleep(60)
            elif "timeout" in str(e).lower():
                print(f"请求超时，等待10秒后重试... (尝试 {attempt + 1}/{max_retries})")
                time.sleep(10)
            else:
                print(f"其他错误: {e}")
                break
        except Exception as e:
            print(f"未知错误: {e}")
            break
    
    return None

# 使用示例
result = safe_scrape("https://example.com")
if result:
    print("爬取成功")
else:
    print("爬取失败")
```

## Node.js SDK

### 安装

```bash
npm install @mendable/firecrawl-js
# 或
yarn add @mendable/firecrawl-js
```

### 基本使用

```javascript
import { Firecrawl } from '@mendable/firecrawl-js';

// 初始化客户端
const app = new Firecrawl({ apiKey: 'fc-YOUR-API-KEY' });

// 基本爬取
const result = await app.scrape({ url: 'https://example.com' });
console.log(result.data.markdown);
```

### 详细配置

```javascript
import { Firecrawl } from '@mendable/firecrawl-js';

const app = new Firecrawl({ 
    apiKey: 'fc-YOUR-API-KEY',
    baseUrl: 'https://api.firecrawl.dev' // 可选
});

// 高级爬取配置
const result = await app.scrape({
    url: 'https://example.com',
    formats: ['markdown', 'html', 'screenshot'],
    onlyMainContent: true,
    includeTags: ['title', 'meta', 'article'],
    excludeTags: ['nav', 'footer', 'aside'],
    waitFor: 3000,
    timeout: 30000,
    mobile: false,
    actions: [
        { type: 'wait', milliseconds: 2000 },
        { type: 'click', selector: '.load-more' },
        { type: 'wait', milliseconds: 2000 }
    ]
});

console.log(`标题: ${result.data.metadata.title}`);
console.log(`内容长度: ${result.data.markdown.length}`);
```

### JSON模式提取

```javascript
// 使用JSON Schema
const productSchema = {
    type: 'object',
    properties: {
        name: { type: 'string' },
        price: { type: 'number' },
        description: { type: 'string' },
        inStock: { type: 'boolean' }
    },
    required: ['name', 'price']
};

const result = await app.scrape({
    url: 'https://example.com/product',
    formats: [{
        type: 'json',
        schema: productSchema
    }]
});

const product = result.data.json;
console.log(`产品: ${product.name}, 价格: $${product.price}`);
```

### 爬取整站

```javascript
// 同步爬取
const result = await app.crawl({
    url: 'https://example.com',
    limit: 50,
    maxDepth: 3,
    includePaths: ['/blog/*', '/news/*'],
    excludePaths: ['/admin/*', '/login/*'],
    scrapeOptions: {
        formats: ['markdown'],
        onlyMainContent: true
    },
    allowExternalLinks: false,
    deduplicateSimilarUrls: true
});

console.log(`爬取了 ${result.data.length} 个页面`);
result.data.forEach(page => {
    console.log(`- ${page.metadata.title}: ${page.metadata.sourceURL}`);
});
```

### 异步爬取

```javascript
// 启动爬取作业
const crawlResult = await app.startCrawl({
    url: 'https://example.com',
    limit: 100,
    scrapeOptions: {
        formats: ['markdown']
    }
});

const crawlId = crawlResult.id;
console.log(`爬取作业ID: ${crawlId}`);

// 检查状态
const checkStatus = async () => {
    while (true) {
        const status = await app.getCrawlStatus(crawlId);
        console.log(`状态: ${status.status}, 进度: ${status.completed}/${status.total}`);
        
        if (status.status === 'completed') {
            console.log('爬取完成！');
            status.data.forEach(page => {
                console.log(`- ${page.metadata.title}`);
            });
            break;
        } else if (status.status === 'failed') {
            console.log('爬取失败');
            break;
        }
        
        await new Promise(resolve => setTimeout(resolve, 10000)); // 等待10秒
    }
};

checkStatus();
```

### 搜索功能

```javascript
// 基本搜索
const result = await app.search({
    query: 'firecrawl API tutorial',
    limit: 10,
    sources: ['web', 'news']
});

console.log(`找到 ${result.data.web.length} 个网页结果`);
result.data.web.forEach(item => {
    console.log(`- ${item.title}: ${item.url}`);
});
```

### 错误处理

```javascript
import { Firecrawl } from '@mendable/firecrawl-js';

const app = new Firecrawl({ apiKey: 'fc-YOUR-API-KEY' });

async function safeScrape(url, maxRetries = 3) {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            const result = await app.scrape({ url });
            return result;
        } catch (error) {
            if (error.message.toLowerCase().includes('rate limit')) {
                console.log(`遇到速率限制，等待60秒后重试... (尝试 ${attempt + 1}/${maxRetries})`);
                await new Promise(resolve => setTimeout(resolve, 60000));
            } else if (error.message.toLowerCase().includes('timeout')) {
                console.log(`请求超时，等待10秒后重试... (尝试 ${attempt + 1}/${maxRetries})`);
                await new Promise(resolve => setTimeout(resolve, 10000));
            } else {
                console.log(`其他错误: ${error.message}`);
                break;
            }
        }
    }
    return null;
}

// 使用示例
const result = await safeScrape('https://example.com');
if (result) {
    console.log('爬取成功');
} else {
    console.log('爬取失败');
}
```

## Go SDK

### 安装

```bash
go get github.com/firecrawl/firecrawl-go
```

### 基本使用

```go
package main

import (
    "fmt"
    "log"
    "github.com/firecrawl/firecrawl-go"
)

func main() {
    // 初始化客户端
    client := firecrawl.NewClient("fc-YOUR-API-KEY")
    
    // 基本爬取
    result, err := client.Scrape(firecrawl.ScrapeRequest{
        URL: "https://example.com",
        Formats: []string{"markdown"},
    })
    
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Println(result.Data.Markdown)
}
```

### 详细配置

```go
package main

import (
    "fmt"
    "log"
    "github.com/firecrawl/firecrawl-go"
)

func main() {
    client := firecrawl.NewClient("fc-YOUR-API-KEY")
    
    // 高级爬取配置
    result, err := client.Scrape(firecrawl.ScrapeRequest{
        URL:             "https://example.com",
        Formats:         []string{"markdown", "html"},
        OnlyMainContent: true,
        IncludeTags:     []string{"title", "meta", "article"},
        ExcludeTags:     []string{"nav", "footer", "aside"},
        WaitFor:         3000,
        Timeout:         30000,
        Actions: []firecrawl.Action{
            {Type: "wait", Milliseconds: 2000},
            {Type: "click", Selector: ".load-more"},
            {Type: "wait", Milliseconds: 2000},
        },
    })
    
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("标题: %s\n", result.Data.Metadata.Title)
    fmt.Printf("内容长度: %d\n", len(result.Data.Markdown))
}
```

## cURL示例

### 基本爬取

```bash
curl -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer fc-YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown"]
  }'
```

### 高级爬取

```bash
curl -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer fc-YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown", "html"],
    "onlyMainContent": true,
    "includeTags": ["title", "meta", "article"],
    "excludeTags": ["nav", "footer"],
    "waitFor": 3000,
    "actions": [
      {"type": "wait", "milliseconds": 2000},
      {"type": "click", "selector": ".load-more"}
    ]
  }'
```

### JSON模式提取

```bash
curl -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer fc-YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/product",
    "formats": [{
      "type": "json",
      "schema": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "price": {"type": "number"}
        }
      }
    }]
  }'
```

### 启动爬取作业

```bash
curl -X POST https://api.firecrawl.dev/v2/crawl \
  -H "Authorization: Bearer fc-YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "limit": 50,
    "scrapeOptions": {
      "formats": ["markdown"]
    }
  }'
```

### 检查爬取状态

```bash
curl -X GET https://api.firecrawl.dev/v2/crawl/{crawl-id} \
  -H "Authorization: Bearer fc-YOUR-API-KEY"
```

### 搜索

```bash
curl -X POST https://api.firecrawl.dev/v2/search \
  -H "Authorization: Bearer fc-YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "firecrawl tutorial",
    "limit": 10,
    "sources": ["web"]
  }'
```

## 框架集成

### Langchain Python

```python
from langchain.document_loaders import FirecrawlLoader

# 爬取单页
loader = FirecrawlLoader(
    api_key="fc-YOUR-API-KEY",
    url="https://example.com",
    mode="scrape"
)
docs = loader.load()

# 爬取整站
loader = FirecrawlLoader(
    api_key="fc-YOUR-API-KEY",
    url="https://example.com",
    mode="crawl",
    params={
        "limit": 50,
        "scrapeOptions": {
            "formats": ["markdown"]
        }
    }
)
docs = loader.load()

print(f"加载了 {len(docs)} 个文档")
```

### Langchain JavaScript

```javascript
import { FirecrawlLoader } from "langchain/document_loaders/web/firecrawl";

// 爬取单页
const loader = new FirecrawlLoader({
    apiKey: "fc-YOUR-API-KEY",
    url: "https://example.com",
    mode: "scrape"
});

const docs = await loader.load();
console.log(`加载了 ${docs.length} 个文档`);
```

### LlamaIndex

```python
from llama_index.readers.web import FirecrawlWebReader

# 初始化读取器
reader = FirecrawlWebReader(
    api_key="fc-YOUR-API-KEY"
)

# 读取文档
documents = reader.load_data(
    url="https://example.com",
    mode="scrape"
)

print(f"读取了 {len(documents)} 个文档")
```

## 最佳实践

### 1. 性能优化

```python
# 只提取主要内容
result = app.scrape(
    url="https://example.com",
    only_main_content=True,
    exclude_tags=["nav", "footer", "aside", "ads"]
)

# 使用合适的格式
result = app.scrape(
    url="https://example.com",
    formats=["markdown"]  # 只要markdown，不要html
)

# 设置合理的限制
result = app.crawl(
    url="https://example.com",
    limit=100,  # 不要设置过大
    max_depth=3  # 控制深度
)
```

### 2. 错误处理和重试

```python
import time
import random
from firecrawl import Firecrawl

def exponential_backoff_scrape(app, url, max_retries=5):
    """指数退避重试策略"""
    for attempt in range(max_retries):
        try:
            return app.scrape(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"重试 {attempt + 1}/{max_retries}，等待 {wait_time:.2f} 秒")
            time.sleep(wait_time)

app = Firecrawl(api_key="fc-YOUR-API-KEY")
result = exponential_backoff_scrape(app, "https://example.com")
```

### 3. 批量处理

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def scrape_url(url):
    """爬取单个URL"""
    try:
        app = Firecrawl(api_key="fc-YOUR-API-KEY")
        return app.scrape(url)
    except Exception as e:
        print(f"爬取 {url} 失败: {e}")
        return None

def batch_scrape(urls, max_workers=5):
    """批量爬取URL"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(scrape_url, urls))
    return [r for r in results if r is not None]

# 使用示例
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

results = batch_scrape(urls)
print(f"成功爬取 {len(results)} 个页面")
```

### 4. 内容验证

```python
def validate_content(result):
    """验证爬取内容的质量"""
    if not result or 'data' not in result:
        return False
    
    data = result['data']
    
    # 检查是否有内容
    if not data.get('markdown') or len(data['markdown'].strip()) < 100:
        return False
    
    # 检查状态码
    if data.get('metadata', {}).get('statusCode') != 200:
        return False
    
    # 检查是否是错误页面
    title = data.get('metadata', {}).get('title', '').lower()
    if any(error in title for error in ['404', 'not found', 'error']):
        return False
    
    return True

# 使用示例
result = app.scrape("https://example.com")
if validate_content(result):
    print("内容有效")
else:
    print("内容无效，需要重新爬取")
```

### 5. 配额管理

```python
class QuotaManager:
    def __init__(self, daily_limit=1000):
        self.daily_limit = daily_limit
        self.used_today = 0
        self.last_reset = datetime.now().date()
    
    def can_make_request(self):
        # 检查是否需要重置计数器
        if datetime.now().date() > self.last_reset:
            self.used_today = 0
            self.last_reset = datetime.now().date()
        
        return self.used_today < self.daily_limit
    
    def record_request(self):
        self.used_today += 1
    
    def get_remaining(self):
        return max(0, self.daily_limit - self.used_today)

# 使用示例
quota = QuotaManager(daily_limit=500)
app = Firecrawl(api_key="fc-YOUR-API-KEY")

def safe_scrape_with_quota(url):
    if not quota.can_make_request():
        print(f"已达到每日限额，剩余: {quota.get_remaining()}")
        return None
    
    try:
        result = app.scrape(url)
        quota.record_request()
        return result
    except Exception as e:
        print(f"爬取失败: {e}")
        return None
```

## 故障排除

### 常见问题

#### 1. 认证错误
```
401 Unauthorized
```
**解决方案**: 检查API密钥是否正确，确保以"fc-"开头

#### 2. 速率限制
```
429 Too Many Requests
```
**解决方案**: 实现重试机制，增加请求间隔

#### 3. 超时错误
```
Timeout Error
```
**解决方案**: 增加timeout参数，或者分批处理

#### 4. 内容为空
**可能原因**:
- 页面需要JavaScript渲染
- 页面有反爬虫机制
- URL无效或页面不存在

**解决方案**:
```python
# 增加等待时间
result = app.scrape(
    url="https://example.com",
    wait_for=5000,
    actions=[
        {"type": "wait", "milliseconds": 3000}
    ]
)

# 使用移动端视图
result = app.scrape(
    url="https://example.com",
    mobile=True
)
```

#### 5. JSON提取失败
**解决方案**:
```python
# 使用更详细的提示
result = app.scrape(
    url="https://example.com",
    formats=[{
        "type": "json",
        "prompt": "请仔细分析页面内容，提取所有产品信息，包括名称、价格、描述等。如果某些信息不存在，请设置为null。"
    }]
)

# 或者使用更宽松的schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {"type": ["number", "string", "null"]}
    },
    "additionalProperties": True
}
```

### 调试技巧

#### 1. 启用详细日志
```python
import logging

logging.basicConfig(level=logging.DEBUG)
app = Firecrawl(api_key="fc-YOUR-API-KEY")
```

#### 2. 检查原始响应
```python
result = app.scrape("https://example.com")
print("完整响应:", json.dumps(result, indent=2, ensure_ascii=False))
```

#### 3. 测试不同配置
```python
# 测试基本配置
result1 = app.scrape("https://example.com")

# 测试只提取主要内容
result2 = app.scrape(
    "https://example.com",
    only_main_content=True
)

# 测试包含所有内容
result3 = app.scrape(
    "https://example.com",
    only_main_content=False,
    formats=["markdown", "html"]
)

# 比较结果
print(f"基本: {len(result1['data']['markdown'])} 字符")
print(f"主要内容: {len(result2['data']['markdown'])} 字符")
print(f"完整内容: {len(result3['data']['markdown'])} 字符")
```

## 总结

Firecrawl SDK提供了强大而灵活的网页数据提取能力：

1. **多语言支持** - Python、Node.js、Go、Rust等
2. **丰富的配置选项** - 满足各种爬取需求
3. **框架集成** - 与主流AI框架无缝集成
4. **错误处理** - 完善的错误处理和重试机制
5. **性能优化** - 多种优化策略提升效率

通过合理使用这些SDK和最佳实践，您可以高效地构建强大的网页数据提取应用。