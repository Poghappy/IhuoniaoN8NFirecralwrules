# Firecrawl数据采集器 - 项目配置常量

## 项目基本信息

- **项目名称**: Firecrawl数据采集器
- **项目代号**: FIRECRAWL-AGENT
- **技术栈**: Python + FastAPI + Next.js + Vercel AI SDK + Pinecone + Docker
- **业务领域**: 数据采集、AI分析、多租户SaaS

## 通用常量（占位符）

### 项目常量

- `{PROJECT_NAME}`: Firecrawl数据采集器
- `{PROJECT_CODE}`: FIRECRAWL-AGENT
- `{REPO_CONVENTION}`: 仓库结构约定（docs/src/tests/prompts/scripts/config/...）

### 技术栈常量

- `{BACKEND_STACK}`: Python + FastAPI + SQLAlchemy + Pydantic
- `{FRONTEND_STACK}`: Next.js + Vercel AI SDK + TypeScript + Tailwind CSS
- `{DATABASE_STACK}`: PostgreSQL + Pinecone + Redis
- `{DEPLOY_STACK}`: Docker + GitHub Actions + Vercel + Docker Hub

### 命令常量

- `{LINT_CMD}`: 代码检查命令，默认：`make lint` 或 `python -m flake8 src/`
- `{TEST_CMD}`: 测试命令，默认：`make test` 或 `python -m pytest tests/`
- `{COVERAGE_CMD}`: 覆盖率命令，默认：`make cov` 或 `python -m pytest --cov=src tests/`
- `{BUILD_CMD}`: 构建命令，默认：`docker build -t firecrawl-agent .`
- `{DEPLOY_CMD}`: 部署命令，默认：`./scripts/deploy.sh`

### 限制常量

- `{MAX_FILES}`: 单回合最大改动文件数，默认：5
- `{MAX_LINES}`: 单文件最大改动行数，默认：200
- `{MAX_API_CALLS}`: 单回合最大API调用数，默认：10
- `{TIMEOUT_SECONDS}`: 单次操作超时时间，默认：300秒

### 风险识别阈值

- `{RISK_BAR}`: 风险识别阈值说明，默认：数据安全/API限流/性能瓶颈/依赖稳定性/成本控制
- `{NON_FUNC_TARGETS}`: 非功能目标，默认：性能/可用性/安全性/可观测性/可扩展性/成本效益

### 交接格式

- `{HANDOFF_FORMAT}`: 统一交接JSON结构（见下文）

### 业务领域常量

- `{DATA_SOURCES}`: 支持的数据源，默认：Web页面/API接口/文档/社交媒体
- `{AI_FEATURES}`: AI功能模块，默认：智能查询/数据分类/内容摘要/相似性搜索
- `{TENANT_MODEL}`: 多租户模式，默认：数据隔离/权限控制/资源配额/计费管理

### 质量指标

- `{PERFORMANCE_TARGETS}`: 性能目标，默认：API响应<500ms/数据采集<30s/并发用户>1000
- `{SECURITY_REQUIREMENTS}`: 安全要求，默认：数据加密/访问控制/审计日志/合规性
- `{RELIABILITY_TARGETS}`: 可靠性目标，默认：可用性>99.9%/数据完整性>99.99%/故障恢复<5min

### 部署环境

- `{DEV_ENV}`: 开发环境，默认：localhost:8000
- `{STAGING_ENV}`: 测试环境，默认：staging.firecrawl-agent.com
- `{PROD_ENV}`: 生产环境，默认：api.firecrawl-agent.com
- `{MONITORING_URL}`: 监控地址，默认：monitoring.firecrawl-agent.com

### API配置

- `{FIRECRAWL_API}`: Firecrawl API端点，默认：https://api.firecrawl.dev
- `{PINECONE_API}`: Pinecone API端点，默认：https://api.pinecone.io
- `{VERCEL_API}`: Vercel API端点，默认：https://api.vercel.com

### 数据配置

- `{MAX_FILE_SIZE}`: 最大文件大小，默认：100MB
- `{MAX_BATCH_SIZE}`: 最大批处理大小，默认：1000条
- `{RETENTION_DAYS}`: 数据保留天数，默认：90天
- `{BACKUP_FREQUENCY}`: 备份频率，默认：每日

### 成本控制

- `{API_QUOTA}`: API调用配额，默认：10000次/月
- `{STORAGE_QUOTA}`: 存储配额，默认：100GB
- `{COMPUTE_QUOTA}`: 计算配额，默认：1000小时/月
- `{BANDWIDTH_QUOTA}`: 带宽配额，默认：1TB/月

### 合规要求

- `{GDPR_COMPLIANCE}`: GDPR合规性要求
- `{CCPA_COMPLIANCE}`: CCPA合规性要求
- `{SOC2_COMPLIANCE}`: SOC2合规性要求
- `{ISO27001_COMPLIANCE}`: ISO27001合规性要求

### 监控指标

- `{HEALTH_CHECK}`: 健康检查端点，默认：/health
- `{METRICS_ENDPOINT}`: 指标收集端点，默认：/metrics
- `{LOGS_ENDPOINT}`: 日志收集端点，默认：/logs
- `{ALERTS_ENDPOINT}`: 告警通知端点，默认：/alerts

### 版本控制

- `{VERSION_SCHEME}`: 版本号规范，默认：语义化版本控制（SemVer）
- `{BRANCH_STRATEGY}`: 分支策略，默认：GitFlow
- `{TAG_PATTERN}`: 标签模式，默认：v{major}.{minor}.{patch}
- `{RELEASE_NOTES}`: 发布说明模板，默认：CHANGELOG.md

### 文档标准

- `{API_DOCS}`: API文档格式，默认：OpenAPI 3.0
- `{CODE_DOCS}`: 代码文档格式，默认：Sphinx + reStructuredText
- `{USER_DOCS}`: 用户文档格式，默认：Markdown + Mermaid
- `{TECH_DOCS}`: 技术文档格式，默认：Markdown + PlantUML

### 测试标准

- `{UNIT_TEST_COVERAGE}`: 单元测试覆盖率，默认：>80%
- `{INTEGRATION_TEST_COVERAGE}`: 集成测试覆盖率，默认：>70%
- `{E2E_TEST_COVERAGE}`: 端到端测试覆盖率，默认：>60%
- `{PERFORMANCE_TEST_THRESHOLD}`: 性能测试阈值，默认：<500ms响应时间

### 安全标准

- `{SECURITY_SCAN}`: 安全扫描频率，默认：每日
- `{DEPENDENCY_CHECK}`: 依赖检查频率，默认：每周
- `{VULNERABILITY_SCAN}`: 漏洞扫描频率，默认：每月
- `{PENETRATION_TEST}`: 渗透测试频率，默认：每季度

### 备份策略

- `{BACKUP_FREQUENCY}`: 备份频率，默认：每日
- `{BACKUP_RETENTION}`: 备份保留期，默认：30天
- `{DISASTER_RECOVERY}`: 灾难恢复时间，默认：<4小时
- `{RTO_TARGET}`: 恢复时间目标，默认：<1小时
- `{RPO_TARGET}`: 恢复点目标，默认：<15分钟

---

**配置版本**: v1.0.0  
**最后更新**: 2024-09-22  
**维护者**: AI Assistant  
**适用范围**: Firecrawl数据采集器项目全生命周期
