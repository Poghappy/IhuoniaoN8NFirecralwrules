# Firecrawl MCP Server

> 通过模型上下文协议 (MCP) 使用 Firecrawl 的 API

一个模型上下文协议 (MCP) 服务器实现，集成了 [Firecrawl](https://github.com/mendableai/firecrawl) 以实现网页抓取功能。我们的 MCP 服务器是开源的，可在 [GitHub](https://github.com/mendableai/firecrawl-mcp-server) 上获取。

## 功能特性

* Web 抓取、爬取和发现
* 搜索和内容提取
* 深度研究和批量抓取
* 云和自托管支持
* 流式 HTTP 支持

## 安装

您可以使用我们的远程托管 URL，也可以在本地运行服务器。请从 [https://firecrawl.dev/app/api-keys](https://www.firecrawl.dev/app/api-keys) 获取您的 API 密钥。

### 远程托管 URL

```bash
https://mcp.firecrawl.dev/{FIRECRAWL_API_KEY}/v2/mcp
```

### 使用 npx 运行

```bash
env FIRECRAWL_API_KEY=fc-YOUR_API_KEY npx -y firecrawl-mcp
```

### 手动安装

```bash
npm install -g firecrawl-mcp
```

### 在 Cursor 中运行

#### 自动安装

点击以下按钮一键安装：

<a href="cursor://anysphere.cursor-deeplink/mcp/install?name=firecrawl&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsImZpcmVjcmF3bC1tY3AiXSwiZW52Ijp7IkZJUkVDUkFXTF9BUElfS0VZIjoiWU9VUi1BUEktS0VZIn19">
  <img src="https://cursor.com/deeplink/mcp-install-dark.png" alt="Add Firecrawl MCP server to Cursor" style={{ maxHeight: 32 }} />
</a>

#### 手动安装

**注意：** 需要 Cursor 版本 0.45.6+

有关最新的配置说明，请参阅官方 Cursor 文档：
[Cursor MCP Server 配置指南](https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers)

**在 Cursor v0.48.6 中配置 Firecrawl MCP：**

1. 打开 Cursor 设置
2. 前往 Features > MCP Servers
3. 点击 "+ Add new global MCP server"
4. 输入以下代码：

```json
{
  "mcpServers": {
    "firecrawl-mcp": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "YOUR-API-KEY"
      }
    }
  }
}
```

**在 Cursor v0.45.6 中配置 Firecrawl MCP：**

1. 打开 Cursor 设置
2. 前往 Features > MCP Servers
3. 点击 "+ Add New MCP Server"
4. 输入以下内容：
   * Name: "firecrawl-mcp"（或您喜欢的名称）
   * Type: "command"
   * Command: `env FIRECRAWL_API_KEY=your-api-key npx -y firecrawl-mcp`

> 如果您使用的是 Windows 并遇到问题，请尝试 `cmd /c "set FIRECRAWL_API_KEY=your-api-key && npx -y firecrawl-mcp"`

将 `your-api-key` 替换为您的 Firecrawl API 密钥。如果您还没有，可以创建一个帐户并从 [https://www.firecrawl.dev/app/api-keys](https://www.firecrawl.dev/app/api-keys) 获取。

添加后，刷新 MCP 服务器列表即可查看新工具。Composer Agent 会在适当的情况下自动使用 Firecrawl MCP，但您可以通过描述您的网页抓取需求来明确请求使用 Firecrawl MCP。通过 Command+L (Mac) 访问 Composer，选择提交按钮旁边的 "Agent"，然后输入您的查询。

### 在 Windsurf 中运行

将其添加到您的 `./codeium/windsurf/model_config.json`：

```json
{
  "mcpServers": {
    "mcp-server-firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### 使用流式 HTTP 模式运行

要在本地使用流式 HTTP 传输而不是默认的 stdio 传输运行服务器：

```bash
env HTTP_STREAMABLE_SERVER=true FIRECRAWL_API_KEY=fc-YOUR_API_KEY npx -y firecrawl-mcp
```

使用 URL：[http://localhost:3000/v2/mcp](http://localhost:3000/v2/mcp) 或 [https://mcp.firecrawl.dev/{FIRECRAWL_API_KEY}/v2/mcp](https://mcp.firecrawl.dev/{FIRECRAWL_API_KEY}/v2/mcp)

### 在 VS Code 中运行

#### 一键安装

点击以下安装按钮之一：

[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-NPM-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=firecrawl&inputs=%5B%7B%22type%22%3A%22promptString%22%2C%22id%22%3A%22apiKey%22%2C%22description%22%3A%22Firecrawl%20API%20Key%22%2C%22password%22%3Atrue%7D%5D&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22firecrawl-mcp%22%5D%2C%22env%22%3A%7B%22FIRECRAWL_API_KEY%22%3A%22%24%7Binput%3AapiKey%7D%22%7D%7D)

#### 手动安装

将以下 JSON 块添加到 VS Code 中的用户设置 (JSON) 文件中。您可以按下 `Ctrl + Shift + P` 并输入 `Preferences: Open User Settings (JSON)` 来完成此操作。

```json
{
  "mcp": {
    "inputs": [
      {
        "type": "promptString",
        "id": "apiKey",
        "description": "Firecrawl API Key",
        "password": true
      }
    ],
    "servers": {
      "firecrawl": {
        "command": "npx",
        "args": ["-y", "firecrawl-mcp"],
        "env": {
          "FIRECRAWL_API_KEY": "${input:apiKey}"
        }
      }
    }
  }
}
```

或者，您可以将其添加到工作区中名为 `.vscode/mcp.json` 的文件中。这将允许您与其他人共享配置：

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "apiKey",
      "description": "Firecrawl API Key",
      "password": true
    }
  ],
  "servers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${input:apiKey}"
      }
    }
  }
}
```

**注意：** 某些用户报告在 VS Code 中添加 MCP 服务器时遇到问题，这是由于它使用过时的模式格式验证 JSON 导致的。这会影响包括 Firecrawl 在内的多个 MCP 工具。

**解决方法：** 在 VS Code 中禁用 JSON 验证以允许 MCP 服务器正常加载。

## 配置

### 环境变量

#### 云 API 必需

* `FIRECRAWL_API_KEY`：您的 Firecrawl API 密钥
  * 使用云 API 时必填（默认）
  * 使用带有 `FIRECRAWL_API_URL` 的自托管实例时可选
* `FIRECRAWL_API_URL`（可选）：自托管实例的自定义 API 端点
  * 示例：`https://firecrawl.your-domain.com`
  * 如果未提供，则将使用云 API（需要 API 密钥）

#### 可选配置

##### 重试配置

* `FIRECRAWL_RETRY_MAX_ATTEMPTS`：最大重试次数（默认值：3）
* `FIRECRAWL_RETRY_INITIAL_DELAY`：第一次重试前的初始延迟（以毫秒为单位）（默认值：1000）
* `FIRECRAWL_RETRY_MAX_DELAY`：重试之间的最大延迟时间（以毫秒为单位）（默认值：10000）
* `FIRECRAWL_RETRY_BACKOFF_FACTOR`：指数退避乘数（默认值：2）

##### 信用使用情况监控

* `FIRECRAWL_CREDIT_WARNING_THRESHOLD`：信用使用警告阈值（默认值：1000）
* `FIRECRAWL_CREDIT_CRITICAL_THRESHOLD`：信用使用临界阈值（默认值：100）

### 配置示例

对于具有自定义重试和信用监控的云 API 使用情况：

```bash
# 云 API 必需
export FIRECRAWL_API_KEY=your-api-key

# 可选的重试配置
export FIRECRAWL_RETRY_MAX_ATTEMPTS=5 # 增加最大重试次数
export FIRECRAWL_RETRY_INITIAL_DELAY=2000 # 延迟 2 秒启动
export FIRECRAWL_RETRY_MAX_DELAY=30000 # 最大延迟30秒
export FIRECRAWL_RETRY_BACKOFF_FACTOR=3 # 更积极的退避

# 可选信用监控
export FIRECRAWL_CREDIT_WARNING_THRESHOLD=2000 # 2000 个信用点发出警告
export FIRECRAWL_CREDIT_CRITICAL_THRESHOLD=500 # 500 个信用点达到临界值
```

对于自托管实例：

```bash
# 自托管必需
export FIRECRAWL_API_URL=https://firecrawl.your-domain.com

# 自托管的可选身份验证
export FIRECRAWL_API_KEY=your-api-key # 如果您的实例需要身份验证

# 自定义重试配置
export FIRECRAWL_RETRY_MAX_ATTEMPTS=10
export FIRECRAWL_RETRY_INITIAL_DELAY=500 # 以更快的重试开始
```

### 系统配置

服务器包含几个可配置的参数，可以通过环境变量设置。如果未配置，则使用以下默认值：

```typescript
const config = {
  retry: {
    maxAttempts: 3, // 限速请求的重试次数
    initialDelay: 1000, // 第一次重试前的初始延迟（以毫秒为单位）
    maxDelay: 10000, // 重试之间的最大延迟（以毫秒为单位）
    backoffFactor: 2, // 指数退避乘数
  },
  credit: {
    warningThreshold: 1000, // 当信用使用量达到此水平时发出警告
    criticalThreshold: 100, // 当信用使用量达到此水平时发出严重警报
  },
};
```

这些配置控制：

1. **重试行为**
   * 自动重试因速率限制而失败的请求
   * 使用指数退避算法来避免 API 过载
   * 示例：使用默认设置，将在以下时间尝试重试：
     * 第一次重试：延迟 1 秒
     * 第二次重试：延迟 2 秒
     * 第三次重试：延迟 4 秒（上限为 maxDelay）

2. **信用使用监控**
   * 跟踪云 API 使用情况的 API 信用消耗
   * 在指定阈值时发出警告
   * 有助于防止意外的服务中断
   * 示例：使用默认设置：
     * 剩余 1000 个积分时发出警告
     * 剩余 100 个积分时发出严重警报

### 速率限制和批处理

该服务器利用 Firecrawl 的内置速率限制和批处理功能：

* 使用指数退避算法自动处理速率限制
* 批量操作的高效并行处理
* 智能请求排队和节流
* 瞬时错误自动重试

## 可用工具

### 1. Scrape 工具 (`firecrawl_scrape`)

使用高级选项从单个 URL 抓取内容。

**最佳用于：** 单页内容提取，当您确切知道哪个页面包含信息时。

**不推荐用于：** 多个页面（使用 batch_scrape），未知页面（使用 search），结构化数据（使用 extract）。

**常见错误：** 使用 scrape 处理 URL 列表（应使用 batch_scrape）。如果 batch_scrape 不起作用，只需多次调用 scrape。

**提示示例：** "获取 https://example.com 页面的内容"

**使用示例：**

```json
{
  "name": "firecrawl_scrape",
  "arguments": {
    "url": "https://example.com",
    "formats": ["markdown"],
    "maxAge": 172800000
  }
}
```

**性能：** 添加 maxAge 参数可使用缓存数据实现 500% 更快的抓取。

**返回：** Markdown、HTML 或其他指定格式。

### 2. Batch Scrape 工具 (`firecrawl_batch_scrape`)

高效地抓取多个 URL，内置速率限制和并行处理。

```json
{
  "name": "firecrawl_batch_scrape",
  "arguments": {
    "urls": ["https://example1.com", "https://example2.com"],
    "options": {
      "formats": ["markdown"],
      "onlyMainContent": true
    }
  }
}
```

响应包括用于状态检查的操作 ID：

```json
{
  "content": [
    {
      "type": "text",
      "text": "Batch operation queued with ID: batch_1. Use firecrawl_check_batch_status to check progress."
    }
  ],
  "isError": false
}
```

### 3. 检查批次状态 (`firecrawl_check_batch_status`)

检查批量操作的状态。

```json
{
  "name": "firecrawl_check_batch_status",
  "arguments": {
    "id": "batch_1"
  }
}
```

### 4. Map 工具 (`firecrawl_map`)

映射网站以发现站点上所有已索引的 URL。

**最佳用于：** 在决定要抓取什么之前发现网站上的 URL；查找网站的特定部分。

**不推荐用于：** 当您已经知道需要哪个特定 URL 时（使用 scrape 或 batch_scrape）；当您需要页面内容时（映射后使用 scrape）。

**常见错误：** 使用 crawl 发现 URL 而不是 map。

**提示示例：** "列出 example.com 上的所有 URL"

**使用示例：**

```json
{
  "name": "firecrawl_map",
  "arguments": {
    "url": "https://example.com"
  }
}
```

**返回：** 在站点上找到的 URL 数组。

#### Map 工具选项

* `url`：要映射的网站的基本 URL
* `search`：用于过滤 URL 的可选搜索词
* `sitemap`：控制站点地图使用 - "include"、"skip" 或 "only"
* `includeSubdomains`：是否在映射中包含子域
* `limit`：要返回的最大 URL 数量
* `ignoreQueryParameters`：映射时是否忽略查询参数

### 5. Search 工具 (`firecrawl_search`)

搜索网络并选择性地从搜索结果中提取内容。这是最强大的网络搜索工具，如果可用，您应该始终默认使用此工具进行任何网络搜索需求。

查询还支持搜索运算符，如果需要，您可以使用它们来优化搜索：

| 运算符 | 功能 | 示例 |
|--------|------|------|
| `""` | 非模糊匹配文本字符串 | `"Firecrawl"` |
| `-` | 排除某些关键字或否定其他运算符 | `-bad`, `-site:firecrawl.dev` |
| `site:` | 仅返回来自指定网站的结果 | `site:firecrawl.dev` |
| `inurl:` | 仅返回 URL 中包含单词的结果 | `inurl:firecrawl` |
| `allinurl:` | 仅返回 URL 中包含多个单词的结果 | `allinurl:git firecrawl` |
| `intitle:` | 仅返回标题中包含单词的结果 | `intitle:Firecrawl` |
| `allintitle:` | 仅返回标题中包含多个单词的结果 | `allintitle:firecrawl playground` |
| `related:` | 仅返回与特定域相关的结果 | `related:firecrawl.dev` |
| `imagesize:` | 仅返回具有精确尺寸的图像 | `imagesize:1920x1080` |
| `larger:` | 仅返回大于指定尺寸的图像 | `larger:1920x1080` |

**最佳用于：** 在多个网站上查找特定信息，当您不知道哪个网站有信息时；当您需要查询最相关内容时。

**不推荐用于：** 当您需要搜索文件系统时。当您已经知道要抓取哪个网站时（使用 scrape）；当您需要单个网站的全面覆盖时（使用 map 或 crawl）。

**常见错误：** 使用 crawl 或 map 进行开放式问题（应使用 search）。

**提示示例：** "查找 2023 年发布的关于 AI 的最新研究论文"

**来源：** web、images、news，默认为 web，除非需要 images 或 news。

**抓取选项：** 仅在您认为绝对必要时使用 scrapeOptions。这样做时，默认使用较低的 limit 以避免超时，5 或更低。

**最佳工作流程：** 首先使用 firecrawl_search 不使用 formats 进行搜索，然后在获取结果后，使用 scrape 工具获取您想要抓取的相关页面的内容。

**使用示例（无格式，推荐）：**

```json
{
  "name": "firecrawl_search",
  "arguments": {
    "query": "top AI companies",
    "limit": 5,
    "sources": [
      {
        "type": "web"
      }
    ]
  }
}
```

**使用示例（带格式）：**

```json
{
  "name": "firecrawl_search",
  "arguments": {
    "query": "latest AI research papers 2023",
    "limit": 5,
    "lang": "en",
    "country": "us",
    "sources": [
      {
        "type": "web"
      },
      {
        "type": "images"
      },
      {
        "type": "news"
      }
    ],
    "scrapeOptions": {
      "formats": ["markdown"],
      "onlyMainContent": true
    }
  }
}
```

**返回：** 搜索结果数组（带可选的抓取内容）。

### 6. Crawl 工具 (`firecrawl_crawl`)

在网站上启动爬取作业并提取所有页面的内容。

**最佳用于：** 从多个相关页面提取内容，当您需要全面覆盖时。

**不推荐用于：** 从单个页面提取内容（使用 scrape）；当令牌限制是一个问题时（使用 map + batch_scrape）；当您需要快速结果时（爬取可能很慢）。

**警告：** Crawl 响应可能非常大，可能超过令牌限制。限制爬取深度和页面数量，或使用 map + batch_scrape 以获得更好的控制。

**常见错误：** 将 limit 或 maxDiscoveryDepth 设置得太高（导致令牌溢出）或太低（导致缺少页面）；使用 crawl 处理单个页面（应使用 scrape）。不推荐使用 `/*` 通配符。

**提示示例：** "获取 example.com/blog 的前两个级别的所有博客文章"

**使用示例：**

```json
{
  "name": "firecrawl_crawl",
  "arguments": {
    "url": "https://example.com/blog/*",
    "maxDiscoveryDepth": 5,
    "limit": 20,
    "allowExternalLinks": false,
    "deduplicateSimilarURLs": true,
    "sitemap": "include"
  }
}
```

**返回：** 用于状态检查的操作 ID；使用 firecrawl_check_crawl_status 检查进度。

### 7. 检查爬取状态 (`firecrawl_check_crawl_status`)

检查爬取作业的状态。

**使用示例：**

```json
{
  "name": "firecrawl_check_crawl_status",
  "arguments": {
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**返回：** 爬取作业的状态和进度，包括结果（如果可用）。

### 8. Extract 工具 (`firecrawl_extract`)

使用 LLM 功能从网页中提取结构化信息。支持云端 AI 和自托管 LLM 提取。

**最佳用于：** 从网页中提取特定结构化数据，如价格、名称、详细信息。

**不推荐用于：** 当您需要页面的完整内容时（使用 scrape）；当您不寻找特定结构化数据时。

**参数：**
* `urls`：要从中提取信息的 URL 数组
* `prompt`：LLM 提取的自定义提示
* `schema`：用于结构化数据提取的 JSON 模式
* `allowExternalLinks`：允许从外部链接提取
* `enableWebSearch`：启用网络搜索以获取更多上下文
* `includeSubdomains`：在提取中包含子域

**提示示例：** "从这些产品页面中提取产品名称、价格和描述"

**使用示例：**

```json
{
  "name": "firecrawl_extract",
  "arguments": {
    "urls": ["https://example.com/page1", "https://example.com/page2"],
    "prompt": "Extract product information including name, price, and description",
    "schema": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "price": {
          "type": "number"
        },
        "description": {
          "type": "string"
        }
      },
      "required": ["name", "price"]
    },
    "allowExternalLinks": false,
    "enableWebSearch": false,
    "includeSubdomains": false
  }
}
```

**返回：** 根据您的模式定义的提取结构化数据。

使用自托管实例时，提取将使用您配置的 LLM。对于云 API，它使用 Firecrawl 的托管 LLM 服务。

## 日志系统

服务器包括全面的日志记录：

* 运营状态及进度
* 性能指标
* 信用使用情况监控
* 速率限制跟踪
* 错误条件

日志消息示例：

```
[INFO] Firecrawl MCP Server initialized successfully
[INFO] Starting scrape for URL: https://example.com
[INFO] Batch operation queued with ID: batch_1
[WARNING] Credit usage has reached warning threshold
[ERROR] Rate limit exceeded, retrying in 2s...
```

## 错误处理

服务器提供了强大的错误处理：

* 瞬时错误自动重试
* 带退避的速率限制处理
* 详细的错误信息
* 信用使用警告
* 网络弹性

错误响应示例：

```json
{
  "content": [
    {
      "type": "text",
      "text": "Error: Rate limit exceeded. Retrying in 2 seconds..."
    }
  ],
  "isError": true
}
```

## 开发

```bash
# 安装依赖项
npm install

# 构建
npm run build

# 运行测试
npm test
```

### 贡献

1. Fork 仓库
2. 创建您的功能分支
3. 运行测试：`npm test`
4. 提交拉取请求

### 感谢贡献者

感谢 [@vrknetha](https://github.com/vrknetha)、[@cawstudios](https://caw.tech) 的初步实现！

感谢 MCP.so 和 Klavis AI 提供托管，以及 [@gstarwd](https://github.com/gstarwd)、[@xiangkaiz](https://github.com/xiangkaiz) 和 [@zihaolin96](https://github.com/zihaolin96) 集成我们的服务器。

## 许可证

MIT 许可证 - 详情请参阅许可证文件

---

**参考文档：** [Firecrawl MCP Server 官方文档](https://docs.firecrawl.dev/mcp-server)

**最后更新：** 2025-11-17
