# Firecrawl 实际应用案例

> 真实项目中的Firecrawl应用实例和解决方案
> 更新时间: 2024年

## 目录

1. [新闻资讯采集系统](#新闻资讯采集系统)
2. [电商价格监控系统](#电商价格监控系统)
3. [学术论文收集器](#学术论文收集器)
4. [竞品分析工具](#竞品分析工具)
5. [内容聚合平台](#内容聚合平台)
6. [SEO分析工具](#seo分析工具)
7. [社交媒体监控](#社交媒体监控)
8. [房产信息采集](#房产信息采集)
9. [招聘信息聚合](#招聘信息聚合)
10. [技术文档整理](#技术文档整理)

## 新闻资讯采集系统

### 项目背景
构建一个自动化新闻采集系统，从多个新闻网站收集最新资讯，进行分类整理并推送给用户。

### 技术架构
```
新闻源网站 → Firecrawl API → 内容处理 → 数据库存储 → 用户界面
```

### 实现代码

```python
import asyncio
import json
from datetime import datetime, timedelta
from firecrawl import Firecrawl
from dataclasses import dataclass
from typing import List, Dict
import sqlite3
import hashlib

@dataclass
class NewsArticle:
    title: str
    content: str
    url: str
    published_date: str
    category: str
    source: str
    summary: str
    keywords: List[str]

class NewsCollector:
    def __init__(self, api_key: str):
        self.firecrawl = Firecrawl(api_key=api_key)
        self.news_sources = {
            "科技": [
                "https://techcrunch.com",
                "https://www.theverge.com",
                "https://arstechnica.com"
            ],
            "财经": [
                "https://www.bloomberg.com",
                "https://www.reuters.com/business",
                "https://finance.yahoo.com"
            ],
            "AI": [
                "https://www.artificialintelligence-news.com",
                "https://venturebeat.com/ai"
            ]
        }
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect('news.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                url TEXT UNIQUE,
                published_date TEXT,
                category TEXT,
                source TEXT,
                summary TEXT,
                keywords TEXT,
                content_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def get_content_hash(self, content: str) -> str:
        """生成内容哈希用于去重"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def is_duplicate(self, content_hash: str) -> bool:
        """检查是否重复内容"""
        cursor = self.conn.execute(
            "SELECT 1 FROM articles WHERE content_hash = ?", 
            (content_hash,)
        )
        return cursor.fetchone() is not None
    
    def extract_article_info(self, url: str) -> Dict:
        """提取文章信息"""
        try:
            result = self.firecrawl.scrape(
                url=url,
                formats=[{
                    "type": "json",
                    "prompt": """
                    请提取以下信息：
                    1. 文章标题
                    2. 文章正文内容
                    3. 发布日期
                    4. 作者
                    5. 文章摘要（如果没有请生成一个100字以内的摘要）
                    6. 关键词（3-5个）
                    
                    请确保提取的内容准确完整。
                    """,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "published_date": {"type": "string"},
                            "author": {"type": "string"},
                            "summary": {"type": "string"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["title", "content"]
                    }
                }],
                only_main_content=True,
                exclude_tags=["nav", "footer", "aside", "ads"]
            )
            
            return result['data']['json']
        except Exception as e:
            print(f"提取文章信息失败 {url}: {e}")
            return None
    
    def collect_from_source(self, source_url: str, category: str) -> List[NewsArticle]:
        """从单个新闻源收集文章"""
        articles = []
        
        try:
            # 首先获取网站地图
            map_result = self.firecrawl.map(
                url=source_url,
                limit=100
            )
            
            # 过滤出文章链接
            article_urls = []
            for link in map_result['links']:
                # 根据URL模式过滤文章链接
                if any(pattern in link.lower() for pattern in 
                      ['/article/', '/news/', '/post/', '/blog/', '/story/']):
                    article_urls.append(link)
            
            # 限制每次处理的文章数量
            article_urls = article_urls[:20]
            
            print(f"从 {source_url} 发现 {len(article_urls)} 篇文章")
            
            for url in article_urls:
                article_info = self.extract_article_info(url)
                if not article_info:
                    continue
                
                # 检查内容是否重复
                content_hash = self.get_content_hash(article_info.get('content', ''))
                if self.is_duplicate(content_hash):
                    continue
                
                article = NewsArticle(
                    title=article_info.get('title', ''),
                    content=article_info.get('content', ''),
                    url=url,
                    published_date=article_info.get('published_date', ''),
                    category=category,
                    source=source_url,
                    summary=article_info.get('summary', ''),
                    keywords=article_info.get('keywords', [])
                )
                
                articles.append(article)
                
                # 保存到数据库
                self.save_article(article, content_hash)
                
        except Exception as e:
            print(f"收集新闻失败 {source_url}: {e}")
        
        return articles
    
    def save_article(self, article: NewsArticle, content_hash: str):
        """保存文章到数据库"""
        try:
            self.conn.execute("""
                INSERT OR IGNORE INTO articles 
                (title, content, url, published_date, category, source, summary, keywords, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.title,
                article.content,
                article.url,
                article.published_date,
                article.category,
                article.source,
                article.summary,
                json.dumps(article.keywords),
                content_hash
            ))
            self.conn.commit()
        except Exception as e:
            print(f"保存文章失败: {e}")
    
    def collect_all_news(self):
        """收集所有新闻源的文章"""
        all_articles = []
        
        for category, sources in self.news_sources.items():
            print(f"\n开始收集 {category} 类别新闻...")
            
            for source in sources:
                print(f"正在处理: {source}")
                articles = self.collect_from_source(source, category)
                all_articles.extend(articles)
                print(f"收集到 {len(articles)} 篇文章")
        
        return all_articles
    
    def get_recent_articles(self, hours: int = 24) -> List[Dict]:
        """获取最近的文章"""
        cursor = self.conn.execute("""
            SELECT title, url, category, summary, created_at 
            FROM articles 
            WHERE created_at > datetime('now', '-{} hours')
            ORDER BY created_at DESC
        """.format(hours))
        
        return [{
            'title': row[0],
            'url': row[1],
            'category': row[2],
            'summary': row[3],
            'created_at': row[4]
        } for row in cursor.fetchall()]
    
    def generate_daily_report(self) -> str:
        """生成每日新闻报告"""
        articles = self.get_recent_articles(24)
        
        if not articles:
            return "今日暂无新闻更新"
        
        # 按类别分组
        by_category = {}
        for article in articles:
            category = article['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(article)
        
        report = f"# 每日新闻报告 - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        report += f"今日共收集到 {len(articles)} 篇文章\n\n"
        
        for category, cat_articles in by_category.items():
            report += f"## {category} ({len(cat_articles)}篇)\n\n"
            for article in cat_articles[:5]:  # 每个类别显示前5篇
                report += f"- **{article['title']}**\n"
                report += f"  {article['summary']}\n"
                report += f"  [阅读原文]({article['url']})\n\n"
        
        return report

# 使用示例
if __name__ == "__main__":
    collector = NewsCollector(api_key="fc-YOUR-API-KEY")
    
    # 收集新闻
    print("开始收集新闻...")
    articles = collector.collect_all_news()
    print(f"\n总共收集到 {len(articles)} 篇文章")
    
    # 生成报告
    report = collector.generate_daily_report()
    print("\n=== 每日新闻报告 ===")
    print(report)
    
    # 保存报告
    with open(f"news_report_{datetime.now().strftime('%Y%m%d')}.md", 'w', encoding='utf-8') as f:
        f.write(report)
```

### 定时任务配置

```python
import schedule
import time

def run_news_collection():
    """运行新闻收集任务"""
    collector = NewsCollector(api_key="fc-YOUR-API-KEY")
    collector.collect_all_news()
    
    # 发送每日报告
    report = collector.generate_daily_report()
    # 这里可以集成邮件发送或推送通知
    print("新闻收集完成")

# 每天早上8点和下午6点运行
schedule.every().day.at("08:00").do(run_news_collection)
schedule.every().day.at("18:00").do(run_news_collection)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 电商价格监控系统

### 项目背景
监控电商平台商品价格变化，为用户提供价格趋势分析和降价提醒。

### 实现代码

```python
import asyncio
from datetime import datetime
from firecrawl import Firecrawl
from dataclasses import dataclass
from typing import List, Optional
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

@dataclass
class Product:
    name: str
    url: str
    current_price: float
    original_price: float
    availability: str
    rating: float
    reviews_count: int
    description: str
    images: List[str]
    last_updated: datetime

class PriceMonitor:
    def __init__(self, api_key: str):
        self.firecrawl = Firecrawl(api_key=api_key)
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect('price_monitor.db')
        
        # 产品表
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT UNIQUE,
                target_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 价格历史表
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                price REAL,
                availability TEXT,
                rating REAL,
                reviews_count INTEGER,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        self.conn.commit()
    
    def extract_product_info(self, url: str) -> Optional[Product]:
        """提取商品信息"""
        try:
            result = self.firecrawl.scrape(
                url=url,
                formats=[{
                    "type": "json",
                    "prompt": """
                    请提取以下商品信息：
                    1. 商品名称
                    2. 当前价格（数字）
                    3. 原价（如果有折扣）
                    4. 库存状态（有货/缺货/预订等）
                    5. 评分（1-5分）
                    6. 评论数量
                    7. 商品描述
                    8. 商品图片链接
                    
                    请确保价格是纯数字，不包含货币符号。
                    """,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "current_price": {"type": "number"},
                            "original_price": {"type": "number"},
                            "availability": {"type": "string"},
                            "rating": {"type": "number"},
                            "reviews_count": {"type": "integer"},
                            "description": {"type": "string"},
                            "images": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["name", "current_price"]
                    }
                }],
                only_main_content=True,
                wait_for=3000
            )
            
            data = result['data']['json']
            
            return Product(
                name=data.get('name', ''),
                url=url,
                current_price=data.get('current_price', 0),
                original_price=data.get('original_price', data.get('current_price', 0)),
                availability=data.get('availability', '未知'),
                rating=data.get('rating', 0),
                reviews_count=data.get('reviews_count', 0),
                description=data.get('description', ''),
                images=data.get('images', []),
                last_updated=datetime.now()
            )
            
        except Exception as e:
            print(f"提取商品信息失败 {url}: {e}")
            return None
    
    def add_product(self, url: str, target_price: float = None) -> int:
        """添加监控商品"""
        product = self.extract_product_info(url)
        if not product:
            raise ValueError("无法提取商品信息")
        
        cursor = self.conn.execute("""
            INSERT OR REPLACE INTO products (name, url, target_price)
            VALUES (?, ?, ?)
        """, (product.name, url, target_price))
        
        product_id = cursor.lastrowid
        
        # 记录初始价格
        self.record_price(product_id, product)
        
        self.conn.commit()
        return product_id
    
    def record_price(self, product_id: int, product: Product):
        """记录价格历史"""
        self.conn.execute("""
            INSERT INTO price_history 
            (product_id, price, availability, rating, reviews_count)
            VALUES (?, ?, ?, ?, ?)
        """, (
            product_id,
            product.current_price,
            product.availability,
            product.rating,
            product.reviews_count
        ))
    
    def check_all_products(self) -> List[Dict]:
        """检查所有监控商品的价格"""
        cursor = self.conn.execute("SELECT id, url, target_price FROM products")
        products = cursor.fetchall()
        
        alerts = []
        
        for product_id, url, target_price in products:
            print(f"检查商品: {url}")
            
            current_product = self.extract_product_info(url)
            if not current_product:
                continue
            
            # 记录新价格
            self.record_price(product_id, current_product)
            
            # 检查是否需要发送价格提醒
            if target_price and current_product.current_price <= target_price:
                alerts.append({
                    'product_id': product_id,
                    'name': current_product.name,
                    'url': url,
                    'current_price': current_product.current_price,
                    'target_price': target_price,
                    'discount': target_price - current_product.current_price
                })
        
        self.conn.commit()
        return alerts
    
    def get_price_history(self, product_id: int, days: int = 30) -> pd.DataFrame:
        """获取价格历史"""
        query = """
            SELECT recorded_at, price, availability, rating, reviews_count
            FROM price_history
            WHERE product_id = ? AND recorded_at > datetime('now', '-{} days')
            ORDER BY recorded_at
        """.format(days)
        
        df = pd.read_sql_query(query, self.conn, params=(product_id,))
        df['recorded_at'] = pd.to_datetime(df['recorded_at'])
        return df
    
    def generate_price_chart(self, product_id: int, days: int = 30):
        """生成价格趋势图"""
        df = self.get_price_history(product_id, days)
        
        if df.empty:
            print("没有价格历史数据")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['recorded_at'], df['price'], marker='o', linewidth=2)
        plt.title(f'商品价格趋势 (最近{days}天)')
        plt.xlabel('日期')
        plt.ylabel('价格')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图表
        filename = f'price_chart_{product_id}_{datetime.now().strftime("%Y%m%d")}.png'
        plt.savefig(filename)
        plt.show()
        
        return filename
    
    def get_price_analysis(self, product_id: int) -> Dict:
        """获取价格分析"""
        df = self.get_price_history(product_id, 90)  # 90天历史
        
        if df.empty:
            return {"error": "没有足够的历史数据"}
        
        current_price = df['price'].iloc[-1]
        min_price = df['price'].min()
        max_price = df['price'].max()
        avg_price = df['price'].mean()
        
        # 计算价格趋势
        if len(df) >= 7:
            recent_avg = df['price'].tail(7).mean()
            older_avg = df['price'].head(7).mean()
            trend = "上涨" if recent_avg > older_avg else "下跌"
        else:
            trend = "数据不足"
        
        return {
            "current_price": current_price,
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
            "trend": trend,
            "discount_from_max": ((max_price - current_price) / max_price) * 100,
            "premium_from_min": ((current_price - min_price) / min_price) * 100
        }
    
    def send_price_alerts(self, alerts: List[Dict]):
        """发送价格提醒"""
        if not alerts:
            print("没有价格提醒")
            return
        
        print(f"\n=== 价格提醒 ({len(alerts)}个) ===")
        for alert in alerts:
            print(f"🎉 {alert['name']}")
            print(f"   当前价格: ${alert['current_price']:.2f}")
            print(f"   目标价格: ${alert['target_price']:.2f}")
            print(f"   节省: ${alert['discount']:.2f}")
            print(f"   链接: {alert['url']}")
            print()

# 使用示例
if __name__ == "__main__":
    monitor = PriceMonitor(api_key="fc-YOUR-API-KEY")
    
    # 添加监控商品
    product_urls = [
        "https://www.amazon.com/dp/B08N5WRWNW",  # Echo Dot
        "https://www.amazon.com/dp/B07XJ8C8F5",  # iPad
    ]
    
    for url in product_urls:
        try:
            product_id = monitor.add_product(url, target_price=50.0)
            print(f"已添加商品监控，ID: {product_id}")
        except Exception as e:
            print(f"添加失败: {e}")
    
    # 检查价格变化
    alerts = monitor.check_all_products()
    monitor.send_price_alerts(alerts)
    
    # 生成价格分析报告
    for product_id in [1, 2]:  # 假设有这些产品ID
        analysis = monitor.get_price_analysis(product_id)
        print(f"\n商品 {product_id} 价格分析:")
        print(f"当前价格: ${analysis.get('current_price', 0):.2f}")
        print(f"历史最低: ${analysis.get('min_price', 0):.2f}")
        print(f"历史最高: ${analysis.get('max_price', 0):.2f}")
        print(f"平均价格: ${analysis.get('avg_price', 0):.2f}")
        print(f"价格趋势: {analysis.get('trend', '未知')}")
```

## 学术论文收集器

### 项目背景
自动收集特定研究领域的最新学术论文，提取关键信息并进行分类整理。

### 实现代码

```python
from firecrawl import Firecrawl
from dataclasses import dataclass
from typing import List, Dict
import re
import sqlite3
from datetime import datetime
import requests
from urllib.parse import urljoin, urlparse

@dataclass
class Paper:
    title: str
    authors: List[str]
    abstract: str
    publication_date: str
    journal: str
    doi: str
    pdf_url: str
    keywords: List[str]
    citation_count: int
    url: str

class AcademicCollector:
    def __init__(self, api_key: str):
        self.firecrawl = Firecrawl(api_key=api_key)
        self.academic_sources = {
            "arxiv": "https://arxiv.org",
            "pubmed": "https://pubmed.ncbi.nlm.nih.gov",
            "ieee": "https://ieeexplore.ieee.org",
            "acm": "https://dl.acm.org"
        }
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect('academic_papers.db')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authors TEXT,
                abstract TEXT,
                publication_date TEXT,
                journal TEXT,
                doi TEXT UNIQUE,
                pdf_url TEXT,
                keywords TEXT,
                citation_count INTEGER,
                url TEXT,
                research_field TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def search_arxiv(self, query: str, max_results: int = 50) -> List[Paper]:
        """搜索arXiv论文"""
        papers = []
        
        try:
            # 使用Firecrawl搜索arXiv
            search_results = self.firecrawl.search(
                query=f"site:arxiv.org {query}",
                limit=max_results,
                scrape_options={
                    "formats": ["markdown"]
                }
            )
            
            for result in search_results['data']['web']:
                if 'arxiv.org' in result['url']:
                    paper = self.extract_arxiv_paper(result['url'])
                    if paper:
                        papers.append(paper)
        
        except Exception as e:
            print(f"搜索arXiv失败: {e}")
        
        return papers
    
    def extract_arxiv_paper(self, url: str) -> Paper:
        """提取arXiv论文信息"""
        try:
            result = self.firecrawl.scrape(
                url=url,
                formats=[{
                    "type": "json",
                    "prompt": """
                    请提取以下论文信息：
                    1. 论文标题
                    2. 作者列表（数组格式）
                    3. 摘要
                    4. 提交日期
                    5. 学科分类
                    6. DOI（如果有）
                    7. PDF下载链接
                    8. 关键词（从摘要中提取3-5个）
                    
                    请确保信息准确完整。
                    """,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "authors": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "abstract": {"type": "string"},
                            "publication_date": {"type": "string"},
                            "subject_class": {"type": "string"},
                            "doi": {"type": "string"},
                            "pdf_url": {"type": "string"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["title", "authors", "abstract"]
                    }
                }]
            )
            
            data = result['data']['json']
            
            return Paper(
                title=data.get('title', ''),
                authors=data.get('authors', []),
                abstract=data.get('abstract', ''),
                publication_date=data.get('publication_date', ''),
                journal='arXiv',
                doi=data.get('doi', ''),
                pdf_url=data.get('pdf_url', ''),
                keywords=data.get('keywords', []),
                citation_count=0,  # arXiv通常不显示引用数
                url=url
            )
            
        except Exception as e:
            print(f"提取arXiv论文失败 {url}: {e}")
            return None
    
    def search_pubmed(self, query: str, max_results: int = 50) -> List[Paper]:
        """搜索PubMed论文"""
        papers = []
        
        try:
            search_results = self.firecrawl.search(
                query=f"site:pubmed.ncbi.nlm.nih.gov {query}",
                limit=max_results,
                scrape_options={
                    "formats": ["markdown"]
                }
            )
            
            for result in search_results['data']['web']:
                if 'pubmed.ncbi.nlm.nih.gov' in result['url']:
                    paper = self.extract_pubmed_paper(result['url'])
                    if paper:
                        papers.append(paper)
        
        except Exception as e:
            print(f"搜索PubMed失败: {e}")
        
        return papers
    
    def extract_pubmed_paper(self, url: str) -> Paper:
        """提取PubMed论文信息"""
        try:
            result = self.firecrawl.scrape(
                url=url,
                formats=[{
                    "type": "json",
                    "prompt": """
                    请提取以下医学论文信息：
                    1. 论文标题
                    2. 作者列表
                    3. 摘要
                    4. 发表日期
                    5. 期刊名称
                    6. DOI
                    7. PMID
                    8. 关键词/MeSH terms
                    9. 引用次数（如果显示）
                    
                    请确保信息准确。
                    """,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "authors": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "abstract": {"type": "string"},
                            "publication_date": {"type": "string"},
                            "journal": {"type": "string"},
                            "doi": {"type": "string"},
                            "pmid": {"type": "string"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "citation_count": {"type": "integer"}
                        },
                        "required": ["title", "authors"]
                    }
                }]
            )
            
            data = result['data']['json']
            
            return Paper(
                title=data.get('title', ''),
                authors=data.get('authors', []),
                abstract=data.get('abstract', ''),
                publication_date=data.get('publication_date', ''),
                journal=data.get('journal', ''),
                doi=data.get('doi', ''),
                pdf_url='',  # PubMed通常不直接提供PDF
                keywords=data.get('keywords', []),
                citation_count=data.get('citation_count', 0),
                url=url
            )
            
        except Exception as e:
            print(f"提取PubMed论文失败 {url}: {e}")
            return None
    
    def save_paper(self, paper: Paper, research_field: str):
        """保存论文到数据库"""
        try:
            self.conn.execute("""
                INSERT OR IGNORE INTO papers 
                (title, authors, abstract, publication_date, journal, doi, 
                 pdf_url, keywords, citation_count, url, research_field)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                paper.title,
                ', '.join(paper.authors),
                paper.abstract,
                paper.publication_date,
                paper.journal,
                paper.doi,
                paper.pdf_url,
                ', '.join(paper.keywords),
                paper.citation_count,
                paper.url,
                research_field
            ))
            self.conn.commit()
        except Exception as e:
            print(f"保存论文失败: {e}")
    
    def collect_papers_by_field(self, research_field: str, keywords: List[str]) -> List[Paper]:
        """按研究领域收集论文"""
        all_papers = []
        
        for keyword in keywords:
            print(f"搜索关键词: {keyword}")
            
            # 搜索arXiv
            arxiv_papers = self.search_arxiv(keyword, max_results=20)
            print(f"从arXiv找到 {len(arxiv_papers)} 篇论文")
            
            # 搜索PubMed（如果是生物医学相关）
            if research_field.lower() in ['biology', 'medicine', 'biomedical']:
                pubmed_papers = self.search_pubmed(keyword, max_results=20)
                print(f"从PubMed找到 {len(pubmed_papers)} 篇论文")
                all_papers.extend(pubmed_papers)
            
            all_papers.extend(arxiv_papers)
            
            # 保存论文
            for paper in arxiv_papers + (pubmed_papers if 'pubmed_papers' in locals() else []):
                self.save_paper(paper, research_field)
        
        return all_papers
    
    def generate_research_report(self, research_field: str, days: int = 30) -> str:
        """生成研究报告"""
        cursor = self.conn.execute("""
            SELECT title, authors, journal, publication_date, url, keywords
            FROM papers 
            WHERE research_field = ? AND created_at > datetime('now', '-{} days')
            ORDER BY created_at DESC
        """.format(days), (research_field,))
        
        papers = cursor.fetchall()
        
        if not papers:
            return f"最近{days}天没有收集到{research_field}领域的论文"
        
        report = f"# {research_field} 研究报告\n\n"
        report += f"时间范围: 最近{days}天\n"
        report += f"论文数量: {len(papers)}篇\n\n"
        
        # 按期刊分组
        by_journal = {}
        for paper in papers:
            journal = paper[2] or '未知期刊'
            if journal not in by_journal:
                by_journal[journal] = []
            by_journal[journal].append(paper)
        
        report += "## 按期刊分布\n\n"
        for journal, journal_papers in by_journal.items():
            report += f"### {journal} ({len(journal_papers)}篇)\n\n"
            for paper in journal_papers[:5]:  # 每个期刊显示前5篇
                report += f"- **{paper[0]}**\n"
                report += f"  作者: {paper[1]}\n"
                report += f"  发表日期: {paper[3]}\n"
                report += f"  [查看详情]({paper[4]})\n\n"
        
        # 关键词统计
        all_keywords = []
        for paper in papers:
            if paper[5]:  # keywords
                all_keywords.extend([k.strip() for k in paper[5].split(',')])
        
        keyword_count = {}
        for keyword in all_keywords:
            keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        
        top_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        report += "## 热门关键词\n\n"
        for keyword, count in top_keywords:
            report += f"- {keyword}: {count}次\n"
        
        return report
    
    def download_papers(self, research_field: str, download_dir: str = "./papers"):
        """下载论文PDF"""
        import os
        
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        cursor = self.conn.execute("""
            SELECT title, pdf_url FROM papers 
            WHERE research_field = ? AND pdf_url != ''
        """, (research_field,))
        
        papers = cursor.fetchall()
        
        for title, pdf_url in papers:
            try:
                response = requests.get(pdf_url)
                if response.status_code == 200:
                    # 清理文件名
                    safe_title = re.sub(r'[^\w\s-]', '', title)[:50]
                    filename = f"{safe_title}.pdf"
                    filepath = os.path.join(download_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"已下载: {filename}")
                else:
                    print(f"下载失败: {title}")
            except Exception as e:
                print(f"下载错误 {title}: {e}")

# 使用示例
if __name__ == "__main__":
    collector = AcademicCollector(api_key="fc-YOUR-API-KEY")
    
    # 定义研究领域和关键词
    research_fields = {
        "Machine Learning": [
            "deep learning", "neural networks", "transformer", 
            "computer vision", "natural language processing"
        ],
        "Quantum Computing": [
            "quantum algorithm", "quantum machine learning", 
            "quantum cryptography", "quantum error correction"
        ],
        "Biomedical AI": [
            "medical imaging AI", "drug discovery machine learning",
            "genomics deep learning", "clinical decision support"
        ]
    }
    
    # 收集论文
    for field, keywords in research_fields.items():
        print(f"\n开始收集 {field} 领域论文...")
        papers = collector.collect_papers_by_field(field, keywords)
        print(f"收集到 {len(papers)} 篇论文")
        
        # 生成报告
        report = collector.generate_research_report(field)
        print(f"\n=== {field} 研究报告 ===")
        print(report)
        
        # 保存报告
        with open(f"{field.replace(' ', '_')}_report.md", 'w', encoding='utf-8') as f:
            f.write(report)
```

## 总结

这些实际应用案例展示了Firecrawl在不同场景下的强大能力：

### 核心优势
1. **智能内容提取** - 自动识别和提取结构化数据
2. **多源数据整合** - 支持从多个网站收集数据
3. **实时监控** - 定期检查内容变化
4. **数据质量保证** - 内置去重和验证机制
5. **易于集成** - 简单的API接口，易于集成到现有系统

### 适用场景
- **内容聚合平台** - 新闻、博客、论坛内容收集
- **价格监控系统** - 电商、房产、股票价格跟踪
- **竞品分析** - 竞争对手信息收集和分析
- **学术研究** - 论文、专利、技术文档收集
- **市场调研** - 行业报告、用户评论、趋势分析

### 最佳实践
1. **合理设置爬取频率** - 避免对目标网站造成压力
2. **实现错误处理和重试机制** - 提高系统稳定性
3. **数据去重和验证** - 确保数据质量
4. **定期备份数据** - 防止数据丢失
5. **监控API配额使用** - 合理控制成本

通过这些实际案例，您可以快速了解如何在自己的项目中应用Firecrawl，构建强大的数据采集和分析系统。