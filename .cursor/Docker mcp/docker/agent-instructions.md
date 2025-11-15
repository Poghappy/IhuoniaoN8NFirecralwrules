# Docker Hub MCP Server - AI Agent 指令

## 🎯 项目概述

这是一个 Docker Hub MCP Server 配置项目，包含完整的文档系统和 Markdown 自动修复配置。

## 📚 核心文档

### 必读文档（按优先级）

1. **README_FIRST.md** - 快速导航和项目概览
2. **QUICK_START.md** - 5 分钟快速上手
3. **README.md** - 完整配置指南
4. **EXAMPLES.md** - 35+ 实战场景

### 配置文档

- **CONFIGURATION_SUMMARY.md** - 配置总结和进度
- **CONFIGURATION_COMPLETE.md** - 完整配置清单
- **MARKDOWN_CONFIG.md** - Markdown 自动修复配置
- **MARKDOWN_BEST_PRACTICES.md** - Markdown 最佳实践
- **FIXES_SUMMARY.md** - 错误修复总结
- **PYTHON_PATH_FIX.md** - Python 路径修复

## 🔧 配置文件

### MCP 配置

- `.cursor/mcp.json` - Docker Hub MCP Server 配置
  - 需要填入 Docker Hub 用户名和个人访问令牌
  - 使用 Docker 容器运行

### 编辑器配置

- `.vscode/settings.json` - 项目级编辑器配置
  - Markdown 自动格式化
  - Markdownlint 自动修复
  - AI 工具自动授权

### 代码质量

- `.markdownlint.json` - Markdownlint 规则（8 个规则已禁用）
- `.prettierrc.json` - Prettier 格式化规则
- `.gitignore` - Git 忽略规则（保护敏感信息）

## 🤖 AI Agent 行为规范

### 1. 文件操作原则

**严格禁止:**

- ❌ 随意创建新文件
- ❌ 创建重复文件
- ❌ 创建临时测试文件后不清理

**必须遵守:**

- ✅ 优先更新现有文件
- ✅ 创建前检查是否已存在
- ✅ 使用版本控制
- ✅ 清理临时文件

### 2. 文档更新规范

**更新现有文档时:**

```markdown
# 在现有章节中添加内容

## 现有章节

现有内容...

### 新增小节

新增内容...
```

**避免:**

```markdown
# 创建新文档

## 重复的章节

重复的内容...
```

### 3. MCP 工具优先级

**优先使用 MCP 工具:**

1. `mcp_firecrawl_*` - 网页搜索和采集
2. `mcp_github_*` - GitHub 操作
3. `mcp_filesystem_*` - 文件系统操作
4. `mcp_Chrome_DevTools_*` - 浏览器操作

**避免使用终端命令:**

- ❌ `cat` - 使用 `read_file`
- ❌ `echo` - 使用 `write`
- ❌ `sed/awk` - 使用 `search_replace`

### 4. Markdown 链接规范

**Emoji 标题的锚点:**

```markdown
## 🔧 故障排查

[链接](#-故障排查) ✅ 正确
[链接](#🔧-故障排查) ❌ 错误
```

**代码块必须指定语言:**

````markdown
# 正确示例

```bash
echo "Hello"
```
````

# 错误示例

```
echo "Hello"
```

````

## 📝 响应模板

### 任务开始时

```markdown
## 📋 任务分析

**目标:** [简要描述任务]

**涉及文件:**

- 文件 1 - 操作类型
- 文件 2 - 操作类型

**执行计划:**

1. 步骤 1
2. 步骤 2
3. 步骤 3
````

### 任务完成时

```markdown
## ✅ 任务完成

**完成内容:**

- ✅ 项目 1
- ✅ 项目 2

**修改文件:**

- 文件 1 (新增 X 行)
- 文件 2 (修改 Y 行)

**验证结果:**

- ✅ Linter 检查通过
- ✅ 功能测试通过
```

### 遇到问题时

```markdown
## ⚠️ 问题报告

**问题描述:**
[详细描述问题]

**根本原因:**
[分析根本原因]

**解决方案:**

1. 方案 1 (推荐)
2. 方案 2 (备选)

**需要用户确认:**

- [ ] 选择解决方案
- [ ] 提供额外信息
```

## 🔍 常见任务处理

### 任务 1: 更新文档

**步骤:**

1. 读取现有文档
2. 找到相关章节
3. 在章节中添加内容
4. 验证 Markdown 格式
5. 检查链接有效性

**示例:**

```markdown
# 读取文档

read_file("README.md")

# 更新章节

search_replace(
file="README.md",
old_string="## 现有章节\n 现有内容",
new_string="## 现有章节\n 现有内容\n\n### 新增内容\n 新内容..."
)
```

### 任务 2: 修复配置错误

**步骤:**

1. 读取配置文件
2. 识别错误
3. 修复错误
4. 验证语法
5. 测试配置

**示例:**

```json
// 修复前
{
  "key": "value"  // 缺少逗号
  "key2": "value2"
}

// 修复后
{
  "key": "value",
  "key2": "value2"
}
```

### 任务 3: 创建新功能

**步骤:**

1. 检查是否已存在类似功能
2. 确认需要创建新文件
3. 创建文件
4. 更新相关文档
5. 添加到导航

**必须更新:**

- README.md - 添加功能说明
- CONFIGURATION_SUMMARY.md - 更新配置清单
- README_FIRST.md - 更新文档导航

## 🎯 质量标准

### 代码质量

- ✅ 所有 Python 函数有类型注解
- ✅ 所有函数有中文文档字符串
- ✅ 使用 Ruff 格式化
- ✅ 通过 mypy --strict 检查
- ✅ 测试覆盖率 > 80%

### 文档质量

- ✅ 标题层级正确
- ✅ 链接有效
- ✅ 代码块有语言标记
- ✅ 示例可运行
- ✅ 通过 Markdownlint 检查

### 配置质量

- ✅ JSON 语法正确
- ✅ 路径有效
- ✅ 没有敏感信息
- ✅ 有注释说明

## 🚨 错误处理

### 常见错误

1. **文件不存在**

   - 检查路径是否正确
   - 使用 `list_dir` 查看目录
   - 使用 `glob_file_search` 搜索文件

2. **权限错误**

   - 检查文件权限
   - 使用 `chmod` 修改权限
   - 使用 `sudo` 提升权限（谨慎）

3. **语法错误**

   - 使用 `read_lints` 检查
   - 使用在线工具验证
   - 查看错误消息

4. **配置错误**
   - 检查配置格式
   - 验证路径存在
   - 测试配置生效

## 📊 进度跟踪

### 当前状态

- ✅ MCP Server 配置完成（需填入个人信息）
- ✅ Markdown 自动修复配置完成
- ✅ 文档系统完成（10 个文档）
- ✅ Python 路径修复完成
- ✅ 所有 Linter 错误修复完成

### 待完成任务

- [ ] 安装 Docker Desktop
- [ ] 获取 Docker Hub 个人访问令牌
- [ ] 配置 `.cursor/mcp.json`
- [ ] 测试 MCP Server 功能
- [ ] 安装 Prettier 和 Markdownlint 扩展

## 🎓 学习资源

### 项目文档

所有文档都在项目根目录，按需查阅：

- 快速任务 → QUICK_START.md
- 详细说明 → README.md
- 实战示例 → EXAMPLES.md
- 问题排查 → 各文档的故障排查章节

### 外部资源

- [Docker Hub MCP Server GitHub](https://github.com/docker/hub-mcp)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Cursor 文档](https://docs.cursor.com/)
- [Firecrawl 文档](https://docs.firecrawl.dev/)

## ✅ 检查清单

### 每次任务前

- [ ] 阅读相关文档
- [ ] 理解任务目标
- [ ] 检查现有文件
- [ ] 规划执行步骤

### 每次任务后

- [ ] 验证功能正常
- [ ] 检查 Linter 错误
- [ ] 更新相关文档
- [ ] 清理临时文件
- [ ] 提交变更（如需要）

---

**记住：优先更新，避免重复，使用 MCP，参考文档！**
