#!/usr/bin/env python3
"""
Firecrawl采集器配置管理模块

提供配置文件加载、环境变量管理、配置验证等功能。
支持多环境配置和动态配置更新。

作者: Trae IDE Agent
创建时间: 2025-01-17
版本: v1.0
"""

from dataclasses import dataclass, field
from enum import Enum
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class OutputFormat(Enum):
    """输出格式枚举"""

    MARKDOWN = "markdown"
    HTML = "html"
    STRUCTURED = "structured"


class LogLevel(Enum):
    """日志级别枚举"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class SourceConfig:
    """数据源配置"""

    name: str
    url: str
    type: str = "crawl"  # crawl, scrape, extract
    schedule: Optional[str] = None  # cron表达式
    category: Optional[str] = None
    enabled: bool = True
    max_depth: int = 2
    limit: int = 10
    custom_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.type not in ["crawl", "scrape", "extract"]:
            raise ValueError(f"不支持的数据源类型: {self.type}")


@dataclass
class ProcessingConfig:
    """数据处理配置"""

    enable_dedup: bool = True
    auto_category: bool = True
    content_filter: bool = True
    min_content_length: int = 100
    max_content_length: int = 50000
    extract_summary: bool = True
    extract_keywords: bool = True
    language_detection: bool = True


@dataclass
class FirecrawlAPIConfig:
    """Firecrawl API配置"""

    api_key: str
    base_url: str = "https://api.firecrawl.dev"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    rate_limit: int = 100  # 每分钟请求数

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("Firecrawl API密钥不能为空")


@dataclass
class CacheConfig:
    """缓存配置"""

    enabled: bool = True
    ttl: int = 3600  # 缓存时间（秒）
    max_size: int = 1000  # 最大缓存条目数
    storage_type: str = "memory"  # memory, redis, file
    redis_url: Optional[str] = None
    cache_dir: Optional[str] = None

    def __post_init__(self):
        if self.storage_type == "redis" and not self.redis_url:
            raise ValueError("Redis缓存需要提供redis_url")
        if self.storage_type == "file" and not self.cache_dir:
            self.cache_dir = "./cache"


@dataclass
class ConcurrencyConfig:
    """并发配置"""

    max_concurrent: int = 5
    batch_size: int = 10
    queue_size: int = 100
    worker_timeout: int = 300

    def __post_init__(self):
        if self.max_concurrent <= 0:
            raise ValueError("最大并发数必须大于0")
        if self.batch_size <= 0:
            raise ValueError("批处理大小必须大于0")


@dataclass
class StorageConfig:
    """存储配置"""

    output_dir: str = "./output"
    backup_dir: str = "./backup"
    log_dir: str = "./logs"
    temp_dir: str = "./temp"
    auto_backup: bool = True
    backup_retention_days: int = 30
    compress_backups: bool = True

    def __post_init__(self):
        # 确保目录存在
        for dir_path in [
            self.output_dir,
            self.backup_dir,
            self.log_dir,
            self.temp_dir,
        ]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)


@dataclass
class LoggingConfig:
    """日志配置"""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    console_enabled: bool = True
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    log_file: Optional[str] = None

    def __post_init__(self):
        if self.level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            raise ValueError(f"不支持的日志级别: {self.level}")
        if not self.log_file:
            self.log_file = "firecrawl_collector.log"


@dataclass
class FirecrawlCollectorConfig:
    """Firecrawl采集器完整配置"""

    # 基础配置
    app_name: str = "Firecrawl采集器"
    version: str = "1.0.0"
    environment: str = "development"  # development, staging, production

    # 核心配置
    firecrawl_api: Optional[FirecrawlAPIConfig] = None
    sources: List[SourceConfig] = field(default_factory=list)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    # 输出配置
    default_output_format: str = "markdown"
    supported_formats: List[str] = field(
        default_factory=lambda: ["markdown", "html", "json", "csv"]
    )

    # 监控配置
    enable_monitoring: bool = True
    metrics_port: int = 9090
    health_check_interval: int = 60

    def __post_init__(self):
        if not self.firecrawl_api:
            # 尝试从环境变量获取API密钥
            api_key = os.getenv("FIRECRAWL_API_KEY")
            if api_key:
                self.firecrawl_api = FirecrawlAPIConfig(api_key=api_key)
            else:
                raise ValueError("必须提供Firecrawl API配置")

        if self.default_output_format not in self.supported_formats:
            raise ValueError(f"不支持的默认输出格式: {self.default_output_format}")

    def validate(self) -> List[str]:
        """验证配置

        Returns:
            List[str]: 验证错误列表
        """
        errors = []

        # 验证API配置
        if not self.firecrawl_api or not self.firecrawl_api.api_key:
            errors.append("Firecrawl API密钥未配置")

        # 验证数据源
        if not self.sources:
            errors.append("至少需要配置一个数据源")

        for i, source in enumerate(self.sources):
            if not source.url:
                errors.append(f"数据源{i + 1}的URL不能为空")
            if not source.name:
                errors.append(f"数据源{i + 1}的名称不能为空")

        # 验证并发配置
        if self.concurrency.max_concurrent > 20:
            errors.append("最大并发数不建议超过20")

        # 验证缓存配置
        if self.cache.enabled and self.cache.storage_type == "redis":
            if not self.cache.redis_url:
                errors.append("Redis缓存需要配置redis_url")

        return errors

    def to_dict(self, mask_sensitive: bool = True) -> Dict[str, Any]:
        """转换为字典格式

        Args:
            mask_sensitive: 是否对敏感字段进行脱敏处理
        """

        def mask(value: Optional[str]) -> Optional[str]:
            if not mask_sensitive:
                return value
            return "***" if value else None

        return {
            "app_name": self.app_name,
            "version": self.version,
            "environment": self.environment,
            "firecrawl_api": (
                {
                    "api_key": mask(self.firecrawl_api.api_key),
                    "base_url": self.firecrawl_api.base_url,
                    "timeout": self.firecrawl_api.timeout,
                    "max_retries": self.firecrawl_api.max_retries,
                    "retry_delay": self.firecrawl_api.retry_delay,
                    "rate_limit": self.firecrawl_api.rate_limit,
                }
                if self.firecrawl_api
                else None
            ),
            "sources": [
                {
                    "name": s.name,
                    "url": s.url,
                    "type": s.type,
                    "schedule": s.schedule,
                    "category": s.category,
                    "enabled": s.enabled,
                    "max_depth": s.max_depth,
                    "limit": s.limit,
                    "custom_params": s.custom_params,
                }
                for s in self.sources
            ],
            "processing": {
                "enable_dedup": self.processing.enable_dedup,
                "auto_category": self.processing.auto_category,
                "content_filter": self.processing.content_filter,
                "min_content_length": self.processing.min_content_length,
                "max_content_length": self.processing.max_content_length,
                "extract_summary": self.processing.extract_summary,
                "extract_keywords": self.processing.extract_keywords,
                "language_detection": self.processing.language_detection,
            },
            "cache": {
                "enabled": self.cache.enabled,
                "ttl": self.cache.ttl,
                "max_size": self.cache.max_size,
                "storage_type": self.cache.storage_type,
                "redis_url": mask(self.cache.redis_url),
                "cache_dir": self.cache.cache_dir,
            },
            "concurrency": {
                "max_concurrent": self.concurrency.max_concurrent,
                "batch_size": self.concurrency.batch_size,
                "queue_size": self.concurrency.queue_size,
                "worker_timeout": self.concurrency.worker_timeout,
            },
            "storage": {
                "output_dir": self.storage.output_dir,
                "backup_dir": self.storage.backup_dir,
                "log_dir": self.storage.log_dir,
                "temp_dir": self.storage.temp_dir,
                "auto_backup": self.storage.auto_backup,
                "backup_retention_days": self.storage.backup_retention_days,
                "compress_backups": self.storage.compress_backups,
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format,
                "file_enabled": self.logging.file_enabled,
                "console_enabled": self.logging.console_enabled,
                "max_file_size": self.logging.max_file_size,
                "backup_count": self.logging.backup_count,
                "log_file": self.logging.log_file,
            },
            "default_output_format": self.default_output_format,
            "supported_formats": self.supported_formats,
            "enable_monitoring": self.enable_monitoring,
            "metrics_port": self.metrics_port,
            "health_check_interval": self.health_check_interval,
        }


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: Optional[str] = None):
        """初始化配置管理器

        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file or "firecrawl_config.yaml"
        self._config: Optional[FirecrawlCollectorConfig] = None

    def load_config(self, config_file: Optional[str] = None) -> FirecrawlCollectorConfig:
        """加载配置文件

        Args:
            config_file: 配置文件路径

        Returns:
            FirecrawlCollectorConfig: 配置对象
        """
        config_file = config_file or self.config_file
        config_path = Path(config_file)

        if not config_path.exists():
            # 创建默认配置
            self._config = self._create_default_config()
            self.save_config(config_file)
            return self._config

        try:
            with open(config_path, encoding="utf-8") as f:
                if config_path.suffix.lower() in [".yaml", ".yml"]:
                    data = yaml.safe_load(f)
                elif config_path.suffix.lower() == ".json":
                    data = json.load(f)
                else:
                    raise ValueError(f"不支持的配置文件格式: {config_path.suffix}")

            self._config = self._dict_to_config(data)
            return self._config

        except Exception as e:
            raise ValueError(f"加载配置文件失败: {e!s}")

    def save_config(
        self,
        config_file: Optional[str] = None,
        config: Optional[FirecrawlCollectorConfig] = None,
    ) -> bool:
        """保存配置文件

        Args:
            config_file: 配置文件路径
            config: 配置对象

        Returns:
            bool: 保存是否成功
        """
        try:
            config_file = config_file or self.config_file
            config = config or self._config

            if not config:
                raise ValueError("没有可保存的配置")

            config_path = Path(config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)

            data = config.to_dict(mask_sensitive=False)

            with open(config_path, "w", encoding="utf-8") as f:
                if config_path.suffix.lower() in [".yaml", ".yml"]:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                elif config_path.suffix.lower() == ".json":
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    raise ValueError(f"不支持的配置文件格式: {config_path.suffix}")

            return True

        except Exception as e:
            print(f"保存配置文件失败: {e!s}")
            return False

    def get_config(self) -> Optional[FirecrawlCollectorConfig]:
        """获取当前配置"""
        return self._config

    def update_config(self, **kwargs) -> bool:
        """更新配置

        Args:
            **kwargs: 配置参数

        Returns:
            bool: 更新是否成功
        """
        if not self._config:
            return False

        try:
            for key, value in kwargs.items():
                if hasattr(self._config, key):
                    setattr(self._config, key, value)
            return True
        except Exception:
            return False

    def _create_default_config(self) -> FirecrawlCollectorConfig:
        """创建默认配置"""
        # 从环境变量获取API密钥
        api_key = os.getenv("FIRECRAWL_API_KEY", "your-firecrawl-api-key")

        return FirecrawlCollectorConfig(
            firecrawl_api=FirecrawlAPIConfig(api_key=api_key),
            sources=[
                SourceConfig(
                    name="Firecrawl博客",
                    url="https://firecrawl.dev/blog",
                    type="crawl",
                    category="技术资讯",
                    limit=5,
                ),
                SourceConfig(
                    name="Firecrawl文档",
                    url="https://docs.firecrawl.dev",
                    type="scrape",
                    category="技术文档",
                ),
            ],
        )

    def _dict_to_config(self, data: Dict[str, Any]) -> FirecrawlCollectorConfig:
        """将字典转换为配置对象"""
        # 处理Firecrawl API配置
        api_data = data.get("firecrawl_api", {})
        firecrawl_api = FirecrawlAPIConfig(
            api_key=api_data.get("api_key", os.getenv("FIRECRAWL_API_KEY", "")),
            base_url=api_data.get("base_url", "https://api.firecrawl.dev"),
            timeout=api_data.get("timeout", 30),
            max_retries=api_data.get("max_retries", 3),
            retry_delay=api_data.get("retry_delay", 1.0),
            rate_limit=api_data.get("rate_limit", 100),
        )

        # 处理数据源配置
        sources = []
        for source_data in data.get("sources", []):
            source = SourceConfig(
                name=source_data.get("name", ""),
                url=source_data.get("url", ""),
                type=source_data.get("type", "crawl"),
                schedule=source_data.get("schedule"),
                category=source_data.get("category"),
                enabled=source_data.get("enabled", True),
                max_depth=source_data.get("max_depth", 2),
                limit=source_data.get("limit", 10),
                custom_params=source_data.get("custom_params", {}),
            )
            sources.append(source)

        # 处理其他配置
        processing_data = data.get("processing", {})
        processing = ProcessingConfig(
            enable_dedup=processing_data.get("enable_dedup", True),
            auto_category=processing_data.get("auto_category", True),
            content_filter=processing_data.get("content_filter", True),
            min_content_length=processing_data.get("min_content_length", 100),
            max_content_length=processing_data.get("max_content_length", 50000),
            extract_summary=processing_data.get("extract_summary", True),
            extract_keywords=processing_data.get("extract_keywords", True),
            language_detection=processing_data.get("language_detection", True),
        )

        cache_data = data.get("cache", {})
        cache = CacheConfig(
            enabled=cache_data.get("enabled", True),
            ttl=cache_data.get("ttl", 3600),
            max_size=cache_data.get("max_size", 1000),
            storage_type=cache_data.get("storage_type", "memory"),
            redis_url=cache_data.get("redis_url"),
            cache_dir=cache_data.get("cache_dir"),
        )

        concurrency_data = data.get("concurrency", {})
        concurrency = ConcurrencyConfig(
            max_concurrent=concurrency_data.get("max_concurrent", 5),
            batch_size=concurrency_data.get("batch_size", 10),
            queue_size=concurrency_data.get("queue_size", 100),
            worker_timeout=concurrency_data.get("worker_timeout", 300),
        )

        storage_data = data.get("storage", {})
        storage = StorageConfig(
            output_dir=storage_data.get("output_dir", "./output"),
            backup_dir=storage_data.get("backup_dir", "./backup"),
            log_dir=storage_data.get("log_dir", "./logs"),
            temp_dir=storage_data.get("temp_dir", "./temp"),
            auto_backup=storage_data.get("auto_backup", True),
            backup_retention_days=storage_data.get("backup_retention_days", 30),
            compress_backups=storage_data.get("compress_backups", True),
        )

        logging_data = data.get("logging", {})
        logging_config = LoggingConfig(
            level=logging_data.get("level", "INFO"),
            format=logging_data.get(
                "format",
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            ),
            file_enabled=logging_data.get("file_enabled", True),
            console_enabled=logging_data.get("console_enabled", True),
            max_file_size=logging_data.get("max_file_size", 10 * 1024 * 1024),
            backup_count=logging_data.get("backup_count", 5),
            log_file=logging_data.get("log_file", "firecrawl_collector.log"),
        )

        return FirecrawlCollectorConfig(
            app_name=data.get("app_name", "Firecrawl采集器"),
            version=data.get("version", "1.0.0"),
            environment=data.get("environment", "development"),
            firecrawl_api=firecrawl_api,
            sources=sources,
            processing=processing,
            cache=cache,
            concurrency=concurrency,
            storage=storage,
            logging=logging_config,
            default_output_format=data.get("default_output_format", "markdown"),
            supported_formats=data.get("supported_formats", ["markdown", "html", "json", "csv"]),
            enable_monitoring=data.get("enable_monitoring", True),
            metrics_port=data.get("metrics_port", 9090),
            health_check_interval=data.get("health_check_interval", 60),
        )


# 全局配置管理器实例
config_manager = ConfigManager()


def get_config() -> FirecrawlCollectorConfig:
    """获取全局配置"""
    config = config_manager.get_config()
    if not config:
        config = config_manager.load_config()
    if not config:
        raise ValueError("配置加载失败，请检查配置文件")
    return config


def load_config_from_file(config_file: str) -> FirecrawlCollectorConfig:
    """从文件加载配置"""
    return config_manager.load_config(config_file)


def save_config_to_file(config: FirecrawlCollectorConfig, config_file: str) -> bool:
    """保存配置到文件"""
    return config_manager.save_config(config_file, config)


# 使用示例
if __name__ == "__main__":
    # 创建配置管理器
    manager = ConfigManager("example_config.yaml")

    # 加载配置
    config = manager.load_config()

    # 验证配置
    errors = config.validate()
    if errors:
        print("配置验证失败:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("配置验证通过")

    # 打印配置摘要
    print(f"\n应用名称: {config.app_name}")
    print(f"版本: {config.version}")
    print(f"环境: {config.environment}")
    print(f"数据源数量: {len(config.sources)}")
    print(f"默认输出格式: {config.default_output_format}")
    print(f"最大并发数: {config.concurrency.max_concurrent}")
    print(f"缓存启用: {config.cache.enabled}")

    # 保存配置
    if manager.save_config():
        print("\n配置保存成功")
    else:
        print("\n配置保存失败")
