# Docker Hub MCP Server - 5 分钟快速上手

## ⚡ 三步配置

### 1️⃣ 获取令牌 (2 分钟)

访问: <https://hub.docker.com/settings/security>

1. 点击 **"New Access Token"**
2. 描述: `Cursor MCP Server`
3. 权限: ✅ **Read** (必需)
4. 点击 **"Generate"**
5. **立即复制令牌** (只显示一次!)

### 2️⃣ 配置文件 (1 分钟)

编辑 `.cursor/mcp.json`,替换两处:

```json
{
  "mcpServers": {
    "docker-hub": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "HUB_PAT_TOKEN",
        "docker/hub-mcp-server:latest",
        "--username=你的用户名" // ← 改这里
      ],
      "env": {
        "HUB_PAT_TOKEN": "你的令牌" // ← 改这里
      }
    }
  }
}
```

### 3️⃣ 启动服务 (2 分钟)

1. **重启 Cursor** (完全退出后重新打开)
2. `Cmd+Shift+P` → 输入 `MCP: List Servers`
3. 选择 `docker-hub` → 点击 `Start Server`

## ✅ 验证配置

在 Cursor 中输入:

```
"List all repositories in my namespace"
```

如果看到你的仓库列表,配置成功! 🎉

## 🎯 常用命令

```bash
# 搜索镜像
"Search for official nginx images"

# 列出仓库
"List all my repositories"

# 查看标签
"Show me all tags for my 'my-app' repository"

# 拉取镜像
"Pull the latest postgres image"

# 查找最新标签
"What's the most recent tag for my 'my-app' repository?"
```

## 🔧 遇到问题?

### Docker 未运行

```bash
# 启动 Docker Desktop
open -a Docker
```

### 镜像拉取慢

```bash
# 手动拉取
docker pull docker/hub-mcp-server:latest
```

### 认证失败

1. 检查用户名是否正确
2. 重新生成令牌
3. 确保令牌有 **Read** 权限

## 📖 完整文档

查看 [README.md](./README.md) 了解:

- 详细配置说明
- 所有可用功能
- 完整故障排查指南
- 安全最佳实践

---

**5 分钟配置完成,立即开始使用! 🚀**
