# 🎉 Firecrawl 爬取规则功能 (v2.0)

> 根据官方文档新增的完整爬取规则支持
>
> 更新日期: 2025-10-30

## 📝 功能概述

本次更新根据 Firecrawl 官方文档，为项目添加了完整的爬取规则 (Rules) 支持，实现了精确的路径控制和 100% 云端采集。

## ✨ 核心特性

### 1. 路径规则控制

```python
# 只爬取博客内容
include_paths = ["^/blog/.*$", "^/post/.*$"]

# 排除管理页面
exclude_paths = ["^/admin/.*$", "^/login/.*$"]
```

### 2. 预设规则库

内置 15+ 种常用场景：

- 博客内容
- 新闻网站
- 文档站点
- 电商产品
- 学术论文
- 社交媒体
- 企业官网
- 政府网站
- 教育资源
- 招聘信息
- 房产租赁
- 旅游网站
- ...更多

### 3. 类型安全

使用 Pydantic 模型提供完整的类型检查：

```python
from src.models.crawl_rules import CrawlRulesConfig

rules = CrawlRulesConfig(
    include_paths=["^/blog/.*$"],
    exclude_paths=["^/admin/.*$"],
    max_discovery_depth=3,
    limit=200
)
```

### 4. 云端采集

100% 使用 Firecrawl API，无需本地爬虫：

```python
from src.scrapers.firecrawl_v2_unified_scraper import FirecrawlV2UnifiedScraper

scraper = FirecrawlV2UnifiedScraper(api_key="your-api-key")
task_id = scraper.crawl_website_v2(
    url="https://example.com",
    include_paths=["^/blog/.*$"],
    exclude_paths=["^/admin/.*$"]
)
```

## 📂 新增文件列表

### 核心代码

1. **`src/scrapers/firecrawl_v2_unified_scraper.py`** (更新)

   - 新增 `crawl_website_v2()` - 支持规则的爬取方法
   - 新增 `get_crawl_status_v2()` - 查询任务状态
   - 新增 `wait_for_crawl_completion()` - 等待任务完成
   - 新增 `default_crawl_rules` - 默认规则配置

2. **`src/models/crawl_rules.py`** (新建, 300+ 行)
   - `CrawlRulesConfig` - 爬取规则配置类
   - `CrawlMode` - 爬取模式枚举
   - `CommonRulesPresets` - 常用规则预设
   - `create_custom_rules()` - 自定义规则创建函数

### 配置文件

3. **`config/crawl_rules_examples.yaml`** (新建, 300+ 行)
   - 15+ 种场景的完整配置示例
   - 包含详细注释和说明
   - 支持直接复制使用

### 示例代码

4. **`examples/crawl_with_rules_example.py`** (新建, 400+ 行)

   - 示例 1: 博客内容爬取（预设规则）
   - 示例 2: 新闻网站爬取（延迟控制）
   - 示例 3: 自定义规则创建
   - 示例 4: 文档网站爬取（深度爬取）
   - 示例 5: 查询任务状态

5. **`examples/quick_test_rules.py`** (新建, 300+ 行)
   - 正则表达式测试工具
   - 规则验证工具
   - API 连接测试
   - 交互式测试界面

### 文档

6. **`docs/CRAWL_RULES_GUIDE.md`** (新建, 600+ 行)

   - 完整的使用指南
   - 正则表达式语法详解
   - 常用模式示例
   - 最佳实践
   - 常见问题解答
   - 性能优化建议

7. **`docs/CRAWL_RULES_UPDATE.md`** (新建, 400+ 行)

   - 功能更新说明
   - 快速开始指南
   - 详细的使用示例
   - 性能指标
   - 成本优化建议

8. **`README.md`** (更新)
   - 新增爬取规则功能介绍
   - 更新最佳实践
   - 新增文档链接
   - 更新项目历史

## 🚀 快速开始

### 1. 使用预设规则

```python
from src.scrapers.firecrawl_v2_unified_scraper import FirecrawlV2UnifiedScraper
from src.models.crawl_rules import CommonRulesPresets

# 初始化
scraper = FirecrawlV2UnifiedScraper(api_key="your-api-key")

# 使用博客预设
rules = CommonRulesPresets.blog_only()

# 爬取
task_id = scraper.crawl_website_v2(
    url="https://example.com",
    include_paths=rules.include_paths,
    exclude_paths=rules.exclude_paths,
    max_depth=rules.max_discovery_depth,
    limit=rules.limit
)

# 获取结果
results = scraper.wait_for_crawl_completion(task_id)
```

### 2. 自定义规则

```python
from src.models.crawl_rules import create_custom_rules, CrawlMode

rules = create_custom_rules(
    include_patterns=["^/blog/.*$", "^/news/.*$"],
    exclude_patterns=["^/admin/.*$"],
    depth=3,
    max_pages=200,
    mode=CrawlMode.BASIC
)

task_id = scraper.crawl_website_v2(
    url="https://example.com",
    include_paths=rules.include_paths,
    exclude_paths=rules.exclude_paths
)
```

### 3. 运行示例

```bash
# 设置 API 密钥
export FIRECRAWL_API_KEY="fc-your-api-key"

# 运行示例
python examples/crawl_with_rules_example.py

# 运行测试工具
python examples/quick_test_rules.py
```

## 📖 文档导航

| 文档                                             | 说明               |
| ------------------------------------------------ | ------------------ |
| [使用指南](docs/CRAWL_RULES_GUIDE.md)            | 完整的规则使用说明 |
| [更新说明](docs/CRAWL_RULES_UPDATE.md)           | v2.0 功能详情      |
| [配置示例](config/crawl_rules_examples.yaml)     | 15+ 种场景配置     |
| [示例代码](examples/crawl_with_rules_example.py) | 5 个完整示例       |
| [测试工具](examples/quick_test_rules.py)         | 规则测试工具       |

## 💡 使用场景

### 博客爬取

```python
rules = CommonRulesPresets.blog_only()
# 只爬取 /blog/, /post/, /article/ 路径
```

### 新闻网站

```python
rules = CommonRulesPresets.news_site()
# 爬取新闻和日期路径，排除用户页面
```

### 电商产品

```python
rules = CommonRulesPresets.e_commerce_products()
# 只爬取产品页面，排除购物车和结账
```

### 文档站点

```python
rules = CommonRulesPresets.documentation()
# 深度爬取文档，支持整个域名
```

## ⚙️ 配置参数

| 参数                       | 类型        | 默认值  | 说明                 |
| -------------------------- | ----------- | ------- | -------------------- |
| `include_paths`            | `List[str]` | `[]`    | 包含路径正则表达式   |
| `exclude_paths`            | `List[str]` | `[]`    | 排除路径正则表达式   |
| `max_discovery_depth`      | `int`       | `2`     | 最大发现深度 (1-10)  |
| `limit`                    | `int`       | `100`   | 最大页面数 (1-10000) |
| `crawl_entire_domain`      | `bool`      | `False` | 爬取整个域名         |
| `allow_external_links`     | `bool`      | `False` | 允许外部链接         |
| `allow_subdomains`         | `bool`      | `False` | 允许子域名           |
| `deduplicate_similar_urls` | `bool`      | `True`  | 去重相似 URL         |
| `delay`                    | `float`     | `None`  | 请求延迟（秒）       |

## 🎓 最佳实践

### 1. 使用精确的正则表达式

```python
# ✅ 推荐
"^/blog/.*$"  # 明确的开始和结束

# ❌ 不推荐
"/blog/"      # 可能误匹配
```

### 2. 先测试再部署

```python
# 先用小范围测试
task_id = scraper.crawl_website_v2(url, include_paths, limit=10)

# 确认无误后扩大范围
task_id = scraper.crawl_website_v2(url, include_paths, limit=200)
```

### 3. 监控成本

```python
status = scraper.get_crawl_status_v2(task_id)
print(f"使用积分: {status['creditsUsed']}")
```

### 4. 使用缓存

```python
scrape_options = {
    "maxAge": 172800000,  # 2天缓存
    "onlyMainContent": True
}
```

## 💰 成本优化

1. **精确规则**: 只爬取需要的页面
2. **合理深度**: `max_depth=2` 通常足够
3. **启用缓存**: 减少重复请求
4. **先用 Map**: 估算页面数

## 🔧 技术细节

### 实现方式

- 使用 Firecrawl API v2
- 正则表达式路径匹配
- 异步任务提交和监控
- Pydantic 模型验证

### 兼容性

- Python 3.9+
- Firecrawl API v2
- 所有操作系统

## 📊 代码统计

- **新增代码**: ~2000 行
- **新增文件**: 8 个
- **文档**: ~2000 行
- **示例**: 5 个完整示例
- **预设规则**: 15+ 种场景

## 🎯 下一步

1. 运行快速测试：`python examples/quick_test_rules.py`
2. 阅读使用指南：[CRAWL_RULES_GUIDE.md](docs/CRAWL_RULES_GUIDE.md)
3. 尝试示例代码：`python examples/crawl_with_rules_example.py`
4. 查看配置示例：[crawl_rules_examples.yaml](config/crawl_rules_examples.yaml)

## 📞 获取帮助

如有问题：

1. 查看 [使用指南](docs/CRAWL_RULES_GUIDE.md)
2. 运行 [测试工具](examples/quick_test_rules.py)
3. 查看 [官方文档](https://docs.firecrawl.dev/)
4. 参考 [示例代码](examples/crawl_with_rules_example.py)

---

**版本**: v2.0
**更新日期**: 2025-10-30
**作者**: Firecrawl Team
