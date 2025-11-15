# Docker Hub MCP Server - 实战示例

这里收集了 Docker Hub MCP Server 的实际使用场景和示例。

## 📋 目录

- [镜像搜索](#-镜像搜索)
- [仓库管理](#-仓库管理)
- [标签管理](#️-标签管理)
- [镜像操作](#-镜像操作)
- [安全加固](#-安全加固)
- [自动化工作流](#-自动化工作流)

## 🔍 镜像搜索

### 场景 1: 选择合适的基础镜像

**需求:** 为 Node.js 项目选择轻量级基础镜像

```
"Search for minimal Node.js images with small footprint"
```

**AI 会返回:**

- 镜像大小对比
- 官方 vs 社区镜像
- Alpine vs Debian 版本
- 推荐选择

### 场景 2: 查找特定版本

**需求:** 查找 Python 3.11 的所有可用镜像

```
"Search for Python 3.11 images on Docker Hub"
```

### 场景 3: 生产环境镜像选择

**需求:** 查找生产级 PostgreSQL 镜像

```
"Search for production ready PostgreSQL images with high reliability"
```

**AI 会考虑:**

- ⭐ 官方认证
- 📊 下载量
- 🔄 更新频率
- 🔒 安全性

### 场景 4: 架构兼容性

**需求:** 查找支持 ARM64 的 Redis 镜像

```
"Search for Redis images that support ARM64 architecture"
```

## 📦 仓库管理

### 场景 5: 审计仓库

**需求:** 查找所有超过 1GB 的仓库

```
"Which of my repositories are larger than 1GB?"
```

### 场景 6: 清理不活跃仓库

**需求:** 查找 90 天未更新的仓库

```
"Show me repositories that haven't been updated in the last 90 days"
```

**后续操作:**

```
"Delete the repository 'old-project' from my namespace"
```

### 场景 7: 创建新项目仓库

**需求:** 为新项目创建仓库

```
"Create a new repository called 'my-web-app' in my namespace with description 'Production web application'"
```

### 场景 8: 批量查看仓库信息

**需求:** 获取所有仓库的统计信息

```
"List all my repositories with their sizes, pull counts, and last updated dates"
```

### 场景 9: 仓库可见性管理

**需求:** 将仓库设为私有

```
"Update my 'internal-tool' repository to be private"
```

## 🏷️ 标签管理

### 场景 10: 版本管理

**需求:** 查看应用的所有版本标签

```
"Show me all tags for my 'my-app' repository sorted by date"
```

### 场景 11: 查找最新稳定版

**需求:** 获取最新的 stable 标签

```
"What's the most recent stable tag for my 'my-app' repository?"
```

### 场景 12: 多架构标签

**需求:** 查看支持多架构的标签

```
"List tags for 'my-app' that support both amd64 and arm64"
```

### 场景 13: 标签清理

**需求:** 查找旧的开发标签

```
"Show me all dev-* tags older than 30 days in my 'my-app' repository"
```

### 场景 14: 验证标签存在

**需求:** 部署前检查标签

```
"Check if tag 'v2.1.0' exists for my 'my-app' repository"
```

## 📥📤 镜像操作

### 场景 15: 拉取最新版本

**需求:** 获取最新的官方镜像

```
"Pull the latest nginx image"
```

**AI 会:**

1. 检查最新标签
2. 执行 `docker pull`
3. 显示镜像信息

### 场景 16: 推送新版本

**需求:** 推送本地构建的镜像

```
"Push my local image 'my-app:v1.2.0' to my Docker Hub repository 'my-app'"
```

### 场景 17: 批量拉取

**需求:** 拉取项目所需的所有镜像

```
"Pull the following images: postgres:15, redis:7, nginx:alpine"
```

### 场景 18: 镜像迁移

**需求:** 从一个仓库复制到另一个

```
"Copy all tags from my 'old-repo' to 'new-repo'"
```

## 🔒 安全加固

### 场景 19: 查找加固镜像

**需求:** 使用 Docker 官方加固镜像

```
"What is the most secure image I can use to run a Node.js application?"
```

**AI 会推荐:**

- Docker Hardened Images (DHI)
- 安全扫描结果
- CVE 漏洞数量
- 合规性认证

### 场景 20: 转换到加固镜像

**需求:** 更新 Dockerfile 使用加固镜像

```
"Can you help me update my Dockerfile to use a docker hardened image instead of node:18?"
```

**AI 会:**

1. 分析当前 Dockerfile
2. 推荐对应的加固镜像
3. 提供迁移步骤
4. 更新配置

### 场景 21: 安全审计

**需求:** 检查所有仓库的安全状态

```
"Audit all my repositories for security vulnerabilities"
```

## 🤖 自动化工作流

### 场景 22: CI/CD 集成

**需求:** 在 CI 中验证镜像

```yaml
# .github/workflows/deploy.yml
- name: Verify Docker Hub Image
  run: |
    # AI 帮助生成验证脚本
    docker ai "Check if tag ${VERSION} exists for my 'my-app' repository"
```

### 场景 23: 定期清理

**需求:** 每周清理旧的开发标签

```
"Create a script to delete all dev-* tags older than 7 days from my 'my-app' repository"
```

### 场景 24: 版本发布

**需求:** 自动化发布流程

```
"Help me create a release workflow:
1. Build image with tag v1.3.0
2. Push to Docker Hub
3. Also tag as 'latest'
4. Verify the push succeeded"
```

### 场景 25: 监控和告警

**需求:** 监控镜像拉取量

```
"Show me the pull count trends for my 'my-app' repository over the last 30 days"
```

## 🎯 高级场景

### 场景 26: 多环境管理

**需求:** 管理开发/测试/生产环境的镜像

```
"List all tags for 'my-app' and categorize them by environment (dev, staging, prod)"
```

### 场景 27: 团队协作

**需求:** 查看团队的所有仓库

```
"List all repositories in the 'my-team' organization namespace"
```

### 场景 28: 成本优化

**需求:** 识别占用空间最大的镜像

```
"Which of my repositories consume the most storage? Show me the top 10"
```

**后续优化:**

```
"Help me reduce the size of my 'my-app' repository by:
1. Removing unused layers
2. Using multi-stage builds
3. Cleaning up old tags"
```

### 场景 29: 合规性检查

**需求:** 确保所有镜像符合公司政策

```
"Check if all my repositories:
1. Have descriptions
2. Are properly tagged
3. Have been updated in the last 6 months
4. Use approved base images"
```

### 场景 30: 灾难恢复

**需求:** 备份关键镜像

```
"Help me create a backup plan for my critical repositories:
1. List all production repositories
2. Pull all their tags
3. Save to local registry
4. Document the versions"
```

## 💡 最佳实践

### 标签命名规范

```
# 语义化版本
v1.2.3, v2.0.0-beta.1

# 环境标签
dev, staging, prod

# 日期标签
2025-01-15, 20250115

# Git 提交
sha-abc1234, commit-abc1234

# 组合标签
v1.2.3-prod, v2.0.0-staging-20250115
```

### 仓库组织

```
# 按项目
my-company/web-app
my-company/api-server
my-company/worker

# 按环境
my-app-dev
my-app-staging
my-app-prod

# 按功能
my-app-frontend
my-app-backend
my-app-database
```

### 清理策略

```
# 保留规则
- 最近 30 天的所有标签
- 所有 prod-* 标签
- 最新的 10 个版本标签
- 所有语义化版本标签 (v*.*.*)

# 删除规则
- 90 天前的 dev-* 标签
- 60 天前的 test-* 标签
- 未使用的 sha-* 标签
```

## 📊 性能优化

### 场景 31: 镜像大小优化

```
"Analyze my 'my-app:latest' image and suggest ways to reduce its size"
```

**AI 会检查:**

- 基础镜像选择
- 层数和缓存
- 未使用的文件
- 多阶段构建机会

### 场景 32: 拉取速度优化

```
"Which registry mirror should I use for fastest pulls in Asia?"
```

## 🔍 故障排查

### 场景 33: 推送失败

```
"I'm getting 'denied: requested access to the resource is denied' when pushing to my-app. Help me debug."
```

### 场景 34: 标签不存在

```
"Why can't I pull my-app:v1.2.0? It shows 'manifest unknown'."
```

### 场景 35: 配额超限

```
"I'm hitting Docker Hub rate limits. What are my options?"
```

**AI 会建议:**

- 升级到付费计划
- 使用认证拉取
- 配置本地缓存
- 使用镜像代理

## 📚 学习资源

### 场景 36: 学习最佳实践

```
"Show me examples of well-maintained Docker Hub repositories"
```

### 场景 37: 对比分析

```
"Compare the official nginx image with nginx:alpine. Which should I use?"
```

## 🎓 进阶技巧

### 使用过滤器

```
"List my repositories that:
- Are public
- Have more than 1000 pulls
- Were updated in the last month
- Are larger than 500MB"
```

### 批量操作

```
"For all my repositories starting with 'legacy-':
1. Add a deprecation notice
2. Make them private
3. Tag them with 'archived'"
```

### 自定义报告

```
"Generate a monthly report of:
- Total pull counts per repository
- New repositories created
- Storage usage trends
- Most active repositories"
```

---

## 💬 获取更多帮助

如果你有其他使用场景或问题:

1. 查看 [README.md](./README.md) 了解基础配置
2. 阅读 [Docker Hub 文档](https://docs.docker.com/docker-hub/)
3. 提交 [GitHub Issue](https://github.com/docker/hub-mcp/issues)

**记住: 使用自然语言描述你的需求,AI 会帮你完成! 🚀**
