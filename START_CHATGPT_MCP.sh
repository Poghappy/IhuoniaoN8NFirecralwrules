#!/bin/bash
# ChatGPT MCP Gateway 一键启动脚本

echo "🚀 ChatGPT MCP Gateway 启动脚本"
echo "================================"
echo ""

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ 错误: Docker 未运行"
    echo "   请先启动 Docker Desktop"
    exit 1
fi

# 检查端口
PORT=3000
if lsof -ti:$PORT > /dev/null 2>&1; then
    echo "⚠️  警告: 端口 $PORT 已被占用"
    read -p "是否使用其他端口? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "请输入端口号: " PORT
    else
        echo "请先停止占用端口 $PORT 的进程"
        exit 1
    fi
fi

echo "📋 配置信息:"
echo "  - 端口: $PORT"
echo "  - 端点: http://localhost:$PORT/sse"
echo ""

# 启动 Gateway
cd "$(dirname "$0")/chatgpt-mcp-server"
PORT=$PORT ./start-gateway.sh
