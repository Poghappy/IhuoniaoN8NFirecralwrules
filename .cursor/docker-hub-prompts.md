# Docker Hub MCP Server - AI 提示词库

## 📝 提示词分类

### 1. 镜像搜索

#### 基础搜索

```
搜索 Docker Hub 上的官方 nginx 镜像
Search for official nginx images on Docker Hub
```

```
查找最新的 Python 3.11 镜像
Find the latest Python 3.11 images
```

```
显示所有 Node.js LTS 镜像
Show me all Node.js LTS images
```

#### 高级搜索

```
搜索星标数超过 1000 的 PostgreSQL 镜像
Search for PostgreSQL images with more than 1000 stars
```

```
查找官方的、支持 ARM 架构的 Redis 镜像
Find official Redis images that support ARM architecture
```

```
搜索最近更新的 Ubuntu 镜像，按更新时间排序
Search for recently updated Ubuntu images, sorted by update time
```

### 2. 仓库管理

#### 列出仓库

```
列出我的所有 Docker Hub 仓库
List all my Docker Hub repositories
```

```
显示我的公开仓库
Show my public repositories
```

```
查看我的私有仓库列表
View my private repository list
```

#### 仓库详情

```
显示 my-app 仓库的详细信息
Show details for my-app repository
```

```
获取 nginx 仓库的统计信息
Get statistics for nginx repository
```

```
查看 my-service 仓库的协作者
View collaborators for my-service repository
```

#### 创建仓库

```
创建一个名为 my-service 的新仓库
Create a new repository named my-service
```

```
创建一个私有仓库 my-private-app，包含描述
Create a private repository my-private-app with description
```

### 3. 标签操作

#### 列出标签

```
显示 nginx 仓库的所有标签
Show all tags for nginx repository
```

```
获取 my-app 的最新标签
Get the latest tag for my-app
```

```
列出按日期排序的标签
List tags sorted by date
```

#### 标签详情

```
显示 my-app:v1.0.0 标签的详细信息
Show details for my-app:v1.0.0 tag
```

```
获取 nginx:alpine 的镜像层信息
Get image layers for nginx:alpine
```

```
查看 my-service:latest 的构建历史
View build history for my-service:latest
```

### 4. 镜像操作

#### 拉取镜像

```
拉取最新的 postgres 镜像
Pull the latest postgres image
```

```
下载 redis:7-alpine 镜像
Download redis:7-alpine image
```

```
获取 mysql:8.0 镜像
Get mysql:8.0 image
```

#### 推送镜像

```
推送 my-app:v1.0.0 到 Docker Hub
Push my-app:v1.0.0 to Docker Hub
```

```
上传本地镜像 my-service:latest
Upload local image my-service:latest
```

#### 标签操作

```
将本地镜像标记为 my-app:latest
Tag local image as my-app:latest
```

```
为 my-service 创建新标签 v2.0.0
Create new tag v2.0.0 for my-service
```

### 5. 自动化工作流

#### 构建和推送

```
构建并推送 my-app 的新版本
Build and push new version of my-app
```

```
自动化构建 my-service 并推送到 Docker Hub
Automate build of my-service and push to Docker Hub
```

#### 批量操作

```
批量拉取所有 Python 3.x 镜像
Batch pull all Python 3.x images
```

```
批量更新我的所有仓库的描述
Batch update descriptions for all my repositories
```

### 6. 监控和分析

#### 统计信息

```
显示我的仓库的下载统计
Show download statistics for my repositories
```

```
获取 my-app 的星标和拉取次数
Get stars and pull count for my-app
```

```
分析我的镜像使用趋势
Analyze my image usage trends
```

#### 健康检查

```
检查我的所有镜像是否有安全漏洞
Check all my images for security vulnerabilities
```

```
验证我的令牌是否仍然有效
Verify if my token is still valid
```

## 🎯 场景化提示词

### 场景 1: 新项目启动

```
我要开始一个新的 Node.js 项目，帮我：
1. 搜索最新的 Node.js LTS 官方镜像
2. 创建一个名为 my-nodejs-app 的新仓库
3. 设置仓库为公开，添加描述 "My awesome Node.js application"
```

### 场景 2: 镜像更新

```
我需要更新 my-app 镜像，帮我：
1. 检查当前 my-app 的所有标签
2. 构建新版本并标记为 v1.1.0
3. 推送到 Docker Hub
4. 同时更新 latest 标签
```

### 场景 3: 安全审计

```
帮我进行安全审计：
1. 列出我的所有仓库
2. 检查每个仓库的最新标签
3. 识别超过 6 个月未更新的镜像
4. 检查是否有已知的安全漏洞
```

### 场景 4: 清理工作

```
帮我清理旧镜像：
1. 列出我的所有仓库和标签
2. 识别超过 1 年未使用的标签
3. 生成删除命令列表（但不执行）
4. 提供清理建议
```

### 场景 5: 迁移项目

```
我要将项目从 GitLab 迁移到 Docker Hub，帮我：
1. 创建新的 Docker Hub 仓库
2. 配置自动构建
3. 设置 webhook 通知
4. 迁移所有历史标签
```

## 💡 提示词优化技巧

### 1. 明确性

```
❌ 不好：搜索镜像
✅ 好：搜索 Docker Hub 上星标数超过 1000 的官方 nginx 镜像
```

### 2. 上下文

```
❌ 不好：推送镜像
✅ 好：将本地构建的 my-app:v1.0.0 镜像推送到我的 Docker Hub 仓库
```

### 3. 步骤化

```
✅ 好：
1. 首先搜索 Python 3.11 镜像
2. 然后显示前 5 个结果的详细信息
3. 最后推荐最适合生产环境的镜像
```

### 4. 约束条件

```
✅ 好：
搜索 PostgreSQL 镜像，要求：
- 官方镜像
- 支持 ARM64 架构
- 星标数 > 500
- 最近 3 个月内更新过
```

## 🔍 调试提示词

### 问题诊断

```
我的 MCP Server 无法连接到 Docker Hub，帮我：
1. 检查令牌是否有效
2. 验证网络连接
3. 查看错误日志
4. 提供解决方案
```

### 性能分析

```
我的镜像搜索很慢，帮我：
1. 分析当前的缓存配置
2. 检查 API 调用次数
3. 识别性能瓶颈
4. 提供优化建议
```

## 📚 学习提示词

### 了解功能

```
解释 Docker Hub MCP Server 的以下功能：
1. 镜像搜索的工作原理
2. 缓存机制如何提升性能
3. 如何处理 API 速率限制
```

### 最佳实践

```
教我 Docker Hub MCP Server 的最佳实践：
1. 如何安全地管理访问令牌
2. 如何优化镜像搜索性能
3. 如何处理大量并发请求
```

## 🎨 自定义提示词模板

### 模板 1: 镜像搜索

```
搜索 [镜像名称] 镜像，要求：
- 类型：[official/verified/community]
- 架构：[amd64/arm64/arm/...]
- 最小星标：[数字]
- 更新时间：[时间范围]
```

### 模板 2: 仓库操作

```
对 [仓库名称] 执行以下操作：
1. [操作 1]
2. [操作 2]
3. [操作 3]
并提供详细的执行结果
```

### 模板 3: 批量处理

```
批量处理我的仓库：
- 筛选条件：[条件]
- 执行操作：[操作]
- 错误处理：[策略]
- 生成报告：[格式]
```

---

**提示：使用清晰、具体的提示词可以获得更好的结果！**
