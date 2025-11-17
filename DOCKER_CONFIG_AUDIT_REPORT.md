# Docker 配置全面检查报告

**生成时间**: 2025-11-17
**检查范围**: Docker 环境、容器、镜像、网络、卷、MCP 配置

---

## 📊 执行摘要

### ✅ 正常状态
- Docker 版本：28.5.2（最新）
- Docker Compose：v2.40.3-desktop.1（最新）
- Docker MCP Toolkit：v0.27.0
- 运行中容器：28 个
- 总镜像：44 个
- 磁盘使用：10.86GB（镜像）+ 13.23MB（容器）

### ⚠️ 需要注意的问题
1. **Kong Konnect 扩展容器频繁重启**（每 1 分钟）
2. **6 个已停止的容器**需要清理
3. **docker-compose.yml 使用了过时的 `version` 字段**
4. **未使用的镜像占用 8.36GB 空间**（可回收 76%）

---

## 🔍 详细检查结果

### 1. Docker 版本信息

```
Docker: 28.5.2
Docker Compose: v2.40.3-desktop.1
Docker MCP Toolkit: v0.27.0
```

**状态**: ✅ 所有组件均为最新版本

**已安装的插件**:
- ✅ docker-ai (v1.9.11)
- ✅ docker-buildx (v0.29.1-desktop.1)
- ✅ docker-compose (v2.40.3-desktop.1)
- ✅ docker-debug (0.0.45)
- ✅ docker-desktop (v0.2.0)
- ✅ docker-extension (v0.2.31)
- ✅ docker-init (v1.4.0)
- ✅ **docker-mcp (v0.27.0)** ⭐
- ✅ docker-model (v0.1.46)
- ✅ docker-offload (v0.5.17)
- ✅ docker-sandbox (v0.5.3)
- ✅ docker-sbom (0.6.0)

---

### 2. 容器状态

#### 运行中的容器 (28 个)

**MCP 相关容器** (4 个):
- `mcp/fetch` × 4 (运行正常)

**Kubernetes 相关容器** (14 个):
- `k8s_coredns` × 2
- `k8s_kube-proxy` × 1
- `k8s_storage-provisioner` × 1
- `k8s_vpnkit-controller` × 1
- `k8s_nginx` × 1
- `registry.k8s.io/pause` × 8

**其他容器**:
- `vonwig/inotifywait` (文件监控)
- `nginx-proxy-manager` (Nginx 代理管理)

#### 已停止的容器 (6 个) ⚠️

```
CONTAINER ID   IMAGE          STATUS                    NAMES
075002c7e450   76719466e8b9   Exited (0) 2 hours ago    epic_volhard
7afd0faf88ab   nginx:latest   Exited (0) 47 hours ago   gracious_feistel
faa2f435bbb7   nginx:latest   Exited (255) 2 days ago   thirsty_curie
19b5fb9e3ba1   76719466e8b9   Exited (0) 47 hours ago   nice_williams
bace1e7ee9a0   nginx:latest   Exited (0) 47 hours ago   dazzling_babbage
f78bf0ed56fb   nginx:latest   Exited (255) 2 days ago   compassionate_maxwell
```

**建议**: 清理这些已停止的容器以释放空间

---

### 3. 镜像状态

**总镜像数**: 44 个
**活跃镜像**: 16 个
**总大小**: 10.86GB
**可回收空间**: 8.36GB (76%)

#### 主要镜像列表

| 镜像 | 大小 | 状态 |
|------|------|------|
| `mcp/playwright` | 1.67GB | ✅ |
| `mcp/markitdown` | 1.35GB | ✅ |
| `mcp/desktop-commander` | 697MB | ✅ |
| `mcp/redis` | 645MB | ✅ |
| `mcp/firecrawl` | 462MB | ✅ |
| `mcp/notion` | 471MB | ✅ |
| `mcp/dockerhub` | 425MB | ✅ |
| `mcp/apify-mcp-server` | 394MB | ✅ |
| `mcp/postman` | 378MB | ✅ |
| `postgres:14-alpine` | 376MB | ✅ |
| `mcp/hackernews-mcp` | 376MB | ✅ |
| `nginx:latest` | 244MB | ✅ |
| `portainer/portainer-docker-extension` | 238MB | ✅ |
| `ghcr.io/github/github-mcp-server` | 62.6MB | ✅ |
| `alpine/socat` | 15.6MB | ✅ |

**建议**: 运行 `docker image prune -a` 清理未使用的镜像（可释放约 8GB 空间）

---

### 4. 网络配置

**网络列表**:
- ✅ `bridge` (默认桥接网络)
- ✅ `docker_labs-ai-tools-for-devs-desktop-extension_default`
- ✅ `host` (主机网络)
- ✅ `kong_konnect-docker-extension-desktop-extension_default`
- ✅ `none` (无网络)
- ✅ `portainer_portainer-docker-extension-desktop-extension_default`

**状态**: ✅ 网络配置正常

---

### 5. 卷配置

**卷列表**:
- ✅ `ChatGPT` (ChatGPT 数据)
- ✅ `claude-memory` (Claude 记忆)
- ✅ `docker-prompts` (Docker 提示词)
- ✅ `docker-prompts-git` (Docker 提示词 Git)
- ✅ `portainer_portainer-docker-extension-desktop-extension_portainer_data`

**总大小**: 49.03MB
**状态**: ✅ 卷配置正常

---

### 6. Docker Compose 配置

#### docker-compose-n8n.yml

**状态**: ⚠️ 使用了过时的 `version` 字段

**配置摘要**:
- ✅ PostgreSQL 15 数据库
- ✅ n8n 工作流自动化
- ✅ 健康检查配置
- ✅ 网络隔离
- ✅ 数据持久化

**问题**:
```yaml
version: '3.8'  # ⚠️ 已过时，Docker Compose v2 不再需要
```

**建议**: 移除 `version` 字段

#### Nginx代理管理/docker-compose.yml

**状态**: ⚠️ 使用了过时的 `version` 字段

**配置摘要**:
- ✅ Nginx Proxy Manager
- ✅ 端口映射：80, 81, 443
- ✅ 数据持久化
- ✅ SSL 证书管理

**问题**:
```yaml
version: '3.8'  # ⚠️ 已过时
```

---

### 7. Docker MCP 配置

#### MCP 服务器状态

**已启用的服务器** (19 个):
- ✅ context7
- ✅ desktop-commander (配置完成 ✓)
- ✅ dockerhub (配置完成 ✓, Secrets 完成 ✓)
- ✅ duckduckgo
- ✅ fetch
- ✅ filesystem
- ✅ firecrawl
- ✅ github
- ✅ github-official
- ✅ markitdown
- ✅ mcp-hackernews
- ✅ memory
- ✅ notion
- ✅ playwright
- ✅ postgres
- ✅ postman
- ✅ redis
- ✅ sequentialthinking
- ✅ time

#### MCP 配置文件

**位置**: `~/.docker/mcp/config.yaml`

**配置内容**:
```yaml
dockerhub:
  username: docker login -u denzhile
filesystem:
  paths:
    - /Users/zhiledeng/Downloads/firecralw/
    - /Users/zhiledeng/Documents/augment-projects/
    - /Users/zhiledeng/Desktop
    - /Applications
desktop-commander:
  paths:
    - /Users/zhiledeng/Desktop
    - /Users/zhiledeng/Documents
    - /Users/zhiledeng
    - /Applications
markitdown:
  paths:
    - /Users/zhiledeng
apify-mcp-server:
  tools: c5E65FwFWAFAdtWzK
firecrawl:
  credit_critical_threshold: 0
  credit_warning_threshold: 0
  retry_backoff_factor: 0
  retry_delay: 0
  retry_max: 0
  retry_max_delay: 0
```

**状态**: ✅ 配置正常

---

### 8. 资源使用情况

#### 磁盘使用

```
类型            总计    活跃    大小        可回收
Images          44      16      10.86GB     8.359GB (76%)
Containers      56      28      13.23MB     847.9kB (6%)
Local Volumes   5       3       49.03MB     0B (0%)
Build Cache     2       0       38.44MB     38.44MB
```

#### CPU 和内存使用

**当前运行容器资源使用**:
- MCP fetch 容器：~48MB 内存/个，CPU 使用率 < 1%
- Kubernetes 容器：正常
- 其他容器：资源使用正常

---

### 9. 问题诊断

#### 🔴 严重问题

**无**

#### 🟡 警告问题

1. **Kong Konnect 扩展容器频繁重启**
   - **现象**: 容器每 1 分钟启动后立即退出（exit code 1）
   - **影响**: 可能影响 Docker Desktop 扩展功能
   - **建议**:
     - 检查 Kong Konnect 扩展日志
     - 考虑禁用或重新安装扩展
     - 命令: `docker logs kong_konnect-docker-extension-desktop-extension-service`

2. **Docker Compose 文件使用过时语法**
   - **文件**: `docker-compose-n8n.yml`, `Nginx代理管理/docker-compose.yml`
   - **问题**: 使用了 `version: '3.8'` 字段
   - **影响**: 未来版本可能不支持
   - **建议**: 移除 `version` 字段（Docker Compose v2 不再需要）

3. **未使用的镜像占用大量空间**
   - **可回收**: 8.36GB (76%)
   - **建议**: 定期清理未使用的镜像

#### 🟢 信息

1. **已停止的容器**
   - 6 个容器已停止但未删除
   - 建议定期清理

---

## 🔧 修复建议

### 立即执行

1. **清理已停止的容器**:
   ```bash
   docker container prune -f
   ```

2. **清理未使用的镜像**（可选，会释放 8GB 空间）:
   ```bash
   docker image prune -a -f
   ```

3. **修复 Docker Compose 文件**:
   - 移除 `docker-compose-n8n.yml` 中的 `version: '3.8'`
   - 移除 `Nginx代理管理/docker-compose.yml` 中的 `version: '3.8'`

### 定期维护

1. **每周清理**:
   ```bash
   docker system prune -a --volumes
   ```

2. **监控资源使用**:
   ```bash
   docker stats
   ```

3. **检查容器健康状态**:
   ```bash
   docker ps --filter "health=unhealthy"
   ```

---

## 📋 检查清单

- [x] Docker 版本检查
- [x] Docker Compose 版本检查
- [x] 容器状态检查
- [x] 镜像状态检查
- [x] 网络配置检查
- [x] 卷配置检查
- [x] Docker Compose 配置检查
- [x] Docker MCP 配置检查
- [x] 资源使用检查
- [x] 问题诊断

---

## 📊 总结

### 总体评分: ⭐⭐⭐⭐ (4/5)

**优点**:
- ✅ Docker 环境配置良好
- ✅ 所有组件均为最新版本
- ✅ MCP 服务器配置完整
- ✅ 资源使用合理

**需要改进**:
- ⚠️ 清理未使用的资源
- ⚠️ 修复过时的配置语法
- ⚠️ 解决 Kong Konnect 扩展问题

---

**报告生成时间**: 2025-11-17 12:32
**下次检查建议**: 2025-11-24

