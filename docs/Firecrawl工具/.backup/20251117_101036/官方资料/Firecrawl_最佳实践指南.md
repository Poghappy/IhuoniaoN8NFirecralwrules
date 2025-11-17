# Firecrawl 最佳实践指南

> 专业的Firecrawl使用指南，涵盖性能优化、错误处理、安全防护等核心实践
> 更新时间: 2024年

## 目录

1. [性能优化策略](#性能优化策略)
2. [错误处理与重试机制](#错误处理与重试机制)
3. [反爬虫应对策略](#反爬虫应对策略)
4. [数据质量保证](#数据质量保证)
5. [成本控制与配额管理](#成本控制与配额管理)
6. [安全与合规](#安全与合规)
7. [监控与日志](#监控与日志)
8. [架构设计模式](#架构设计模式)
9. [常见问题解决](#常见问题解决)
10. [生产环境部署](#生产环境部署)

## 性能优化策略

### 1. 选择合适的抓取模式

```python
from firecrawl import Firecrawl
from typing import Dict, List
import time

class OptimizedCrawler:
    def __init__(self, api_key: str):
        self.firecrawl = Firecrawl(api_key=api_key)
    
    def choose_optimal_method(self, url: str, requirements: Dict) -> str:
        """
        根据需求选择最优的抓取方法
        
        Args:
            url: 目标URL
            requirements: 需求配置
                - single_page: 是否只需要单页
                - structured_data: 是否需要结构化数据
                - full_site: 是否需要整站数据
                - discovery_only: 是否只需要发现链接
        
        Returns:
            推荐的方法名称
        """
        if requirements.get('discovery_only'):
            return 'map'  # 最快的链接发现
        elif requirements.get('single_page') and not requirements.get('structured_data'):
            return 'scrape'  # 单页内容抓取
        elif requirements.get('structured_data'):
            return 'extract'  # 结构化数据提取
        elif requirements.get('full_site'):
            return 'crawl'  # 全站爬取
        else:
            return 'search'  # 搜索模式
    
    def optimized_scrape(self, url: str, **kwargs) -> Dict:
        """
        优化的单页抓取
        """
        # 使用缓存减少重复请求
        cache_key = f"scrape_{hash(url)}_{hash(str(kwargs))}"
        
        # 优化的配置
        optimized_config = {
            'formats': ['markdown'],  # 只请求需要的格式
            'only_main_content': True,  # 只提取主要内容
            'exclude_tags': ['nav', 'footer', 'aside', 'ads', 'script', 'style'],
            'max_age': 3600000,  # 1小时缓存
            **kwargs
        }
        
        return self.firecrawl.scrape(url=url, **optimized_config)
    
    def batch_scrape_with_delay(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """
        批量抓取，带延迟控制
        """
        results = []
        
        for i, url in enumerate(urls):
            try:
                result = self.optimized_scrape(url)
                results.append(result)
                
                # 添加延迟，避免触发限制
                if i < len(urls) - 1:  # 最后一个不需要延迟
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"抓取失败 {url}: {e}")
                results.append({'error': str(e), 'url': url})
        
        return results
    
    def smart_crawl(self, url: str, **kwargs) -> str:
        """
        智能爬取，自动优化参数
        """
        # 根据网站规模调整参数
        site_map = self.firecrawl.map(url=url, limit=10)
        estimated_pages = len(site_map.get('links', []))
        
        if estimated_pages > 1000:
            # 大型网站，限制深度和页面数
            crawl_config = {
                'max_discovery_depth': 2,
                'limit': 500,
                'delay': 2,  # 增加延迟
                **kwargs
            }
        elif estimated_pages > 100:
            # 中型网站
            crawl_config = {
                'max_discovery_depth': 3,
                'limit': 200,
                'delay': 1,
                **kwargs
            }
        else:
            # 小型网站
            crawl_config = {
                'max_discovery_depth': 4,
                'limit': 100,
                'delay': 0.5,
                **kwargs
            }
        
        return self.firecrawl.crawl(url=url, **crawl_config)
```

### 2. 并发控制与限流

```python
import asyncio
import aiohttp
from asyncio import Semaphore
from typing import List, Dict
import time

class ConcurrentCrawler:
    def __init__(self, api_key: str, max_concurrent: int = 5, rate_limit: float = 1.0):
        self.api_key = api_key
        self.semaphore = Semaphore(max_concurrent)
        self.rate_limit = rate_limit
        self.last_request_time = 0
    
    async def rate_limited_request(self, func, *args, **kwargs):
        """
        带限流的请求
        """
        async with self.semaphore:
            # 确保请求间隔
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.rate_limit:
                await asyncio.sleep(self.rate_limit - time_since_last)
            
            self.last_request_time = time.time()
            return await func(*args, **kwargs)
    
    async def concurrent_scrape(self, urls: List[str]) -> List[Dict]:
        """
        并发抓取多个URL
        """
        tasks = []
        
        for url in urls:
            task = self.rate_limited_request(self._scrape_single, url)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def _scrape_single(self, url: str) -> Dict:
        """
        单个URL抓取
        """
        # 这里使用异步HTTP客户端调用Firecrawl API
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'url': url,
                'formats': ['markdown'],
                'only_main_content': True
            }
            
            async with session.post(
                'https://api.firecrawl.dev/v1/scrape',
                json=payload,
                headers=headers
            ) as response:
                return await response.json()
```

### 3. 缓存策略

```python
import redis
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class CacheManager:
    def __init__(self, redis_url: str = 'redis://localhost:6379'):
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1小时
    
    def generate_cache_key(self, url: str, params: Dict = None) -> str:
        """
        生成缓存键
        """
        key_data = f"{url}_{json.dumps(params or {}, sort_keys=True)}"
        return f"firecrawl:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def get_cached_result(self, url: str, params: Dict = None) -> Optional[Dict]:
        """
        获取缓存结果
        """
        cache_key = self.generate_cache_key(url, params)
        
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"缓存读取失败: {e}")
        
        return None
    
    def cache_result(self, url: str, result: Dict, params: Dict = None, ttl: int = None) -> bool:
        """
        缓存结果
        """
        cache_key = self.generate_cache_key(url, params)
        ttl = ttl or self.default_ttl
        
        try:
            # 添加缓存时间戳
            cache_data = {
                'result': result,
                'cached_at': datetime.now().isoformat(),
                'url': url
            }
            
            self.redis_client.setex(
                cache_key,
                ttl,
                json.dumps(cache_data)
            )
            return True
        except Exception as e:
            print(f"缓存写入失败: {e}")
            return False
    
    def invalidate_cache(self, pattern: str = "firecrawl:*"):
        """
        清除缓存
        """
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                print(f"清除了 {len(keys)} 个缓存项")
        except Exception as e:
            print(f"缓存清除失败: {e}")

class CachedFirecrawl:
    def __init__(self, api_key: str, cache_manager: CacheManager):
        self.firecrawl = Firecrawl(api_key=api_key)
        self.cache = cache_manager
    
    def scrape_with_cache(self, url: str, **kwargs) -> Dict:
        """
        带缓存的抓取
        """
        # 检查缓存
        cached_result = self.cache.get_cached_result(url, kwargs)
        if cached_result:
            print(f"使用缓存结果: {url}")
            return cached_result['result']
        
        # 执行抓取
        try:
            result = self.firecrawl.scrape(url=url, **kwargs)
            
            # 缓存结果
            self.cache.cache_result(url, result, kwargs)
            
            return result
        except Exception as e:
            print(f"抓取失败: {e}")
            raise
```

## 错误处理与重试机制

### 1. 智能重试策略

```python
import time
import random
from typing import Callable, Any, Dict
from functools import wraps

class RetryManager:
    def __init__(self):
        self.retry_configs = {
            'rate_limit': {
                'max_retries': 5,
                'base_delay': 60,  # 1分钟
                'backoff_factor': 2,
                'jitter': True
            },
            'server_error': {
                'max_retries': 3,
                'base_delay': 5,
                'backoff_factor': 2,
                'jitter': True
            },
            'network_error': {
                'max_retries': 3,
                'base_delay': 2,
                'backoff_factor': 1.5,
                'jitter': False
            },
            'timeout': {
                'max_retries': 2,
                'base_delay': 10,
                'backoff_factor': 1,
                'jitter': False
            }
        }
    
    def classify_error(self, error: Exception) -> str:
        """
        分类错误类型
        """
        error_str = str(error).lower()
        
        if 'rate limit' in error_str or '429' in error_str:
            return 'rate_limit'
        elif 'server error' in error_str or '500' in error_str or '502' in error_str:
            return 'server_error'
        elif 'timeout' in error_str or 'timed out' in error_str:
            return 'timeout'
        elif 'network' in error_str or 'connection' in error_str:
            return 'network_error'
        else:
            return 'unknown'
    
    def calculate_delay(self, attempt: int, error_type: str) -> float:
        """
        计算重试延迟
        """
        config = self.retry_configs.get(error_type, self.retry_configs['server_error'])
        
        delay = config['base_delay'] * (config['backoff_factor'] ** (attempt - 1))
        
        if config['jitter']:
            # 添加随机抖动，避免雷群效应
            jitter = random.uniform(0.5, 1.5)
            delay *= jitter
        
        return min(delay, 300)  # 最大延迟5分钟
    
    def should_retry(self, error: Exception, attempt: int) -> bool:
        """
        判断是否应该重试
        """
        error_type = self.classify_error(error)
        
        if error_type == 'unknown':
            return False
        
        config = self.retry_configs.get(error_type)
        return attempt <= config['max_retries']
    
    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """
        带退避的重试执行
        """
        attempt = 1
        last_error = None
        
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                if not self.should_retry(e, attempt):
                    print(f"重试失败，放弃执行: {e}")
                    raise e
                
                error_type = self.classify_error(e)
                delay = self.calculate_delay(attempt, error_type)
                
                print(f"第{attempt}次重试失败 ({error_type}): {e}")
                print(f"等待 {delay:.1f} 秒后重试...")
                
                time.sleep(delay)
                attempt += 1
        
        raise last_error

def retry_on_failure(retry_manager: RetryManager = None):
    """
    重试装饰器
    """
    if retry_manager is None:
        retry_manager = RetryManager()
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return retry_manager.retry_with_backoff(func, *args, **kwargs)
        return wrapper
    return decorator

class RobustFirecrawl:
    def __init__(self, api_key: str):
        self.firecrawl = Firecrawl(api_key=api_key)
        self.retry_manager = RetryManager()
    
    @retry_on_failure()
    def robust_scrape(self, url: str, **kwargs) -> Dict:
        """
        健壮的抓取方法
        """
        return self.firecrawl.scrape(url=url, **kwargs)
    
    @retry_on_failure()
    def robust_crawl(self, url: str, **kwargs) -> str:
        """
        健壮的爬取方法
        """
        return self.firecrawl.crawl(url=url, **kwargs)
    
    def safe_extract(self, urls: List[str], **kwargs) -> List[Dict]:
        """
        安全的批量提取
        """
        results = []
        failed_urls = []
        
        for url in urls:
            try:
                result = self.retry_manager.retry_with_backoff(
                    self.firecrawl.extract,
                    urls=[url],
                    **kwargs
                )
                results.append(result)
            except Exception as e:
                print(f"提取失败 {url}: {e}")
                failed_urls.append(url)
                results.append({'error': str(e), 'url': url})
        
        if failed_urls:
            print(f"\n失败的URL ({len(failed_urls)}个):")
            for url in failed_urls:
                print(f"  - {url}")
        
        return results
```

### 2. 错误监控与报警

```python
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List

class ErrorMonitor:
    def __init__(self, alert_config: Dict = None):
        self.error_counts = defaultdict(int)
        self.error_history = []
        self.alert_config = alert_config or {}
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('firecrawl_errors.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_error(self, error: Exception, context: Dict = None):
        """
        记录错误
        """
        error_type = type(error).__name__
        error_msg = str(error)
        
        # 更新错误计数
        self.error_counts[error_type] += 1
        
        # 记录错误历史
        error_record = {
            'timestamp': datetime.now(),
            'type': error_type,
            'message': error_msg,
            'context': context or {}
        }
        self.error_history.append(error_record)
        
        # 记录日志
        self.logger.error(f"{error_type}: {error_msg}", extra={'context': context})
        
        # 检查是否需要报警
        self.check_alert_conditions(error_type)
    
    def check_alert_conditions(self, error_type: str):
        """
        检查报警条件
        """
        # 错误频率报警
        recent_errors = [
            e for e in self.error_history
            if e['timestamp'] > datetime.now() - timedelta(minutes=10)
            and e['type'] == error_type
        ]
        
        if len(recent_errors) >= 5:  # 10分钟内同类错误超过5次
            self.send_alert(f"高频错误报警: {error_type}", {
                'error_type': error_type,
                'count': len(recent_errors),
                'time_window': '10分钟'
            })
    
    def send_alert(self, subject: str, details: Dict):
        """
        发送报警
        """
        if not self.alert_config.get('enabled', False):
            return
        
        try:
            # 邮件报警
            if self.alert_config.get('email'):
                self._send_email_alert(subject, details)
            
            # Webhook报警
            if self.alert_config.get('webhook'):
                self._send_webhook_alert(subject, details)
                
        except Exception as e:
            self.logger.error(f"发送报警失败: {e}")
    
    def _send_email_alert(self, subject: str, details: Dict):
        """
        发送邮件报警
        """
        email_config = self.alert_config['email']
        
        msg = MIMEMultipart()
        msg['From'] = email_config['from']
        msg['To'] = email_config['to']
        msg['Subject'] = f"[Firecrawl Alert] {subject}"
        
        body = f"""
        Firecrawl错误报警
        
        时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        主题: {subject}
        
        详细信息:
        {json.dumps(details, indent=2, ensure_ascii=False)}
        
        错误统计:
        {json.dumps(dict(self.error_counts), indent=2, ensure_ascii=False)}
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        server.starttls()
        server.login(email_config['username'], email_config['password'])
        server.send_message(msg)
        server.quit()
    
    def get_error_report(self, hours: int = 24) -> Dict:
        """
        生成错误报告
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_errors = [
            e for e in self.error_history
            if e['timestamp'] > cutoff_time
        ]
        
        # 按类型统计
        error_by_type = defaultdict(int)
        for error in recent_errors:
            error_by_type[error['type']] += 1
        
        # 按小时统计
        error_by_hour = defaultdict(int)
        for error in recent_errors:
            hour = error['timestamp'].strftime('%Y-%m-%d %H:00')
            error_by_hour[hour] += 1
        
        return {
            'total_errors': len(recent_errors),
            'error_by_type': dict(error_by_type),
            'error_by_hour': dict(error_by_hour),
            'time_range': f'最近{hours}小时',
            'generated_at': datetime.now().isoformat()
        }
```

## 反爬虫应对策略

### 1. 智能请求伪装

```python
import random
import time
from typing import Dict, List
from user_agents import UserAgent

class AntiDetectionManager:
    def __init__(self):
        self.ua = UserAgent()
        self.proxy_pool = []
        self.request_patterns = {
            'conservative': {
                'min_delay': 2.0,
                'max_delay': 5.0,
                'burst_size': 3,
                'burst_delay': 30
            },
            'moderate': {
                'min_delay': 1.0,
                'max_delay': 3.0,
                'burst_size': 5,
                'burst_delay': 20
            },
            'aggressive': {
                'min_delay': 0.5,
                'max_delay': 1.5,
                'burst_size': 10,
                'burst_delay': 10
            }
        }
    
    def get_random_headers(self) -> Dict[str, str]:
        """
        生成随机请求头
        """
        return {
            'User-Agent': self.ua.random,
            'Accept': random.choice([
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            ]),
            'Accept-Language': random.choice([
                'en-US,en;q=0.9',
                'en-US,en;q=0.8,zh-CN;q=0.6',
                'zh-CN,zh;q=0.9,en;q=0.8'
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': random.choice(['1', '0']),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def calculate_smart_delay(self, pattern: str = 'moderate', request_count: int = 0) -> float:
        """
        计算智能延迟
        """
        config = self.request_patterns[pattern]
        
        # 基础随机延迟
        base_delay = random.uniform(config['min_delay'], config['max_delay'])
        
        # 突发控制
        if request_count > 0 and request_count % config['burst_size'] == 0:
            base_delay += config['burst_delay']
        
        # 时间段调整（模拟人类行为）
        current_hour = time.localtime().tm_hour
        if 9 <= current_hour <= 17:  # 工作时间，稍微快一点
            base_delay *= 0.8
        elif 22 <= current_hour or current_hour <= 6:  # 深夜，慢一点
            base_delay *= 1.5
        
        return base_delay
    
    def detect_anti_crawler(self, response_content: str, status_code: int) -> Dict[str, bool]:
        """
        检测反爬虫机制
        """
        detection_results = {
            'captcha': False,
            'rate_limit': False,
            'ip_block': False,
            'js_challenge': False,
            'honeypot': False
        }
        
        content_lower = response_content.lower()
        
        # 验证码检测
        captcha_indicators = ['captcha', 'recaptcha', 'verify you are human', '验证码']
        detection_results['captcha'] = any(indicator in content_lower for indicator in captcha_indicators)
        
        # 限流检测
        if status_code == 429 or 'rate limit' in content_lower or 'too many requests' in content_lower:
            detection_results['rate_limit'] = True
        
        # IP封禁检测
        block_indicators = ['access denied', 'forbidden', 'blocked', 'ip banned']
        detection_results['ip_block'] = any(indicator in content_lower for indicator in block_indicators)
        
        # JS挑战检测
        js_indicators = ['cloudflare', 'ddos protection', 'checking your browser']
        detection_results['js_challenge'] = any(indicator in content_lower for indicator in js_indicators)
        
        # 蜜罐检测
        honeypot_indicators = ['honeypot', 'bot detected', 'automated access']
        detection_results['honeypot'] = any(indicator in content_lower for indicator in honeypot_indicators)
        
        return detection_results
    
    def get_evasion_strategy(self, detection_results: Dict[str, bool]) -> Dict[str, any]:
        """
        获取规避策略
        """
        strategy = {
            'wait_time': 0,
            'change_pattern': False,
            'use_proxy': False,
            'add_headers': {},
            'modify_request': {}
        }
        
        if detection_results['rate_limit']:
            strategy['wait_time'] = random.uniform(60, 180)  # 等待1-3分钟
            strategy['change_pattern'] = True
        
        if detection_results['ip_block']:
            strategy['use_proxy'] = True
            strategy['wait_time'] = random.uniform(300, 600)  # 等待5-10分钟
        
        if detection_results['js_challenge']:
            strategy['modify_request']['wait_for'] = 5000  # 等待JS执行
            strategy['add_headers']['Accept'] = 'text/html,application/xhtml+xml'
        
        if detection_results['captcha']:
            strategy['wait_time'] = random.uniform(1800, 3600)  # 等待30-60分钟
            strategy['use_proxy'] = True
        
        return strategy

class StealthFirecrawl:
    def __init__(self, api_key: str):
        self.firecrawl = Firecrawl(api_key=api_key)
        self.anti_detection = AntiDetectionManager()
        self.request_count = 0
        self.current_pattern = 'moderate'
    
    def stealth_scrape(self, url: str, **kwargs) -> Dict:
        """
        隐蔽抓取
        """
        # 计算延迟
        delay = self.anti_detection.calculate_smart_delay(
            self.current_pattern, 
            self.request_count
        )
        
        if self.request_count > 0:
            print(f"等待 {delay:.1f} 秒...")
            time.sleep(delay)
        
        # 添加随机请求头
        headers = self.anti_detection.get_random_headers()
        
        # 执行请求
        try:
            result = self.firecrawl.scrape(
                url=url,
                **kwargs
            )
            
            self.request_count += 1
            
            # 检测反爬虫
            if 'data' in result and 'markdown' in result['data']:
                detection = self.anti_detection.detect_anti_crawler(
                    result['data']['markdown'], 
                    200
                )
                
                if any(detection.values()):
                    strategy = self.anti_detection.get_evasion_strategy(detection)
                    self._apply_evasion_strategy(strategy)
            
            return result
            
        except Exception as e:
            # 分析错误并调整策略
            if 'rate limit' in str(e).lower():
                self._switch_to_conservative_mode()
            raise e
    
    def _apply_evasion_strategy(self, strategy: Dict):
        """
        应用规避策略
        """
        if strategy['wait_time'] > 0:
            print(f"检测到反爬虫机制，等待 {strategy['wait_time']:.0f} 秒...")
            time.sleep(strategy['wait_time'])
        
        if strategy['change_pattern']:
            self.current_pattern = 'conservative'
            print("切换到保守模式")
        
        if strategy['use_proxy']:
            print("建议使用代理服务器")
    
    def _switch_to_conservative_mode(self):
        """
        切换到保守模式
        """
        self.current_pattern = 'conservative'
        print("切换到保守抓取模式")
```

## 数据质量保证

### 1. 内容验证与清洗

```python
import re
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import difflib

class ContentValidator:
    def __init__(self):
        self.min_content_length = 100
        self.max_content_length = 1000000
        self.spam_patterns = [
            r'click here',
            r'buy now',
            r'limited time offer',
            r'act now',
            r'free trial'
        ]
        self.quality_indicators = {
            'has_title': 10,
            'has_headings': 8,
            'has_paragraphs': 6,
            'proper_length': 15,
            'low_spam_score': 12,
            'has_metadata': 5
        }
    
    def validate_content(self, content: Dict) -> Dict[str, any]:
        """
        验证内容质量
        """
        validation_result = {
            'is_valid': True,
            'quality_score': 0,
            'issues': [],
            'warnings': [],
            'metadata': {}
        }
        
        # 检查基本结构
        markdown_content = content.get('data', {}).get('markdown', '')
        
        if not markdown_content:
            validation_result['is_valid'] = False
            validation_result['issues'].append('内容为空')
            return validation_result
        
        # 长度检查
        content_length = len(markdown_content)
        if content_length < self.min_content_length:
            validation_result['issues'].append(f'内容过短: {content_length} 字符')
        elif content_length > self.max_content_length:
            validation_result['warnings'].append(f'内容过长: {content_length} 字符')
        else:
            validation_result['quality_score'] += self.quality_indicators['proper_length']
        
        # 结构检查
        structure_score = self._check_content_structure(markdown_content)
        validation_result['quality_score'] += structure_score
        
        # 垃圾内容检查
        spam_score = self._calculate_spam_score(markdown_content)
        if spam_score < 0.3:  # 低垃圾分数
            validation_result['quality_score'] += self.quality_indicators['low_spam_score']
        else:
            validation_result['warnings'].append(f'可能包含垃圾内容 (分数: {spam_score:.2f})')
        
        # 元数据检查
        metadata_score = self._check_metadata(content)
        validation_result['quality_score'] += metadata_score
        
        # 设置质量等级
        validation_result['quality_level'] = self._get_quality_level(validation_result['quality_score'])
        
        return validation_result
    
    def _check_content_structure(self, markdown: str) -> int:
        """
        检查内容结构
        """
        score = 0
        
        # 检查标题
        if re.search(r'^#\s+.+', markdown, re.MULTILINE):
            score += self.quality_indicators['has_title']
        
        # 检查子标题
        if re.search(r'^#{2,6}\s+.+', markdown, re.MULTILINE):
            score += self.quality_indicators['has_headings']
        
        # 检查段落
        paragraphs = re.findall(r'^[^#\n].{50,}$', markdown, re.MULTILINE)
        if len(paragraphs) >= 3:
            score += self.quality_indicators['has_paragraphs']
        
        return score
    
    def _calculate_spam_score(self, content: str) -> float:
        """
        计算垃圾内容分数
        """
        content_lower = content.lower()
        spam_count = 0
        
        for pattern in self.spam_patterns:
            matches = len(re.findall(pattern, content_lower))
            spam_count += matches
        
        # 计算相对分数
        words_count = len(content.split())
        if words_count == 0:
            return 1.0
        
        return min(spam_count / words_count, 1.0)
    
    def _check_metadata(self, content: Dict) -> int:
        """
        检查元数据
        """
        score = 0
        data = content.get('data', {})
        
        # 检查是否有标题
        if data.get('title'):
            score += 2
        
        # 检查是否有描述
        if data.get('description'):
            score += 2
        
        # 检查是否有其他元数据
        if data.get('author') or data.get('published_date'):
            score += 1
        
        return score
    
    def _get_quality_level(self, score: int) -> str:
        """
        获取质量等级
        """
        if score >= 40:
            return 'excellent'
        elif score >= 30:
            return 'good'
        elif score >= 20:
            return 'fair'
        else:
            return 'poor'

class ContentCleaner:
    def __init__(self):
        self.noise_patterns = [
            r'\[Advertisement\].*?\[/Advertisement\]',
            r'\bAd\b.*?\n',
            r'Subscribe to.*?newsletter',
            r'Follow us on.*?social media',
            r'Cookie policy.*?\n'
        ]
    
    def clean_content(self, content: Dict) -> Dict:
        """
        清洗内容
        """
        cleaned_content = content.copy()
        
        if 'data' in cleaned_content and 'markdown' in cleaned_content['data']:
            markdown = cleaned_content['data']['markdown']
            
            # 移除噪音内容
            cleaned_markdown = self._remove_noise(markdown)
            
            # 标准化格式
            cleaned_markdown = self._normalize_format(cleaned_markdown)
            
            # 修复常见问题
            cleaned_markdown = self._fix_common_issues(cleaned_markdown)
            
            cleaned_content['data']['markdown'] = cleaned_markdown
        
        return cleaned_content
    
    def _remove_noise(self, markdown: str) -> str:
        """
        移除噪音内容
        """
        for pattern in self.noise_patterns:
            markdown = re.sub(pattern, '', markdown, flags=re.IGNORECASE | re.DOTALL)
        
        return markdown
    
    def _normalize_format(self, markdown: str) -> str:
        """
        标准化格式
        """
        # 统一换行符
        markdown = re.sub(r'\r\n', '\n', markdown)
        
        # 移除多余空行
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # 修复标题格式
        markdown = re.sub(r'^(#{1,6})([^\s])', r'\1 \2', markdown, flags=re.MULTILINE)
        
        # 修复列表格式
        markdown = re.sub(r'^([*+-])([^\s])', r'\1 \2', markdown, flags=re.MULTILINE)
        
        return markdown.strip()
    
    def _fix_common_issues(self, markdown: str) -> str:
        """
        修复常见问题
        """
        # 修复链接格式
        markdown = re.sub(r'\[([^\]]+)\]\s*\(([^)]+)\)', r'[\1](\2)', markdown)
        
        # 修复图片格式
        markdown = re.sub(r'!\[([^\]]*)\]\s*\(([^)]+)\)', r'![\1](\2)', markdown)
        
        # 移除HTML标签残留
        markdown = re.sub(r'<[^>]+>', '', markdown)
        
        return markdown

class DuplicateDetector:
    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold
        self.content_hashes = set()
        self.content_fingerprints = []
    
    def is_duplicate(self, content: str) -> Tuple[bool, float]:
        """
        检查是否重复内容
        """
        # 生成内容哈希
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # 精确重复检查
        if content_hash in self.content_hashes:
            return True, 1.0
        
        # 相似度检查
        content_fingerprint = self._generate_fingerprint(content)
        
        for existing_fingerprint in self.content_fingerprints:
            similarity = self._calculate_similarity(content_fingerprint, existing_fingerprint)
            if similarity >= self.similarity_threshold:
                return True, similarity
        
        # 记录新内容
        self.content_hashes.add(content_hash)
        self.content_fingerprints.append(content_fingerprint)
        
        return False, 0.0
    
    def _generate_fingerprint(self, content: str) -> str:
        """
        生成内容指纹
        """
        # 移除标点和空格，转换为小写
        cleaned = re.sub(r'[^\w\s]', '', content.lower())
        words = cleaned.split()
        
        # 取前50个和后50个词作为指纹
        if len(words) > 100:
            fingerprint_words = words[:50] + words[-50:]
        else:
            fingerprint_words = words
        
        return ' '.join(fingerprint_words)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度
        """
        return difflib.SequenceMatcher(None, text1, text2).ratio()
```

## 成本控制与配额管理

### 1. 智能配额管理

```python
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class QuotaUsage:
    api_calls: int
    pages_crawled: int
    data_extracted_mb: float
    cost_usd: float
    timestamp: datetime

class QuotaManager:
    def __init__(self, monthly_budget: float = 100.0):
        self.monthly_budget = monthly_budget
        self.usage_history: List[QuotaUsage] = []
        self.cost_per_operation = {
            'scrape': 0.01,
            'crawl_page': 0.01,
            'extract': 0.02,
            'search': 0.05,
            'map': 0.005
        }
        self.load_usage_history()
    
    def load_usage_history(self):
        """
        加载使用历史
        """
        try:
            with open('quota_usage.json', 'r') as f:
                data = json.load(f)
                for item in data:
                    usage = QuotaUsage(
                        api_calls=item['api_calls'],
                        pages_crawled=item['pages_crawled'],
                        data_extracted_mb=item['data_extracted_mb'],
                        cost_usd=item['cost_usd'],
                        timestamp=datetime.fromisoformat(item['timestamp'])
                    )
                    self.usage_history.append(usage)
        except FileNotFoundError:
            pass
    
    def save_usage_history(self):
        """
        保存使用历史
        """
        data = []
        for usage in self.usage_history:
            data.append({
                'api_calls': usage.api_calls,
                'pages_crawled': usage.pages_crawled,
                'data_extracted_mb': usage.data_extracted_mb,
                'cost_usd': usage.cost_usd,
                'timestamp': usage.timestamp.isoformat()
            })
        
        with open('quota_usage.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def record_usage(self, operation: str, pages: int = 1, data_size_mb: float = 0.1):
        """
        记录使用情况
        """
        cost = self.cost_per_operation.get(operation, 0.01) * pages
        
        usage = QuotaUsage(
            api_calls=1,
            pages_crawled=pages,
            data_extracted_mb=data_size_mb,
            cost_usd=cost,
            timestamp=datetime.now()
        )
        
        self.usage_history.append(usage)
        self.save_usage_history()
    
    def get_current_month_usage(self) -> Dict[str, float]:
        """
        获取当月使用情况
        """
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        month_usage = [
            usage for usage in self.usage_history
            if usage.timestamp >= month_start
        ]
        
        total_calls = sum(usage.api_calls for usage in month_usage)
        total_pages = sum(usage.pages_crawled for usage in month_usage)
        total_data = sum(usage.data_extracted_mb for usage in month_usage)
        total_cost = sum(usage.cost_usd for usage in month_usage)
        
        return {
            'api_calls': total_calls,
            'pages_crawled': total_pages,
            'data_extracted_mb': total_data,
            'cost_usd': total_cost,
            'budget_remaining': self.monthly_budget - total_cost,
            'budget_usage_percent': (total_cost / self.monthly_budget) * 100
        }
    
    def can_afford_operation(self, operation: str, pages: int = 1) -> Tuple[bool, str]:
        """
        检查是否可以执行操作
        """
        estimated_cost = self.cost_per_operation.get(operation, 0.01) * pages
        current_usage = self.get_current_month_usage()
        
        if current_usage['budget_remaining'] < estimated_cost:
            return False, f"预算不足。剩余: ${current_usage['budget_remaining']:.2f}, 需要: ${estimated_cost:.2f}"
        
        # 检查是否接近预算限制
        if current_usage['budget_usage_percent'] > 90:
            return False, f"已使用预算的 {current_usage['budget_usage_percent']:.1f}%，接近限制"
        
        return True, "可以执行"
    
    def get_cost_optimization_suggestions(self) -> List[str]:
        """
        获取成本优化建议
        """
        suggestions = []
        current_usage = self.get_current_month_usage()
        
        if current_usage['budget_usage_percent'] > 80:
            suggestions.append("预算使用率较高，建议减少爬取频率")
        
        # 分析操作类型
        recent_usage = [
            usage for usage in self.usage_history
            if usage.timestamp > datetime.now() - timedelta(days=7)
        ]
        
        if len(recent_usage) > 100:
            suggestions.append("API调用频率较高，建议使用缓存减少重复请求")
        
        avg_pages_per_call = current_usage['pages_crawled'] / max(current_usage['api_calls'], 1)
        if avg_pages_per_call < 5:
            suggestions.append("平均每次调用爬取页面较少，建议批量处理")
        
        return suggestions
    
    def generate_usage_report(self) -> str:
        """
        生成使用报告
        """
        current_usage = self.get_current_month_usage()
        suggestions = self.get_cost_optimization_suggestions()
        
        report = f"""
# Firecrawl 使用报告 - {datetime.now().strftime('%Y年%m月')}

## 当月使用情况
- API调用次数: {current_usage['api_calls']:,}
- 爬取页面数: {current_usage['pages_crawled']:,}
- 提取数据量: {current_usage['data_extracted_mb']:.2f} MB
- 总费用: ${current_usage['cost_usd']:.2f}
- 剩余预算: ${current_usage['budget_remaining']:.2f}
- 预算使用率: {current_usage['budget_usage_percent']:.1f}%

## 成本优化建议
"""
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                report += f"{i}. {suggestion}\n"
        else:
            report += "当前使用情况良好，无特殊建议。\n"
        
        return report

class CostOptimizedFirecrawl:
    def __init__(self, api_key: str, monthly_budget: float = 100.0):
        self.firecrawl = Firecrawl(api_key=api_key)
        self.quota_manager = QuotaManager(monthly_budget)
    
    def smart_scrape(self, url: str, **kwargs) -> Dict:
        """
        智能抓取，考虑成本
        """
        # 检查预算
        can_afford, message = self.quota_manager.can_afford_operation('scrape')
        if not can_afford:
            raise Exception(f"操作被拒绝: {message}")
        
        # 执行抓取
        result = self.firecrawl.scrape(url=url, **kwargs)
        
        # 记录使用情况
        data_size = len(str(result)) / (1024 * 1024)  # 转换为MB
        self.quota_manager.record_usage('scrape', 1, data_size)
        
        return result
    
    def budget_aware_crawl(self, url: str, max_pages: int = None, **kwargs) -> str:
        """
        预算感知的爬取
        """
        # 估算页面数
        if max_pages is None:
            # 先用map估算
            map_result = self.firecrawl.map(url=url, limit=10)
            estimated_pages = min(len(map_result.get('links', [])), 100)
        else:
            estimated_pages = max_pages
        
        # 检查预算
        can_afford, message = self.quota_manager.can_afford_operation('crawl_page', estimated_pages)
        if not can_afford:
            # 尝试减少页面数
            current_usage = self.quota_manager.get_current_month_usage()
            affordable_pages = int(current_usage['budget_remaining'] / self.quota_manager.cost_per_operation['crawl_page'])
            
            if affordable_pages > 0:
                print(f"预算限制，将爬取页面数从 {estimated_pages} 减少到 {affordable_pages}")
                kwargs['limit'] = affordable_pages
            else:
                raise Exception(f"操作被拒绝: {message}")
        
        # 执行爬取
        crawl_id = self.firecrawl.crawl(url=url, **kwargs)
        
        # 记录使用情况
        actual_pages = kwargs.get('limit', estimated_pages)
        self.quota_manager.record_usage('crawl_page', actual_pages)
        
        return crawl_id
    
    def get_usage_summary(self) -> Dict:
        """
        获取使用摘要
        """
        return self.quota_manager.get_current_month_usage()
```

## 总结

这份最佳实践指南涵盖了Firecrawl使用中的关键方面：

### 核心原则
1. **性能优先** - 选择合适的抓取模式，优化请求参数
2. **稳定可靠** - 实现完善的错误处理和重试机制
3. **智能规避** - 应对各种反爬虫机制
4. **质量保证** - 确保数据的准确性和完整性
5. **成本控制** - 合理管理API配额和预算

### 实施建议
1. **分阶段实施** - 从基础功能开始，逐步添加高级特性
2. **监控优化** - 持续监控性能和成本，及时优化
3. **文档记录** - 详细记录配置和使用经验
4. **团队培训** - 确保团队成员了解最佳实践
5. **定期评估** - 定期评估和更新策略

通过遵循这些最佳实践，您可以最大化Firecrawl的价值，构建高效、稳定、经济的数据采集系统。