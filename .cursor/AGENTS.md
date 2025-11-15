# 项目说明

- 这是 HawaiiHub Firecrawl × 火鸟门户 × n8n 的采集与自动化运营仓库。
- 主要代码：`Firecrawl工具/代码模块/*`、`n8n工具/*`、`.cursor/rules/python.mdc`。
- 默认语言：Python（采集、Agent）、TypeScript/JS（n8n 节点），全部返回简体中文。

# 行为准则

## Do
- 先阅读 `.cursor/rules/python.mdc` 并严格遵循其中的 Python 规范。
- Python 函数/方法全部补齐类型注解和中文 docstring。
- 采集→处理→发布保持 `ArticleData → ProcessedArticle → PublishRequest` 三段流。
- 复用既有模块：Firecrawl ⇒ `FirecrawlCollector`，数据处理 ⇒ `DataProcessor`，发布 ⇒ `APIIntegration`。
- 使用 `logging` 记录关键流程，日志带 URL / external_id 等索引。
- 新功能先补测试：`tests/` 或 `集成测试.py` 中新增 pytest/unittest。

## Don't
- 不在生产代码里写 `print`、裸异常或硬编码 API 密钥。
- 不绕过 `ConfigManager`，也不直接访问外部 API 而无速率/重试控制。
- 不创建重复文件/文档；若需扩展规则，优先更新现有文件。

# 常用命令

```bash
# Python
uv run pytest                     # 运行 pytest（如未安装 uv，可使用 poetry/pipenv 等项目默认工具）
uv run python Firecrawl工具/代码模块/集成测试.py  # 现有 unittest 集成套件
ruff check . && ruff format --check .
mypy --strict Firecrawl工具/代码模块

# n8n / Node
pnpm install
pnpm lint
pnpm test
```

- 修改单个 Python 文件后可运行：`uv run pytest path/to/test_file.py`、`ruff format path/to/file.py`、`mypy path/to/module.py`。
- 未经确认禁止运行 `git push`、`rm -rf`、`docker prune` 等破坏性命令。

# 安全与权限
- 允许无提示执行：读取/列出文件、针对修改文件运行 `ruff`、`mypy`、`pytest` 单测、`pnpm lint/test`。
- 执行前需征询：安装/卸载依赖、删除或批量移动文件、运行全量构建或长时间脚本、访问外部 API。
- 严禁：提交/推送 Git、更改系统权限、暴露密钥或生产数据。

# 项目结构速览

- `Firecrawl工具/代码模块/火爬采集器.py`：Firecrawl Collector，封装采集与存储。
- `Firecrawl工具/代码模块/数据处理.py`：清洗、关键词、分类、评分。
- `Firecrawl工具/代码模块/API集成.py`：火鸟门户 API 客户端、数据映射、发布统计。
- `Firecrawl工具/代码模块/集成测试.py`：采集→处理→发布全链路测试。
- `n8n工具/配置/MCP配置.json`：MCP Server 与 n8n 节点配置。
- `.cursor/rules/python.mdc`：始终生效的 Python 规范。

# 案例与参考

- Firecrawl 官方资料位于 `Firecrawl工具/官方资料/`。
- 火鸟门户系统 API / 业务文档位于 `火鸟门户系统官方文档/`。
- `归档/火鸟门户_内容处理核心模块.js` 供 JS 节点参考。

# 示例参考
- Python 采集入口：`Firecrawl工具/代码模块/火爬采集器.py` 中的 `FirecrawlCollector.scrape_single_page`。
- 数据清洗与评分：`Firecrawl工具/代码模块/数据处理.py` 内 `DataProcessor.process_firecrawl_data`。
- API 发布流程：`Firecrawl工具/代码模块/API集成.py` 的 `APIIntegration.process_and_publish`。
- n8n 节点示例：`归档/火鸟门户_内容处理核心模块.js`。
- 避免复制：`Firecrawl工具/代码模块/集成测试.py` 中旧式 `unittest` mock 结构，若新增测试优先 pytest。

# API 文档索引
- 火鸟门户 REST 说明：`火鸟门户系统官方文档/02_API接口/`。
- Firecrawl 官方指南：`Firecrawl工具/官方资料/02-API参考/` 与 `Firecrawl工具/官方资料/03-SDK与集成/`。
- n8n 节点配置：`n8n工具/配置/MCP配置.json` 与 `n8n工具/文档/项目规则.md`。
- 需引用外部资料时，优先通过已配置的 MCP 工具获取最新版本。

# PR / 交付检查表

- [ ] 代码通过 Ruff、mypy、pytest/集成测试。
- [ ] 关键日志、错误处理、重试策略完整。
- [ ] 描述变更内容、上下文与验证方式，确保 diff 精简聚焦。
- [ ] 若影响 n8n 工作流或配置，注明同步步骤。

# 故障与求助

- 优先翻阅 `Firecrawl工具/文档` 与 `n8n工具/文档`。
- 若任务存在不确定性：先提出澄清问题或给出执行计划，再继续实现。

# 当遇到阻塞时

- 提供最少可复现示例或失败日志。
- 给出可行的下一步方案（重试策略、Mock、回退计划），必要时征求用户确认。
- 若信息不足：列出假设、提出澄清问题或先提交最小化计划，再执行。

