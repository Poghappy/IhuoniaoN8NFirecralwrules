#!/bin/bash
# ChatGPT MCP 服务状态检查脚本

echo "🔍 ChatGPT MCP 服务状态检查"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 检查 Gateway
echo "📡 Docker MCP Gateway:"
if lsof -ti:3000 > /dev/null 2>&1; then
    PID=$(lsof -ti:3000 | head -1)
    echo "  ✅ 运行中 (PID: $PID)"
    echo "  📍 端点: http://localhost:3000/sse"
    
    # 检查工具数量
    TOOLS=$(cat /tmp/gateway.log 2>/dev/null | grep -oP "\d+ tools listed" | head -1 || echo "未知")
    echo "  🔧 工具: $TOOLS"
else
    echo "  ❌ 未运行"
    echo "  💡 启动: cd chatgpt-mcp-server && ./start-gateway.sh"
fi
echo ""

# 检查 ngrok
echo "🌐 ngrok 隧道:"
if ps aux | grep -E "ngrok.*3000" | grep -v grep > /dev/null; then
    PID=$(ps aux | grep -E "ngrok.*3000" | grep -v grep | awk '{print $2}' | head -1)
    echo "  ✅ 运行中 (PID: $PID)"
    
    # 获取 URL
    URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null)
    if [ -n "$URL" ]; then
        echo "  🌍 公网 URL: $URL"
        echo "  🔗 连接器 URL: ${URL}/sse"
    else
        echo "  ⏳ 等待 URL 生成..."
    fi
else
    echo "  ❌ 未运行"
    echo "  💡 启动: ngrok http 3000"
fi
echo ""

# 配置信息
echo "📋 ChatGPT 配置信息:"
if [ -f /tmp/ngrok_url.txt ]; then
    URL=$(cat /tmp/ngrok_url.txt)
    echo "  连接器名称: HawaiiHub MCP Gateway"
    echo "  连接器 URL: ${URL}/sse"
    echo "  描述: 本地 MCP 工具网关"
else
    echo "  ⚠️  未找到保存的 URL"
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
