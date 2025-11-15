# Firecrawl Python SDK 快速开始

**5 分钟上手 Firecrawl SDK** 🚀

---

## 📋 环境检查

你的环境已配置完成：

```bash
✅ Python 3.14.0
✅ firecrawl-py 4.5.0
✅ python-dotenv
✅ API 密钥 (1主 + 3备用)
```

---

## 🏃 立即开始

### 1️⃣ 最简单的例子（10 秒）

```python
from firecrawl import FirecrawlApp

# 初始化（自动从 .env 读取 API 密钥）
app = FirecrawlApp()

# 爬取一个网页
result = app.scrape("https://firecrawl.dev")

# 查看结果
print(result.markdown)  # Markdown 内容
print(result.metadata.title)  # 页面标题
```

### 2️⃣ 运行官方示例（1 分钟）

```bash
# 基础 Scrape 示例（5 个场景）
python3 examples/01_basic_scrape.py

# Crawl 深度爬取示例
python3 examples/02_crawl_website.py

# Batch Scrape 批量采集示例
python3 examples/03_batch_scrape.py
```

### 3️⃣ 测试你的配置（30 秒）

```bash
python3 examples/00_test_setup.py
```

这个脚本会检查：

- Python 版本
- 包安装状态
- 环境变量配置
- API 连接

---

## 💡 核心功能速查

### Scrape - 单页采集

```python
# 最简单
result = app.scrape("https://example.com")

# 完整配置
result = app.scrape(
    url="https://example.com",
    formats=["markdown", "html"],
    only_main_content=True,  # 只提取主要内容
    max_age=172800000        # 使用 2 天缓存
)
```

### Crawl - 深度爬取

```python
# 爬取整个网站
job = app.crawl(
    url="https://docs.firecrawl.dev",
    limit=10,           # 限制 10 个页面
    poll_interval=1,    # 每秒检查一次
    timeout=120         # 最多等待 2 分钟
)

# 访问结果
for doc in job.data:
    print(doc.metadata.source_url)
    print(doc.markdown[:100])
```

### Batch Scrape - 批量采集

```python
urls = [
    "https://firecrawl.dev",
    "https://docs.firecrawl.dev",
    "https://blog.firecrawl.dev"
]

job = app.batch_scrape(
    urls=urls,
    formats=["markdown"],
    poll_interval=1,
    timeout=60
)

print(f"完成: {job.completed}/{job.total}")
```

### Map - 站点地图

```python
# 发现网站所有 URL
result = app.map(
    url="https://firecrawl.dev",
    limit=100
)

print(f"发现 {len(result.links)} 个 URL")
for link in result.links[:5]:
    print(link)
```

---

## 🎯 实战案例

### 案例 1: 爬取博客

```python
from firecrawl import FirecrawlApp
import json

app = FirecrawlApp()

# 1. 发现所有博客 URL
urls = app.map(url="https://firecrawl.dev/blog", limit=50)
blog_urls = [u for u in urls.links if "/blog/" in u]

# 2. 批量爬取
job = app.batch_scrape(blog_urls, formats=["markdown"])

# 3. 保存结果
articles = [{"url": doc.metadata.source_url, "content": doc.markdown}
            for doc in job.data]

with open("blog.json", "w") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"✅ 保存了 {len(articles)} 篇文章")
```

### 案例 2: 监控网站变更

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp()

# 爬取竞品价格页面
result = app.scrape(
    url="https://competitor.com/pricing",
    formats=["markdown"],
    max_age=3600000  # 1小时缓存
)

# 保存内容
current_content = result.markdown

# 下次运行时对比
if current_content != previous_content:
    print("⚠️  价格页面有更新！")
```

---

## 💰 成本优化技巧

### 1. 使用缓存（节省 50%+）

```python
result = app.scrape(
    url="https://example.com",
    max_age=172800000  # 2天缓存
)

# 第二次访问相同 URL，命中缓存，不计费！
```

### 2. 只提取主要内容

```python
result = app.scrape(
    url="https://example.com",
    only_main_content=True  # 去除导航、广告
)
```

### 3. 批量处理

```python
# ✅ 推荐：批量（快 3-5 倍）
results = app.batch_scrape(urls, formats=["markdown"])

# ❌ 避免：逐个（慢且贵）
for url in urls:
    result = app.scrape(url)
```

---

## 🔧 错误处理

```python
from firecrawl import FirecrawlApp
from firecrawl.exceptions import RequestTimeoutError, RateLimitError
import time

app = FirecrawlApp()

def safe_scrape(url: str, max_retries: int = 3):
    """带重试的安全爬取"""
    for attempt in range(max_retries):
        try:
            return app.scrape(url, formats=["markdown"])
        except RateLimitError:
            wait = 2 ** attempt  # 指数退避：2s, 4s, 8s
            print(f"速率限制，{wait}秒后重试...")
            time.sleep(wait)
        except RequestTimeoutError:
            print(f"超时，重试 {attempt + 1}/{max_retries}...")
            if attempt == max_retries - 1:
                raise
    return None

# 使用
result = safe_scrape("https://example.com")
```

---

## 📚 学习资源

### 🔥 必读

1. **完整指南** (860 行教程)

   ```
   Firecrawl学习手册/03-API参考/08-Python-SDK完整指南.md
   ```

2. **示例代码**

   ```
   examples/01_basic_scrape.py
   examples/02_crawl_website.py
   examples/03_batch_scrape.py
   ```

3. **示例文档**

   ```
   examples/README.md
   ```

### 🌐 官方资源

- **文档**: https://docs.firecrawl.dev/sdks/python
- **API 参考**: https://docs.firecrawl.dev/api-reference/v2-introduction
- **Discord**: https://discord.gg/gSmWdAkdwd

---

## 🚨 常见问题

### Q: API 调用很慢？

A: 这是正常的。Firecrawl 需要：

1. 渲染 JavaScript
2. 等待页面加载
3. 提取和转换内容

**优化方案**：

- 使用缓存 (`max_age=172800000`)
- 批量处理 (`batch_scrape`)
- 非阻塞模式 (`start_crawl`)

### Q: 如何节省成本？

A: 3 个关键策略：

1. **缓存**: `max_age=172800000` 节省 50%+
2. **主要内容**: `only_main_content=True` 减少响应大小
3. **批量处理**: 用 `batch_scrape` 代替多次 `scrape`

### Q: 返回结果是什么类型？

A: SDK v2 返回 **Document 对象**（不是字典）：

```python
# ✅ 正确
result.markdown       # 属性访问
result.metadata.title

# ❌ 错误
result["markdown"]    # 会报错
result.get("markdown")
```

---

## 🎯 下一步

### 今天（10 分钟）

1. ✅ 运行 `python3 examples/01_basic_scrape.py`
2. ✅ 理解核心概念（Scrape、Crawl、Batch）

### 本周（1 小时）

1. 📖 阅读完整指南
2. 🧪 运行所有示例
3. 🚀 爬取一个你感兴趣的网站

### 本月（实战项目）

1. 🏗️ 构建 HawaiiHub 数据采集系统
2. 📰 夏威夷新闻自动采集
3. 🏠 租房信息监控
4. 🍜 餐厅数据抓取

---

## 💬 需要帮助？

1. **查看完整指南**: `Firecrawl学习手册/03-API参考/08-Python-SDK完整指南.md`
2. **运行测试脚本**: `python3 examples/00_test_setup.py`
3. **查看示例**: `examples/README.md`
4. **官方 Discord**: https://discord.gg/gSmWdAkdwd

---

**准备好了吗？立即开始：**

```bash
python3 examples/01_basic_scrape.py
```

🚀 祝你爬取愉快！

---

**维护者**: HawaiiHub AI Team
**版本**: v1.0.0
**最后更新**: 2025-10-28
