# ChatGPT MCP Gateway Server

将本地 MCP 工具暴露为 HTTP 端点，供 ChatGPT 桌面版连接使用。

## 📋 功能特性

- ✅ 将本地 MCP 服务器暴露为 HTTP 端点
- ✅ 支持多个 ChatGPT 会话
- ✅ 自动管理 MCP 服务器连接
- ✅ 支持通过 ngrok 或 cloudflared 暴露为 HTTPS

## 🚀 快速开始

### 1. 安装依赖

```bash
cd chatgpt-mcp-server
npm install
```

### 2. 配置环境变量（可选）

创建 `.env` 文件：

```bash
PORT=3000
MCP_SERVER_COMMAND=npx
MCP_SERVER_ARGS=-y,firecrawl-mcp
FIRECRAWL_API_KEY=your-api-key-here
```

### 3. 启动服务器

```bash
npm start
```

服务器将在 `http://localhost:3000` 启动，MCP 端点为 `/mcp`。

### 4. 暴露为 HTTPS

#### 使用 ngrok

```bash
ngrok http 3000
```

#### 使用 cloudflared

```bash
cloudflared tunnel --url http://localhost:3000
```

### 5. 在 ChatGPT 中配置

1. 打开 ChatGPT 桌面版
2. 进入 **Settings → Apps & Connectors → Advanced settings**
3. 启用 **Developer mode**
4. 点击 **Settings → Connectors → Create**
5. 填写连接器信息：
   - **Connector name**: `HawaiiHub MCP Gateway`
   - **Description**: `本地 MCP 工具网关，提供 Firecrawl、GitHub 等工具`
   - **Connector URL**: `https://your-ngrok-url.ngrok.app/mcp`
6. 点击 **Create**

## 🔧 配置说明

### 支持的 MCP 服务器

可以通过环境变量配置要使用的 MCP 服务器：

```bash
# 使用 Firecrawl
MCP_SERVER_COMMAND=npx
MCP_SERVER_ARGS=-y,firecrawl-mcp

# 使用 GitHub
MCP_SERVER_COMMAND=npx
MCP_SERVER_ARGS=-y,@modelcontextprotocol/server-github

# 使用 Filesystem
MCP_SERVER_COMMAND=npx
MCP_SERVER_ARGS=-y,@modelcontextprotocol/server-filesystem,--root,/path/to/directory
```

### 多服务器支持

当前版本支持单个 MCP 服务器。如需支持多个服务器，需要修改服务器代码以路由到不同的 MCP 实例。

## 📝 使用示例

### 测试服务器

```bash
# 检查服务器状态
curl http://localhost:3000/mcp

# 发送 MCP 请求
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: test-session" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

## 🔍 故障排查

### 问题：无法连接到服务器

1. 检查服务器是否运行：`curl http://localhost:3000/mcp`
2. 检查防火墙设置
3. 确保 ngrok/cloudflared 正常运行

### 问题：MCP 工具不可用

1. 检查环境变量是否正确设置
2. 查看服务器日志
3. 验证 MCP 服务器命令是否正确

### 问题：ChatGPT 无法连接

1. 确保 connector URL 使用 HTTPS
2. 检查 ngrok/cloudflared 隧道是否正常
3. 验证 URL 格式：`https://your-domain.com/mcp`

## 📚 参考文档

- [OpenAI Apps SDK - Connect from ChatGPT](https://developers.openai.com/apps-sdk/deploy/connect-chatgpt/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/typescript-sdk)

## 🛠️ 开发

### 开发模式（自动重启）

```bash
npm run dev
```

### 日志

服务器会输出详细的日志信息，包括：
- 连接创建和关闭
- MCP 请求和响应
- 错误信息

## 📄 许可证

MIT

