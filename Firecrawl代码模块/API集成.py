#!/usr/bin/env python3
"""
API集成模块

负责将Firecrawl采集的数据推送到火鸟门户API，支持内容发布、
修改、删除、查询等操作，并提供错误处理、重试机制和数据映射功能。

主要功能：
- 火鸟门户API客户端
- 数据格式转换和映射
- 内容发布和管理
- 错误处理和重试
- 批量操作支持
- 状态同步

作者: Trae IDE Agent
创建时间: 2025-01-17
版本: v1.0
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
import logging
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests


# 导入本地模块
try:
    from .数据处理 import DataProcessor, ProcessedArticle
except ImportError:
    # 如果作为独立模块运行
    import sys

    sys.path.append(".")
    from 数据处理 import DataProcessor, ProcessedArticle


class PublishStatus(Enum):
    """发布状态枚举"""

    DRAFT = "draft"  # 草稿
    PUBLISHED = "published"  # 已发布
    SCHEDULED = "scheduled"  # 定时发布
    ARCHIVED = "archived"  # 已归档
    DELETED = "deleted"  # 已删除


class ContentType(Enum):
    """内容类型枚举"""

    ARTICLE = "article"  # 文章
    NEWS = "news"  # 新闻
    BLOG = "blog"  # 博客
    ANNOUNCEMENT = "announcement"  # 公告


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
        if not self.base_url.endswith("/"):
            self.base_url += "/"


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
        data: Dict[str, Any] = {
            "title": self.title,
            "content": self.content,
            "status": self.status.value,
        }

        # 添加可选字段
        if self.summary:
            data["summary"] = self.summary
        if self.category_id:
            data["category_id"] = self.category_id
        if self.author_id:
            data["author_id"] = self.author_id
        if self.tags:
            data["tags"] = self.tags
        if self.publish_time:
            data["publish_time"] = self.publish_time.isoformat()

        # SEO字段
        if self.seo_title:
            data["seo_title"] = self.seo_title
        if self.seo_description:
            data["seo_description"] = self.seo_description
        if self.seo_keywords:
            data["seo_keywords"] = self.seo_keywords

        # 媒体字段
        if self.featured_image:
            data["featured_image"] = self.featured_image
        if self.images:
            data["images"] = self.images

        # 元数据
        if self.source_url:
            data["source_url"] = self.source_url
        if self.external_id:
            data["external_id"] = self.external_id
        if self.metadata:
            data["metadata"] = self.metadata

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
    def from_api_response(cls, response_data: Dict[str, Any]) -> "PublishResponse":
        """从API响应创建对象"""
        return cls(
            success=response_data.get("success", False),
            article_id=response_data.get("data", {}).get("id"),
            message=response_data.get("message"),
            error_code=response_data.get("error_code"),
            data=response_data.get("data"),
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
        self.requests = [
            req_time for req_time in self.requests if now - req_time < self.time_window
        ]

        # 检查是否超过限制
        if len(self.requests) >= self.max_requests:
            # 计算需要等待的时间
            oldest_request = min(self.requests)
            wait_time = self.time_window - (now - oldest_request)

            if wait_time > 0:
                self.logger.info(f"达到速率限制，等待 {wait_time:.2f} 秒")
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
        self.session.headers.update(
            {
                "User-Agent": config.user_agent,
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # SSL验证
        self.session.verify = config.verify_ssl

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """发送API请求

        Args:
            method: HTTP方法
            endpoint: API端点
            data: 请求数据
            params: 查询参数

        Returns:
            Dict[str, Any]: 响应数据

        Raises:
            requests.RequestException: 请求异常
        """
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
                    timeout=self.config.timeout,
                )

                # 检查响应状态
                response.raise_for_status()

                # 解析响应
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {"success": True, "data": response.text}

            except requests.RequestException as e:
                self.logger.warning(
                    f"请求失败 (尝试 {attempt + 1}/{self.config.max_retries + 1}): {e!s}"
                )

                if attempt < self.config.max_retries:
                    # 指数退避
                    delay = self.config.retry_delay * (self.config.backoff_factor**attempt)
                    time.sleep(delay)
                else:
                    raise

        # 理论上不会到达这里，但为了类型检查
        raise requests.RequestException("请求失败")

    def test_connection(self) -> bool:
        """测试API连接

        Returns:
            bool: 连接是否成功
        """
        try:
            response = self._make_request("GET", "api/system/status")
            return response.get("success", False)
        except Exception as e:
            self.logger.error(f"连接测试失败: {e!s}")
            return False

    def get_categories(self) -> List[Dict[str, Any]]:
        """获取分类列表

        Returns:
            List[Dict[str, Any]]: 分类列表
        """
        try:
            response = self._make_request("GET", "api/categories")
            return response.get("data", [])
        except Exception as e:
            self.logger.error(f"获取分类失败: {e!s}")
            return []

    def get_authors(self) -> List[Dict[str, Any]]:
        """获取作者列表

        Returns:
            List[Dict[str, Any]]: 作者列表
        """
        try:
            response = self._make_request("GET", "api/authors")
            return response.get("data", [])
        except Exception as e:
            self.logger.error(f"获取作者失败: {e!s}")
            return []

    def publish_article(self, request: PublishRequest) -> PublishResponse:
        """发布文章

        Args:
            request: 发布请求

        Returns:
            PublishResponse: 发布响应
        """
        try:
            data = request.to_api_data()
            response = self._make_request("POST", "api/articles", data=data)
            return PublishResponse.from_api_response(response)
        except Exception as e:
            self.logger.error(f"发布文章失败: {e!s}")
            return PublishResponse(
                success=False,
                message=f"发布失败: {e!s}",
                error_code="PUBLISH_ERROR",
            )

    def update_article(self, article_id: int, request: PublishRequest) -> PublishResponse:
        """更新文章

        Args:
            article_id: 文章ID
            request: 更新请求

        Returns:
            PublishResponse: 更新响应
        """
        try:
            data = request.to_api_data()
            response = self._make_request("PUT", f"api/articles/{article_id}", data=data)
            return PublishResponse.from_api_response(response)
        except Exception as e:
            self.logger.error(f"更新文章失败: {e!s}")
            return PublishResponse(
                success=False,
                message=f"更新失败: {e!s}",
                error_code="UPDATE_ERROR",
            )

    def delete_article(self, article_id: int) -> PublishResponse:
        """删除文章

        Args:
            article_id: 文章ID

        Returns:
            PublishResponse: 删除响应
        """
        try:
            response = self._make_request("DELETE", f"api/articles/{article_id}")
            return PublishResponse.from_api_response(response)
        except Exception as e:
            self.logger.error(f"删除文章失败: {e!s}")
            return PublishResponse(
                success=False,
                message=f"删除失败: {e!s}",
                error_code="DELETE_ERROR",
            )

    def get_article(self, article_id: int) -> Optional[Dict[str, Any]]:
        """获取文章详情

        Args:
            article_id: 文章ID

        Returns:
            Optional[Dict[str, Any]]: 文章数据
        """
        try:
            response = self._make_request("GET", f"api/articles/{article_id}")
            return response.get("data")
        except Exception as e:
            self.logger.error(f"获取文章失败: {e!s}")
            return None

    def search_articles(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索文章

        Args:
            query: 搜索关键词
            limit: 限制数量

        Returns:
            List[Dict[str, Any]]: 文章列表
        """
        try:
            params = {"q": query, "limit": limit}
            response = self._make_request("GET", "api/articles/search", params=params)
            return response.get("data", [])
        except Exception as e:
            self.logger.error(f"搜索文章失败: {e!s}")
            return []

    def batch_publish(self, requests: List[PublishRequest]) -> List[PublishResponse]:
        """批量发布文章

        Args:
            requests: 发布请求列表

        Returns:
            List[PublishResponse]: 发布响应列表
        """
        responses = []

        for i, request in enumerate(requests):
            self.logger.info(f"批量发布进度: {i + 1}/{len(requests)}")
            response = self.publish_article(request)
            responses.append(response)

            # 如果失败，记录错误但继续处理
            if not response.success:
                self.logger.error(f"批量发布第 {i + 1} 项失败: {response.message}")

        return responses


class DataMapper:
    """数据映射器"""

    def __init__(self, api_client: HuoNiaoAPIClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

        # 缓存分类和作者信息
        self._categories_cache = None
        self._authors_cache = None
        self._cache_time = None
        self._cache_ttl = 3600  # 缓存1小时

    def _get_categories(self) -> List[Dict[str, Any]]:
        """获取分类列表（带缓存）"""
        now = time.time()
        if (
            self._categories_cache is None
            or self._cache_time is None
            or now - self._cache_time > self._cache_ttl
        ):
            self._categories_cache = self.api_client.get_categories()
            self._cache_time = now

        return self._categories_cache or []

    def _get_authors(self) -> List[Dict[str, Any]]:
        """获取作者列表（带缓存）"""
        now = time.time()
        if (
            self._authors_cache is None
            or self._cache_time is None
            or now - self._cache_time > self._cache_ttl
        ):
            self._authors_cache = self.api_client.get_authors()
            self._cache_time = now

        return self._authors_cache or []

    def find_category_by_name(self, name: str) -> Optional[int]:
        """根据名称查找分类ID

        Args:
            name: 分类名称

        Returns:
            Optional[int]: 分类ID
        """
        categories = self._get_categories()

        for category in categories:
            if category.get("name", "").lower() == name.lower():
                return category.get("id")

        return None

    def find_author_by_name(self, name: str) -> Optional[int]:
        """根据名称查找作者ID

        Args:
            name: 作者名称

        Returns:
            Optional[int]: 作者ID
        """
        authors = self._get_authors()

        for author in authors:
            if author.get("name", "").lower() == name.lower():
                return author.get("id")

        return None

    def map_processed_article(
        self, article: ProcessedArticle, config: Optional[APIConfig] = None
    ) -> PublishRequest:
        """将处理后的文章映射为发布请求

        Args:
            article: 处理后的文章
            config: API配置

        Returns:
            PublishRequest: 发布请求
        """
        # 基础映射
        request = PublishRequest(
            title=article.title,
            content=article.content,
            summary=article.summary,
            tags=article.keywords[:10],  # 限制标签数量
        )

        # 设置源URL和外部ID（如果存在）
        if article.source_url:
            request.source_url = article.source_url
        elif article.url:
            request.source_url = article.url

        if article.external_id:
            request.external_id = article.external_id

        # 设置元数据
        if article.metadata:
            request.metadata = article.metadata

        # SEO映射
        request.seo_title = article.title[:60] if article.title else None  # 限制SEO标题长度
        request.seo_description = (
            article.summary[:160] if article.summary else None
        )  # 限制SEO描述长度
        request.seo_keywords = article.keywords[:5]  # 限制SEO关键词数量

        # 媒体映射
        if article.images:
            request.featured_image = article.images[0]  # 第一张图作为特色图片
            request.images = article.images

        # 分类映射
        if article.category:
            category_id = self.find_category_by_name(article.category)
            if category_id:
                request.category_id = category_id
            elif config and config.default_category_id:
                request.category_id = config.default_category_id
        elif config and config.default_category_id:
            request.category_id = config.default_category_id

        # 作者映射
        if article.author:
            author_id = self.find_author_by_name(article.author)
            if author_id:
                request.author_id = author_id
            elif config and config.default_author_id:
                request.author_id = config.default_author_id
        elif config and config.default_author_id:
            request.author_id = config.default_author_id

        # 状态映射
        if config:
            request.status = config.default_status

        # 元数据映射
        request.metadata = {
            "quality_score": article.quality_score,
            "reading_time": article.reading_time,
            "language": article.language,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "firecrawl_source": True,
        }

        # 添加原始数据的元数据
        if hasattr(article, "metadata") and article.metadata:
            request.metadata.update(article.metadata)

        return request


class APIIntegration:
    """API集成主类"""

    def __init__(self, config: APIConfig, data_processor: Optional[DataProcessor] = None):
        self.config = config
        self.api_client = HuoNiaoAPIClient(config)
        self.data_mapper = DataMapper(self.api_client)
        self.data_processor = data_processor or DataProcessor()
        self.logger = logging.getLogger(__name__)

        # 发布统计
        self.stats = {
            "total_processed": 0,
            "successful_publishes": 0,
            "failed_publishes": 0,
            "skipped_items": 0,
        }

    def test_connection(self) -> bool:
        """测试API连接

        Returns:
            bool: 连接是否成功
        """
        return self.api_client.test_connection()

    def process_and_publish(
        self, raw_data: Dict[str, Any], auto_publish: bool = False
    ) -> PublishResponse:
        """处理原始数据并发布

        Args:
            raw_data: Firecrawl原始数据
            auto_publish: 是否自动发布

        Returns:
            PublishResponse: 发布响应
        """
        try:
            self.stats["total_processed"] += 1

            # 数据处理
            processed_article = self.data_processor.process_article(raw_data)

            if not processed_article:
                self.logger.warning("数据处理失败，跳过发布")
                self.stats["skipped_items"] += 1
                return PublishResponse(
                    success=False,
                    message="数据处理失败",
                    error_code="PROCESSING_ERROR",
                )

            # 质量检查
            if processed_article.quality_score < 0.6:  # 质量阈值
                self.logger.warning(
                    f"文章质量分数过低: {processed_article.quality_score}，跳过发布"
                )
                self.stats["skipped_items"] += 1
                return PublishResponse(
                    success=False,
                    message=f"文章质量分数过低: {processed_article.quality_score}",
                    error_code="QUALITY_TOO_LOW",
                )

            # 数据映射
            publish_request = self.data_mapper.map_processed_article(processed_article, self.config)

            # 设置发布状态
            if auto_publish:
                publish_request.status = PublishStatus.PUBLISHED
            else:
                publish_request.status = self.config.default_status

            # 发布文章
            response = self.api_client.publish_article(publish_request)

            if response.success:
                self.stats["successful_publishes"] += 1
                self.logger.info(
                    f"文章发布成功: {processed_article.title} (ID: {response.article_id})"
                )
            else:
                self.stats["failed_publishes"] += 1
                self.logger.error(f"文章发布失败: {response.message}")

            return response

        except Exception as e:
            self.stats["failed_publishes"] += 1
            self.logger.error(f"处理和发布失败: {e!s}")
            return PublishResponse(
                success=False,
                message=f"处理和发布失败: {e!s}",
                error_code="INTEGRATION_ERROR",
            )

    def batch_process_and_publish(
        self, raw_data_list: List[Dict[str, Any]], auto_publish: bool = False
    ) -> List[PublishResponse]:
        """批量处理和发布

        Args:
            raw_data_list: 原始数据列表
            auto_publish: 是否自动发布

        Returns:
            List[PublishResponse]: 发布响应列表
        """
        responses = []

        for i, raw_data in enumerate(raw_data_list):
            self.logger.info(f"批量处理进度: {i + 1}/{len(raw_data_list)}")
            response = self.process_and_publish(raw_data, auto_publish)
            responses.append(response)

        return responses

    def sync_article_status(self, external_id: str, new_status: PublishStatus) -> bool:
        """同步文章状态

        Args:
            external_id: 外部ID
            new_status: 新状态

        Returns:
            bool: 是否同步成功
        """
        try:
            # 搜索文章
            articles = self.api_client.search_articles(external_id)

            if not articles:
                self.logger.warning(f"未找到外部ID为 {external_id} 的文章")
                return False

            article = articles[0]
            article_id = article.get("id")

            if not article_id:
                self.logger.error("文章ID为空")
                return False

            # 更新状态
            update_request = PublishRequest(
                title=article.get("title", ""),
                content=article.get("content", ""),
                status=new_status,
            )

            response = self.api_client.update_article(article_id, update_request)

            if response.success:
                self.logger.info(f"文章状态同步成功: {external_id} -> {new_status.value}")
                return True
            self.logger.error(f"文章状态同步失败: {response.message}")
            return False

        except Exception as e:
            self.logger.error(f"同步文章状态失败: {e!s}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息

        Returns:
            Dict[str, Any]: 统计信息
        """
        stats: Dict[str, Any] = self.stats.copy()

        if stats["total_processed"] > 0:
            stats["success_rate"] = float(stats["successful_publishes"] / stats["total_processed"])
            stats["failure_rate"] = float(stats["failed_publishes"] / stats["total_processed"])
            stats["skip_rate"] = float(stats["skipped_items"] / stats["total_processed"])
        else:
            stats["success_rate"] = 0.0
            stats["failure_rate"] = 0.0
            stats["skip_rate"] = 0.0

        return stats

    def reset_statistics(self):
        """重置统计信息"""
        self.stats = {
            "total_processed": 0,
            "successful_publishes": 0,
            "failed_publishes": 0,
            "skipped_items": 0,
        }


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 创建API配置
    api_config = APIConfig(
        base_url="https://api.huoniao.com/",
        api_key="your_api_key_here",
        default_category_id=1,
        default_author_id=1,
        default_status=PublishStatus.DRAFT,
    )

    # 创建集成实例
    integration = APIIntegration(api_config)

    # 测试连接
    if integration.test_connection():
        print("API连接成功")

        # 模拟Firecrawl数据
        mock_data = {
            "url": "https://example.com/article",
            "title": "测试文章标题",
            "content": "这是一篇测试文章的内容...",
            "metadata": {
                "description": "文章摘要",
                "keywords": ["测试", "文章", "API"],
                "author": "作者名称",
                "publish_date": "2025-01-17",
            },
        }

        # 处理和发布
        response = integration.process_and_publish(mock_data, auto_publish=False)

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
