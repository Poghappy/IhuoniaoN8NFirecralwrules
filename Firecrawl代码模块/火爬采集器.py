#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl数据采集模块

基于Firecrawl SDK实现的智能网页内容采集系统，支持单页抓取、批量爬取和结构化数据提取。
集成火鸟门户API，实现自动化新闻内容采集和发布。

作者: Trae IDE Agent
创建时间: 2025-01-17
版本: v1.0
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    from firecrawl import FirecrawlApp
except ImportError:
    print("请安装Firecrawl SDK: pip install firecrawl-py")
    raise

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class CollectorConfig:
    """采集器配置类"""
    api_key: str
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: int = 30
    concurrent_limit: int = 5
    enable_cache: bool = True
    cache_ttl: int = 3600  # 缓存时间（秒）
    output_format: str = "markdown"  # markdown, html, structured
    
    def __post_init__(self):
        if not self.api_key:
            raise ValueError("API密钥不能为空")


@dataclass
class ArticleData:
    """文章数据结构"""
    title: str
    content: str
    url: str
    summary: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    extracted_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.extracted_at:
            self.extracted_at = datetime.now().isoformat()
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CrawlResult:
    """爬取结果"""
    success: bool
    articles: List[ArticleData]
    errors: List[str]
    total_pages: int
    processed_pages: int
    start_time: str
    end_time: str
    duration: float
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'success': self.success,
            'articles': [asdict(article) for article in self.articles],
            'errors': self.errors,
            'total_pages': self.total_pages,
            'processed_pages': self.processed_pages,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration
        }


class FirecrawlCollector:
    """Firecrawl数据采集器"""
    
    def __init__(self, config: CollectorConfig):
        """初始化采集器
        
        Args:
            config: 采集器配置
        """
        self.config = config
        self.firecrawl = FirecrawlApp(api_key=config.api_key)
        self._cache = {} if config.enable_cache else None
        self._semaphore = asyncio.Semaphore(config.concurrent_limit)
        
        logger.info(f"Firecrawl采集器初始化完成，并发限制: {config.concurrent_limit}")
    
    async def scrape_single_page(self, url: str, **kwargs) -> Optional[ArticleData]:
        """抓取单个页面
        
        Args:
            url: 目标URL
            **kwargs: 额外的抓取参数
            
        Returns:
            ArticleData: 抓取的文章数据，失败时返回None
        """
        async with self._semaphore:
            try:
                # 检查缓存
                if self._cache and url in self._cache:
                    cache_time, cached_data = self._cache[url]
                    if time.time() - cache_time < self.config.cache_ttl:
                        logger.info(f"从缓存获取数据: {url}")
                        return cached_data
                
                logger.info(f"开始抓取页面: {url}")
                
                # 准备抓取参数
                scrape_params = {
                    'formats': [self.config.output_format],
                    'timeout': self.config.timeout * 1000,  # 转换为毫秒
                    **kwargs
                }
                
                # 执行抓取
                result = await self._retry_operation(
                    lambda: self.firecrawl.scrape(url, scrape_params)
                )
                
                if not result:
                    logger.error(f"抓取失败: {url}")
                    return None
                
                # 处理返回结果
                article_data = self._process_scrape_result(result, url)
                
                # 缓存结果
                if self._cache and article_data:
                    self._cache[url] = (time.time(), article_data)
                
                logger.info(f"页面抓取成功: {url}")
                return article_data
                
            except Exception as e:
                logger.error(f"抓取页面时发生错误 {url}: {str(e)}")
                return None
    
    async def crawl_website(self, base_url: str, **kwargs) -> CrawlResult:
        """爬取整个网站
        
        Args:
            base_url: 基础URL
            **kwargs: 额外的爬取参数
            
        Returns:
            CrawlResult: 爬取结果
        """
        start_time = datetime.now()
        articles = []
        errors = []
        
        try:
            logger.info(f"开始爬取网站: {base_url}")
            
            # 准备爬取参数
            crawl_params = {
                'formats': [self.config.output_format],
                'timeout': self.config.timeout * 1000,
                'limit': kwargs.get('limit', 10),
                'maxDepth': kwargs.get('max_depth', 2),
                **{k: v for k, v in kwargs.items() if k not in ['limit', 'max_depth']}
            }
            
            # 执行爬取
            result = await self._retry_operation(
                lambda: self.firecrawl.crawl(base_url, crawl_params)
            )
            
            if not result:
                errors.append(f"爬取网站失败: {base_url}")
            else:
                # 处理爬取结果
                if hasattr(result, 'data') and result.data:
                    for item in result.data:
                        try:
                            article = self._process_crawl_item(item)
                            if article:
                                articles.append(article)
                        except Exception as e:
                            error_msg = f"处理爬取项目时出错: {str(e)}"
                            errors.append(error_msg)
                            logger.error(error_msg)
                
                logger.info(f"网站爬取完成: {base_url}, 获取文章数: {len(articles)}")
            
        except Exception as e:
            error_msg = f"爬取网站时发生错误 {base_url}: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return CrawlResult(
            success=len(errors) == 0,
            articles=articles,
            errors=errors,
            total_pages=len(articles) + len(errors),
            processed_pages=len(articles),
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration=duration
        )
    
    async def extract_structured_data(self, url: str, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """结构化数据提取
        
        Args:
            url: 目标URL
            schema: 提取模式
            
        Returns:
            Dict: 提取的结构化数据
        """
        try:
            logger.info(f"开始结构化数据提取: {url}")
            
            # 准备提取参数
            extract_params = {
                'schema': schema,
                'timeout': self.config.timeout * 1000
            }
            
            # 执行提取
            result = await self._retry_operation(
                lambda: self.firecrawl.extract(url, extract_params)
            )
            
            if not result:
                logger.error(f"结构化数据提取失败: {url}")
                return None
            
            # 处理提取结果
            if hasattr(result, 'data'):
                logger.info(f"结构化数据提取成功: {url}")
                return result.data
            else:
                logger.warning(f"提取结果格式异常: {url}")
                return None
                
        except Exception as e:
            logger.error(f"结构化数据提取时发生错误 {url}: {str(e)}")
            return None
    
    async def batch_scrape(self, urls: List[str], **kwargs) -> List[Optional[ArticleData]]:
        """批量抓取页面
        
        Args:
            urls: URL列表
            **kwargs: 额外的抓取参数
            
        Returns:
            List[Optional[ArticleData]]: 抓取结果列表
        """
        logger.info(f"开始批量抓取，URL数量: {len(urls)}")
        
        tasks = [self.scrape_single_page(url, **kwargs) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"批量抓取异常 {urls[i]}: {str(result)}")
                processed_results.append(None)
            else:
                processed_results.append(result)
        
        success_count = sum(1 for r in processed_results if r is not None)
        logger.info(f"批量抓取完成，成功: {success_count}/{len(urls)}")
        
        return processed_results
    
    def save_results(self, results: Union[CrawlResult, List[ArticleData]], 
                    output_path: str, format: str = "json") -> bool:
        """保存抓取结果
        
        Args:
            results: 抓取结果
            output_path: 输出路径
            format: 输出格式 (json, csv, markdown)
            
        Returns:
            bool: 保存是否成功
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if isinstance(results, CrawlResult):
                data = results.to_dict()
            elif isinstance(results, list):
                data = {
                    'articles': [asdict(article) for article in results if article],
                    'total_count': len([a for a in results if a]),
                    'exported_at': datetime.now().isoformat()
                }
            else:
                raise ValueError("不支持的结果类型")
            
            if format.lower() == "json":
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            elif format.lower() == "csv":
                import pandas as pd
                if 'articles' in data:
                    df = pd.DataFrame(data['articles'])
                    df.to_csv(output_file, index=False, encoding='utf-8')
                else:
                    raise ValueError("CSV格式需要文章数据")
            elif format.lower() == "markdown":
                self._save_as_markdown(data, output_file)
            else:
                raise ValueError(f"不支持的输出格式: {format}")
            
            logger.info(f"结果保存成功: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存结果时发生错误: {str(e)}")
            return False
    
    async def _retry_operation(self, operation, max_retries: Optional[int] = None):
        """重试操作"""
        max_retries = max_retries or self.config.max_retries
        
        for attempt in range(max_retries + 1):
            try:
                return operation()
            except Exception as e:
                if attempt == max_retries:
                    logger.error(f"操作失败，已达到最大重试次数 {max_retries}: {str(e)}")
                    raise
                
                wait_time = self.config.retry_delay * (2 ** attempt)
                logger.warning(f"操作失败，{wait_time}秒后重试 (第{attempt + 1}次): {str(e)}")
                await asyncio.sleep(wait_time)
    
    def _process_scrape_result(self, result, url: str) -> Optional[ArticleData]:
        """处理抓取结果"""
        try:
            # 处理Document对象
            if hasattr(result, 'markdown'):
                content = getattr(result, 'markdown', '')
            elif hasattr(result, 'content'):
                content = getattr(result, 'content', '')
            else:
                content = str(result)
            
            # 获取元数据
            metadata = getattr(result, 'metadata', {}) if hasattr(result, 'metadata') else {}
            
            # 提取标题
            title = metadata.get('title', '')
            if not title and content:
                # 从内容中提取标题
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('#') or len(line) < 100):
                        title = line.lstrip('#').strip()
                        break
            
            if not title:
                title = f"页面内容 - {url}"
            
            return ArticleData(
                title=title,
                content=content,
                url=url,
                summary=metadata.get('description', ''),
                author=metadata.get('author', ''),
                publish_date=metadata.get('publishedTime', ''),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"处理抓取结果时出错: {str(e)}")
            return None
    
    def _process_crawl_item(self, item) -> Optional[ArticleData]:
        """处理爬取项目"""
        try:
            if hasattr(item, 'url'):
                url = item.url
            else:
                url = item.get('url', '') if isinstance(item, dict) else ''
            
            return self._process_scrape_result(item, url)
            
        except Exception as e:
            logger.error(f"处理爬取项目时出错: {str(e)}")
            return None
    
    def _save_as_markdown(self, data: Dict[str, Any], output_file: Path):
        """保存为Markdown格式"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# 抓取结果报告\n\n")
            f.write(f"**导出时间**: {data.get('exported_at', datetime.now().isoformat())}\n\n")
            
            if 'articles' in data:
                f.write(f"**文章总数**: {len(data['articles'])}\n\n")
                
                for i, article in enumerate(data['articles'], 1):
                    f.write(f"## {i}. {article.get('title', '无标题')}\n\n")
                    f.write(f"**URL**: {article.get('url', '')}\n\n")
                    if article.get('summary'):
                        f.write(f"**摘要**: {article['summary']}\n\n")
                    if article.get('author'):
                        f.write(f"**作者**: {article['author']}\n\n")
                    if article.get('publish_date'):
                        f.write(f"**发布时间**: {article['publish_date']}\n\n")
                    
                    content = article.get('content', '')
                    if content:
                        f.write(f"### 内容\n\n{content}\n\n")
                    
                    f.write("---\n\n")


# 使用示例和测试函数
async def example_usage():
    """使用示例"""
    # 配置采集器
    config = CollectorConfig(
        api_key="your-firecrawl-api-key",
        max_retries=3,
        concurrent_limit=3,
        output_format="markdown"
    )
    
    collector = FirecrawlCollector(config)
    
    # 示例1: 抓取单个页面
    print("=== 抓取单个页面 ===")
    article = await collector.scrape_single_page("https://firecrawl.dev/blog")
    if article:
        print(f"标题: {article.title}")
        print(f"内容长度: {len(article.content)}")
    
    # 示例2: 爬取整个网站
    print("\n=== 爬取整个网站 ===")
    crawl_result = await collector.crawl_website(
        "https://firecrawl.dev/blog",
        limit=5,
        max_depth=1
    )
    print(f"爬取成功: {crawl_result.success}")
    print(f"获取文章数: {len(crawl_result.articles)}")
    print(f"错误数: {len(crawl_result.errors)}")
    
    # 示例3: 结构化数据提取
    print("\n=== 结构化数据提取 ===")
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "author": {"type": "string"}
        }
    }
    
    structured_data = await collector.extract_structured_data(
        "https://firecrawl.dev/blog",
        schema
    )
    if structured_data:
        print(f"结构化数据: {structured_data}")
    
    # 示例4: 批量抓取
    print("\n=== 批量抓取 ===")
    urls = [
        "https://firecrawl.dev/blog",
        "https://docs.firecrawl.dev"
    ]
    
    batch_results = await collector.batch_scrape(urls)
    success_count = sum(1 for r in batch_results if r is not None)
    print(f"批量抓取完成: {success_count}/{len(urls)}")
    
    # 保存结果
    if crawl_result.articles:
        collector.save_results(
            crawl_result.articles,
            "output/crawl_results.json",
            "json"
        )
        print("结果已保存到 output/crawl_results.json")


if __name__ == "__main__":
    # 运行示例
    asyncio.run(example_usage())