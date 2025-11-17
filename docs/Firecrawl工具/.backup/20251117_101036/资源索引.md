# N8N自动化项目资源索引

## 📋 资源概览

**索引版本**: v1.0  
**最后更新**: 2025年1月16日  
**适用范围**: N8N自动化集成系统全项目资源  
**索引路径**: `.trae/rules/resource_index.md`

## 🎯 AI智能体资源配置

### 执行官Agent专用资源
```yaml
核心工作流模板:
  - 用户注册自动化: /n8n-workflows-main/templates/user-registration.json
  - 数据同步工作流: /n8n-workflows-main/templates/data-sync.json
  - API集成模板: /n8n-workflows-main/templates/api-integration.json
  - 错误处理模板: /n8n-workflows-main/templates/error-handling.json

节点配置库:
  - 火鸟门户节点: /n8n-nodes-wechat-offiaccount-master/
  - 微信公众号节点: /n8n-nodes-wechat-offiaccount-master/
  - 自定义节点集: /n8n-mcp-main/src/nodes/

MCP工具集成:
  - N8N MCP服务: /n8n-mcp-main/
  - MCP服务器: /n8n-mcp-server/
  - 工具配置: /n8n-mcp-main/src/mcp/
```

### 教学老师Agent专用资源
```yaml
教学文档库:
  - N8N官方文档: /n8n官方文档/docs/
  - 进阶教程: /n8n官方文档/docs/courses/level-two/
  - 集成指南: /n8n官方文档/docs/integrations/
  - 最佳实践: /n8n-docs-main/docs/

示例工作流:
  - 社区模板: /awesome-n8n-templates-main/
  - 免费模板: /n8n-free-templates-main/
  - 工作流示例: /n8n-workflows-main/

技术文档:
  - API文档: /n8n-docs-main/docs/api/
  - 节点开发: /n8n-docs-main/docs/integrations/creating-nodes/
  - 部署指南: /n8n-docs-main/docs/hosting/
```

## 📚 文档资源分类

### 1. 核心系统文档
```yaml
项目文档:
  - 项目索引: /PROJECT_INDEX.md
  - 项目元数据: /PROJECT_METADATA.json
  - 项目规则: /PROJECT_RULES.md
  - 项目说明: /README.md

规则文档:
  - 项目规则: /.trae/rules/project_rules.md
  - 增强规则: /.augment/rules/rules.md
  - 资源索引: /.trae/rules/resource_index.md (本文件)
```

### 2. N8N官方文档
```yaml
核心文档:
  - 主文档: /n8n-docs-main/docs/
  - 备份文档: /n8n-docs-main 2/docs/
  - 中文文档: /n8n官方文档/

教学资源:
  - 快速开始: /n8n-docs-main/docs/try-it-out/
  - 进阶教程: /n8n官方文档/docs/courses/
  - AI功能: /n8n-docs-main/docs/advanced-ai/
  - 集成指南: /n8n-docs-main/docs/integrations/

技术文档:
  - API参考: /n8n-docs-main/docs/api/
  - 代码示例: /n8n-docs-main/docs/code/
  - 数据处理: /n8n-docs-main/docs/data/
  - 嵌入集成: /n8n-docs-main/docs/embed/
```

### 3. 社区资源文档
```yaml
社区资源:
  - 精选资源: /awesome-n8n-main/
  - 中文本地化: /n8n-i18n-chinese-main/
  - 免费模板: /n8n-free-templates-main/
  - 社区模板: /awesome-n8n-templates-main/

专业文档:
  - 火鸟门户助手: /n8n-huoniao-portal-assistant-prompt.md
  - 文档分类索引: /n8n官方文档/文档分类目录索引.md
  - 教学媒体清单: /n8n官方文档/教学媒体文件清单.md
```

## 🔧 节点资源库

### 1. 官方节点
```yaml
核心节点:
  - 内置节点: /n8n-docs-main/docs/integrations/builtin/core-nodes/
  - 应用节点: /n8n-docs-main/docs/integrations/builtin/app-nodes/
  - 集群节点: /n8n-docs-main/docs/integrations/builtin/cluster-nodes/

AI节点:
  - LangChain节点: /n8n官方文档/docs/integrations/builtin/cluster-nodes/root-nodes/
  - 代码节点: /n8n-docs-main/docs/integrations/builtin/core-nodes/n8n-nodes-base.code.md
  - 评估节点: /n8n-docs-main 2/docs/integrations/builtin/core-nodes/n8n-nodes-base.evaluation.md
```

### 2. 自定义节点
```yaml
扩展节点:
  - 微信公众号: /n8n-nodes-wechat-offiaccount-master/
  - MCP集成节点: /n8n-mcp-main/src/nodes/
  - 自定义开发: /n8n-mcp-server/src/

节点开发:
  - 开发指南: /n8n-docs-main/docs/integrations/creating-nodes/
  - 构建工具: /n8n-docs-main/docs/integrations/creating-nodes/build/
  - 测试框架: /n8n-docs-main/docs/integrations/creating-nodes/test/
```

### 3. 凭据配置
```yaml
认证配置:
  - 凭据文档: /n8n-docs-main/docs/integrations/builtin/credentials/
  - API密钥管理: /n8n-docs-main/docs/integrations/builtin/credentials/api/
  - OAuth配置: /n8n-docs-main/docs/integrations/builtin/credentials/oauth/
  - 数据库连接: /n8n-docs-main/docs/integrations/builtin/credentials/database/
```

## 🔄 工作流资源库

### 1. 模板工作流
```yaml
官方模板:
  - 工作流模板: /n8n-docs-main 2/docs/embed/workflow-templates.md
  - 模板库: /n8n-templates-main/
  - 社区模板: /awesome-n8n-templates-main/

分类模板:
  - 数据处理: /n8n-workflows-main/templates/data-processing/
  - API集成: /n8n-workflows-main/templates/api-integration/
  - 自动化: /n8n-workflows-main/templates/automation/
  - 监控告警: /n8n-workflows-main/templates/monitoring/
```

### 2. 示例工作流
```yaml
实战示例:
  - 用户管理: /n8n-workflows-main/examples/user-management/
  - 数据同步: /n8n-workflows-main/examples/data-sync/
  - 通知系统: /n8n-workflows-main/examples/notification/
  - 报表生成: /n8n-workflows-main/examples/reporting/

业务场景:
  - 电商自动化: /n8n-workflows-main/examples/ecommerce/
  - 客户服务: /n8n-workflows-main/examples/customer-service/
  - 营销自动化: /n8n-workflows-main/examples/marketing/
  - 财务处理: /n8n-workflows-main/examples/finance/
```

### 3. 部署配置
```yaml
部署资源:
  - Docker配置: /n8n-deployment/docker-compose.yml
  - 快速部署: /n8n-deployment/quick-setup-guide.md
  - 配置方法: /n8n-deployment/configuration-methods.md
  - 环境变量: /n8n-deployment/.env.example

专用工作流:
  - 火鸟门户集成: /hawaiihub.net/n8n-integration/
  - 网页抓取: /n8n-deployment/honolulu-firecrawl-scraper.json
  - 数据处理: /n8n-workflows-main/workflows/
```

## 🏗️ 系统集成资源

### 1. 火鸟门户系统
```yaml
核心系统:
  - 门户源码: /hawaiihub.net/
  - 管理后台: /hawaiihub.net/admin/
  - API接口: /hawaiihub.net/api/
  - 配置文件: /hawaiihub.net/config/

模块资源:
  - 用户管理: /hawaiihub.net/admin/member/
  - 房产模块: /hawaiihub.net/admin/house/
  - 婚庆模块: /hawaiihub.net/admin/marry/
  - 内容管理: /hawaiihub.net/admin/article/

集成配置:
  - 支付配置: /hawaiihub.net/admin/payPhoneConfig.php
  - 微信配置: /hawaiihub.net/admin/weixinConfig.php
  - 站点配置: /hawaiihub.net/admin/siteConfig.php
  - 自定义配置: /hawaiihub.net/admin/siteDiyConfig.php
```

### 2. MCP协议集成
```yaml
MCP服务:
  - 主服务: /n8n-mcp-main/
  - 服务器: /n8n-mcp-server/
  - 配置文件: /n8n-mcp-main/package.json
  - 源码目录: /n8n-mcp-main/src/

集成组件:
  - 数据库: /n8n-mcp-main/src/database/
  - 服务层: /n8n-mcp-main/src/services/
  - 工具集: /n8n-mcp-main/src/mcp/
  - N8N集成: /n8n-mcp-main/src/n8n/

测试资源:
  - 单元测试: /n8n-mcp-main/tests/unit/
  - 集成测试: /n8n-mcp-main/tests/integration/
  - 测试数据: /n8n-mcp-main/tests/data/
  - 测试工具: /n8n-mcp-main/tests/utils/
```

## 🛠️ 开发工具资源

### 1. 构建工具
```yaml
项目配置:
  - Package.json: /n8n-mcp-main/package.json
  - 依赖管理: /n8n-workflows-main/requirements.txt
  - Docker配置: /n8n-mcp-main/Dockerfile
  - 部署脚本: /n8n-mcp-main/scripts/

开发工具:
  - 代码生成: /n8n-mcp-main/scripts/generate/
  - 数据迁移: /n8n-mcp-main/scripts/migration/
  - 测试脚本: /n8n-mcp-main/scripts/test/
  - 部署脚本: /n8n-mcp-main/scripts/deploy/
```

### 2. 配置文件
```yaml
环境配置:
  - 开发环境: /n8n-mcp-main/.env.example
  - 测试环境: /n8n-mcp-main/.env.test
  - Docker环境: /n8n-mcp-main/.env.docker
  - 生产环境: /n8n-mcp-main/deploy/production.env

CI/CD配置:
  - GitHub Actions: /n8n-mcp-main/.github/workflows/
  - 代码覆盖: /n8n-mcp-main/codecov.yml
  - 安全扫描: /n8n-mcp-main/SECURITY.md
  - 许可证: /n8n-mcp-main/LICENSE
```

## 📊 资源使用统计

### 项目规模
```yaml
文档资源:
  - 总文档数: 800+ 个文件
  - 核心文档: 200+ 个文件
  - 教学文档: 150+ 个文件
  - API文档: 100+ 个文件

代码资源:
  - 总代码行数: 50,000+ 行
  - PHP代码: 20,000+ 行 (40%)
  - JavaScript/TypeScript: 17,500+ 行 (35%)
  - 配置文件: 12,500+ 行 (25%)

工作流资源:
  - 模板工作流: 50+ 个
  - 示例工作流: 30+ 个
  - 自定义工作流: 20+ 个
  - 集成工作流: 15+ 个
```

### 资源质量
```yaml
文档覆盖率: 80%
代码测试覆盖率: 60%
API文档完整性: 90%
工作流模板可用性: 95%
```

## 🎯 AI智能体资源访问策略

### 执行官Agent资源优先级
```yaml
高优先级:
  1. MCP工具集: /n8n-mcp-main/src/mcp/
  2. 工作流模板: /n8n-workflows-main/templates/
  3. 节点配置: /n8n-mcp-main/src/nodes/
  4. API文档: /n8n-docs-main/docs/api/

中优先级:
  1. 部署配置: /n8n-deployment/
  2. 集成示例: /n8n-workflows-main/examples/
  3. 错误处理: /n8n-docs-main/docs/error-handling/
  4. 性能优化: /n8n-docs-main/docs/performance/
```

### 教学老师Agent资源优先级
```yaml
高优先级:
  1. 教学文档: /n8n官方文档/docs/courses/
  2. 快速开始: /n8n-docs-main/docs/try-it-out/
  3. 集成指南: /n8n-docs-main/docs/integrations/
  4. 最佳实践: /n8n-docs-main/docs/best-practices/

中优先级:
  1. 示例工作流: /n8n-workflows-main/examples/
  2. 社区资源: /awesome-n8n-main/
  3. 常见问题: /n8n-docs-main/docs/faq/
  4. 故障排除: /n8n-docs-main/docs/troubleshooting/
```

## 🔄 资源更新维护

### 自动更新机制
```yaml
文档同步:
  - 官方文档: 每日同步
  - 社区资源: 每周同步
  - 模板库: 实时同步
  - 配置文件: 手动更新

版本管理:
  - 主版本: 重大功能更新
  - 次版本: 功能增强和修复
  - 补丁版本: 错误修复和优化
  - 文档版本: 独立版本管理
```

### 质量保证
```yaml
资源验证:
  - 链接有效性检查
  - 文档完整性验证
  - 代码语法检查
  - 工作流可执行性测试

定期审查:
  - 月度资源审查
  - 季度质量评估
  - 年度架构优化
  - 持续改进计划
```

---

**维护说明**: 本资源索引由AI智能体系统自动维护，确保资源信息的准确性和时效性。

**最后更新**: 2025年1月16日  
**下次审查**: 2025年2月16日  
**维护责任**: AI智能体系统 + 项目团队