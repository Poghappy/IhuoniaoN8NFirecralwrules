# 🔧 火鸟门户系统MCP配置完整指南

## 📋 概述

本文档详细介绍火鸟门户系统的MCP（Model Context Protocol）配置方法，包括环境配置、服务器设置、自动化工具配置等。

## 🚀 MCP基础配置

### 环境变量配置

```bash
# MCP 基础配置
MCP_CONFIG_PATH="/Users/zhiledeng/Desktop/Trea/src/.vscode/mcp.json"
MCP_LOG_LEVEL="info"
MCP_TIMEOUT=30000

# 数据文件路径配置
MEMORY_FILE_PATH="/Users/zhiledeng/Desktop/Trea/data/mcp/firebird-memory.json"
SQLITE_DB_PATH="/Users/zhiledeng/Desktop/Trea/data/mcp/firebird.db"
TASK_MANAGER_FILE_PATH="/Users/zhiledeng/Desktop/Trea/data/mcp/firebird-tasks.json"
KNOWLEDGE_GRAPH_FILE="/Users/zhiledeng/Desktop/Trea/data/mcp/firebird-knowledge.json"
```

### MCP服务器配置

```json
{
  "mcpServers": {
    "browser-mcp": {
      "command": "npx",
      "args": ["-y", "@browsermcp/mcp"],
      "env": {
        "BROWSER_MCP_PORT": "3000"
      }
    },
    "mcp-taskmanager": {
      "command": "mcp-taskmanager",
      "args": [],
      "env": {
        "TASKS_FILE": "/Users/zhiledeng/Documents/tasks.json"
      }
    },
    "content-processor": {
      "command": "node",
      "args": ["/Users/zhiledeng/Desktop/Trea ai /mcp-servers/content-processor/server.js"],
      "env": {
        "NODE_ENV": "production",
        "REDIS_URL": "redis://localhost:6379",
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_DATABASE": "hawaiihub"
      }
    }
  }
}
```

## 🔧 系统集成配置

### 数据库连接配置

```php
// 数据库配置文件：include/dbinfo.inc.php
$cfg_dbhost = 'localhost';
$cfg_dbname = 'hawaiihub';
$cfg_dbuser = 'root';
$cfg_dbpwd = 'your_password';
$cfg_dbprefix = 'hn_';
$cfg_db_language = 'utf8mb4';
```

### 网站基础配置

```php
// 网站配置文件：include/config/siteConfig.inc.php
$cfg_basehost = 'hawaiihub.net';
$cfg_webname = 'HawaiiHub华人生活平台';
$cfg_secureAccess = 'https://';
$cfg_fileUrl = 'https://hawaiihub.net';
$cfg_uploadDir = '/uploads';
```

## 🤖 自动化工具配置

### N8N工作流配置

```json
{
  "n8n_webhook": "http://localhost:5678/webhook/firebird-automation",
  "n8n_api_key": "your_api_key",
  "n8n_username": "admin",
  "n8n_password": "huoniao2024"
}
```

### 备份和恢复配置

```json
{
  "backup_and_recovery": {
    "auto_backup": true,
    "backup_interval": 86400000,
    "backup_location": "/Users/zhiledeng/Desktop/Trea/backups",
    "max_backups": 7,
    "recovery_mode": "auto"
  }
}
```

## 📊 监控和日志配置

### 日志配置

```bash
# 日志文件路径
LOG_PATH="/Users/zhiledeng/Desktop/Trea/logs"
ERROR_LOG_LEVEL="error"
ACCESS_LOG_ENABLED=true
```

### 性能监控

```json
{
  "monitoring": {
    "enabled": true,
    "metrics_endpoint": "/metrics",
    "health_check_endpoint": "/health",
    "alert_thresholds": {
      "cpu_usage": 80,
      "memory_usage": 85,
      "disk_usage": 90
    }
  }
}
```

## 🔐 安全配置

### SSL证书配置

```bash
# SSL证书路径
SSL_CERT_PATH="/etc/ssl/certs/hawaiihub.crt"
SSL_KEY_PATH="/etc/ssl/private/hawaiihub.key"
SSL_CHAIN_PATH="/etc/ssl/certs/hawaiihub-chain.crt"
```

### 防火墙配置

```bash
# 开放端口
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3306/tcp
ufw allow 6379/tcp
```

## 🚀 部署和启动

### 启动MCP服务

```bash
# 启动MCP服务器
npm start

# 启动后台服务
pm2 start ecosystem.config.js

# 检查服务状态
pm2 status
```

### 验证配置

```bash
# 检查MCP连接
curl http://localhost:3000/health

# 检查数据库连接
mysql -h localhost -u root -p hawaiihub

# 检查Redis连接
redis-cli ping
```

## 🔧 故障排除

### 常见问题

1. **MCP连接失败**
   - 检查端口是否被占用
   - 验证环境变量配置
   - 查看日志文件

2. **数据库连接错误**
   - 验证数据库凭据
   - 检查数据库服务状态
   - 确认网络连接

3. **文件权限问题**
   - 设置正确的文件权限
   - 检查目录所有权
   - 验证写入权限

### 日志查看

```bash
# 查看MCP日志
tail -f /Users/zhiledeng/Desktop/Trea/logs/mcp.log

# 查看系统日志
tail -f /var/log/syslog

# 查看错误日志
tail -f /Users/zhiledeng/Desktop/Trea/logs/error.log
```

## 📝 维护和更新

### 定期维护任务

1. **每日任务**
   - 检查服务状态
   - 查看错误日志
   - 验证备份完成

2. **每周任务**
   - 更新系统补丁
   - 清理临时文件
   - 检查磁盘空间

3. **每月任务**
   - 更新MCP组件
   - 优化数据库
   - 安全审计

### 更新流程

```bash
# 1. 备份当前配置
cp mcp.json mcp.json.backup

# 2. 更新MCP组件
npm update

# 3. 重启服务
pm2 restart all

# 4. 验证更新
npm run test
```

## 📞 技术支持

- **官方文档**: <https://docs.hawaiihub.net>
- **技术支持**: <support@hawaiihub.net>
- **社区论坛**: <https://community.hawaiihub.net>
