# HawaiiHub Firecrawl × 火鸟门户 × n8n 自动化仓库

本仓库聚合了 Firecrawl 采集、数据处理、火鸟门户 API 发布和 n8n 自动化流程相关的代码与文档，用于支撑内容采集、治理与分发的一体化链路。

## 项目概览
- **采集与处理**：`Firecrawl代码模块/` 下提供采集器、数据处理与 API 集成模块，以及集成测试脚本，覆盖 ArticleData → ProcessedArticle → PublishRequest 的三段流。
- **文档中心**：`docs/Firecrawl工具/` 为 Firecrawl 官方/自研文档中心，包含快速开始、配置、功能特性与项目报告等资料。
- **门户与工作流资源**：根目录保留火鸟门户集成脚本（如 `火鸟门户_API集成模块.js`）、运营指南与 n8n 相关编排文件（如 `docker-compose-n8n.yml`），用于对接门户与自动化平台。
- **工具与配置**：`chatgpt-mcp-server/`、`.cursor/` 等目录提供 MCP、Cursor 及开发工具链配置，可作为本地或云端开发环境的基础。

## 目录速览
- `Firecrawl代码模块/`：采集器、配置、数据处理、API 发布及 `集成测试.py` 集成验证脚本。
- `docs/Firecrawl工具/`：Firecrawl 文档中心（含 `README.md`、`QUICKSTART.md`、官方资料、项目规则与报告等）。
- `document-quality*.mdc` 系列：文档质量检查清单与规范。
- `docker-compose-n8n.yml`：n8n/辅助服务的编排样例。
- `火鸟门户_*` & `新闻模块API接口文档.md`：火鸟门户侧的集成脚本与接口说明。
- `chatgpt-mcp-server/`：MCP Server 配置与脚本。

## 快速上手
1. **阅读规则**：在处理 Python 代码前先查看 `.cursor/rules/python.mdc`，遵循类型注解、日志与错误处理要求。
2. **安装依赖**（示例）：`pip install -r docs/Firecrawl工具/requirements.txt`（或按需使用 `uv/poetry`）。
3. **运行集成测试**：`python Firecrawl代码模块/集成测试.py`（验证采集→处理→发布链路）。
4. **开发与自动化**：n8n/门户相关流程可参考 `docker-compose-n8n.yml` 和 `火鸟门户_*.js` 进行自定义。

## 协作与分支
- 现以 `main` 为主分支，后续特性可在短分支开发后合并回主分支，保持仓库简洁。
- 提交遵循约定式提交（feat/fix/docs/refactor/test/chore），并在合并前确保必要的测试与占位 lint/测试脚本已执行。

## 常用检查
- Python：`uv run pytest` / `uv run python Firecrawl代码模块/集成测试.py`（如未安装 `uv`，可用 `poetry`/`pip` 替代）。
- JS/TS（占位）：`npm run lint`、`npm test` 当前作为占位检查，后续可接入真实 lint/Test 工具。

更多细节请参考 `docs/Firecrawl工具/README.md` 与相关指南、报告文档。
