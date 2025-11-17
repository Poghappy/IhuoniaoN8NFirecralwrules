# 快速开始指南

> **版本**: v1.0  
> **最后更新**: 2025-01-27

## 📋 概述

本指南将帮助您快速开始使用 Firecrawl 工具项目。

## 🚀 快速开始

### 1. 环境准备

#### 安装 Python
确保您的系统已安装 Python 3.9 或更高版本：

```bash
python3 --version
```

#### 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置设置

#### 环境变量
创建 `.env` 文件并配置必要的环境变量：

```bash
# Firecrawl API 配置
FIRECRAWL_API_KEY=your_api_key_here

# Supabase 配置
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# 火鸟门户 API 配置
HUONIAO_API_URL=https://your-huoniao-portal.com/api/
HUONIAO_API_KEY=your_api_key
```

#### 配置文件
复制配置示例并修改：

```bash
cp config/examples/aliyun-credentials.example.md config/aliyun-credentials.md
cp config/examples/openai-api-key.example.md config/openai-api-key.md
```

### 3. 运行示例

#### 运行 FastMCP 示例
```bash
python examples/fastmcp_quickstart_example.py
```

#### 运行集成测试
```bash
python 代码模块/integration-test.py
```

### 4. 使用代码模块

#### API 集成
```python
from 代码模块.api_integration import HuoniaoAPIClient

client = HuoniaoAPIClient(
    base_url="https://your-api.com",
    api_key="your-key"
)

# 发布内容
result = client.publish_article({
    "title": "文章标题",
    "content": "文章内容"
})
```

#### Firecrawl 采集器
```python
from 代码模块.firecrawl_collector import FirecrawlCollector

collector = FirecrawlCollector(api_key="your-api-key")
result = collector.scrape("https://example.com")
```

## 📚 文档导航

### 核心文档
- [README.md](./README.md) - 项目主文档
- [API 参考手册](./官方资料/Firecrawl_API参考手册.md) - API 详细文档
- [SDK 使用指南](./官方资料/Firecrawl_SDK使用指南.md) - SDK 使用说明

### 使用指南
- [Docker 部署指南](./docs/guides/docker-guide.md)
- [MCP 设置指南](./docs/guides/mcp-setup-guide.md)
- [Cursor Git 使用指南](./docs/guides/cursor-git-guide.md)

### 功能特性
- [爬取规则特性](./docs/features/crawl-rules-features.md)

## 🔧 开发工具

### 运行测试
```bash
pytest tests/ -v
```

### 代码格式化
```bash
black code/ tests/
```

### 文档验证
```bash
./scripts/validate-docs.sh
```

## 🆘 获取帮助

### 常见问题
1. **API Key 错误**: 检查环境变量配置
2. **依赖安装失败**: 确保 Python 版本正确
3. **导入错误**: 检查 Python 路径配置

### 相关资源
- [项目规则](./docs/project/project-rules.md)
- [贡献指南](./CONTRIBUTING.md)
- [更新日志](./CHANGELOG.md)

## 📝 下一步

1. 阅读 [API 参考手册](./官方资料/Firecrawl_API参考手册.md)
2. 查看 [最佳实践指南](./官方资料/Firecrawl_最佳实践指南.md)
3. 参考 [应用案例](./官方资料/Firecrawl_实际应用案例.md)

---

**维护者**: AI Agent Team

