#!/usr/bin/env node
/**
 * ChatGPT MCP HTTP Server
 * 
 * 将本地 MCP 工具暴露为 HTTP 端点，供 ChatGPT 桌面版连接
 * 
 * 使用方法：
 * 1. 启动服务器: node server.js
 * 2. 使用 ngrok 暴露: ngrok http 3000
 * 3. 在 ChatGPT 中配置 connector URL: https://your-ngrok-url.ngrok.app/mcp
 */

const http = require('http');
const https = require('https');
const { spawn } = require('child_process');
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

const PORT = process.env.PORT || 3000;
const MCP_SERVER_COMMAND = process.env.MCP_SERVER_COMMAND || 'npx';
const MCP_SERVER_ARGS = process.env.MCP_SERVER_ARGS 
  ? process.env.MCP_SERVER_ARGS.split(',')
  : ['-y', 'firecrawl-mcp'];

// 存储活跃的 MCP 服务器连接
const activeConnections = new Map();

/**
 * 创建 MCP 服务器实例
 */
function createMCPServer(sessionId) {
  const server = new Server(
    {
      name: 'chatgpt-mcp-gateway',
      version: '1.0.0',
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // 启动子进程运行实际的 MCP 服务器
  const childProcess = spawn(MCP_SERVER_COMMAND, MCP_SERVER_ARGS, {
    env: { ...process.env },
    stdio: ['pipe', 'pipe', 'pipe'],
  });

  const transport = new StdioServerTransport({
    command: childProcess,
    args: [],
  });

  server.connect(transport);

  // 错误处理
  childProcess.on('error', (error) => {
    console.error(`[${sessionId}] MCP 服务器进程错误:`, error);
  });

  childProcess.on('exit', (code) => {
    console.log(`[${sessionId}] MCP 服务器进程退出，代码: ${code}`);
    activeConnections.delete(sessionId);
  });

  return { server, childProcess };
}

/**
 * HTTP 请求处理器
 */
const server = http.createServer(async (req, res) => {
  // CORS 头
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // 只处理 /mcp 端点
  if (req.url !== '/mcp' && !req.url.startsWith('/mcp/')) {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not Found' }));
    return;
  }

  const sessionId = req.headers['x-session-id'] || `session-${Date.now()}`;

  try {
    // 获取或创建 MCP 服务器连接
    let mcpConnection = activeConnections.get(sessionId);
    if (!mcpConnection) {
      console.log(`[${sessionId}] 创建新的 MCP 连接`);
      mcpConnection = createMCPServer(sessionId);
      activeConnections.set(sessionId, mcpConnection);
    }

    // 处理 POST 请求（MCP 消息）
    if (req.method === 'POST') {
      let body = '';
      req.on('data', (chunk) => {
        body += chunk.toString();
      });

      req.on('end', async () => {
        try {
          const message = JSON.parse(body);
          
          // 转发消息到 MCP 服务器
          const response = await mcpConnection.server.handleRequest(message);
          
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(response));
        } catch (error) {
          console.error(`[${sessionId}] 处理请求错误:`, error);
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: error.message }));
        }
      });
    } else {
      // GET 请求 - 返回服务器信息
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        name: 'ChatGPT MCP Gateway',
        version: '1.0.0',
        status: 'running',
        sessionId,
        activeConnections: activeConnections.size,
      }));
    }
  } catch (error) {
    console.error(`[${sessionId}] 服务器错误:`, error);
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: error.message }));
  }
});

// 启动服务器
server.listen(PORT, () => {
  console.log(`🚀 ChatGPT MCP Gateway 服务器运行在 http://localhost:${PORT}`);
  console.log(`📡 MCP 端点: http://localhost:${PORT}/mcp`);
  console.log(`\n📝 下一步:`);
  console.log(`   1. 使用 ngrok 暴露: ngrok http ${PORT}`);
  console.log(`   2. 或使用 cloudflared: cloudflared tunnel --url http://localhost:${PORT}`);
  console.log(`   3. 在 ChatGPT 中配置 connector URL`);
});

// 优雅关闭
process.on('SIGTERM', () => {
  console.log('正在关闭服务器...');
  activeConnections.forEach(({ childProcess }) => {
    childProcess.kill();
  });
  server.close(() => {
    console.log('服务器已关闭');
    process.exit(0);
  });
});

