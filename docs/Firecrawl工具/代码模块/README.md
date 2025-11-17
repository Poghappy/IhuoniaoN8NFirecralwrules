# 代码模块

> **最后更新**: 2025-01-27

## 📋 目录说明

本目录包含 Firecrawl 工具的核心代码模块，包括数据采集、处理、API 集成和任务调度等功能。

## 📚 文件列表

### 核心模块

#### 数据采集
- [firecrawl-collector.py](./firecrawl-collector.py) - Firecrawl 数据采集器
  - 单页抓取
  - 批量爬取
  - 结构化数据提取

#### 数据处理
- [data-processing.py](./data-processing.py) - 数据处理和转换模块
  - 内容清洗和过滤
  - 自动分类和标签提取
  - 摘要生成
  - 格式转换

#### API 集成
- [api-integration.py](./api-integration.py) - 火鸟门户 API 集成
  - 内容发布和管理
  - 错误处理和重试
  - 批量操作支持
  - 状态同步

#### 任务调度
- [task-scheduler.py](./task-scheduler.py) - 任务调度器
  - 定时任务调度
  - 任务队列管理
  - 并发控制
  - 任务重试机制

#### 配置管理
- [firecrawl-config.py](./firecrawl-config.py) - Firecrawl 配置管理
- [config-example.json](./config-example.json) - 配置示例文件

#### 测试
- [integration-test.py](./integration-test.py) - 集成测试脚本

## 🚀 快速开始

### 基本使用

#### 1. 数据采集
```python
from firecrawl_collector import FirecrawlCollector

collector = FirecrawlCollector(api_key="your-api-key")
result = collector.scrape("https://example.com")
```

#### 2. 数据处理
```python
from data_processing import DataProcessor

processor = DataProcessor()
processed = processor.process(raw_data)
```

#### 3. API 集成
```python
from api_integration import HuoniaoAPIClient

client = HuoniaoAPIClient(
    base_url="https://api.example.com",
    api_key="your-key"
)
result = client.publish_article(article_data)
```

#### 4. 任务调度
```python
from task_scheduler import TaskScheduler

scheduler = TaskScheduler()
scheduler.add_task(task_func, schedule="0 0 * * *")
scheduler.start()
```

## 📖 详细文档

### 模块文档
- [Firecrawl 采集器](./firecrawl-collector.py) - 查看源代码了解详细用法
- [数据处理模块](./data-processing.py) - 数据处理功能说明
- [API 集成模块](./api-integration.py) - API 集成详细文档
- [任务调度器](./task-scheduler.py) - 任务调度使用说明

### 配置说明
- [配置示例](./config-example.json) - 查看配置示例
- [配置管理](./firecrawl-config.py) - 配置加载和管理

## 🔧 开发指南

### 运行测试
```bash
# 运行集成测试
python integration-test.py

# 运行单元测试（在项目根目录）
pytest tests/ -v
```

### 代码规范
- 遵循 PEP 8 代码风格
- 使用类型提示
- 编写文档字符串
- 添加单元测试

## 🔗 相关链接

- [返回项目首页](../README.md)
- [快速开始指南](../QUICKSTART.md)
- [代码文件](../code/)
- [测试文件](../tests/)

---

**维护者**: AI Agent Team

