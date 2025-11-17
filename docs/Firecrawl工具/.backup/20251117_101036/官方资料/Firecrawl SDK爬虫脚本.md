# Firecrawl SDK 爬虫脚本

**功能：** 网页抓取、批量爬取、结构化数据提取

**作者：** Trae IDE Agent

**创建时间：** 2025-01-17

## 概述

这是一个完整的 Firecrawl SDK Python 爬虫脚本，支持单页面抓取、批量网站爬取和结构化数据提取功能。

## 主要功能

- 🔍 **单页面抓取** - 抓取指定URL的内容
- 🕷️ **批量网站爬取** - 爬取整个网站的多个页面
- 📊 **结构化数据提取** - 根据自定义schema提取结构化数据
- 💾 **多格式保存** - 支持JSON、Markdown、文本格式保存
- ⚙️ **灵活配置** - 支持自定义标签过滤、输出格式等

## 代码实现

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl SDK 爬虫脚本
功能：网页抓取、批量爬取、结构化数据提取、API集成
作者：Trae IDE Agent
创建时间：2025-01-17
版本：v2.0 - 增加API集成功能
"""

import os
import json
import time
import requests
import logging
from typing import List, Dict, Any, Optional, Union, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urljoin, urlparse
import hashlib
import re
from pathlib import Path
from firecrawl import FirecrawlApp

@dataclass
class ScrapingConfig:
    """爬取配置类"""
    api_key: str
    output_format: List[str] = None  # ["markdown", "html", "structured"]
    max_pages: int = 10
    include_tags: List[str] = None
    exclude_tags: List[str] = None
    wait_for: int = 0  # 等待时间（毫秒）
    
    def __post_init__(self):
        if self.output_format is None:
            self.output_format = ["markdown"]
        if self.include_tags is None:
            self.include_tags = []
        if self.exclude_tags is None:
            self.exclude_tags = ["nav", "footer", "script", "style"]

class FirecrawlScraper:
    """Firecrawl 爬虫类"""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        [self.app](http://self.app) = FirecrawlApp(api_key=config.api_key)
        
    def scrape_single_page(self, url: str) -> Optional[Dict[str, Any]]:
        """抓取单个页面"""
        try:
            options = {
                'formats': self.config.output_format,
                'includeTags': self.config.include_tags,
                'excludeTags': self.config.exclude_tags,
                'waitFor': self.config.wait_for
            }
            
            result = [self.app](http://self.app).scrape_url(url, options)
            return result
            
        except Exception as e:
            print(f"抓取失败: {str(e)}")
            return None
    
    def crawl_website(self, url: str) -> List[Dict[str, Any]]:
        """爬取整个网站"""
        try:
            options = {
                'formats': self.config.output_format,
                'includeTags': self.config.include_tags,
                'excludeTags': self.config.exclude_tags,
                'limit': self.config.max_pages
            }
            
            results = [self.app](http://self.app).crawl_url(url, options)
            return results
            
        except Exception as e:
            print(f"爬取失败: {str(e)}")
            return []

# ================== API 集成模块 ==================

class PublishStatus(Enum):
    """发布状态枚举"""
    DRAFT = "draft"              # 草稿
    PUBLISHED = "published"      # 已发布
    SCHEDULED = "scheduled"      # 定时发布
    ARCHIVED = "archived"        # 已归档
    DELETED = "deleted"          # 已删除

class ContentType(Enum):
    """内容类型枚举"""
    ARTICLE = "article"          # 文章
    NEWS = "news"                # 新闻
    BLOG = "blog"                # 博客
    ANNOUNCEMENT = "announcement" # 公告

@dataclass
class APIConfig:
    """API配置"""
    # 基础配置
    base_url: str
    api_key: str
    timeout: int = 30
    
    # 重试配置
    max_retries: int = 3
    retry_delay: float = 1.0
    backoff_factor: float = 2.0
    
    # 请求配置
    user_agent: str = "Firecrawl-HuoNiao-Integration/1.0"
    verify_ssl: bool = True
    
    # 限流配置
    rate_limit: int = 60  # 每分钟请求数
    rate_window: int = 60  # 时间窗口（秒）
    
    # 默认配置
    default_category_id: Optional[int] = None
    default_author_id: Optional[int] = None
    default_status: PublishStatus = PublishStatus.DRAFT
    
    def __post_init__(self):
        """配置验证"""
        if not self.base_url:
            raise ValueError("base_url不能为空")
        if not self.api_key:
            raise ValueError("api_key不能为空")
            
        # 确保base_url以/结尾
        if not self.base_url.endswith('/'):
            self.base_url += '/'

@dataclass
class PublishRequest:
    """发布请求"""
    title: str
    content: str
    
    # 可选字段
    summary: Optional[str] = None
    category_id: Optional[int] = None
    author_id: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    
    # 发布配置
    status: PublishStatus = PublishStatus.DRAFT
    publish_time: Optional[datetime] = None
    
    # SEO配置
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: List[str] = field(default_factory=list)
    
    # 媒体配置
    featured_image: Optional[str] = None
    images: List[str] = field(default_factory=list)
    
    # 元数据
    source_url: Optional[str] = None
    external_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_api_data(self) -> Dict[str, Any]:
        """转换为API数据格式"""
        data = {
            'title': self.title,
            'content': self.content,
            'status': self.status.value
        }
        
        # 添加可选字段
        if self.summary:
            data['summary'] = self.summary
        if self.category_id:
            data['category_id'] = self.category_id
        if [self.author](http://self.author)_id:
            data['author_id'] = [self.author](http://self.author)_id
        if self.tags:
            data['tags'] = self.tags
        if self.publish_time:
            data['publish_time'] = self.publish_time.isoformat()
            
        # SEO字段
        if self.seo_title:
            data['seo_title'] = self.seo_title
        if self.seo_description:
            data['seo_description'] = self.seo_description
        if self.seo_keywords:
            data['seo_keywords'] = self.seo_keywords
            
        # 媒体字段
        if self.featured_image:
            data['featured_image'] = self.featured_image
        if self.images:
            data['images'] = self.images
            
        # 元数据
        if self.source_url:
            data['source_url'] = self.source_url
        if self.external_id:
            data['external_id'] = self.external_id
        if self.metadata:
            data['metadata'] = self.metadata
            
        return data

@dataclass
class PublishResponse:
    """发布响应"""
    success: bool
    article_id: Optional[int] = None
    message: Optional[str] = None
    error_code: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_api_response(cls, response_data: Dict[str, Any]) -> 'PublishResponse':
        """从API响应创建对象"""
        return cls(
            success=response_data.get('success', False),
            article_id=response_data.get('data', {}).get('id'),
            message=response_data.get('message'),
            error_code=response_data.get('error_code'),
            data=response_data.get('data')
        )

class RateLimiter:
    """速率限制器"""
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.logger = logging.getLogger(__name__)
    
    def wait_if_needed(self):
        """如果需要，等待直到可以发送请求"""
        now = time.time()
        
        # 清理过期的请求记录
        self.requests = [req_time for req_time in self.requests
                        if now - req_time < self.time_window]
        
        # 检查是否超过限制
        if len(self.requests) >= self.max_requests:
            # 计算需要等待的时间
            oldest_request = min(self.requests)
            wait_time = self.time_window - (now - oldest_request)
            
            if wait_time > 0:
                [self.logger.info](http://self.logger.info)(f"达到速率限制，等待 {wait_time:.2f} 秒")
                time.sleep(wait_time)
        
        # 记录当前请求
        self.requests.append(now)

class HuoNiaoAPIClient:
    """火鸟门户API客户端"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(config.rate_limit, config.rate_window)
        self.logger = logging.getLogger(__name__)
        
        # 设置默认请求头
        self.session.headers.update({
            'User-Agent': config.user_agent,
            'Authorization': f'Bearer {config.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # SSL验证
        self.session.verify = config.verify_ssl
    
    def _make_request(self, method: str, endpoint: str,
                     data: Optional[Dict[str, Any]] = None,
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """发送API请求"""
        url = urljoin(self.config.base_url, endpoint)
        
        for attempt in range(self.config.max_retries + 1):
            try:
                # 速率限制
                self.rate_limiter.wait_if_needed()
                
                # 发送请求
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    timeout=self.config.timeout
                )
                
                # 检查响应状态
                response.raise_for_status()
                
                # 解析响应
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {'success': True, 'data': response.text}
                    
            except requests.RequestException as e:
                self.logger.warning(f"请求失败 (尝试 {attempt + 1}/{self.config.max_retries + 1}): {str(e)}")
                
                if attempt < self.config.max_retries:
                    # 指数退避
                    delay = self.config.retry_delay * (self.config.backoff_factor ** attempt)
                    time.sleep(delay)
                else:
                    raise
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            response = self._make_request('GET', 'api/system/status')
            return response.get('success', False)
        except Exception as e:
            self.logger.error(f"连接测试失败: {str(e)}")
            return False
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """获取分类列表"""
        try:
            response = self._make_request('GET', 'api/categories')
            return response.get('data', [])
        except Exception as e:
            self.logger.error(f"获取分类失败: {str(e)}")
            return []
    
    def publish_article(self, request: PublishRequest) -> PublishResponse:
        """发布文章"""
        try:
            data = [request.to](http://request.to)_api_data()
            response = self._make_request('POST', 'api/articles', data=data)
            return PublishResponse.from_api_response(response)
        except Exception as e:
            self.logger.error(f"发布文章失败: {str(e)}")
            return PublishResponse(
                success=False,
                message=f"发布失败: {str(e)}",
                error_code="PUBLISH_ERROR"
            )
    
    def update_article(self, article_id: int, request: PublishRequest) -> PublishResponse:
        """更新文章"""
        try:
            data = [request.to](http://request.to)_api_data()
            response = self._make_request('PUT', f'api/articles/{article_id}', data=data)
            return PublishResponse.from_api_response(response)
        except Exception as e:
            self.logger.error(f"更新文章失败: {str(e)}")
            return PublishResponse(
                success=False,
                message=f"更新失败: {str(e)}",
                error_code="UPDATE_ERROR"
            )
    
    def delete_article(self, article_id: int) -> PublishResponse:
        """删除文章"""
        try:
            response = self._make_request('DELETE', f'api/articles/{article_id}')
            return PublishResponse.from_api_response(response)
        except Exception as e:
            self.logger.error(f"删除文章失败: {str(e)}")
            return PublishResponse(
                success=False,
                message=f"删除失败: {str(e)}",
                error_code="DELETE_ERROR"
            )
    
    def search_articles(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索文章"""
        try:
            params = {'q': query, 'limit': limit}
            response = self._make_request('GET', 'api/articles/search', params=params)
            return response.get('data', [])
        except Exception as e:
            self.logger.error(f"搜索文章失败: {str(e)}")
            return []
    
    def batch_publish(self, requests: List[PublishRequest]) -> List[PublishResponse]:
        """批量发布文章"""
        responses = []
        
        for i, request in enumerate(requests):
            [self.logger.info](http://self.logger.info)(f"批量发布进度: {i + 1}/{len(requests)}")
            response = self.publish_article(request)
            responses.append(response)
            
            # 如果失败，记录错误但继续处理
            if not response.success:
                self.logger.error(f"批量发布第 {i + 1} 项失败: {response.message}")
        
        return responses

class APIIntegration:
    """API集成主类"""
    
    def __init__(self, firecrawl_config: ScrapingConfig, api_config: APIConfig):
        self.firecrawl_config = firecrawl_config
        self.api_config = api_config
        self.scraper = FirecrawlScraper(firecrawl_config)
        self.api_client = HuoNiaoAPIClient(api_config)
        self.logger = logging.getLogger(__name__)
        
        # 发布统计
        self.stats = {
            'total_processed': 0,
            'successful_publishes': 0,
            'failed_publishes': 0,
            'skipped_items': 0
        }
    
    def scrape_and_publish(self, url: str, auto_publish: bool = False) -> PublishResponse:
        """抓取页面并发布到API"""
        try:
            self.stats['total_processed'] += 1
            
            # 抓取数据
            raw_data = self.scraper.scrape_single_page(url)
            
            if not raw_data:
                self.logger.warning(f"抓取失败，跳过发布: {url}")
                self.stats['skipped_items'] += 1
                return PublishResponse(
                    success=False,
                    message="抓取失败",
                    error_code="SCRAPING_ERROR"
                )
            
            # 创建发布请求
            publish_request = PublishRequest(
                title=raw_data.get('title', '无标题'),
                content=raw_data.get('content', ''),
                summary=raw_data.get('metadata', {}).get('description', ''),
                source_url=url,
                status=PublishStatus.PUBLISHED if auto_publish else self.api_config.default_status,
                metadata={
                    'scraped_at': [datetime.now](http://datetime.now)(timezone.utc).isoformat(),
                    'firecrawl_source': True,
                    'original_url': url
                }
            )
            
            # 发布文章
            response = self.api_client.publish_article(publish_request)
            
            if response.success:
                self.stats['successful_publishes'] += 1
                [self.logger.info](http://self.logger.info)(f"文章发布成功: {publish_request.title} (ID: {response.article_id})")
            else:
                self.stats['failed_publishes'] += 1
                self.logger.error(f"文章发布失败: {response.message}")
            
            return response
            
        except Exception as e:
            self.stats['failed_publishes'] += 1
            self.logger.error(f"抓取和发布失败: {str(e)}")
            return PublishResponse(
                success=False,
                message=f"抓取和发布失败: {str(e)}",
                error_code="INTEGRATION_ERROR"
            )
    
    def batch_scrape_and_publish(self, urls: List[str], auto_publish: bool = False) -> List[PublishResponse]:
        """批量抓取和发布"""
        responses = []
        
        for i, url in enumerate(urls):
            [self.logger.info](http://self.logger.info)(f"批量处理进度: {i + 1}/{len(urls)} - {url}")
            response = self.scrape_and_publish(url, auto_publish)
            responses.append(response)
            
            # 添加延迟以避免过度请求
            time.sleep(1)
        
        return responses
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.stats.copy()
        
        if stats['total_processed'] > 0:
            stats['success_rate'] = stats['successful_publishes'] / stats['total_processed']
            stats['failure_rate'] = stats['failed_publishes'] / stats['total_processed']
            stats['skip_rate'] = stats['skipped_items'] / stats['total_processed']
        else:
            stats['success_rate'] = 0.0
            stats['failure_rate'] = 0.0
            stats['skip_rate'] = 0.0
        
        return stats

# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=[logging.INFO](http://logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Firecrawl配置
    scraping_config = ScrapingConfig(
        api_key="your_firecrawl_api_key_here",
        output_format=["markdown", "html"],
        max_pages=5
    )
    
    # API配置
    api_config = APIConfig(
        base_url="[https://api.huoniao.com](https://api.huoniao.com)",
        api_key="your_huoniao_api_key_here",
        default_category_id=1,
        default_author_id=1,
        default_status=PublishStatus.DRAFT
    )
    
    # 创建集成实例
    integration = APIIntegration(scraping_config, api_config)
    
    # 测试连接
    if integration.api_client.test_connection():
        print("API连接成功")
        
        # 抓取并发布单个页面
        response = integration.scrape_and_publish("[https://example.com](https://example.com)", auto_publish=False)
        
        if response.success:
            print(f"文章发布成功，ID: {response.article_id}")
        else:
            print(f"文章发布失败: {response.message}")
        
        # 打印统计信息
        stats = integration.get_statistics()
        print("\n统计信息:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print("API连接失败")
```

## 使用说明

### 1. 安装依赖

```bash
pip install firecrawl-py
```

### 2. 配置API密钥

设置环境变量：

```bash
export FIRECRAWL_API_KEY="your-api-key-here"
```

或在脚本中直接修改 `API_KEY` 变量。

### 3. 运行脚本

```bash
python firecrawl_
```

## 配置选项

- **`output_format`** - 输出格式：`["markdown", "html", "structured"]`
- **`max_pages`** - 最大爬取页面数
- **`include_tags`** - 包含的HTML标签
- **`exclude_tags`** - 排除的HTML标签
- **`wait_for`** - 等待时间（毫秒）

## 输出文件

所有结果文件将保存在 `output/` 目录中：

- `single_page_result.json` - 单页面抓取结果
- `single_page_[content.md](http://content.md)` - 单页面Markdown内容
- `website_crawl_results.json` - 网站爬取结果
- `structured_data.json` - 结构化数据提取结果

## 相关 Firecrawl 项目

基于 [Firecrawl GitHub 组织](https://github.com/orgs/firecrawl/repositories?type=all)的官方和社区项目，以下是一些重要的相关仓库：

### 核心项目

- [**firecrawl**](https://github.com/firecrawl/firecrawl) ⭐ 52k
    
    主项目 - 面向AI的Web数据API，将整个网站转换为LLM就绪的markdown或结构化数据
    
    `TypeScript` • `GNU AGPL v3.0`
    
- [**firecrawl-mcp-server**](https://github.com/firecrawl/firecrawl-mcp-server) ⭐ 4.3k
    
    官方 Firecrawl MCP 服务器 - 为 Cursor、Claude 和其他LLM客户端添加强大的网页抓取功能
    
    `JavaScript` • `MIT License`
    
- [**firecrawl-docs**](https://github.com/firecrawl/firecrawl-docs)
    
    Firecrawl 官方文档
    
    `MDX`
    

### SDK 和集成

- [**firecrawl-java-sdk**](https://github.com/firecrawl/firecrawl-java-sdk)
    
    Java SDK
    
    `Java` • `MIT License`
    
- [**firecrawl-go**](https://github.com/firecrawl/firecrawl-go)
    
    Go SDK
    
    `Go` • `MIT License`
    
- [**n8n-nodes-firecrawl**](https://github.com/firecrawl/n8n-nodes-firecrawl)
    
    n8n 节点集成
    
    `TypeScript` • `MIT License`
    

### 应用示例和工具

- [**firecrawl-app-examples**](https://github.com/firecrawl/firecrawl-app-examples) ⭐ 520
    
    完整的应用示例集合，包括使用 Firecrawl 开发的网站和其他项目
    
    `Jupyter Notebook`
    
- [**fireplexity**](https://github.com/firecrawl/fireplexity) ⭐ 1.4k
    
    基于 Firecrawl 的超快AI搜索引擎，支持实时引用、流式响应和实时数据
    
    `TypeScript`
    
- [**open-lovable**](https://github.com/firecrawl/open-lovable) ⭐ 17k
    
    在几秒钟内克隆并重新创建任何网站为现代React应用
    
    `TypeScript` • `MIT License`
    

### 专业工具

- [**firecrawl-observer**](https://github.com/firecrawl/firecrawl-observer) ⭐ 279
    
    使用 Firecrawl 强大的变化检测功能监控网站变化
    
    `TypeScript`
    
- [**fire-enrich**](https://github.com/firecrawl/fire-enrich) ⭐ 717
    
    AI驱动的数据丰富工具，将邮件转换为包含公司简介、资金数据、技术栈等的丰富数据集
    
    `TypeScript` • `MIT License`
    
- [**firesearch**](https://github.com/firecrawl/firesearch) ⭐ 351
    
    AI驱动的深度研究工具，使用 Firecrawl 和 LangGraph 提供引用的综合结果
    
    `TypeScript`
    
- [**firestarter**](https://github.com/firecrawl/firestarter) ⭐ 463
    
    为任何网站即时创建具有RAG搜索功能的AI聊天机器人
    
    `TypeScript`
    

### 实用工具

- [**llmstxt-generator**](https://github.com/firecrawl/llmstxt-generator) ⭐ 457
    
    LLMs.txt 生成器
    
    `TypeScript`
    
- [**open-researcher**](https://github.com/firecrawl/open-researcher) ⭐ 236
    
    可视化AI研究助手，显示实时思考过程
    
    `TypeScript`
    
- [**firecrawl-migrator**](https://github.com/firecrawl/firecrawl-migrator)
    
    迁移工具
    
    `TypeScript`
    

> 💡 **提示：** 这些项目展示了 Firecrawl 生态系统的丰富性，涵盖了从基础SDK到复杂应用的各种用例。您可以参考这些项目来扩展您的爬虫脚本功能。
> 

---

> **注意：** 使用前请确保已获取有效的 Firecrawl API 密钥。
> 

## 代码库

以下是 Firecrawl SDK 爬虫脚本的完整代码实现:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl SDK 爬虫脚本
功能：网页抓取、批量爬取、结构化数据提取
作者：Trae IDE Agent
创建时间：2025-01-17
"""

import os
import json
import time
import argparse
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from urllib.parse import urlparse
from firecrawl import FirecrawlApp

@dataclass
class ScrapingConfig:
    """爬取配置类"""
    api_key: str
    output_format: List[str] = None  # ["markdown", "html", "structured"]
    max_pages: int = 10
    include_tags: List[str] = None
    exclude_tags: List[str] = None
    wait_for: int = 0  # 等待时间（毫秒）
    
    def __post_init__(self):
        if self.output_format is None:
            self.output_format = ["markdown"]
        if self.include_tags is None:
            self.include_tags = []
        if self.exclude_tags is None:
            self.exclude_tags = ["nav", "footer", "script", "style"]

class FirecrawlScraper:
    """Firecrawl 爬虫类"""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.client = FirecrawlApp(api_key=config.api_key)
        self.output_dir = "output"
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def scrape_single_page(self, url: str) -> Dict[str, Any]:
        """抓取单个页面"""
        print(f"正在抓取页面: {url}")
        
        result = self.client.fetch(
            url=url,
            output_format=self.config.output_format,
            include_tags=self.config.include_tags,
            exclude_tags=self.config.exclude_tags,
            wait_for=self.config.wait_for
        )
        
        # 保存结果
        with open(f"{self.output_dir}/single_page_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # 如果有markdown格式，保存为md文件
        if "markdown" in self.config.output_format and "markdown" in result:
            with open(f"{self.output_dir}/single_page_content.md", "w", encoding="utf-8") as f:
                f.write(result["markdown"])
        
        return result
    
    def crawl_website(self, start_url: str, depth: int = 1) -> List[Dict[str, Any]]:
        """爬取整个网站"""
        print(f"正在爬取网站: {start_url}，深度: {depth}")
        
        domain = urlparse(start_url).netloc
        results = []
        
        crawl_result = self.client.crawl(
            url=start_url,
            max_pages=self.config.max_pages,
            max_depth=depth,
            same_domain=True,
            output_format=self.config.output_format,
            include_tags=self.config.include_tags,
            exclude_tags=self.config.exclude_tags
        )
        
        results.extend(crawl_result)
        
        # 保存结果
        with open(f"{self.output_dir}/website_crawl_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return results
    
    def extract_structured_data(self, url: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """提取结构化数据"""
        print(f"正在从 {url} 提取结构化数据")
        
        result = self.client.extract(
            url=url,
            schema=schema,
            wait_for=self.config.wait_for
        )
        
        # 保存结果
        with open(f"{self.output_dir}/structured_data.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return result
    
    def batch_process(self, urls: List[str]) -> List[Dict[str, Any]]:
        """批量处理多个URL"""
        results = []
        for url in urls:
            try:
                result = self.scrape_single_page(url)
                results.append({
                    "url": url,
                    "success": True,
                    "data": result
                })
            except Exception as e:
                results.append({
                    "url": url,
                    "success": False,
                    "error": str(e)
                })
            # 添加延迟避免请求过快
            time.sleep(1)
        
        return results

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Firecrawl爬虫脚本")
    parser.add_argument("--url", type=str, help="要抓取的URL")
    parser.add_argument("--mode", type=str, default="single", 
                        choices=["single", "crawl", "structured", "batch"],
                        help="抓取模式: single(单页面), crawl(网站爬取), structured(结构化数据), batch(批量处理)")
    parser.add_argument("--depth", type=int, default=1, help="爬取深度")
    parser.add_argument("--max-pages", type=int, default=10, help="最大爬取页面数")
    parser.add_argument("--url-list", type=str, help="URL列表文件路径(用于批量处理)")
    parser.add_argument("--schema", type=str, help="结构化数据提取schema文件路径")
    
    args = parser.parse_args()
    
    # 获取API密钥
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        api_key = input("请输入您的Firecrawl API密钥: ")
    
    config = ScrapingConfig(
        api_key=api_key,
        output_format=["markdown", "html", "structured"],
        max_pages=args.max_pages
    )
    
    scraper = FirecrawlScraper(config)
    
    if args.mode == "single":
        if not args.url:
            args.url = input("请输入要抓取的URL: ")
        scraper.scrape_single_page(args.url)
    
    elif args.mode == "crawl":
        if not args.url:
            args.url = input("请输入起始URL: ")
        scraper.crawl_website(args.url, args.depth)
    
    elif args.mode == "structured":
        if not args.url:
            args.url = input("请输入要抓取的URL: ")
        if not args.schema:
            args.schema = input("请输入schema文件路径: ")
        
        with open(args.schema, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        scraper.extract_structured_data(args.url, schema)
    
    elif args.mode == "batch":
        if not args.url_list:
            args.url_list = input("请输入URL列表文件路径: ")
        
        with open(args.url_list, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        
        scraper.batch_process(urls)

if __name__ == "__main__":
    main()

```

### 示例 Schema 文件

```json
{
  "title": {
    "selector": "h1, .article-title, .entry-title",
    "type": "text"
  },
  "content": {
    "selector": "article, .post-content, .entry-content",
    "type": "html"
  },
  "author": {
    "selector": ".author, .byline",
    "type": "text"
  },
  "published_date": {
    "selector": ".date, time, .published",
    "type": "text"
  },
  "categories": {
    "selector": ".categories a, .tags a",
    "type": "list"
  },
  "images": {
    "selector": "img",
    "type": "list",
    "attribute": "src"
  }
}
```

### URL 列表文件示例

```
https://example.com/page1
https://example.com/page2
https://example.com/blog/article1
https://example.com/blog/article2
```

### 使用示例

```bash
# 单页面抓取
python firecrawl_scraper.py --mode single --url https://example.com

# 网站爬取
python firecrawl_scraper.py --mode crawl --url https://example.com --depth 2 --max-pages 20

# 结构化数据提取
python firecrawl_scraper.py --mode structured --url https://example.com/article --schema schema.json

# 批量处理
python firecrawl_scraper.py --mode batch --url-list urls.txt
```