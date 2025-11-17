# Firecrawl 工具文档中心

> **版本**: v2.0  
> **最后更新**: 2025-01-27  
> **维护者**: AI Agent Team

## 📋 文档概述

本目录包含 Firecrawl 网页采集工具的完整文档，包括官方资料、代码模块、集成指南和最佳实践。

## 🚀 快速开始

**新用户？** 查看 [快速开始指南](./QUICKSTART.md) 快速上手！

**快速命令**:
```bash
# 安装依赖
pip install -r requirements.txt

# 运行示例
python examples/fastmcp_quickstart_example.py

# 运行测试
pytest tests/ -v
```

## 🗂️ 文档结构

```
Firecrawl工具/
├── README.md                    # 本文档 - 主入口
├── .cursor/                     # Cursor IDE 配置
│   └── rules/                   # 规则文件
├── docs/                        # 文档目录
│   ├── guides/                  # 使用指南
│   ├── ai-agents/               # AI 智能体文档
│   ├── project/                 # 项目文档
│   ├── features/                # 功能特性
│   ├── design/                  # 设计文档
│   ├── reports/                 # 项目报告文档
│   └── assets/                  # 资源文件（PDF、图片等）
├── config/                      # 配置文件
│   └── examples/                # 配置示例
├── code/                        # 代码文件
├── scripts/                     # 脚本工具
├── examples/                    # 示例代码
├── 官方资料/                    # 官方文档资料
├── 代码模块/                    # 代码模块
└── 文档/                        # 其他文档
```

## 📚 快速导航

### 🚀 快速开始

- [快速入门指南](./官方资料/01-快速开始/quick-start.md)
- [安装与配置](./官方资料/01-快速开始/ai-platforms.md)
- [第一个爬虫](./官方资料/01-快速开始/scrape.md)

### 📖 核心文档

#### 使用指南
- [Docker 部署指南](./docs/guides/docker-guide.md)
- [Cursor Git 使用指南](./docs/guides/cursor-git-guide.md)
- [MCP 设置指南](./docs/guides/mcp-setup-guide.md)
- [Cursor 配置迁移](./docs/guides/cursor-config-migration.md)
- [代码模块使用指南](./docs/guides/code-modules-guide.md)

#### AI 智能体
- [AI 智能体配置](./docs/ai-agents/ai-agent-config.md)
- [AI 智能体提示词](./docs/ai-agents/ai-agent-prompts.md)
- [智能体系统说明](./docs/ai-agents/agents.md)

#### 项目文档
- [项目规则](./docs/project/project-rules.md)
- [项目特定规则](./docs/project/project-specific-rules.md)
- [资源索引](./docs/project/resource-index.md)
- [文档合并方案](./docs/project/docs-merge-plan-and-best-practices.md)

#### 项目报告
- [项目改进完成报告](./docs/reports/项目改进完成报告.md)
- [项目状态总结](./docs/reports/项目状态总结.md)
- [推进总结](./docs/reports/推进总结.md)
- [所有报告文档](./docs/reports/) - 查看完整报告列表

#### 功能特性
- [爬取规则特性](./docs/features/crawl-rules-features.md)

### 🔧 配置和代码

#### 配置文件
- [默认设置](./config/default-settings.json)
- [Vercel 配置](./config/vercel.json)
- [配置示例](./config/examples/)

#### 代码模块
- [Flask 存储](./code/flask-storage.py)
- [Supabase 客户端](./code/supabase-client.py)
- [代码模块目录](./代码模块/) (已规范化命名)
- [代码模块使用指南](./docs/guides/code-modules-guide.md)

### 📦 官方资料

**核心文档**:
- [官方资料索引](./官方资料/README.md) - 完整的官方资料导航
- [API 参考手册](./官方资料/Firecrawl_API参考手册.md)
- [API 端点文档](./官方资料/API/) - 详细的 API 端点参考（21 个端点）
- [SDK 使用指南](./官方资料/Firecrawl_SDK使用指南.md)
- [集成说明文档](./官方资料/Firecrawl集成说明文档.md)
- [最佳实践指南](./官方资料/Firecrawl_最佳实践指南.md)
- [应用案例](./官方资料/Firecrawl_实际应用案例.md)

**分类文档**:
- [快速开始指南](./官方资料/01-快速开始/) - 入门教程和基础指南
- [API 参考](./官方资料/02-API参考/) - API 参考文档
- [SDK 与集成](./官方资料/03-SDK与集成/) - SDK 集成指南
- [最佳实践](./官方资料/04-最佳实践/) - 最佳实践文档
- [应用案例](./官方资料/05-应用案例/) - 应用案例集合
- [高级功能](./官方资料/06-高级功能/) - 高级功能说明
- [参考资料](./官方资料/07-参考资料/) - 参考资料
- [社区与支持](./官方资料/08-社区与支持/) - 社区资源

### 🔗 集成指南

- [n8n 集成指南](./docs/guides/n8n-integration-guide.md)

## 🎯 按角色导航

### 👨‍💻 开发人员

**必读文档**:
1. [快速入门指南](./官方资料/01-快速开始/快速入门.md)
2. [API 参考手册](./官方资料/Firecrawl_API参考手册.md)
3. [SDK 使用指南](./官方资料/Firecrawl_SDK使用指南.md)
4. [代码模块](./代码模块/)

**进阶文档**:
- [爬取规则特性](./docs/features/crawl-rules-features.md)
- [最佳实践指南](./官方资料/Firecrawl_最佳实践指南.md)
- [应用案例](./官方资料/Firecrawl_实际应用案例.md)

### 🤖 AI 智能体开发者

**必读文档**:
1. [AI 智能体配置](./docs/ai-agents/ai-agent-config.md)
2. [AI 智能体提示词](./docs/ai-agents/ai-agent-prompts.md)
3. [项目规则](./docs/project/project-rules.md)
4. [MCP 设置指南](./docs/guides/mcp-setup-guide.md)

**配置文档**:
- [Cursor 规则文件](./.cursor/rules/)
- [项目特定规则](./docs/project/project-specific-rules.md)

### 📚 文档维护者

**必读文档**:
1. [文档合并方案](./docs/project/docs-merge-plan-and-best-practices.md)
2. [资源索引](./docs/project/resource-index.md)
3. [文档整理方案](./文档整理方案.md)

## 🔍 文档搜索

### 按功能分类

- **网页抓取**: [Scrape 文档](./官方资料/01-快速开始/scrape.md)
- **网站爬取**: [Crawl 文档](./官方资料/01-快速开始/crawl.md)
- **链接发现**: [Map 文档](./官方资料/01-快速开始/map.md)
- **数据提取**: [Extract 文档](./官方资料/01-快速开始/extract.md)
- **搜索功能**: [Search 文档](./官方资料/01-快速开始/search.md)

### 按场景分类

- **博客爬取**: [爬取规则特性 - 博客](./docs/features/crawl-rules-features.md#博客爬取)
- **新闻网站**: [爬取规则特性 - 新闻](./docs/features/crawl-rules-features.md#新闻网站)
- **电商产品**: [爬取规则特性 - 电商](./docs/features/crawl-rules-features.md#电商产品)
- **文档站点**: [爬取规则特性 - 文档](./docs/features/crawl-rules-features.md#文档站点)

## 🛠️ 工具和脚本

### 文档整理工具

```bash
# 执行文档整理脚本
./scripts/reorganize-docs.sh
```

### MCP 工具

```bash
# 设置 MCP
./scripts/setup-mcp.sh

# 测试 MCP
./scripts/test-mcp.sh
```

## 📊 文档统计

- **总文档数**: 100+ 个文件
- **官方资料**: 50+ 个文档
- **代码模块**: 7 个 Python 文件
- **配置示例**: 3 个示例文件
- **规则文件**: 5 个 .mdc 文件
- **测试文件**: 4 个测试文件
- **脚本工具**: 6 个自动化脚本

## 🔄 更新记录

### v2.0 (2025-01-27)
- ✅ 完成文档结构重组
- ✅ 统一文件命名规范 (kebab-case)
- ✅ 创建文档索引系统
- ✅ 优化目录结构

### v1.0 (2025-01-16)
- ✅ 初始文档合并
- ✅ 建立基础文档结构

## 📞 获取帮助

如有问题或建议：

1. 查看 [文档整理方案](./文档整理方案.md)
2. 参考 [文档合并最佳实践](./docs/project/docs-merge-plan-and-best-practices.md)
3. 查看 [资源索引](./docs/project/resource-index.md)

## 🔗 相关链接

- [Firecrawl 官方文档](https://docs.firecrawl.dev/)
- [Firecrawl GitHub](https://github.com/mendableai/firecrawl)
- [n8n 集成指南](./文档/n8n与Firecrawl集成指南.md)

---

**维护说明**: 本文档由 AI Agent Team 维护，定期更新以确保信息的准确性和时效性。

