# 🚀 ChatGPT MCP Gateway 快速启动指南

## 3 步完成配置

### 步骤 1: 启动 Docker MCP Gateway

**在终端 1 中运行**:

```bash
cd /Users/zhiledeng/Movies/Hawaiihub.net/chatgpt-mcp-server
./start-gateway.sh
```

**预期输出**:
```
🚀 启动 Docker MCP Gateway (HTTP/SSE 模式)
📡 端口: 3000
🔐 环境变量文件: /Users/zhiledeng/Movies/Hawaiihub.net/.env

📋 启用的服务器: firecrawl, github, filesystem, time

[Gateway 启动日志...]
✅ Gateway 已启动
📡 MCP 端点: http://localhost:3000/mcp
```

**保持此终端运行**，不要关闭。

---

### 步骤 2: 启动 ngrok 隧道

**打开新终端（终端 2）**:

```bash
ngrok http 3000
```

**预期输出**:
```
Session Status                online
Account                       [你的账户]
Version                       3.25.1
Region                        [区域]
Latency                       [延迟]
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:3000
```

**重要**: 复制 `Forwarding` 行的 HTTPS URL（例如：`https://xxxx-xx-xx-xx-xx.ngrok-free.app`）

**保持此终端运行**，不要关闭。

---

### 步骤 3: 在 ChatGPT 中创建连接器

1. **打开 ChatGPT 桌面版**

2. **启用开发者模式**:
   - 点击左下角设置图标 ⚙️
   - 进入 **Settings → Apps & Connectors**
   - 滚动到底部，点击 **Advanced settings**
   - 启用 **Developer mode** 开关

3. **创建连接器**:
   - 在 **Settings → Apps & Connectors** 页面
   - 点击 **Create** 按钮
   - 填写连接器信息：
     - **Connector name**: `HawaiiHub MCP Gateway`
     - **Description**: `本地 MCP 工具网关，提供 Firecrawl 网页抓取、GitHub 操作、文件系统访问等工具`
     - **Connector URL**: `https://xxxx-xx-xx-xx-xx.ngrok-free.app/sse`
       - ⚠️ **重要**: 将 `xxxx-xx-xx-xx-xx.ngrok-free.app` 替换为步骤 2 中复制的 URL
       - ⚠️ **必须**: URL 必须以 `/sse` 结尾（不是 `/mcp`）
   - 点击 **Create**

4. **验证连接**:
   - 如果连接成功，会显示服务器提供的工具列表
   - 如果失败，检查：
     - Gateway 是否正在运行（终端 1）
     - ngrok 是否正常运行（终端 2）
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
     - "列出可用的工具"
     - "使用 Firecrawl 抓取 https://example.com 的内容"
     - "获取当前时间"

---

## 🔧 故障排查

### Gateway 无法启动

**检查**:
```bash
# 检查端口是否被占用
lsof -ti:3000

# 检查 Docker 是否运行
docker info
```

**解决**:
- 如果端口被占用，使用其他端口：`PORT=3001 ./start-gateway.sh`
- 确保 Docker Desktop 正在运行

---

### ngrok 连接失败

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

### ChatGPT 无法连接

**检查清单**:
- [ ] URL 格式是否正确：`https://xxx.ngrok-free.app/mcp`
- [ ] URL 是否以 `/mcp` 结尾
- [ ] Gateway 是否正在运行
- [ ] ngrok 隧道是否正常

**解决**:
- 重新检查 URL
- 查看 Gateway 日志（终端 1）
- 重新创建连接器

---

## 📊 当前配置

- **端口**: 3000
- **传输**: SSE (Server-Sent Events)
- **启用的服务器**: firecrawl, github, filesystem, time
- **环境变量**: `/Users/zhiledeng/Movies/Hawaiihub.net/.env`

---

## ✅ 完成检查清单

- [ ] Gateway 已启动（终端 1）
- [ ] ngrok 已启动（终端 2）
- [ ] 已复制 ngrok HTTPS URL
- [ ] 已在 ChatGPT 中启用开发者模式
- [ ] 已创建连接器
- [ ] 连接器显示工具列表
- [ ] 已测试工具调用

---

**需要帮助？** 查看 `CHATGPT_MCP_SETUP.md` 获取详细文档。

