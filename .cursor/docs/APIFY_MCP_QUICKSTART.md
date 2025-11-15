# Apify MCP Server 快速开始指南

本文档帮助你在 Cursor 中快速启用 Apify MCP Server，适用于项目目录 `Hawaiihub.net`。

## 🚀 5 分钟上手

### 步骤 1：获取 Apify Token

1. 打开 [Apify Console](https://console.apify.com/)，登录或注册账户。
2. 进入 **Settings → Integrations → Personal API tokens**。
3. 点击 **Create token**，为本项目生成新的 Token。
4. 复制生成的 Token（格式类似 `apify_api_xxxxx`），妥善保存。

### 步骤 2：配置环境变量

**临时配置（当前终端会话）**

```bash
export APIFY_TOKEN="your-apify-token"
```

**Windows PowerShell**

```powershell
$env:APIFY_TOKEN="your-apify-token"
```

**永久配置（推荐）**

在 `~/.zshrc`、`~/.bashrc` 或 `~/.config/fish/config.fish` 中追加：

```bash
export APIFY_TOKEN="your-apify-token"
```

保存后执行 `source ~/.zshrc`（或对应文件）使其立即生效。

### 步骤 3：验证环境变量

```bash
echo $APIFY_TOKEN
```

若输出被掩码或显示 Token 即代表配置成功；为空则需要重新设置。

### 步骤 4：重启 Cursor

为确保新的环境变量被读取：

1. 完全退出 Cursor（`Cmd+Q` 或 `Alt+F4`）。
2. 重新启动 Cursor 并打开本项目。

启动后，Apify MCP Server 会自动尝试连接。

### 步骤 5：快速自检

在 Composer 中输入：

```
使用 Apify 查找适合新闻采集的 Actor
```

若能列出 Apify 工具或返回搜索结果，则说明配置成功。

## 🔧 配置详情

### MCP 配置文件位置

- 项目级配置：`.cursor/mcp.json`
- 主要条目：`mcpServers.apify-mcp`

当前配置使用 Docker 镜像运行官方 MCP Server：

```json
{
  "apify-mcp": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-e",
      "APIFY_TOKEN=${env:APIFY_TOKEN}",
      "mcp/apify-mcp-server"
    ]
  }
}
```

> ✅ 你也可以将 `command`/`args` 改为 `["-y", "@apify/actors-mcp-server@latest", "--tools", "..."]` 形式的 `npx` 配置；两种写法均受官方支持。若切换方式，请同步更新本文档和 README 中的说明。

### 默认开启的工具

- `actors`：搜索与运行 Apify Actors。
- `docs`：查阅 Apify 文档。
- `apify/rag-web-browser`：适合新闻或网页内容采集。

## 🐛 常见问题排查

### 1. `APIFY_TOKEN` 未设置

- 现象：终端或 Cursor 弹窗显示 `APIFY_TOKEN is undefined or null`。
- 处理：
  1. 重新执行 `echo $APIFY_TOKEN`。
  2. 若为空，按照“步骤 2”重新设置环境变量。
  3. 完整重启 Cursor。

### 2. Token 无效

- 现象：工具调用失败并提示 `Invalid API token`。
- 处理：
  1. 登录 [Apify Console](https://console.apify.com/) 检查 Token 是否仍有效。
  2. 若失效，重新生成并替换环境变量。
  3. 重启 Cursor 后再次测试。

### 3. MCP 服务器未加载

- 现象：在 Cursor 的 MCP 面板中看不到 Apify。
- 处理：
  1. 打开 `.cursor/mcp.json` 确认上述配置存在。
  2. 运行 `docker --version` 确保 Docker 工作正常。
  3. 查看 `.cursor/logs/mcp.log` 获取详细错误。
  4. 如需离线模式，可改用 `npx @apify/actors-mcp-server`。

## ✅ 完成检查清单

- [ ] 已获取并保存 Apify Token
- [ ] 已在 Shell 中配置 `APIFY_TOKEN`
- [ ] `echo $APIFY_TOKEN` 有输出
- [ ] Cursor 已重启
- [ ] MCP 面板中显示 Apify
- [ ] 能通过 AI 调用 `apify` 工具

## 📚 延伸阅读

- [Apify MCP Server GitHub](https://github.com/apify/apify-mcp-server)
- [Apify Store](https://apify.com/store)
- [Model Context Protocol 文档](https://modelcontextprotocol.io/)
- `.cursor/rules/apify-mcp-server.mdc`

---

**最后更新**：2025-11-13  
**维护人**：HawaiiHub 自动化团队
# Apify MCP Server 快速开始指南

## 🚀 5 分钟快速配置

### 步骤 1：获取 Apify Token

1. 访问 [Apify Console](https://console.apify.com/)
2. 登录或注册账户
3. 进入 **Settings** → **Integrations** → **Personal API tokens**
4. 点击 **Create token** 创建新的 API token
5. 复制生成的 token（格式类似：`apify_api_xxxxx`）

### 步骤 2：设置环境变量

**macOS/Linux**：

```bash
export APIFY_TOKEN="your-apify-token"
```

**Windows**：

```cmd
set APIFY_TOKEN=your-apify-token
```

**永久设置**（推荐）：

在 `~/.zshrc` 或 `~/.bashrc` 文件中添加：

```bash
export APIFY_TOKEN="your-apify-token"
```

然后重新加载：

```bash
source ~/.zshrc
```

### 步骤 3：验证配置

检查环境变量是否设置成功：

```bash
echo $APIFY_TOKEN
```

### 步骤 4：重启 Cursor

1. 完全退出 Cursor 编辑器
2. 重新启动 Cursor
3. MCP 服务器会自动加载 Apify MCP Server

### 步骤 5：测试配置

在 Cursor 中询问 AI：

```
使用 Apify 搜索可用的新闻采集 Actor
```

如果配置成功，AI 应该能够使用 Apify MCP Server 的工具。

## 🔧 配置详情

### MCP 配置位置

配置文件位于：`.cursor/mcp.json`

```json
{
  "apify": {
    "command": "npx",
    "args": [
      "-y",
      "@apify/actors-mcp-server@latest",
      "--tools",
      "actors,docs,apify/rag-web-browser"
    ],
    "env": {
      "APIFY_TOKEN": "${env:APIFY_TOKEN}"
    }
  }
}
```

### 可用工具

- **actors** - Actor 发现和调用工具
- **docs** - 文档工具
- **apify/rag-web-browser** - RAG Web Browser Actor（用于新闻采集）

## 🐛 故障排查

### 问题 1：Token 未设置

**错误信息**：`APIFY_TOKEN environment variable is not set`

**解决方案**：

1. 检查环境变量是否设置：
   ```bash
   echo $APIFY_TOKEN
   ```

2. 如果未设置，按照步骤 2 设置环境变量

3. 重启 Cursor 编辑器

### 问题 2：Token 无效

**错误信息**：`Invalid API token`

**解决方案**：

1. 检查 Token 是否正确复制（没有多余空格）
2. 访问 [Apify Console](https://console.apify.com/) 验证 Token 是否有效
3. 重新生成 Token 并更新环境变量

### 问题 3：MCP 服务器未加载

**错误信息**：MCP 工具不可用

**解决方案**：

1. 检查 `.cursor/mcp.json` 配置是否正确
2. 查看 MCP 日志：`.cursor/logs/mcp.log`
3. 验证 Node.js 版本（需要 v18 或更高版本）：
   ```bash
   node -v
   ```
4. 重启 Cursor 编辑器

## 📚 更多资源

- [Apify MCP Server 文档](../rules/apify-mcp-server.mdc)
- [Apify Console](https://console.apify.com/)
- [Apify Store](https://apify.com/store)
- [Apify MCP Server GitHub](https://github.com/apify/apify-mcp-server)

## ✅ 配置检查清单

- [ ] Apify Token 已获取
- [ ] 环境变量已设置
- [ ] 环境变量已验证（`echo $APIFY_TOKEN`）
- [ ] Cursor 编辑器已重启
- [ ] MCP 服务器已加载（检查日志）
- [ ] 测试配置成功（询问 AI 使用 Apify）

## 🎯 下一步

配置完成后，您可以：

1. 使用 Apify Actors 进行网页抓取
2. 使用 RAG Web Browser Actor 进行新闻采集
3. 探索 Apify Store 中的其他工具
4. 结合 Firecrawl 和 Apify 进行数据采集

---

**需要帮助？** 查看 [Apify MCP Server 配置规范](../rules/apify-mcp-server.mdc) 获取详细说明。

