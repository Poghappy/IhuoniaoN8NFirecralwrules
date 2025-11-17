#!/bin/bash
# 启动 Docker MCP Gateway (HTTP/SSE 模式) 供 ChatGPT 使用

PORT=${PORT:-3000}
ENV_FILE="/Users/zhiledeng/Movies/Hawaiihub.net/.env"

echo "🚀 启动 Docker MCP Gateway (HTTP/SSE 模式)"
echo "📡 端口: $PORT"
echo "🔐 环境变量文件: $ENV_FILE"
echo ""

# 检查端口是否被占用
if lsof -ti:$PORT > /dev/null 2>&1; then
    echo "⚠️  警告: 端口 $PORT 已被占用"
    echo "   请先停止占用该端口的进程，或使用其他端口"
    exit 1
fi

# 启动 Gateway
echo "📋 启用的服务器: firecrawl, github, filesystem, time"
echo ""

docker mcp gateway run \
  --port $PORT \
  --transport sse \
  --secrets "$ENV_FILE" \
  --servers firecrawl,github,filesystem,time

echo ""
echo "✅ Gateway 已启动"
echo "📡 SSE 端点: http://localhost:$PORT/sse"
echo ""
echo "📝 下一步:"
echo "   1. 在新终端运行: ngrok http $PORT"
echo "   2. 复制 ngrok 提供的 HTTPS URL"
echo "   3. 在 ChatGPT 中创建连接器，URL: https://your-ngrok-url.ngrok-free.app/sse"
echo "      ⚠️  注意: 端点路径是 /sse，不是 /mcp"

