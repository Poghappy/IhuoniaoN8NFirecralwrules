# ChatGPT MCP 服务器配置指南

## 🎯 推荐方案：使用 Docker MCP Gateway

Docker MCP Gateway 已经支持 HTTP/SSE 传输，这是连接 ChatGPT 最简单的方法。

### 步骤 1: 启动 Docker MCP Gateway (HTTP 模式)

```bash
# 启动 Gateway，监听在端口 3000
docker mcp gateway run \
  --port 3000 \
  --transport sse \
  --secrets /Users/zhiledeng/Movies/Hawaiihub.net/.env \
  --servers firecrawl,github,filesystem
```

### 步骤 2: 使用 ngrok 暴露

```bash
# 在另一个终端
ngrok http 3000
```

### 步骤 3: 在 ChatGPT 中配置

1. 打开 ChatGPT 桌面版
2. Settings → Apps & Connectors → Advanced settings
3. 启用 **Developer mode**
4. Settings → Connectors → Create
5. 填写信息：
   - **Connector name**: `HawaiiHub MCP Gateway`
   - **Description**: `本地 MCP 工具网关，提供 Firecrawl、GitHub 等工具`
   - **Connector URL**: `https://your-ngrok-url.ngrok.app/mcp`（使用 ngrok 提供的 URL）
6. 点击 **Create**

---

## 🔧 方案 2: 使用 Node.js 服务器（需要修复）

如果你需要使用 Node.js 服务器，需要修复 `server.js` 中的传输问题。

### 当前问题

`StdioServerTransport` 需要正确的 stdin/stdout 管道，但当前的实现方式不正确。

### 解决方案

使用 FastMCP 或直接实现 HTTP SSE 传输。参考 `server-fastmcp.js`（需要进一步完善）。

---

## 📝 快速测试

### 测试 Docker MCP Gateway

```bash
# 1. 启动 Gateway
docker mcp gateway run --port 3000 --transport sse --secrets /Users/zhiledeng/Movies/Hawaiihub.net/.env

# 2. 测试端点
curl http://localhost:3000/mcp
```

### 测试 ngrok

```bash
# 启动 ngrok
ngrok http 3000

# 从输出中复制 HTTPS URL
# 例如: https://abc123.ngrok-free.app
```

---

## 🚀 推荐执行步骤

1. **使用 Docker MCP Gateway**（最简单）
   ```bash
   docker mcp gateway run --port 3000 --transport sse --secrets /Users/zhiledeng/Movies/Hawaiihub.net/.env
   ```

2. **启动 ngrok**
   ```bash
   ngrok http 3000
   ```

3. **在 ChatGPT 中配置连接器**

---

## 📚 参考文档

- [OpenAI Apps SDK - Connect from ChatGPT](https://developers.openai.com/apps-sdk/deploy/connect-chatgpt/)
- [FastMCP Documentation](https://fastmcp.wiki/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

