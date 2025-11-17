# N8N Firecrawl 集成指南

## 📋 概述

本文档介绍如何在 n8n 工作流自动化平台中集成和使用 Firecrawl 社区节点，实现 HawaiiHub 的自动化内容采集和数据处理。

**更新时间**: 2025-10-26  
**参考来源**: [n8n Community Node: Firecrawl](https://community.n8n.io/t/n8n-community-node-firecrawl/55546)

---

## 🎯 什么是 n8n Firecrawl 节点？

### 核心价值

n8n-nodes-firecrawl 是一个社区开发的 n8n 节点，允许在工作流中直接调用 Firecrawl API，实现：

1. **可视化工作流**: 无需编写代码，拖拽即可创建采集流程
2. **自动化调度**: 定时触发采集任务
3. **数据处理链**: 采集后自动清洗、转换、存储数据
4. **多系统集成**: 连接数据库、CRM、邮件等 200+ 服务

### 与 HawaiiHub 的关系

```
n8n 工作流平台
    ↓
Firecrawl 节点 (采集执行)
    ↓
HawaiiHub 数据库 (内容存储)
    ↓
前端展示 (用户访问)
```

---

## 🚀 安装配置

### 1. 安装 n8n Firecrawl 节点

#### 方法 A: npm 安装（推荐）

```bash
# 在 n8n 工作目录下
npm install n8n-nodes-firecrawl

# 或使用 pnpm
pnpm add n8n-nodes-firecrawl
```

#### 方法 B: n8n 界面安装

1. 登录 n8n 管理界面
2. 进入 **Settings** → **Community Nodes**
3. 点击 **Install** 按钮
4. 输入: `n8n-nodes-firecrawl`
5. 点击 **Install** 确认

### 2. 配置 Firecrawl API 凭证

在 n8n 中创建 Firecrawl 凭证：

1. 进入 **Credentials** 菜单
2. 点击 **New Credential** → 搜索 "Firecrawl"
3. 填写配置：

```json
{
  "apiKey": "fc-your-api-key-here",
  "apiUrl": "https://api.firecrawl.dev" // 云端 API
}
```

> **API Key 获取**: 访问 [Firecrawl Dashboard](https://firecrawl.dev/app) 生成

### 3. 验证安装

创建测试工作流：

```
[Manual Trigger] → [Firecrawl Scrape] → [Show Output]
```

测试参数：

- **URL**: `https://www.hawaiinewsnow.com/`
- **Formats**: `markdown`

如果返回 Markdown 格式的网页内容，说明安装成功。

---

## 🛠️ 三大核心操作

### Operation 1: Scrape（单页采集）

**功能**: 采集单个网页，返回结构化数据

#### 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| **URL** | 目标网页地址 | `https://honolulu.craigslist.org/search/apa` |
| **Formats** | 输出格式 | `markdown`, `html`, `screenshot`, `links` |
| **Only Main Content** | 只提取正文 | `true` (推荐) |
| **Wait For** | 等待时间(ms) | `2000` (动态加载网页) |
| **Actions** | 页面交互 | 点击、滚动、输入等 |

#### HawaiiHub 使用场景

**场景 1: 采集新闻详情页**

```json
{
  "url": "{{ $json.newsUrl }}",
  "formats": ["markdown", "screenshot"],
  "onlyMainContent": true,
  "waitFor": 1000,
  "includeTags": ["article", "time", "h1", "p"]
}
```

**场景 2: 采集租房列表**

```json
{
  "url": "https://honolulu.craigslist.org/search/apa",
  "formats": ["markdown"],
  "onlyMainContent": false,
  "actions": [
    {
      "type": "scroll",
      "direction": "down"
    },
    {
      "type": "wait",
      "milliseconds": 2000
    }
  ]
}
```

**场景 3: 采集餐厅信息**

```json
{
  "url": "https://www.yelp.com/biz/restaurant-name-honolulu",
  "formats": ["markdown", "links"],
  "onlyMainContent": true,
  "waitFor": 3000
}
```

---

### Operation 2: Crawl（深度爬取）

**功能**: 从起始页开始，自动爬取整个网站或指定范围

#### 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| **URL** | 起始 URL | `https://www.hawaiinewsnow.com/news/` |
| **Max Depth** | 最大爬取深度 | `2` (推荐，避免超额) |
| **Limit** | 最大页面数 | `20` (控制成本) |
| **Include Paths** | 包含路径 | `["/news/*", "/local/*"]` |
| **Exclude Paths** | 排除路径 | `["/ads/*", "/category/*"]` |

#### HawaiiHub 使用场景

**场景 1: 爬取本地新闻站**

```json
{
  "url": "https://www.hawaiinewsnow.com/news/local/",
  "maxDepth": 2,
  "limit": 50,
  "includePaths": ["/news/local/*"],
  "excludePaths": ["/video/*", "/weather/*"],
  "scrapeOptions": {
    "formats": ["markdown"],
    "onlyMainContent": true
  }
}
```

**场景 2: 爬取餐厅目录**

```json
{
  "url": "https://www.yelp.com/search?find_desc=Chinese&find_loc=Honolulu",
  "maxDepth": 1,
  "limit": 30,
  "includePaths": ["/biz/*"],
  "excludePaths": ["/search*", "/collections*"],
  "scrapeOptions": {
    "formats": ["markdown"],
    "waitFor": 2000
  }
}
```

**场景 3: 爬取分类信息**

```json
{
  "url": "https://honolulu.craigslist.org/d/housing/search/hhh",
  "maxDepth": 1,
  "limit": 20,
  "includePaths": ["/*"],
  "excludePaths": ["/about/*", "/help/*"],
  "scrapeOptions": {
    "formats": ["markdown"]
  }
}
```

---

### Operation 3: Map（站点地图）

**功能**: 快速提取网站所有可访问的 URL 链接

#### 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| **URL** | 目标网站 | `https://www.hawaiinewsnow.com/` |
| **Search** | 搜索关键词 | `local news` (可选) |
| **Limit** | 最大链接数 | `100` |
| **Include Subdomains** | 包含子域名 | `false` |

#### HawaiiHub 使用场景

**场景 1: 发现新闻站所有链接**

```json
{
  "url": "https://www.hawaiinewsnow.com/",
  "limit": 200,
  "includeSubdomains": false
}
```

返回示例：

```json
[
  "https://www.hawaiinewsnow.com/news/local/",
  "https://www.hawaiinewsnow.com/weather/",
  "https://www.hawaiinewsnow.com/sports/"
]
```

**场景 2: 搜索特定主题链接**

```json
{
  "url": "https://www.staradvertiser.com/",
  "search": "hawaii chinese community",
  "limit": 50
}
```

---

## 🔄 完整工作流示例

### 示例 1: 每日自动采集夏威夷新闻

```
[Cron Trigger (每天 8:00)] 
    ↓
[Firecrawl Map - 发现新闻链接]
    ↓
[Filter - 过滤今日新闻]
    ↓
[Firecrawl Batch Scrape - 批量采集]
    ↓
[Function - 数据清洗]
    ↓
[MySQL - 存入数据库]
    ↓
[Slack - 发送通知]
```

#### 节点配置

**1. Cron Trigger**

```json
{
  "rule": {
    "hour": 8,
    "minute": 0,
    "timezone": "Pacific/Honolulu"
  }
}
```

**2. Firecrawl Map**

```json
{
  "url": "https://www.hawaiinewsnow.com/",
  "search": "local news",
  "limit": 100
}
```

**3. Filter**

```javascript
// 仅保留今日新闻（URL 中包含日期）
const today = new Date().toISOString().split('T')[0];
return items.filter(item => item.json.url.includes(today));
```

**4. Firecrawl Scrape (Loop)**

```json
{
  "url": "{{ $json.url }}",
  "formats": ["markdown"],
  "onlyMainContent": true
}
```

**5. Function (数据清洗)**

```javascript
// 提取标题、内容、时间
const markdown = $input.first().json.markdown;
const title = markdown.match(/^#\s+(.+)/m)?.[1] || 'Untitled';
const content = markdown.replace(/^#\s+.+/m, '').trim();
const publishTime = new Date().toISOString();

return {
  title,
  content,
  source: 'Hawaii News Now',
  category: 'local',
  publishTime,
  url: $json.url
};
```

**6. MySQL Insert**

```sql
INSERT INTO news (title, content, source, category, publish_time, url)
VALUES (?, ?, ?, ?, ?, ?)
```

---

### 示例 2: 租房信息实时监控

```
[Webhook Trigger] 
    ↓
[Firecrawl Scrape - Craigslist]
    ↓
[Function - 价格过滤]
    ↓
[If - 符合条件？]
    ├─ Yes → [Email - 发送邮件通知]
    └─ No → [End]
```

#### 节点配置

**1. Firecrawl Scrape**

```json
{
  "url": "https://honolulu.craigslist.org/search/apa?min_price=1000&max_price=2500&bedrooms=2",
  "formats": ["markdown"],
  "actions": [
    {
      "type": "scroll",
      "direction": "down"
    }
  ]
}
```

**2. Function (提取租房信息)**

```javascript
// 解析 Markdown，提取租房列表
const markdown = $input.first().json.markdown;
const listings = [];

// 正则匹配租房信息（示例）
const regex = /\$(\d+)\s+-\s+(.+?)\s+\((.+?)\)/g;
let match;

while ((match = regex.exec(markdown)) !== null) {
  listings.push({
    price: parseInt(match[1]),
    title: match[2].trim(),
    location: match[3].trim(),
    url: $json.url
  });
}

return listings;
```

**3. If (价格过滤)**

```javascript
// 仅保留 $1500 以下的房源
return $json.price <= 1500;
```

**4. Email**

```
Subject: 🏠 发现新房源：{{ $json.title }}
Body:
价格：${{ $json.price }}
位置：{{ $json.location }}
链接：{{ $json.url }}
```

---

### 示例 3: 餐厅信息聚合

```
[Schedule Trigger (每周一次)]
    ↓
[Firecrawl Crawl - Yelp 中餐厅]
    ↓
[Function - 提取结构化数据]
    ↓
[Deduplicate - 去重]
    ↓
[Airtable - 更新餐厅数据库]
```

#### 节点配置

**1. Firecrawl Crawl**

```json
{
  "url": "https://www.yelp.com/search?find_desc=Chinese%20Restaurant&find_loc=Honolulu",
  "maxDepth": 1,
  "limit": 50,
  "includePaths": ["/biz/*"],
  "scrapeOptions": {
    "formats": ["markdown"],
    "onlyMainContent": true
  }
}
```

**2. Function (提取数据)**

```javascript
// 从 Markdown 提取餐厅信息
const markdown = $json.markdown;
const name = markdown.match(/^#\s+(.+)/m)?.[1];
const rating = markdown.match(/(\d\.\d)\s+stars?/i)?.[1];
const address = markdown.match(/Address:\s*(.+)/i)?.[1];
const phone = markdown.match(/Phone:\s*(.+)/i)?.[1];

return {
  name,
  rating: parseFloat(rating),
  address,
  phone,
  url: $json.url,
  lastUpdated: new Date().toISOString()
};
```

**3. Airtable**

```json
{
  "table": "Restaurants",
  "operation": "upsert",
  "matchFields": ["url"],
  "data": "{{ $json }}"
}
```

---

## ⚠️ 重要注意事项

### 1. API 版本兼容性问题

根据社区反馈，**当前节点（v0.1.1）仅支持 Firecrawl v0 API**：

```
❌ 不兼容: Firecrawl v1 API (最新版)
✅ 兼容: Firecrawl v0 API (旧版)
```

**解决方案**:

- **方案 A**: 使用 v0 API 端点（`https://api.firecrawl.dev/v0`）
- **方案 B**: 等待社区更新节点到 v1
- **方案 C**: 使用 n8n 的 HTTP Request 节点直接调用 v1 API

### 2. "Load More" 按钮问题

处理动态加载内容（如分页、"加载更多"按钮）的解决方案：

#### 方法 1: 使用 Actions（推荐）

```json
{
  "url": "https://example.com/listings",
  "formats": ["markdown"],
  "actions": [
    {
      "type": "click",
      "selector": "button.load-more"
    },
    {
      "type": "wait",
      "milliseconds": 2000
    },
    {
      "type": "click",
      "selector": "button.load-more"
    },
    {
      "type": "wait",
      "milliseconds": 2000
    }
  ]
}
```

#### 方法 2: 结合 Playwright

```
[Firecrawl Map - 获取分页 URL]
    ↓
[Loop Each Page]
    ↓
[Playwright - 模拟加载]
    ↓
[Firecrawl Scrape - 采集内容]
```

### 3. 成本控制建议

| 操作 | 平均成本 | 建议限制 |
|------|----------|----------|
| **Scrape** | 1 Credit/页 | 单次 < 50 页 |
| **Crawl** | 1 Credit/页 | limit ≤ 20, maxDepth ≤ 2 |
| **Map** | 1 Credit/请求 | limit ≤ 100 |
| **Batch Scrape** | 1 Credit/页 | 批量 < 100 页 |

**HawaiiHub 每日预算**:

- 免费层: 500 Credits/月 ≈ 16 Credits/天
- Starter: 3000 Credits/月 ≈ 100 Credits/天
- 推荐配置: **25 Credits/天**（新闻 15 + 租房 5 + 餐厅 5）

---

## 🔧 高级技巧

### 1. 错误处理

在工作流中添加错误处理节点：

```
[Firecrawl Scrape]
    ├─ Success → [Continue Workflow]
    └─ Error → [Error Trigger]
                  ↓
              [Slack Alert]
                  ↓
              [Store in Error Log]
```

**Error Trigger 配置**:

```javascript
// 记录错误详情
return {
  errorMessage: $json.error.message,
  failedUrl: $json.url,
  timestamp: new Date().toISOString(),
  workflowId: $workflow.id
};
```

### 2. 速率限制

避免触发 API 速率限制：

```
[Split In Batches]
    ↓
[Firecrawl Scrape]
    ↓
[Wait (5秒)]
    ↓
[Loop Back]
```

**Split In Batches 配置**:

```json
{
  "batchSize": 10,
  "options": {
    "reset": false
  }
}
```

### 3. 缓存机制

避免重复采集相同内容：

```
[Firecrawl Scrape]
    ↓
[Redis - Check Cache]
    ├─ Hit → [Return Cached Data]
    └─ Miss → [Continue]
                ↓
            [Redis - Store Cache (TTL: 1h)]
```

**Redis Check**:

```javascript
// 生成缓存 Key
const cacheKey = `firecrawl:${Buffer.from($json.url).toString('base64')}`;

// 检查缓存
const cached = await $redis.get(cacheKey);
if (cached) {
  return { cached: true, data: JSON.parse(cached) };
}

return { cached: false };
```

### 4. 数据验证

确保采集的数据质量：

```
[Firecrawl Scrape]
    ↓
[Function - Validate]
    ├─ Valid → [Store to Database]
    └─ Invalid → [Log Warning]
```

**Validation Function**:

```javascript
// 验证必填字段
const required = ['title', 'content', 'url'];
const missing = required.filter(field => !$json[field]);

if (missing.length > 0) {
  return {
    valid: false,
    missing: missing,
    data: $json
  };
}

// 验证内容长度
if ($json.content.length < 100) {
  return {
    valid: false,
    reason: 'Content too short',
    data: $json
  };
}

return { valid: true, data: $json };
```

---

## 📚 参考资源

### 官方文档

- [n8n-nodes-firecrawl NPM](https://www.npmjs.com/package/n8n-nodes-firecrawl)
- [Firecrawl API 文档](https://docs.firecrawl.dev/)
- [n8n 官方文档](https://docs.n8n.io/)

### 社区资源

- [n8n Community Forum](https://community.n8n.io/)
- [Firecrawl Discord](https://discord.gg/firecrawl)

### HawaiiHub 相关文档

- `Firecrawl快速开始-5分钟示例.md`
- `Firecrawl自动保存使用指南.md`
- `FIRECRAWL_COMPLETE_STUDY_SUMMARY.md`

---

## 🎯 下一步行动

### 立即开始（5 分钟）

1. **安装节点**

```bash
cd /path/to/n8n
npm install n8n-nodes-firecrawl
```

2. **创建凭证**

- 获取 Firecrawl API Key
- 在 n8n 中配置凭证

3. **测试工作流**

```
[Manual] → [Firecrawl Scrape] → [Show Output]
URL: https://www.hawaiinewsnow.com/
```

### 近期计划（1 周）

1. ✅ 部署每日新闻采集工作流
2. ✅ 配置租房信息监控
3. ✅ 建立餐厅数据聚合流程
4. ⏳ 监控 API 用量和成本
5. ⏳ 优化采集策略

### 中期目标（1 月）

1. 🎯 集成更多本地数据源（活动、就业、分类信息）
2. 🎯 实现智能去重和内容推荐
3. 🎯 建立数据质量监控仪表盘
4. 🎯 开发自定义节点（HawaiiHub 专用）

---

## ❓ 常见问题

### Q1: 为什么采集失败，返回 403 错误？

**原因**: 目标网站有反爬虫机制

**解决方案**:

1. 添加 `waitFor` 参数（模拟真人访问）
2. 使用 `actions` 进行页面交互
3. 考虑使用 Playwright 代替

### Q2: 如何处理动态价格或时间？

**方案**: 使用正则表达式或 JSON 提取

```javascript
// 提取价格
const price = markdown.match(/\$(\d+(?:,\d{3})*(?:\.\d{2})?)/)?.[1];

// 提取时间
const time = markdown.match(/(\d{1,2}\/\d{1,2}\/\d{4})/)?.[1];
```

### Q3: 如何避免重复采集？

**方案**: 使用数据库去重

```sql
-- 检查 URL 是否已存在
SELECT COUNT(*) as count FROM news WHERE url = ?

-- 仅插入新数据
INSERT INTO news (...) 
SELECT ... FROM ... 
WHERE NOT EXISTS (SELECT 1 FROM news WHERE url = ?)
```

### Q4: 如何提高采集速度？

**方案**:

1. 使用 **Batch Scrape** 代替循环 Scrape
2. 增加并发数（但注意速率限制）
3. 使用 Redis 缓存

```json
{
  "operation": "batch-scrape",
  "urls": ["url1", "url2", "url3"],
  "concurrency": 5
}
```

---

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2025-10-26 | v1.0 | 初始版本，基于社区文档创建 |

---

## 👥 贡献者

- 原始节点作者: [minhlucvan](https://community.n8n.io/u/minhlucvan)
- HawaiiHub 集成: AI Agent Team
- 文档维护: Content Manager Agent

---

**🔗 快速链接**:

- [社区原文](https://community.n8n.io/t/n8n-community-node-firecrawl/55546)
- [项目 GitHub](https://github.com/firecrawl/firecrawl-docs)
- [技术支持](https://discord.gg/firecrawl)
