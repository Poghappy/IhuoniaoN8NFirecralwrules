# Firecrawl MCP 服务器

> 通过模型上下文协议使用 Firecrawl 的 API

一个模型上下文协议 (MCP) 服务器实现，集成了 [Firecrawl](https://github.com/mendableai/firecrawl) 以实现网页抓取功能。我们的 MCP 服务器是开源的，可在 [GitHub](https://github.com/mendableai/firecrawl-mcp-server) 上获取。

＃＃ 特征

* Web 抓取、爬取和发现
* 搜索和内容提取
* 深入研究和批量抓取
* 云和自托管支持
* SSE 支持

＃＃ 安装

您可以使用我们的远程托管 URL，也可以在本地运行服务器。请从 [https://firecrawl.dev/app/api-keys](https://www.firecrawl.dev/app/api-keys) 获取您的 API 密钥。

### 远程托管 URL

```bash
fc-31ebbe4647b84fdc975318d372eebea8https://mcp.firecrawl.dev/{FIRECRAWL_API_KEY}/v2/sse
```

### 使用 npx 运行

```bash
env FIRECRAWL_API_KEY=fc-YOUR_API_KEY npx -y firecrawl-mcp
```

### 手动安装

```bash
npm install -g firecrawl-mcp
```

> 在 [MCP.so 的游乐场](https://mcp.so/playground?server=firecrawl-mcp-server) 或 [Klavis AI](https://www.klavis.ai/mcp-servers) 上使用我们的 MCP 服务器进行游戏。

### 在光标上运行

<a href="cursor://anysphere.cursor-deeplink/mcp/install?name=firecrawl&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsImZpcmVjcmF3bC1tY3AiXSwiZW52Ijp7IkZJUkVDUkFXTF9BUElfS0VZIjoiWU9VUi1BUEktS0VZIn19">
  <img src="https://cursor.com/deeplink/mcp-install-dark.png" alt="将 Firecrawl MCP 服务器添加到 Cursor" style={{ maxHeight: 32 }} />
</a>

#### 手动安装

配置光标🖥️
注意：需要 Cursor 版本 0.45.6+
有关最新的配置说明，请参阅有关配置 MCP 服务器的官方 Cursor 文档：
Cursor MCP 服务器配置指南

在 Cursor **v0.48.6** 中配置 Firecrawl MCP

1. 打开游标设置
2. 前往“功能”>“MCP 服务器”
3. 点击“+ 添加新的全局 MCP 服务器”
   4.输入以下代码：
   ```json
   {
     "mcp服务器": {
       “firecrawl-mcp”：{
         “命令”：“npx”，
         “args”：[“-y”，“firecrawl-mcp”]，
         “环境”：{
           "FIRECRAWL_API_KEY": "您的 API 密钥"
         }
       }
     }
   }
   ```

在 Cursor **v0.45.6** 中配置 Firecrawl MCP

1. 打开游标设置
2. 前往“功能”>“MCP 服务器”
3. 点击“+ 添加新的 MCP 服务器”
4. 输入以下内容：
   * 名称：“firecrawl-mcp”（或您喜欢的名称）
   * 类型：“命令”
   * 命令：`env FIRECRAWL_API_KEY=your-api-key npx -y firecrawl-mcp`

> 如果您使用的是 Windows 并遇到问题，请尝试 `cmd /c "set FIRECRAWL_API_KEY=your-api-key && npx -y firecrawl-mcp"`

将 `your-api-key` 替换为您的 Firecrawl API 密钥。如果您还没有，可以创建一个帐户并从 [https://www.firecrawl.dev/app/api-keys](https://www.firecrawl.dev/app/api-keys) 获取。

添加后，刷新 MCP 服务器列表即可查看新工具。Composer 代理会在适当的情况下自动使用 Firecrawl MCP，但您可以通过描述您的网页抓取需求来明确请求使用 Firecrawl MCP。通过 Command+L (Mac) 访问 Composer，选择提交按钮旁边的“代理”，然后输入您的查询。

### 在风帆冲浪中奔跑

将其添加到您的 `./codeium/windsurf/model_config.json`：

```json
{
  "mcp服务器": {
    “mcp-服务器-firecrawl”：{
      “命令”：“npx”，
      “args”：[“-y”，“firecrawl-mcp”]，
      “环境”：{
        "FIRECRAWL_API_KEY": "您的 API 密钥"
      }
    }
  }
}
```

### 使用 SSE 模式运行

要在本地使用服务器发送事件 (SSE) 而不是默认的 stdio 传输来运行服务器：

```bash
env SSE_LOCAL=true FIRECRAWL_API_KEY=fc-YOUR_API_KEY npx -y firecrawl-mcp
```

使用以下网址：[http://localhost:3000/v2/sse](http://localhost:3000/v2/sse) 或 [https://mcp.firecrawl.dev/\{FIRECRAWL\_API\_KEY}/v2/sse](https://mcp.firecrawl.dev/\{FIRECRAWL_API_KEY}/v2/sse)

### 通过 Smithery 安装（旧版）

要通过 [Smithery](https://smithery.ai/server/@mendableai/mcp-server-firecrawl) 自动为 Claude Desktop 安装 Firecrawl：

```bash
npx -y @smithery/cli 安装 @mendableai/mcp-server-firecrawl --client claude
```

### 在 VS Code 上运行

对于一键安装，请单击下面的安装按钮之一...

[![在 VS Code 中使用 NPX 安装](https://img.shields.io/badge/VS_Code-NPM-0098FF?style=flat-square\&logo=visualstudiocode\&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=firecrawl\&inputs=%5B%7B%22type%22%3A%22promptString%22%2C%22id%22%3A%22apiKey%22 %2C%22描述%22%3A%22Firecrawl%20API%20Key%22%2C%22密码%22%3Atrue%7D%5D\&config=%7B%22命令%22%3A%22npx%22%2C%22a rgs%22%3A%5B%22-y%22%2C%22firecrawl-mcp%22%5D%2C%22env%22%3A%7B%22FIRECRAWL_API_KEY%22%3A%22%24%7Binput%3AapiKey%7D%22%7D%7D) [![在 VS Code 中使用 NPX 安装Insiders](https://img.shields.io/badge/VS_Code_Insiders-NPM-24bfa5?style=flat-square\&logo=visualstudiocode\&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=firecrawl\&inputs=%5B%7B%22type%22%3A%22promptString%22%2C%22id%22%3A%22apiKey%22%2 C%22描述%22%3A%22Firecrawl%20API%20Key%22%2C%22密码%22%3Atrue%7D%5D\&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A% 5B%22-y%22%2C%22firecrawl-mcp%22%5D%2C%22env%22%3A%7B%22FIRECRAWL_API_KEY%22%3A%22%24%7Binput%3AapiKey%7D%22%7D%7D\&quality=内部人员）

如需手动安装，请将以下 JSON 块添加到 VS Code 中的“用户设置 (JSON)”文件中。您可以按下“Ctrl + Shift + P”并输入“Preferences: Open User Settings (JSON)”来完成此操作。

```json
{
  "mcp": {
    "输入": [
      {
        “type”：“promptString”，
        "id": "apiKey",
        “description”：“Firecrawl API 密钥”，
        “密码”：true
      }
    ]，
    “服务器”：{
      “firecrawl”：{
        “命令”：“npx”，
        “args”：[“-y”，“firecrawl-mcp”]，
        “环境”：{
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
  "输入": [
    {
      “type”：“promptString”，
      "id": "apiKey",
      “description”：“Firecrawl API 密钥”，
      “密码”：true
    }
  ]，
  “服务器”：{
    “firecrawl”：{
      “命令”：“npx”，
      “args”：[“-y”，“firecrawl-mcp”]，
      “环境”：{
        "FIRECRAWL_API_KEY": "${input:apiKey}"
      }
    }
  }
}
```

### 在 Claude 桌面上运行

将其添加到 Claude 配置文件中：

```json
{
  "mcp服务器": {
    “firecrawl”：{
      “url”：“https://mcp.firecrawl.dev/{YOUR_API_KEY}/v2/sse”
    }
  }
}
```

### 在 Claude 代码上运行

使用 Claude Code CLI 添加 Firecrawl MCP 服务器：

```bash
claude mcp 添加 firecrawl -e FIRECRAWL_API_KEY=你的 API 密钥 -- npx -y firecrawl-mcp
```

＃＃ 配置

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
导出 FIRECRAWL_API_KEY=你的 API 密钥

# 可选的重试配置
export FIRECRAWL_RETRY_MAX_ATTEMPTS=5 # 增加最大重试次数
export FIRECRAWL_RETRY_INITIAL_DELAY=2000 # 延迟 2 秒启动
export FIRECRAWL_RETRY_MAX_DELAY=30000 # 最大延迟30秒
导出 FIRECRAWL_RETRY_BACKOFF_FACTOR=3 # 更积极的退避

# 可选信用监控
导出 FIRECRAWL_CREDIT_WARNING_THRESHOLD=2000 # 2000 个信用点发出警告
导出 FIRECRAWL_CREDIT_CRITICAL_THRESHOLD=500 # 500 个信用点达到临界值
```

对于自托管实例：

```bash
# 自托管必需
导出 FIRECRAWL_API_URL=https://firecrawl.your-domain.com

# 自托管的可选身份验证
export FIRECRAWL_API_KEY=your-api-key # 如果您的实例需要身份验证

# 自定义重试配置
导出 FIRECRAWL_RETRY_MAX_ATTEMPTS=10
export FIRECRAWL_RETRY_INITIAL_DELAY=500 # 以更快的重试开始
```

### 使用 Claude Desktop 进行自定义配置

将其添加到您的 `claude_desktop_config.json`：

```json
{
  "mcp服务器": {
    “mcp-服务器-firecrawl”：{
      “命令”：“npx”，
      “args”：[“-y”，“firecrawl-mcp”]，
      “环境”：{
        "FIRECRAWL_API_KEY": "此处输入您的 API 密钥",

        "FIRECRAWL_RETRY_MAX_ATTEMPTS": "5",
        "FIRECRAWL_RETRY_INITIAL_DELAY": "2000",
        "FIRECRAWL_RETRY_MAX_DELAY": "30000",
        "FIRECRAWL_RETRY_BACKOFF_FACTOR": "3",

        "FIRECRAWL_CREDIT_WARNING_THRESHOLD": "2000",
        "FIRECRAWL_CREDIT_CRITICAL_THRESHOLD": "500"
      }
    }
  }
}
```

### 系统配置

服务器包含几个可配置的参数，可以通过环境变量设置。如果未配置，则使用以下默认值：

```typescript
const 配置 = {
  重试：{
    maxAttempts: 3, // 限速请求的重试次数
    initialDelay: 1000, // 第一次重试前的初始延迟（以毫秒为单位）
    maxDelay: 10000, // 重试之间的最大延迟（以毫秒为单位）
    backoffFactor: 2, // 指数退避乘数
  }，
  信用： {
    warningThreshold: 1000, // 当信用使用量达到此水平时发出警告
    criticalThreshold: 100, // 当信用使用量达到此水平时发出严重警报
  }，
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

可用工具

### 1. 抓取工具 (`firecrawl_scrape`)

使用高级选项从单个 URL 抓取内容。

```json
{
  “名称”：“firecrawl_scrape”，
  “参数”：{
    "url": "https://example.com",
    "格式": ["markdown"],
    "onlyMainContent": true,
    “等待”：1000，
    “超时”：30000，
    “移动”：错误，
    "includeTags": ["文章", "主要"],
    “excludeTags”：[“nav”，“页脚”]，
    “skipTlsVerification”：false
  }
}
```

### 2. 批量抓取工具 (`firecrawl_batch_scrape`)

通过内置速率限制和并行处理有效地抓取多个 URL。

```json
{
  “名称”：“firecrawl_batch_scrape”，
  “参数”：{
    "urls": ["https://example1.com", "https://example2.com"],
    “选项”： {
      "格式": ["markdown"],
      "onlyMainContent": true
    }
  }
}
```

响应包括用于状态检查的操作ID：

```json
{
  “内容”： [
    {
      “类型”：“文本”，
      "text": "批量操作已排队，ID：batch_1。使用 firecrawl_check_batch_status 检查进度。"
    }
  ]，
  “isError”：false
}
```

### 3. 检查批次状态（`firecrawl_check_batch_status`）

检查批量操作的状态。

```json
{
  “名称”：“firecrawl_check_batch_status”，
  “参数”：{
    “id”：“batch_1”
  }
}
```

### 4. 搜索工具（`firecrawl_search`）

搜索网络并选择性地从搜索结果中提取内容。

```json
{
  “名称”：“firecrawl_search”，
  “参数”：{
    "query": "您的搜索查询",
    “限制”：5，
    "lang": "en",
    “国家”：“我们”，
    “scrapeOptions”：{
      "格式": ["markdown"],
      "onlyMainContent": true
    }
  }
}
```

### 5. 爬网工具 (`firecrawl_crawl`)

使用高级选项启动异步爬网。

```json
{
  “名称”：“firecrawl_crawl”，
  “参数”：{
    "url": "https://example.com",
    “最大深度”：2，
    “限制”：100，
    “允许外部链接”：false，
    "deduplicate SimilarURLs": true
  }
}
```

### 6. 提取工具 (`firecrawl_extract`)

使用 LLM 功能从网页中提取结构化信息。支持云端 AI 和自托管 LLM 提取。

```json
{
  “名称”：“firecrawl_extract”，
  “参数”：{
    "urls": ["https://example.com/page1", "https://example.com/page2"],
    "prompt": "提取产品信息，包括名称、价格和描述",
    "systemPrompt": "您是提取产品信息的得力助手",
    “模式”：{
      “类型”：“对象”，
      “特性”： {
        “名称”：{“类型”：“字符串”}，
        "价格": { "类型": "数字" },
        “描述”：{“类型”：“字符串”}
      }，
      "required": ["名称", "价格"]
    }，
    “允许外部链接”：false，
    "enableWebSearch": false,
    “includeSubdomains”：false
  }
}
```

响应示例：

```json
{
  “内容”： [
    {
      “类型”：“文本”，
      “文本”： {
        “名称”：“示例产品”，
        “价格”：99.99，
        “description”：“这是产品描述的示例”
      }
    }
  ]，
  “isError”：false
}
```

#### 提取工具选项：

* `urls`：用于从中提取信息的 URL 数组
* `prompt`：LLM 提取的自定义提示
* `systemPrompt`：指导 LLM 的系统提示
  *`schema`：用于结构化数据提取的 JSON 模式
* `allowExternalLinks`: 允许从外部链接提取
* `enableWebSearch`：启用网页搜索以获取更多上下文
* `includeSubdomains`: 在提取中包含子域名

使用自托管实例时，提取将使用您配置的 LLM。对于云 API，它使用 Firecrawl 的托管 LLM 服务。

### 7. 深度研究工具 (firecrawl_deep_research)

使用智能爬取、搜索和 LLM 分析对查询进行深度网络研究。

```json
{
  “名称”：“firecrawl_deep_research”，
  “参数”：{
    “查询”：“碳捕获技术如何工作？”，
    “最大深度”：3，
    “时间限制”：120，
    “maxUrls”：50
  }
}
```

参数：

* 查询（字符串，必需）：要探索的研究问题或主题。
* maxDepth（数字，可选）：爬行/搜索的最大递归深度（默认值：3）。
* timeLimit（数字，可选）：研究会话的时间限制（以秒为单位）（默认值：120）。
* maxUrls（数字，可选）：要分析的最大 URL 数量（默认值：50）。

返回：

* 法学硕士根据研究生成的最终分析结果。(data.finalAnalysis)
* 还可能包括研究过程中使用的结构化活动和来源。

### 8. 生成LLMs.txt工具（firecrawl_generate_llmstxt）

为给定域生成标准化的 llms.txt 文件（以及可选的 llms-full.txt 文件）。该文件定义了大型语言模型应如何与网站交互。

```json
{
  “名称”：“firecrawl_generate_llmstxt”，
  “参数”：{
    "url": "https://example.com",
    “maxUrls”：20，
    “显示全文”：真
  }
}
```

参数：

* url（字符串，必需）：要分析的网站的基本 URL。
* maxUrls（数字，可选）：要包含的最大 URL 数量（默认值：10）。
* showFullText（布尔值，可选）：是否在响应中包含 llms-full.txt 内容。

返回：

* 生成 llms.txt 文件内容和可选的 llms-full.txt（data.llmstxt 和/或 data.llmsfulltxt）

## 日志系统

该服务器包括全面的日志记录：

* 运营状态及进度
* 性能指标
* 信用使用情况监控
* 速率限制跟踪
* 错误条件

日志消息示例：

```
[INFO] Firecrawl MCP 服务器初始化成功
[信息] 开始抓取 URL：https://example.com
[INFO] 批量操作已排队，ID：batch_1
[警告] 信用使用量已达到警告阈值
[错误] 超出速率限制，2 秒后重试...
```

错误处理

服务器提供了强大的错误处理：

* 瞬时错误自动重试
* 带退避的速率限制处理
* 详细的错误信息
* 信用使用警告
* 网络弹性

错误响应示例：

```json
{
  “内容”： [
    {
      “类型”：“文本”，
      “text”：“错误：超出速率限制。2 秒后重试...”
    }
  ]，
  “isError”：true
}
```

＃＃ 发展

```bash
# 安装依赖项
npm 安装

＃ 建造
npm 运行构建

# 运行测试
npm 测试
```

### 贡献

1. fork 仓库
2. 创建你的功能分支
3. 运行测试：`npm test`
4. 提交拉取请求

### 感谢贡献者

感谢 [@vrknetha](https://github.com/vrknetha)、[@cawstudios](https://caw.tech) 的初步实现！

感谢 MCP.so 和 Klavis AI 提供托管，以及 [@gstarwd](https://github.com/gstarwd)、[@xiangkaiz](https://github.com/xiangkaiz) 和 [@zihaolin96](https://github.com/zihaolin96) 集成我们的服务器。

＃＃ 执照

MIT 许可证 - 详情请参阅许可证文件
