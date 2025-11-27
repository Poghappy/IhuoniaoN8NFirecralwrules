# 🚀 下一步行动计划

**生成时间**: 2025-11-17
**基于**: Docker 配置检查报告

---

## 📋 优先级任务清单

### 🔴 高优先级（立即执行）

#### 1. 修复 Docker Compose 过时语法

**问题**: `docker-compose-n8n.yml` 和 `Nginx代理管理/docker-compose.yml` 使用了过时的 `version` 字段

**操作**:
```bash
# 修复 docker-compose-n8n.yml
# 移除第一行的 version: '3.8'

# 修复 Nginx代理管理/docker-compose.yml
# 移除第一行的 version: '3.8'
```

**影响**: 确保未来 Docker Compose 版本兼容性

---

#### 2. 清理未使用的 Docker 资源

**问题**:
- 6 个已停止的容器
- 8.36GB 未使用的镜像（76% 可回收）

**操作**:
```bash
# 清理已停止的容器
docker container prune -f

# 清理未使用的镜像（可选，会释放约 8GB）
docker image prune -a -f

# 或者全面清理（包括构建缓存）
docker system prune -a --volumes
```

**影响**: 释放磁盘空间，提升系统性能

---

#### 3. 解决 Kong Konnect 扩展问题

**问题**: Kong Konnect 扩展容器频繁重启（每 1 分钟）

**操作**:
```bash
# 1. 检查日志
docker logs kong_konnect-docker-extension-desktop-extension-service

# 2. 如果不需要，可以禁用扩展
# 在 Docker Desktop → Extensions → Kong Konnect → Disable

# 3. 或者重新安装扩展
```

**影响**: 减少不必要的资源消耗和日志噪音

---

### 🟡 中优先级（本周完成）

#### 4. 完成 ChatGPT MCP 服务器配置

**当前状态**: 已创建 `chatgpt-mcp-server/` 目录和基础文件

**下一步操作**:

1. **安装依赖**:
   ```bash
   cd chatgpt-mcp-server
   npm install
   ```

2. **配置环境变量**:
   ```bash
   # 创建 .env 文件
   cat > .env << EOF
   PORT=3000
   MCP_SERVER_COMMAND=npx
   MCP_SERVER_ARGS=-y,firecrawl-mcp
   FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}
   EOF
   ```

3. **测试服务器**:
   ```bash
   npm start
   # 在另一个终端测试
   curl http://localhost:3000/mcp
   ```

4. **使用 ngrok 暴露**:
   ```bash
   ngrok http 3000
   # 复制 HTTPS URL，例如: https://abc123.ngrok.app
   ```

5. **在 ChatGPT 中配置**:
   - 打开 ChatGPT 桌面版
   - Settings → Apps & Connectors → Advanced settings
   - 启用 Developer mode
   - Settings → Connectors → Create
   - 填写信息：
     - **Connector name**: `HawaiiHub MCP Gateway`
     - **Description**: `本地 MCP 工具网关，提供 Firecrawl、GitHub 等工具`
     - **Connector URL**: `https://your-ngrok-url.ngrok.app/mcp`
   - 点击 Create

6. **测试连接**:
   - 打开新的 ChatGPT 对话
   - 点击 `+` → `More` → 选择你的连接器
   - 测试工具调用，例如："使用 Firecrawl 抓取 https://example.com"

---

#### 5. 优化 Docker MCP Gateway 配置

**当前状态**: `.cursor/mcp.json` 中已配置 `MCP_DOCKER`

**优化建议**:

1. **测试连接**:
   ```bash
   # 重启 Cursor
   # 在 Cursor 中: Cmd+Shift+P → MCP: List Servers
   # 验证 MCP_DOCKER 是否出现
   ```

2. **配置多个 MCP 服务器**（可选）:
   - 如果需要同时使用多个 MCP 服务器，可以创建多个网关实例
   - 或者使用 Docker MCP Gateway 的 `--servers` 参数指定特定服务器

---

### 🟢 低优先级（可选优化）

#### 6. 设置定期清理任务

**创建清理脚本**:
```bash
# 创建 ~/bin/docker-cleanup.sh
cat > ~/bin/docker-cleanup.sh << 'EOF'
#!/bin/bash
# Docker 定期清理脚本

echo "🧹 开始清理 Docker 资源..."

# 清理已停止的容器
echo "清理已停止的容器..."
docker container prune -f

# 清理未使用的镜像（保留最近 7 天的）
echo "清理未使用的镜像..."
docker image prune -a --filter "until=168h" -f

# 清理构建缓存
echo "清理构建缓存..."
docker builder prune -f

# 显示清理结果
echo "✅ 清理完成！"
docker system df
EOF

chmod +x ~/bin/docker-cleanup.sh

# 添加到 crontab（每周执行一次）
# crontab -e
# 添加: 0 2 * * 0 ~/bin/docker-cleanup.sh
```

---

#### 7. 监控 Docker 资源使用

**设置监控**:
```bash
# 创建监控脚本
cat > ~/bin/docker-monitor.sh << 'EOF'
#!/bin/bash
# Docker 资源监控脚本

echo "📊 Docker 资源使用情况"
echo "======================"
docker system df
echo ""
echo "🔍 运行中的容器"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.CPUPerc}}\t{{.MemUsage}}"
EOF

chmod +x ~/bin/docker-monitor.sh
```

---

#### 8. 文档化 Docker 配置

**创建配置文档**:
- 记录所有 Docker Compose 服务的用途
- 记录端口映射和卷挂载
- 记录环境变量配置
- 创建快速启动脚本

---

## 🎯 推荐执行顺序

### 今天完成（30 分钟）

1. ✅ 修复 Docker Compose 文件（5 分钟）
2. ✅ 清理已停止的容器（1 分钟）
3. ✅ 检查 Kong Konnect 扩展日志（5 分钟）
4. ✅ 安装 ChatGPT MCP 服务器依赖（5 分钟）
5. ✅ 测试 ChatGPT MCP 服务器（10 分钟）

### 本周完成（2-3 小时）

1. ✅ 完成 ChatGPT MCP 服务器配置和测试
2. ✅ 在 ChatGPT 中成功连接并测试工具
3. ✅ 清理未使用的镜像（可选，释放 8GB）
4. ✅ 创建定期清理脚本

### 长期优化（可选）

1. ✅ 设置自动化监控
2. ✅ 完善文档
3. ✅ 优化 Docker Compose 配置

---

## 📝 快速命令参考

### 立即执行

```bash
# 1. 修复 Docker Compose 文件
sed -i '' '/^version:/d' docker-compose-n8n.yml
sed -i '' '/^version:/d' Nginx代理管理/docker-compose.yml

# 2. 清理资源
docker container prune -f
docker image prune -a -f  # 可选，释放 8GB

# 3. 检查 Kong Konnect
docker logs kong_konnect-docker-extension-desktop-extension-service

# 4. 设置 ChatGPT MCP 服务器
cd chatgpt-mcp-server
npm install
npm start
```

### 测试命令

```bash
# 测试 ChatGPT MCP 服务器
curl http://localhost:3000/mcp

# 测试 Docker MCP Gateway
docker mcp gateway run --dry-run

# 检查 Cursor MCP 配置
cat .cursor/mcp.json | jq '.mcpServers.MCP_DOCKER'
```

---

## 🔗 相关文档

- [Docker 配置检查报告](./DOCKER_CONFIG_AUDIT_REPORT.md)
- [ChatGPT MCP 服务器 README](./chatgpt-mcp-server/README.md)
- [OpenAI Apps SDK 文档](https://developers.openai.com/apps-sdk/deploy/connect-chatgpt/)

---

## ✅ 完成检查清单

- [ ] 修复 Docker Compose 文件
- [ ] 清理已停止的容器
- [ ] 检查/解决 Kong Konnect 问题
- [ ] 安装 ChatGPT MCP 服务器依赖
- [ ] 测试 ChatGPT MCP 服务器
- [ ] 配置 ngrok 隧道
- [ ] 在 ChatGPT 中创建连接器
- [ ] 测试 ChatGPT 工具调用
- [ ] 清理未使用的镜像（可选）
- [ ] 创建定期清理脚本（可选）

---

**下一步**: 从"今天完成"部分开始，按顺序执行任务。

