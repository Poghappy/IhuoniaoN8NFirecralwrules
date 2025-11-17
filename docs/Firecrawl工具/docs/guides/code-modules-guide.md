# 代码模块使用指南

> **版本**: v1.0  
> **最后更新**: 2025-01-27

## 📋 概述

本指南介绍如何使用 Firecrawl 工具项目中的各个代码模块。

## 🎯 模块概览

### 核心模块

1. **Firecrawl 采集器** (`firecrawl-collector.py`)
   - 网页内容采集
   - 批量爬取
   - 结构化数据提取

2. **数据处理模块** (`data-processing.py`)
   - 内容清洗
   - 格式转换
   - 分类和标签

3. **API 集成模块** (`api-integration.py`)
   - 内容发布
   - 数据同步
   - 错误处理

4. **任务调度器** (`task-scheduler.py`)
   - 定时任务
   - 队列管理
   - 并发控制

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用示例

#### 1. 单页采集

```python
from 代码模块.firecrawl_collector import FirecrawlCollector

# 初始化采集器
collector = FirecrawlCollector(api_key="your-api-key")

# 采集单页
result = collector.scrape("https://example.com")
print(result.markdown)
```

#### 2. 批量爬取

```python
# 批量爬取网站
results = collector.crawl(
    url="https://example.com",
    max_pages=10,
    include_paths=["/blog/*"]
)
```

#### 3. 数据处理

```python
from 代码模块.data_processing import DataProcessor

processor = DataProcessor()
processed = processor.process(raw_data)
```

#### 4. 发布内容

```python
from 代码模块.api_integration import HuoniaoAPIClient

client = HuoniaoAPIClient(
    base_url="https://api.example.com",
    api_key="your-key"
)

result = client.publish_article({
    "title": "文章标题",
    "content": "文章内容",
    "category_id": 1
})
```

## 📖 详细文档

### Firecrawl 采集器

查看 [firecrawl-collector.py](../代码模块/firecrawl-collector.py) 了解详细用法。

### 数据处理模块

查看 [data-processing.py](../代码模块/data-processing.py) 了解数据处理功能。

### API 集成模块

查看 [api-integration.py](../代码模块/api-integration.py) 了解 API 集成详情。

### 任务调度器

查看 [task-scheduler.py](../代码模块/task-scheduler.py) 了解任务调度功能。

## 🔧 配置说明

### 环境变量

```bash
export FIRECRAWL_API_KEY="your-api-key"
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"
```

### 配置文件

使用 [config-example.json](../代码模块/config-example.json) 作为配置模板。

## 🧪 测试

### 运行单元测试

```bash
pytest tests/ -v
```

### 运行集成测试

```bash
pytest tests/test_integration.py -v
```

### 运行完整测试套件

```bash
pytest tests/ -v --cov=代码模块 --cov-report=html
```

## 🔗 相关链接

- [代码模块 README](../代码模块/README.md)
- [快速开始指南](../../QUICKSTART.md)
- [API 参考手册](../../官方资料/Firecrawl_API参考手册.md)

---

**维护者**: AI Agent Team

