# Firecrawl 快速开始文档

> **最后更新**: 2025-01-27  
> **基于**: Firecrawl v2 官方文档

## 📚 文档列表

### 中文文档

- **[快速开始指南（完整翻译）](./introduction-zh.md)** ⭐ **推荐**
  - 基于 [Firecrawl 官方文档](https://docs.firecrawl.dev/introduction) 的完整中文翻译
  - 包含所有核心功能说明和代码示例
  - 已修复图片链接，可直接使用

### 英文文档

- **[Quick Start](./quick-start.md)**
  - 原始英文文档

## 🚀 快速导航

### 核心功能

1. **[Scrape（抓取）](./introduction-zh.md#抓取)**
   - 抓取单个 URL
   - 支持多种输出格式（markdown、html、screenshot）
   - 支持页面交互操作（Actions）

2. **[Crawl（爬取）](./introduction-zh.md#爬取)**
   - 爬取整个网站
   - 自动发现子页面
   - 支持分页获取结果

3. **[Search（搜索）](./introduction-zh.md#搜索)**
   - 网络搜索功能
   - 支持多种来源（web、images、news）
   - 可抓取搜索结果

4. **[Extract（提取）](./introduction-zh.md#json-模式)**
   - 结构化数据提取
   - 支持 JSON Schema
   - 支持无模式提取（使用 prompt）

5. **[Actions（页面交互）](./introduction-zh.md#使用-actions-与页面交互)**
   - 点击、输入、滚动等操作
   - 支持动态内容抓取
   - 支持登录等复杂场景

## 📖 使用示例

### Python

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

# 抓取页面
doc = firecrawl.scrape("https://firecrawl.dev", formats=["markdown", "html"])

# 爬取网站
docs = firecrawl.crawl(url="https://docs.firecrawl.dev", limit=10)

# 搜索
results = firecrawl.search(query="firecrawl", limit=3)
```

### Node.js

```javascript
import Firecrawl from '@mendable/firecrawl-js';

const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });

// 抓取页面
const doc = await firecrawl.scrape('https://firecrawl.dev', { 
  formats: ['markdown', 'html'] 
});

// 爬取网站
const docs = await firecrawl.crawl({ 
  url: 'https://docs.firecrawl.dev', 
  limit: 10 
});
```

## 🔗 相关资源

- [官方文档](https://docs.firecrawl.dev/introduction)
- [API 参考](https://docs.firecrawl.dev/api-reference/v2-introduction)
- [Python SDK](https://docs.firecrawl.dev/sdks/python)
- [Node SDK](https://docs.firecrawl.dev/sdks/node)
- [项目规则](../../../.cursor/rules/firecrawl-official.mdc)

---

**维护者**: AI Agent Team

