#!/usr/bin/env node
/**
 * ChatGPT MCP HTTP Server (使用 FastMCP)
 *
 * 将本地 MCP 工具暴露为 HTTP 端点，供 ChatGPT 桌面版连接
 *
 * 使用方法：
 * 1. 启动服务器: node server-fastmcp.js
 * 2. 使用 ngrok 暴露: ngrok http 3000
 * 3. 在 ChatGPT 中配置 connector URL: https://your-ngrok-url.ngrok.app/mcp
 */

import FastMCP from 'fastmcp';
import { spawn } from 'child_process';

const PORT = process.env.PORT || 3000;
const MCP_SERVER_COMMAND = process.env.MCP_SERVER_COMMAND || 'npx';
const MCP_SERVER_ARGS = process.env.MCP_SERVER_ARGS
  ? process.env.MCP_SERVER_ARGS.split(',')
  : ['-y', 'firecrawl-mcp'];

// 创建 FastMCP 服务器
const mcp = new FastMCP('ChatGPT MCP Gateway');

// 存储子进程
const childProcesses = new Map();

/**
 * 启动 MCP 服务器子进程并获取工具
 */
async function getToolsFromMCPServer() {
  return new Promise((resolve, reject) => {
    const childProcess = spawn(MCP_SERVER_COMMAND, MCP_SERVER_ARGS, {
      env: { ...process.env },
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    const sessionId = `session-${Date.now()}`;
    childProcesses.set(sessionId, childProcess);

    let stdout = '';
    let stderr = '';

    childProcess.stdout.on('data', (data) => {
      stdout += data.toString();
      // 解析 MCP 消息
      try {
        const lines = stdout.split('\n').filter(line => line.trim());
        for (const line of lines) {
          try {
            const message = JSON.parse(line);
            if (message.method === 'tools/list' && message.result) {
              resolve(message.result.tools || []);
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
      } catch (e) {
        // 忽略错误
      }
    });

    childProcess.stderr.on('data', (data) => {
      stderr += data.toString();
      console.error(`[${sessionId}] MCP 服务器错误:`, data.toString());
    });

    childProcess.on('error', (error) => {
      console.error(`[${sessionId}] MCP 服务器进程错误:`, error);
      reject(error);
    });

    // 发送初始化请求
    const initMessage = {
      jsonrpc: '2.0',
      id: 1,
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        capabilities: {},
        clientInfo: {
          name: 'chatgpt-mcp-gateway',
          version: '1.0.0',
        },
      },
    };

    childProcess.stdin.write(JSON.stringify(initMessage) + '\n');

    // 请求工具列表
    setTimeout(() => {
      const toolsMessage = {
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/list',
        params: {},
      };
      childProcess.stdin.write(JSON.stringify(toolsMessage) + '\n');
    }, 1000);

    // 超时处理
    setTimeout(() => {
      if (!childProcesses.has(sessionId)) {
        resolve([]);
      }
    }, 5000);
  });
}

// 注册工具（从 MCP 服务器获取）
getToolsFromMCPServer().then(tools => {
  console.log(`✅ 从 MCP 服务器获取到 ${tools.length} 个工具`);

  // 为每个工具创建代理函数
  tools.forEach(tool => {
    mcp.tool(tool.name, tool.description || '', {
      // 将工具参数映射
      ...(tool.inputSchema?.properties || {}),
    }, async (args) => {
      // 这里需要实现工具调用逻辑
      // 暂时返回占位符
      return {
        content: [{
          type: 'text',
          text: `工具 ${tool.name} 调用成功，参数: ${JSON.stringify(args)}`,
        }],
      };
    });
  });
}).catch(error => {
  console.error('❌ 获取 MCP 工具失败:', error);
});

// 启动 HTTP 服务器
mcp.serve({
  port: PORT,
  name: 'ChatGPT MCP Gateway',
  version: '1.0.0',
}).then(() => {
  console.log(`🚀 ChatGPT MCP Gateway 服务器运行在 http://localhost:${PORT}`);
  console.log(`📡 MCP 端点: http://localhost:${PORT}/mcp`);
  console.log(`\n📝 下一步:`);
  console.log(`   1. 使用 ngrok 暴露: ngrok http ${PORT}`);
  console.log(`   2. 或使用 cloudflared: cloudflared tunnel --url http://localhost:${PORT}`);
  console.log(`   3. 在 ChatGPT 中配置 connector URL`);
}).catch(error => {
  console.error('❌ 服务器启动失败:', error);
  process.exit(1);
});

// 优雅关闭
process.on('SIGTERM', () => {
  console.log('正在关闭服务器...');
  childProcesses.forEach((childProcess) => {
    childProcess.kill();
  });
  process.exit(0);
});

