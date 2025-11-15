# 项目 MCP 配置说明

## 📋 配置文件位置

**项目级配置**：`.cursor/mcp.json`

**全局配置**：`~/.cursor/mcp.json`

**优先级**：项目级配置会覆盖全局配置

---

## 🔥 已配置的 MCP 服务器

### 1. Firecrawl MCP（核心）🔥 v2

**用途**：网页爬取和内容提取

**版本**：v2（最新，自动使用）

**配置**：

```json
{
  "firecrawl": {
    "command": "npx",
    "args": ["-y", "firecrawl-mcp"],
    "env": {
      "FIRECRAWL_API_KEY": "${env:FIRECRAWL_API_KEY}"
    }
  }
}
```

**环境变量**：

- `FIRECRAWL_API_KEY` - 从 `.env` 文件读取

**功能**：

- ✅ Scrape（单页采集）- v2 优化
- ✅ Crawl（深度爬取）- v2 智能爬取
- ✅ Map（站点地图）- v2 优化
- ✅ Search（智能搜索）- v2 新搜索源
- ✅ Extract（结构化提取）- v2 增强 JSON

**v2 新功能**：

- ✅ Summary 格式：快速获取页面摘要
- ✅ 智能爬取：使用自然语言 `prompt` 自动推导策略
- ✅ 增强 JSON 提取：对象格式 `{ type: "json", prompt, schema }`
- ✅ 增强截图：对象格式 `{ type: "screenshot", fullPage, quality, viewport }`
- ✅ 新搜索源：支持 `"news"` 和 `"images"` 搜索
- ✅ 默认缓存：2 天缓存，减少重复请求

**参考文档**：

- [Firecrawl v2 迁移指南](../FIRECRAWL_V2_MIGRATION.md)
- [Firecrawl v2 MCP 使用指南](../FIRECRAWL_V2_MCP_GUIDE.md)
- [官方迁移文档](https://docs.firecrawl.dev/migrate-to-v2)

### 2. GitHub MCP

**用途**：GitHub 仓库管理

**配置**：

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
    }
  }
}
```

**环境变量**：

- `GITHUB_TOKEN` - GitHub Personal Access Token（可选）

**功能**：

- ✅ 搜索仓库
- ✅ 读取文件
- ✅ 创建 Issue
- ✅ 管理 Pull Request

### 3. Filesystem MCP

**用途**：文件系统操作

**配置**：

```json
{
  "filesystem": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-v",
      "/Users/zhiledeng/Downloads/firecralw:/workspace",
      "mcp/filesystem",
      "/workspace"
    ]
  }
}
```

**功能**：

- ✅ 读取文件
- ✅ 写入文件
- ✅ 列出目录
- ✅ 搜索文件

### 4. Fetch MCP

**用途**：HTTP 请求和网页获取

**配置**：

```json
{
  "fetch": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "mcp/fetch"
    ]
  }
}
```

**功能**：

- ✅ 获取网页内容
- ✅ HTTP 请求
- ✅ URL 提取

---

## 🔧 环境变量配置

### 必需的环境变量

在 `.env` 文件中配置：

```env
# Firecrawl API Key（必需）
FIRECRAWL_API_KEY=fc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GitHub Token（可选）
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 获取 API Key

#### Firecrawl API Key

1. 访问：https://firecrawl.dev/
2. 注册/登录账号
3. 进入 Dashboard
4. 复制 API Key

#### GitHub Token（可选）

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：`repo`, `read:org`
4. 生成并复制 Token

---

## 🚀 使用 MCP 工具

### 在 Cursor 中使用

**方式 1：通过 Composer**

1. 按 `Cmd+L`（Mac）或 `Ctrl+L`（Windows）打开 Composer
2. 选择 "Agent" 模式
3. 描述你的需求，AI 会自动使用 MCP 工具

**示例**：

```
使用 Firecrawl 爬取 https://example.com 的内容
```

**方式 2：直接调用**

在对话中提及工具名称，AI 会自动使用：

```
@firecrawl 请爬取这个网页：https://example.com
```

---

## 📋 MCP 工具列表

### Firecrawl 工具

| 工具      | 功能       | 示例         |
| --------- | ---------- | ------------ |
| `scrape`  | 单页采集   | 爬取单个网页 |
| `crawl`   | 深度爬取   | 爬取整个网站 |
| `map`     | 站点地图   | 发现所有 URL |
| `search`  | 智能搜索   | 搜索互联网   |
| `extract` | 结构化提取 | 提取特定数据 |

### GitHub 工具

| 工具                  | 功能       | 示例         |
| --------------------- | ---------- | ------------ |
| `search_repositories` | 搜索仓库   | 查找相关项目 |
| `get_file_contents`   | 读取文件   | 获取代码文件 |
| `create_issue`        | 创建 Issue | 报告问题     |

### Filesystem 工具

| 工具             | 功能     | 示例          |
| ---------------- | -------- | ------------- |
| `read_file`      | 读取文件 | 查看文件内容  |
| `write_file`     | 写入文件 | 创建/修改文件 |
| `list_directory` | 列出目录 | 查看文件列表  |

---

## ✅ 配置验证

### 检查 MCP 配置

1. **重启 Cursor**：使配置生效

2. **检查 MCP 状态**：
   - 打开 Cursor 设置
   - 前往 Features > MCP Servers
   - 查看服务器状态

3. **测试 Firecrawl**：

   ```
   @firecrawl 请测试连接，爬取 https://example.com
   ```

---

## 🔒 安全注意事项

1. **API Key 安全**：
   - ✅ `.env` 已添加到 `.gitignore`
   - ✅ 不要提交 `.env` 文件到 Git
   - ✅ 不要分享 API Key

2. **MCP 配置**：
   - ✅ 项目级配置使用环境变量
   - ✅ 不硬编码 API Key
   - ✅ 支持团队协作

---

## 📚 相关文档

- [Firecrawl MCP 官方文档](https://docs.firecrawl.dev/mcp)
- [Cursor MCP 配置指南](https://docs.cursor.com/context/model-context-protocol)
- [GitHub MCP 文档](https://github.com/modelcontextprotocol/servers/tree/main/src/github)

---

## 🎯 快速开始

1. **配置环境变量**：

   ```bash
   # 编辑 .env 文件
   code .env

   # 填入 FIRECRAWL_API_KEY
   FIRECRAWL_API_KEY=fc-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

2. **重启 Cursor**：
   - 完全退出 Cursor
   - 重新打开 Cursor

3. **验证配置**：
   - 打开设置 > Features > MCP Servers
   - 查看 Firecrawl 服务器状态

4. **测试使用**：

   ```
   @firecrawl 请爬取 https://example.com 并返回主要内容
   ```

---

**配置完成！现在可以在 Cursor 中使用 Firecrawl MCP 进行网页爬取了！** 🎉
