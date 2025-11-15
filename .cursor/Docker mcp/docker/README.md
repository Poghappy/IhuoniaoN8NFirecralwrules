# .cursor 目录说明

## 📁 目录结构

```
.cursor/
├── README.md                           # 本文件
├── config.json                         # Cursor 配置
├── mcp.json                           # MCP Server 配置
├── rules/                             # 开发规则
│   └── docker-mcp-rules.mdc          # Docker MCP 开发规则
└── prompts/                           # AI 提示词库
    └── docker-hub-prompts.md         # Docker Hub 提示词
```

## 🎯 文件说明

### 1. config.json

**用途：** Cursor 编辑器的主配置文件

**主要配置：**

- 项目信息和类型
- 规则自动应用
- MCP Server 优先级
- 编辑器设置（格式化、代码操作）
- TypeScript 严格模式
- Linting 和测试配置
- Git 提交规范
- 安全扫描
- 性能监控
- **Markdown 配置**（保存时自动格式化、Markdownlint 自动修复、链接验证）

### 2. mcp.json

**用途：** MCP Server 连接配置

**已配置的服务器：**

- ✅ **docker-hub** - Docker Hub MCP Server（已配置令牌）
- ✅ **filesystem** - 文件系统操作（已配置路径）
- ⚠️ **firecrawl** - 网页采集（需要 API 密钥）
- ⚠️ **github** - GitHub 操作（需要访问令牌）

### 3. rules/docker-mcp-rules.mdc

**用途：** Docker Hub MCP Server 开发规则

**包含内容：**

- 🎯 项目目标和架构原则
- 🔧 MCP 工具使用规范
- 📝 开发规范（TypeScript、错误处理、日志）
- 🔐 安全最佳实践
- ⚡ 性能优化（缓存、API 调用）
- 🧪 测试规范
- 📊 监控和日志
- 🚀 Git 提交规范
- ✅ 检查清单

### 4. prompts/docker-hub-prompts.md

**用途：** AI 提示词库和使用示例

**包含内容：**

- 📝 提示词分类（搜索、管理、标签、镜像、自动化、监控）
- 🎯 场景化提示词（新项目、更新、审计、清理、迁移）
- 💡 提示词优化技巧
- 🔍 调试提示词
- 📚 学习提示词
- 🎨 自定义模板

## 🚀 快速开始

### 1. 验证配置

```bash
# 检查 MCP 配置
cat .cursor/mcp.json

# 检查开发规则
cat .cursor/rules/docker-mcp-rules.mdc

# 查看提示词库
cat .cursor/prompts/docker-hub-prompts.md
```

### 2. 测试 MCP Server

在 Cursor 中输入：

```
搜索 Docker Hub 上的官方 nginx 镜像
```

或

```
列出我的所有 Docker Hub 仓库
```

### 3. 应用开发规则

规则会自动应用到以下文件类型：

- `**/*.ts` - TypeScript 文件
- `**/*.js` - JavaScript 文件
- `**/*.json` - JSON 配置文件
- `**/*.md` - Markdown 文档

## 📖 使用指南

### Markdown 自动格式化

**功能特性：**

- ✅ 保存时自动格式化（Prettier）
- ✅ 自动修复 Markdown 语法问题（Markdownlint）
- ✅ 链接有效性验证（支持 emoji 锚点）
- ✅ 代码块语法高亮
- ✅ 中文排版优化

**已禁用的规则：**

- MD013 - 行长度限制（中文排版需要灵活性）
- MD029 - 有序列表前缀
- MD033 - HTML 标签（允许使用）
- MD034 - 裸 URL（允许显示完整 URL）
- MD036 - 强调标题
- MD040 - 代码块语言（不强制要求）
- MD041 - 首行标题
- MD051 - 链接片段验证（避免 emoji 误报）

**使用方法：**

1. 编辑任意 `.md` 文件
2. 按 `Cmd+S` (macOS) 或 `Ctrl+S` (Windows/Linux) 保存
3. Prettier 自动格式化 + Markdownlint 自动修复

**手动格式化：**

- 格式化整个文档：`Shift+Alt+F` (Windows/Linux) 或 `Shift+Option+F` (macOS)
- 格式化选中部分：选中文本 → 右键 → `Format Selection`

**链接锚点规范：**

```markdown
## 🔧 故障排查

[查看故障排查](#-故障排查) ✅ 包含 emoji
```

**详细文档：**

- [MARKDOWN_CONFIG.md](../MARKDOWN_CONFIG.md) - 配置说明
- [MARKDOWN_BEST_PRACTICES.md](../MARKDOWN_BEST_PRACTICES.md) - 最佳实践

### 使用 MCP 工具

**基础搜索：**

```
"Search for official nginx images on Docker Hub"
```

**仓库管理：**

```
"List all my Docker Hub repositories"
"Create a new repository named my-service"
```

**标签操作：**

```
"Show all tags for nginx repository"
"Get the latest tag for my-app"
```

### 遵循开发规范

**文件操作：**

- ✅ 优先更新现有文件
- ✅ 创建前检查是否存在
- ❌ 不要创建重复文件

**代码规范：**

- ✅ 使用 TypeScript 类型注解
- ✅ 实现错误处理
- ✅ 使用结构化日志
- ✅ 编写单元测试

**安全实践：**

- ✅ 使用环境变量存储令牌
- ✅ 定期轮换访问令牌
- ❌ 不要在代码中硬编码敏感信息
- ❌ 不要提交 `.env` 文件

## 🔧 配置管理

### 更新 MCP Server 配置

```bash
# 编辑 MCP 配置
nano .cursor/mcp.json

# 重启 Cursor 以应用更改
```

### 添加新的开发规则

```bash
# 创建新规则文件
nano .cursor/rules/my-custom-rules.mdc

# 在 config.json 中注册
# "files": [
#   ".cursor/rules/docker-mcp-rules.mdc",
#   ".cursor/rules/my-custom-rules.mdc"
# ]
```

### 自定义提示词

```bash
# 编辑提示词库
nano .cursor/prompts/docker-hub-prompts.md

# 添加你的自定义提示词模板
```

## 🔐 安全注意事项

### 敏感信息保护

**已添加到 .gitignore：**

```gitignore
.cursor/mcp.json  # 包含 Docker Hub 令牌
.env
.env.local
*.log
```

**安全检查清单：**

- [ ] Docker Hub 令牌已配置在环境变量中
- [ ] `.cursor/mcp.json` 已添加到 `.gitignore`
- [ ] 定期轮换访问令牌（每 3-6 个月）
- [ ] 使用最小权限原则
- [ ] 不在日志中输出完整令牌

## 📊 监控和调试

### 查看 MCP Server 状态

在 Cursor 中：

1. 打开命令面板（Cmd/Ctrl + Shift + P）
2. 输入 "MCP: Show Server Status"
3. 查看所有 MCP Server 的连接状态

### 调试 MCP 工具

```
帮我调试 Docker Hub MCP Server：
1. 检查令牌是否有效
2. 验证网络连接
3. 查看错误日志
4. 提供解决方案
```

## 🎓 学习资源

### 官方文档

- [MCP Protocol](https://modelcontextprotocol.io/)
- [Docker Hub API](https://docs.docker.com/docker-hub/api/latest/)
- [Cursor Documentation](https://docs.cursor.com/)

### 项目文档

- [README_FIRST.md](../README_FIRST.md) - 快速导航
- [QUICK_START.md](../QUICK_START.md) - 5 分钟快速上手
- [DOCKER_MCP_CURSORRULES_GUIDE.md](../DOCKER_MCP_CURSORRULES_GUIDE.md) - 最佳实践指南

### 社区资源

- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)
- [Docker MCP Examples](https://github.com/docker/mcp-examples)

## ✅ 检查清单

### 初始化完成

- [x] `.cursor/` 目录已创建
- [x] `config.json` 已配置
- [x] `mcp.json` 已配置
- [x] 开发规则已创建
- [x] 提示词库已创建
- [x] README 已创建

### 下一步

- [ ] 测试 MCP Server 连接
- [ ] 验证开发规则自动应用
- [ ] 尝试使用提示词库
- [ ] 根据需求自定义配置
- [ ] 配置其他 MCP Server（可选）

## 🆘 故障排查

### 问题 1: MCP Server 未加载

**症状：** Cursor 无法识别 MCP 工具

**解决方案：**

1. 检查 `.cursor/mcp.json` 是否存在
2. 验证 JSON 格式是否正确
3. 完全重启 Cursor
4. 查看 Cursor 日志

### 问题 2: 开发规则未应用

**症状：** 代码不符合规范但没有提示

**解决方案：**

1. 检查 `.cursor/config.json` 中的 `rules.enabled`
2. 验证规则文件路径是否正确
3. 确认文件类型匹配 `globs` 模式
4. 重启 Cursor

### 问题 3: 提示词不生效

**症状：** AI 不理解自定义提示词

**解决方案：**

1. 检查提示词格式是否清晰
2. 添加更多上下文信息
3. 使用场景化提示词
4. 参考提示词优化技巧

## 📝 更新日志

### v1.0.0 (2025-11-01)

- ✨ 初始化 `.cursor` 目录结构
- ✨ 创建开发规则文件
- ✨ 创建提示词库
- ✨ 配置 Cursor 编辑器设置
- ✨ 添加完整文档

---

**需要帮助？** 查看 [DOCKER_MCP_CURSORRULES_GUIDE.md](../DOCKER_MCP_CURSORRULES_GUIDE.md) 获取详细指南。
