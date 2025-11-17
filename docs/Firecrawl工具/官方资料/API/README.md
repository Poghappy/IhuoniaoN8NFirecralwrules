# Firecrawl API 参考文档

> **目录说明**: 本目录包含 Firecrawl API 的详细参考文档

## 📋 API 文档列表

### 核心 API 端点

#### 网页抓取
- [scrape.yml](./scrape.yml) - 单页抓取 API
- [batch-scrape.yml](./batch-scrape.yml) - 批量抓取 API
- [crawl.yml](./crawl.yml) - 网站爬取 API
- [map.yml](./map.yml) - 网站地图生成 API
- [extract.yml](./extract.yml) - 数据提取 API
- [search.yml](./search.yml) - 搜索 API

#### 任务管理
- [get-active-crawls.yml](./get-active-crawls.yml) - 获取活跃爬取任务
- [get-crawl-status.yml](./get-crawl-status.yml) - 获取爬取状态
- [get-crawl-errors.yml](./get-crawl-errors.yml) - 获取爬取错误
- [cancel-crawl.yml](./cancel-crawl.yml) - 取消爬取任务
- [crawl-params-preview.yml](./crawl-params-preview.yml) - 爬取参数预览

#### 批量操作
- [get-batch-scrape-status.yml](./get-batch-scrape-status.yml) - 获取批量抓取状态
- [get-batch-scrape-errors.yml](./get-batch-scrape-errors.yml) - 获取批量抓取错误
- [cancel-batch-scrape.yml](./cancel-batch-scrape.yml) - 取消批量抓取

#### 提取任务
- [get-extract-status.yml](./get-extract-status.yml) - 获取提取任务状态

#### 队列和状态
- [queue-status.yml](./queue-status.yml) - 队列状态查询

#### 使用统计
- [credit-usage.yml](./credit-usage.yml) - 积分使用情况
- [token-usage.yml](./token-usage.yml) - Token 使用情况
- [historical-credit-usage.yml](./historical-credit-usage.yml) - 历史积分使用
- [historical-token-usage.yml](./historical-token-usage.yml) - 历史 Token 使用

### 参考文档
- [firecrawl-api-reference-v2.md](./firecrawl-api-reference-v2.md) - Firecrawl API 完整参考手册 (v2)

## 🔗 相关文档

- [API 参考手册](../Firecrawl_API参考手册.md) - 主要 API 参考文档
- [快速开始指南](../01-快速开始/) - API 使用快速开始
- [SDK 使用指南](../Firecrawl_SDK使用指南.md) - SDK 集成指南

## 📝 文件命名说明

所有 API 文档文件已规范化命名，采用 `kebab-case` 格式：
- 原格式：`# Batch Scrape.yml`
- 新格式：`batch-scrape.yml`

---

**最后更新**: 2025-01-27  
**维护者**: AI Agent Team

