# 采集新闻

使用 Firecrawl 采集指定主题的新闻。

## 执行步骤

### 1. 确认采集参数

请明确以下信息：
- 新闻主题/关键词
- 采集数量（默认 10 条）
- 时间范围（可选）
- 新闻来源（可选）

### 2. 调用采集工具

使用 Firecrawl MCP 工具进行采集：

```python
from firecrawl_client import FirecrawlClient

client = FirecrawlClient()
news = client.search_news(
    query="关键词",
    limit=10,
    sources=["web"]
)
```

### 3. 数据处理

对采集到的新闻进行处理：
- 去重
- 格式化
- 提取关键信息
- 保存到数据库

### 4. 结果验证

验证采集结果：
- 检查数据完整性
- 验证数据质量
- 确认保存成功

## 采集配置

### 基础配置

```json
{
  "query": "新闻主题",
  "limit": 10,
  "sources": ["web"],
  "scrapeOptions": {
    "formats": ["markdown"],
    "onlyMainContent": true
  }
}
```

### 高级配置

```json
{
  "query": "新闻主题",
  "limit": 20,
  "sources": ["web", "news"],
  "scrapeOptions": {
    "formats": ["markdown", "html"],
    "onlyMainContent": true,
    "removeBase64Images": true
  },
  "filters": {
    "dateRange": "7d",
    "language": "zh"
  }
}
```

## 数据处理流程

### 1. 原始数据提取

```python
def extract_news_data(raw_data):
    """提取新闻关键信息"""
    return {
        'title': raw_data.get('title'),
        'content': raw_data.get('markdown'),
        'url': raw_data.get('url'),
        'published_at': raw_data.get('metadata', {}).get('publishedTime'),
        'source': raw_data.get('metadata', {}).get('sourceURL')
    }
```

### 2. 数据清洗

```python
def clean_news_data(news_data):
    """清洗新闻数据"""
    # 去除 HTML 标签
    # 标准化日期格式
    # 去除特殊字符
    # 验证必填字段
    return cleaned_data
```

### 3. 数据去重

```python
def deduplicate_news(news_list):
    """新闻去重"""
    # 基于 URL 去重
    # 基于标题相似度去重
    # 基于内容相似度去重
    return unique_news
```

### 4. 数据保存

```python
def save_news(news_data):
    """保存新闻到数据库"""
    # 保存到 MySQL
    # 更新索引
    # 记录日志
    return success
```

## 错误处理

### 常见错误

1. **API 限流**
   - 错误：`429 Too Many Requests`
   - 解决：添加延迟，使用速率限制

2. **网络超时**
   - 错误：`Timeout Error`
   - 解决：增加超时时间，重试机制

3. **数据格式错误**
   - 错误：`Invalid Data Format`
   - 解决：验证数据格式，添加异常处理

4. **数据库连接失败**
   - 错误：`Database Connection Error`
   - 解决：检查数据库配置，重试连接

### 错误处理示例

```python
import time
from typing import List, Dict

def collect_news_with_retry(query: str, max_retries: int = 3) -> List[Dict]:
    """带重试的新闻采集"""
    for attempt in range(max_retries):
        try:
            news = client.search_news(query=query)
            return news
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f"采集失败，{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"采集失败，已达到最大重试次数: {e}")
                raise
```

## 输出格式

### 📊 采集结果摘要

- 采集主题：XXX
- 采集数量：X 条
- 成功：X 条
- 失败：X 条
- 去重后：X 条

### 📝 新闻列表

列出采集到的新闻（标题、来源、时间）

### ⚠️ 问题和警告

列出采集过程中遇到的问题

### 💾 保存结果

- 数据库记录数：X
- 文件保存路径：XXX
- 日志文件：XXX

## 使用示例

### 示例 1：基础采集

```
/collect-news
采集关于"人工智能"的最新新闻，限制 10 条
```

### 示例 2：指定来源

```
/collect-news
采集关于"区块链"的新闻，来源：tech.sina.com.cn，限制 20 条
```

### 示例 3：批量采集

```
/collect-news
批量采集以下主题的新闻：
1. 人工智能
2. 机器学习
3. 深度学习
每个主题 5 条
```

## 注意事项

- 遵守 Firecrawl API 的速率限制
- 确保 API 密钥已配置
- 采集前检查数据库连接
- 定期清理过期数据
- 监控采集日志

## 相关文档

- [Firecrawl API 文档](../../docs/Firecrawl官方文档/)
- [新闻采集器使用指南](../../docs/使用指南/新闻采集用户指南.md)
- [Firecrawl 集成方案](../../docs/集成方案/Firecrawl集成方案评估.md)


