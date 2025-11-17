# ChatGPT MCP 连接配置完整指南

**更新时间**: 2025-11-17
**状态**: 准备就绪

---

## 🎯 推荐方案：使用 Docker MCP Gateway

这是最简单、最可靠的方法，因为 Docker MCP Gateway 已经支持 HTTP/SSE 传输。

---

## 📋 快速开始（3 步）

### 步骤 1: 启动 Docker MCP Gateway

```bash
cd /Users/zhiledeng/Movies/Hawaiihub.net/chatgpt-mcp-server
./start-gateway.sh
```

或者手动启动：

```bash
docker mcp gateway run \
  --port 3000 \
  --transport sse \
  --secrets /Users/zhiledeng/Movies/Hawaiihub.net/.env \
  --servers firecrawl,github,filesystem,time
```

**说明**:
- `--port 3000`: 监听端口 3000
- `--transport sse`: 使用 Server-Sent Events 传输（ChatGPT 需要）
- `--secrets`: 从 `.env` 文件读取 API 密钥
- `--servers`: 启用的 MCP 服务器列表

---

### 步骤 2: 使用 ngrok 暴露为 HTTPS

**在新终端中运行**:

```bash
ngrok http 3000
```

**复制 HTTPS URL**:
- 从 ngrok 输出中复制 `Forwarding` 行的 HTTPS URL
- 例如: `https://abc123-xx-xx-xx-xx.ngrok-free.app`

---

### 步骤 3: 在 ChatGPT 中配置连接器

1. **启用开发者模式**:
   - 打开 ChatGPT 桌面版
   - 点击左下角设置图标 ⚙️
   - 进入 **Settings → Apps & Connectors**
   - 滚动到底部，点击 **Advanced settings**
   - 启用 **Developer mode** 开关

2. **创建连接器**:
   - 在 **Settings → Apps & Connectors** 页面
   - 点击 **Create** 按钮
   - 填写连接器信息：
     - **Connector name**: `HawaiiHub MCP Gateway`
     - **Description**: `本地 MCP 工具网关，提供 Firecrawl 网页抓取、GitHub 操作、文件系统访问等工具`
     - **Connector URL**: `https://your-ngrok-url.ngrok-free.app/sse`
       - 将 `your-ngrok-url.ngrok-free.app` 替换为步骤 2 中复制的 URL
       - ⚠️ **重要**: 端点路径是 `/sse`，不是 `/mcp`
   - 点击 **Create**

3. **验证连接**:
   - 如果连接成功，会显示服务器提供的工具列表
   - 如果失败，检查：
     - Gateway 是否正在运行
     - ngrok 是否正常运行
     - URL 是否正确（必须以 `/mcp` 结尾）

---

## 🧪 测试工具调用

1. **打开新对话**:
   - 在 ChatGPT 中创建新的对话

2. **添加连接器**:
   - 点击消息输入框附近的 **+** 按钮
   - 点击 **More**
   - 选择你创建的连接器（HawaiiHub MCP Gateway）

3. **测试工具**:
   - 尝试以下提示：
     - "使用 Firecrawl 抓取 https://example.com 的内容"
     - "列出可用的工具"
     - "获取当前时间"

---

## 🔧 故障排查

### 问题 1: Gateway 无法启动

**检查**:
```bash
# 检查端口是否被占用
lsof -ti:3000

# 检查 Docker 是否运行
docker info
```

**解决**:
- 如果端口被占用，使用其他端口：`--port 3001`
- 确保 Docker Desktop 正在运行

---

### 问题 2: ngrok 连接失败

**检查**:
```bash
# 测试本地服务器
curl http://localhost:3000/mcp

# 检查 ngrok 状态
curl http://localhost:4040/api/tunnels
```

**解决**:
- 确保 Gateway 正在运行
- 检查防火墙设置
- 尝试重启 ngrok

---

### 问题 3: ChatGPT 无法连接

**检查**:
- URL 格式是否正确：`https://xxx.ngrok-free.app/mcp`
- Gateway 日志是否有错误
- ngrok 隧道是否正常

**解决**:
- 确保 URL 以 `/mcp` 结尾
- 检查 Gateway 日志：查看终端输出
- 重新创建连接器

---

## 📊 当前配置状态

### ✅ 已配置的 MCP 服务器

- **firecrawl**: 网页抓取和内容提取
- **github**: GitHub 仓库操作
- **filesystem**: 文件系统访问
- **time**: 时间相关工具

### 🔐 环境变量

从 `/Users/zhiledeng/Movies/Hawaiihub.net/.env` 读取：
- `FIRECRAWL_API_KEY`
- `GITHUB_TOKEN`
- 其他 API 密钥

---

## 🚀 启动脚本

已创建启动脚本：`chatgpt-mcp-server/start-gateway.sh`

**使用方法**:
```bash
cd chatgpt-mcp-server
./start-gateway.sh
```

**自定义端口**:
```bash
PORT=3001 ./start-gateway.sh
```

---

## 📝 下一步

1. ✅ 启动 Gateway
2. ✅ 启动 ngrok
3. ✅ 在 ChatGPT 中配置连接器
4. ✅ 测试工具调用

---

## 🔗 相关文档

- [Docker MCP Gateway 文档](https://docs.docker.com/desktop/extensions-sdk/mcp/)
- [OpenAI Apps SDK 文档](https://developers.openai.com/apps-sdk/deploy/connect-chatgpt/)
- [MCP Protocol 规范](https://modelcontextprotocol.io/)

---

**需要帮助？** 查看 `chatgpt-mcp-server/SETUP_GUIDE.md` 获取更多信息。

