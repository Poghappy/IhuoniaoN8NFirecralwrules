# 项目规则快速参考

> 简洁版规则总结 - 用于快速查阅和记忆

## 🎯 核心原则

### 项目定位

- HawaiiHub Firecrawl × 火鸟门户 × n8n 采集与自动化运营
- 主要代码：`Firecrawl代码模块/*`、`n8n工具/*`
- 默认语言：Python（采集）、TypeScript/JS（n8n），全部返回简体中文

### 工作流程

- 采集 → 处理 → 发布：`ArticleData → ProcessedArticle → PublishRequest`
- 复用模块：`FirecrawlCollector`、`DataProcessor`、`APIIntegration`

## 📝 Python 规范（简化版）

### 必须做

- ✅ 所有函数/方法必须有类型注解和中文 docstring
- ✅ 使用 `logging` 记录关键流程（带 URL/external_id 索引）
- ✅ 新功能先补测试（pytest，不用 unittest）
- ✅ 使用 `ConfigManager` 管理配置，不硬编码 API 密钥

### 禁止做

- ❌ 生产代码不用 `print`、不写裸异常
- ❌ 不绕过 `ConfigManager`，不直接访问外部 API 无速率/重试控制
- ❌ 不创建重复文件/文档，优先更新现有文件

### 命名规范

- 变量/函数：`snake_case`
- 类：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`
- 私有方法：`_single_underscore`

## 🔧 常用命令

```bash
# 测试
uv run pytest
uv run python Firecrawl代码模块/集成测试.py

# 代码质量
ruff check . && ruff format --check .
mypy --strict Firecrawl代码模块

# n8n
pnpm install && pnpm lint
```

## 🚨 安全与权限

### 允许无提示执行

- 读取/列出文件
- 运行 `ruff`、`mypy`、`pytest` 单测
- `pnpm lint/test`

### 执行前需征询

- 安装/卸载依赖
- 删除或批量移动文件
- 运行全量构建或长时间脚本
- 访问外部 API

### 严禁

- ❌ 提交/推送 Git
- ❌ 更改系统权限
- ❌ 暴露密钥或生产数据

## 📚 最新学习要点

### Cron 表达式处理（2025-11-17）

- `cron.get_next()` 返回 `float` 时间戳，需转换为 `datetime`
- 使用 `datetime.fromtimestamp()` 转换
- 比较时间时注意时区问题

### 测试规范

- 优先使用 pytest（不用 unittest）
- 测试文件放在 `tests/` 或 `集成测试.py`
- Mock 外部 API，避免真实调用

### 日志格式

- 使用 lazy % formatting：`logger.info("处理 %s", url)` 而不是 f-string
- 日志必须包含索引信息（URL、external_id 等）

### Firecrawl API（2025-11-17 更新）

- **API Key 获取**：访问 [firecrawl.dev](https://firecrawl.dev) 注册并获取 API Key（格式：`fc-xxxxx`）
- **SDK 安装**：`pip install firecrawl-py`（Python）或 `npm install @mendable/firecrawl-js`（Node.js）
- **核心功能**：Scrape（单页）、Crawl（批量）、Map（URL 发现）、Search（搜索）、Extract（结构化提取）
- **Actions 支持**：支持点击、滚动、输入、等待等交互操作（需使用 `wait` 等待页面加载）
- **输出格式**：markdown、html、summary、structured data（JSON mode）、screenshot
- **注意事项**：
  - `scrape()` 方法支持 `formats` 和 `actions` 参数
  - `crawl()` 方法返回爬取任务 ID，需使用 `get_crawl_status()` 查询状态
  - JSON mode 支持 Pydantic schema 或 prompt 提取结构化数据
  - 需要配置真实的 API 密钥才能运行完整测试

## 🗂️ 项目结构速览

```
Firecrawl代码模块/
├── 火爬采集器.py      # Firecrawl Collector
├── 数据处理.py        # 清洗、关键词、分类、评分
├── API集成.py         # 火鸟门户 API 客户端
└── 集成测试.py        # 全链路测试
```

## 📖 文档索引

- Python 规范：`.cursor/rules/python.mdc`
- 项目说明：`AGENTS.md`
- Firecrawl 文档：`docs/Firecrawl工具/官方资料/`
- 火鸟门户 API：`docs/火鸟门户系统官方文档/02_API接口/`

## ✅ 提交前检查

- [ ] 代码通过 Ruff、mypy、pytest
- [ ] 关键日志、错误处理、重试策略完整
- [ ] 类型注解和 docstring 完整
- [ ] 无硬编码密钥或敏感信息

---

**更新日期**: 2025-11-17（Firecrawl API 文档更新）
**用途**: 快速查阅核心规范，补充详细规则请参考 `.cursor/rules/` 目录
