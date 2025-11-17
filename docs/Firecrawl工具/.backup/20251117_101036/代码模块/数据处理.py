#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理和转换模块

负责处理Firecrawl采集的原始数据，进行清洗、格式化、分类等处理，
并转换为火鸟门户API所需的标准格式。

主要功能：
- 内容清洗和过滤
- 自动分类和标签提取
- 摘要生成
- 格式转换
- 重复检测
- 数据验证

作者: Trae IDE Agent
创建时间: 2025-01-17
版本: v1.0
"""

import re
import hashlib
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass, field
from urllib.parse import urlparse, urljoin
from pathlib import Path
import json

# 第三方库（需要安装）
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import jieba
    import jieba.analyse
except ImportError:
    jieba = None

try:
    from textstat import flesch_reading_ease
except ImportError:
    flesch_reading_ease = None


@dataclass
class ProcessedArticle:
    """处理后的文章数据"""
    # 基础信息
    title: str
    content: str
    url: str
    source_name: str
    
    # 元数据
    author: Optional[str] = None
    publish_date: Optional[datetime] = None
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    # 处理后的内容
    summary: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    content_hash: Optional[str] = None
    
    # 质量指标
    content_length: int = 0
    reading_time: int = 0  # 预估阅读时间（分钟）
    quality_score: float = 0.0
    language: str = "zh"
    
    # 处理状态
    processed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    processing_version: str = "1.0"
    
    # 火鸟门户API格式
    def to_huoniao_format(self) -> Dict[str, Any]:
        """转换为火鸟门户API格式"""
        return {
            "title": self.title,
            "content": self.content,
            "summary": self.summary or self._generate_simple_summary(),
            "author": self.author or "系统采集",
            "source_url": self.url,
            "category": self.category or "未分类",
            "tags": ",".join(self.tags) if self.tags else "",
            "publish_time": self.publish_date.isoformat() if self.publish_date else datetime.now().isoformat(),
            "status": "draft",  # 默认为草稿状态
            "meta_data": {
                "source_name": self.source_name,
                "content_length": self.content_length,
                "reading_time": self.reading_time,
                "quality_score": self.quality_score,
                "language": self.language,
                "keywords": self.keywords,
                "content_hash": self.content_hash,
                "processed_at": self.processed_at.isoformat(),
                "processing_version": self.processing_version
            }
        }
    
    def _generate_simple_summary(self) -> str:
        """生成简单摘要"""
        if not self.content:
            return ""
        
        # 简单的摘要生成：取前200个字符
        content_text = re.sub(r'<[^>]+>', '', self.content)  # 移除HTML标签
        content_text = re.sub(r'\s+', ' ', content_text).strip()  # 规范化空白字符
        
        if len(content_text) <= 200:
            return content_text
        
        # 尝试在句号处截断
        summary = content_text[:200]
        last_period = summary.rfind('。')
        if last_period > 100:  # 确保摘要不会太短
            summary = summary[:last_period + 1]
        else:
            summary = summary + "..."
        
        return summary


class ContentCleaner:
    """内容清洗器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 需要移除的HTML标签
        self.remove_tags = {
            'script', 'style', 'nav', 'header', 'footer', 
            'aside', 'advertisement', 'ads', 'comment'
        }
        
        # 需要保留的HTML标签
        self.keep_tags = {
            'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'pre', 'code',
            'strong', 'b', 'em', 'i', 'a', 'img'
        }
    
    def clean_html(self, html_content: str) -> str:
        """清洗HTML内容
        
        Args:
            html_content: 原始HTML内容
            
        Returns:
            str: 清洗后的HTML内容
        """
        if not html_content or not BeautifulSoup:
            return html_content
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 移除不需要的标签
            for tag_name in self.remove_tags:
                for tag in soup.find_all(tag_name):
                    tag.decompose()
            
            # 移除注释
            for comment in soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--')):
                comment.extract()
            
            # 清理属性，只保留必要的
            for tag in soup.find_all():
                if tag.name in self.keep_tags:
                    # 保留有用的属性
                    attrs_to_keep = {}
                    if tag.name == 'a' and 'href' in tag.attrs:
                        attrs_to_keep['href'] = tag.attrs['href']
                    elif tag.name == 'img':
                        if 'src' in tag.attrs:
                            attrs_to_keep['src'] = tag.attrs['src']
                        if 'alt' in tag.attrs:
                            attrs_to_keep['alt'] = tag.attrs['alt']
                    
                    tag.attrs = attrs_to_keep
                else:
                    # 不在保留列表中的标签，保留内容但移除标签
                    tag.unwrap()
            
            return str(soup)
            
        except Exception as e:
            self.logger.warning(f"HTML清洗失败: {str(e)}")
            return html_content
    
    def extract_text(self, html_content: str) -> str:
        """从HTML中提取纯文本
        
        Args:
            html_content: HTML内容
            
        Returns:
            str: 提取的纯文本
        """
        if not html_content:
            return ""
        
        if BeautifulSoup:
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
            except Exception:
                # 如果BeautifulSoup解析失败，使用正则表达式
                text = re.sub(r'<[^>]+>', '', html_content)
        else:
            # 使用正则表达式移除HTML标签
            text = re.sub(r'<[^>]+>', '', html_content)
        
        # 规范化空白字符
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def filter_content(self, content: str, min_length: int = 100, max_length: int = 50000) -> bool:
        """过滤内容
        
        Args:
            content: 内容文本
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            bool: 是否通过过滤
        """
        if not content:
            return False
        
        content_length = len(content.strip())
        
        # 长度检查
        if content_length < min_length or content_length > max_length:
            return False
        
        # 内容质量检查
        # 检查是否包含足够的有意义内容
        words = content.split()
        if len(words) < 20:  # 至少20个词
            return False
        
        # 检查重复内容比例
        unique_words = set(words)
        if len(unique_words) / len(words) < 0.3:  # 独特词汇比例至少30%
            return False
        
        return True


class CategoryClassifier:
    """分类器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 分类关键词映射
        self.category_keywords = {
            "技术资讯": [
                "技术", "开发", "编程", "代码", "算法", "架构", "框架", 
                "API", "数据库", "云计算", "人工智能", "机器学习", "区块链"
            ],
            "产品动态": [
                "产品", "功能", "更新", "发布", "版本", "特性", "改进", 
                "优化", "升级", "新增", "支持"
            ],
            "行业新闻": [
                "行业", "市场", "趋势", "报告", "分析", "预测", "投资", 
                "融资", "并购", "合作", "竞争"
            ],
            "教程指南": [
                "教程", "指南", "如何", "步骤", "方法", "技巧", "实践", 
                "案例", "示例", "演示", "入门", "进阶"
            ],
            "公司动态": [
                "公司", "团队", "招聘", "文化", "活动", "会议", "演讲", 
                "获奖", "认证", "合规", "公告"
            ]
        }
    
    def classify(self, title: str, content: str, url: str = "") -> str:
        """分类文章
        
        Args:
            title: 文章标题
            content: 文章内容
            url: 文章URL
            
        Returns:
            str: 分类名称
        """
        # 合并标题和内容进行分析（标题权重更高）
        text_to_analyze = (title * 3 + " " + content[:1000]).lower()
        
        # URL路径分析
        url_path = ""
        if url:
            try:
                parsed_url = urlparse(url)
                url_path = parsed_url.path.lower()
            except Exception:
                pass
        
        category_scores = {}
        
        # 基于关键词计算分数
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                # 在文本中计算关键词出现次数
                score += text_to_analyze.count(keyword.lower())
                # URL路径中的关键词权重更高
                if keyword.lower() in url_path:
                    score += 5
            
            category_scores[category] = score
        
        # 返回得分最高的分类
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
        
        return "未分类"


class KeywordExtractor:
    """关键词提取器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 停用词列表
        self.stop_words = {
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", 
            "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", 
            "你", "会", "着", "没有", "看", "好", "自己", "这", "那", "它",
            "他", "她", "我们", "你们", "他们", "这个", "那个", "什么", "怎么",
            "为什么", "因为", "所以", "但是", "然后", "如果", "虽然", "可以",
            "应该", "需要", "可能", "已经", "还是", "或者", "而且", "不过"
        }
    
    def extract_keywords(self, title: str, content: str, max_keywords: int = 10) -> List[str]:
        """提取关键词
        
        Args:
            title: 文章标题
            content: 文章内容
            max_keywords: 最大关键词数量
            
        Returns:
            List[str]: 关键词列表
        """
        keywords = []
        
        # 合并标题和内容
        text = title + " " + content
        
        if jieba:
            try:
                # 使用jieba进行关键词提取
                keywords = jieba.analyse.extract_tags(
                    text, 
                    topK=max_keywords,
                    withWeight=False,
                    allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'v', 'vn', 'a', 'ad')
                )
                
                # 过滤停用词
                keywords = [kw for kw in keywords if kw not in self.stop_words and len(kw) > 1]
                
            except Exception as e:
                self.logger.warning(f"jieba关键词提取失败: {str(e)}")
                keywords = self._simple_keyword_extraction(text, max_keywords)
        else:
            # 简单的关键词提取
            keywords = self._simple_keyword_extraction(text, max_keywords)
        
        return keywords[:max_keywords]
    
    def _simple_keyword_extraction(self, text: str, max_keywords: int) -> List[str]:
        """简单的关键词提取"""
        # 移除标点符号和特殊字符
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 分词（简单按空格分割）
        words = text.split()
        
        # 统计词频
        word_freq = {}
        for word in words:
            word = word.strip().lower()
            if len(word) > 1 and word not in self.stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 按频率排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:max_keywords]]


class DataProcessor:
    """数据处理器主类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化数据处理器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # 初始化组件
        self.cleaner = ContentCleaner()
        self.classifier = CategoryClassifier()
        self.keyword_extractor = KeywordExtractor()
        
        # 处理配置
        self.min_content_length = self.config.get('min_content_length', 100)
        self.max_content_length = self.config.get('max_content_length', 50000)
        self.enable_dedup = self.config.get('enable_dedup', True)
        self.auto_category = self.config.get('auto_category', True)
        self.extract_keywords = self.config.get('extract_keywords', True)
        self.extract_summary = self.config.get('extract_summary', True)
        
        # 重复检测缓存
        self.content_hashes = set()
    
    def process_article(self, raw_data: Dict[str, Any]) -> Optional[ProcessedArticle]:
        """处理单篇文章
        
        Args:
            raw_data: Firecrawl返回的原始数据
            
        Returns:
            Optional[ProcessedArticle]: 处理后的文章数据
        """
        try:
            # 提取基础信息
            title = raw_data.get('title', '').strip()
            content = raw_data.get('content', '').strip()
            url = raw_data.get('url', '').strip()
            source_name = raw_data.get('source_name', '未知来源')
            
            if not title or not content or not url:
                self.logger.warning(f"文章数据不完整: {url}")
                return None
            
            # 清洗内容
            cleaned_content = self.cleaner.clean_html(content)
            content_text = self.cleaner.extract_text(cleaned_content)
            
            # 内容过滤
            if not self.cleaner.filter_content(
                content_text, 
                self.min_content_length, 
                self.max_content_length
            ):
                self.logger.info(f"文章内容未通过过滤: {url}")
                return None
            
            # 重复检测
            content_hash = self._calculate_content_hash(title + content_text)
            if self.enable_dedup and content_hash in self.content_hashes:
                self.logger.info(f"检测到重复内容: {url}")
                return None
            
            self.content_hashes.add(content_hash)
            
            # 创建处理后的文章对象
            article = ProcessedArticle(
                title=title,
                content=cleaned_content,
                url=url,
                source_name=source_name,
                content_hash=content_hash,
                content_length=len(content_text)
            )
            
            # 提取元数据
            article.author = raw_data.get('author')
            article.publish_date = self._parse_date(raw_data.get('publish_date'))
            
            # 自动分类
            if self.auto_category:
                article.category = self.classifier.classify(title, content_text, url)
            
            # 提取关键词
            if self.extract_keywords:
                article.keywords = self.keyword_extractor.extract_keywords(title, content_text)
            
            # 生成摘要
            if self.extract_summary:
                article.summary = self._generate_summary(title, content_text)
            
            # 计算质量分数
            article.quality_score = self._calculate_quality_score(article)
            
            # 计算阅读时间
            article.reading_time = self._calculate_reading_time(content_text)
            
            # 语言检测
            article.language = self._detect_language(content_text)
            
            return article
            
        except Exception as e:
            self.logger.error(f"处理文章失败: {str(e)}, URL: {raw_data.get('url', 'unknown')}")
            return None
    
    def process_batch(self, raw_data_list: List[Dict[str, Any]]) -> List[ProcessedArticle]:
        """批量处理文章
        
        Args:
            raw_data_list: 原始数据列表
            
        Returns:
            List[ProcessedArticle]: 处理后的文章列表
        """
        processed_articles = []
        
        for raw_data in raw_data_list:
            article = self.process_article(raw_data)
            if article:
                processed_articles.append(article)
        
        self.logger.info(f"批量处理完成: {len(processed_articles)}/{len(raw_data_list)} 篇文章")
        return processed_articles
    
    def _calculate_content_hash(self, content: str) -> str:
        """计算内容哈希"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_str:
            return None
        
        # 常见日期格式
        date_formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d',
            '%d/%m/%Y',
            '%d-%m-%Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        self.logger.warning(f"无法解析日期格式: {date_str}")
        return None
    
    def _generate_summary(self, title: str, content: str, max_length: int = 200) -> str:
        """生成文章摘要"""
        # 简单的摘要生成策略
        # 1. 如果内容较短，直接返回
        if len(content) <= max_length:
            return content
        
        # 2. 尝试提取前几句话
        sentences = re.split(r'[。！？.!?]', content)
        summary = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(summary + sentence) <= max_length - 3:
                summary += sentence + "。"
            else:
                break
        
        if not summary:
            # 如果没有找到合适的句子，直接截取
            summary = content[:max_length - 3] + "..."
        
        return summary
    
    def _calculate_quality_score(self, article: ProcessedArticle) -> float:
        """计算文章质量分数"""
        score = 0.0
        
        # 标题质量 (20%)
        title_score = min(len(article.title) / 50, 1.0) * 0.2
        score += title_score
        
        # 内容长度 (30%)
        content_length_score = min(article.content_length / 2000, 1.0) * 0.3
        score += content_length_score
        
        # 关键词数量 (20%)
        keyword_score = min(len(article.keywords) / 10, 1.0) * 0.2
        score += keyword_score
        
        # 是否有作者 (10%)
        if article.author:
            score += 0.1
        
        # 是否有发布日期 (10%)
        if article.publish_date:
            score += 0.1
        
        # 是否有分类 (10%)
        if article.category and article.category != "未分类":
            score += 0.1
        
        return round(score, 2)
    
    def _calculate_reading_time(self, content: str) -> int:
        """计算预估阅读时间（分钟）"""
        # 假设平均阅读速度为每分钟200个中文字符
        words_per_minute = 200
        reading_time = max(1, len(content) // words_per_minute)
        return reading_time
    
    def _detect_language(self, content: str) -> str:
        """检测语言"""
        # 简单的语言检测
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_chars = len(re.findall(r'[a-zA-Z]', content))
        
        if chinese_chars > english_chars:
            return "zh"
        elif english_chars > 0:
            return "en"
        else:
            return "unknown"
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取处理统计信息"""
        return {
            "processed_articles": len(self.content_hashes),
            "unique_content_hashes": len(self.content_hashes),
            "deduplication_enabled": self.enable_dedup,
            "auto_categorization_enabled": self.auto_category,
            "keyword_extraction_enabled": self.extract_keywords,
            "summary_generation_enabled": self.extract_summary
        }
    
    def reset_cache(self):
        """重置缓存"""
        self.content_hashes.clear()
        self.logger.info("处理器缓存已重置")


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建数据处理器
    config = {
        'min_content_length': 100,
        'max_content_length': 50000,
        'enable_dedup': True,
        'auto_category': True,
        'extract_keywords': True,
        'extract_summary': True
    }
    
    processor = DataProcessor(config)
    
    # 模拟原始数据
    raw_data = {
        'title': 'Firecrawl API 使用指南',
        'content': '<p>Firecrawl是一个强大的网页抓取API服务...</p>',
        'url': 'https://docs.firecrawl.dev/guide',
        'source_name': 'Firecrawl文档',
        'author': 'Firecrawl团队',
        'publish_date': '2025-01-17'
    }
    
    # 处理文章
    article = processor.process_article(raw_data)
    
    if article:
        print("处理成功!")
        print(f"标题: {article.title}")
        print(f"分类: {article.category}")
        print(f"关键词: {', '.join(article.keywords)}")
        print(f"摘要: {article.summary}")
        print(f"质量分数: {article.quality_score}")
        print(f"阅读时间: {article.reading_time}分钟")
        
        # 转换为火鸟门户格式
        huoniao_data = article.to_huoniao_format()
        print("\n火鸟门户API格式:")
        print(json.dumps(huoniao_data, ensure_ascii=False, indent=2))
    else:
        print("处理失败!")
    
    # 打印统计信息
    stats = processor.get_statistics()
    print("\n处理统计:")
    for key, value in stats.items():
        print(f"  {key}: {value}")