# Docker Hub MCP Server - Cursor Rules 最佳实践指南

## 📚 文档来源

本指南综合了以下优质资源：

1. **GitHub 社区实践**

   - [ssdeanx/deep-research-mcp-server](https://github.com/ssdeanx/deep-research-mcp-server) - MCP 深度研究服务器
   - [jkarir/cursor-task-sync](https://github.com/jkarir/cursor-task-sync) - MCP 任务同步系统

2. **官方文档**

   - [Docker MCP Server Best Practices](https://www.docker.com/blog/mcp-server-best-practices/)
   - [Docker Hub MCP Server Manual](https://hub.docker.com/mcp/server/dockerhub/manual)
   - [Apidog Docker-Hub MCP Guide](https://apidog.com/blog/how-to-use-the/)

3. **社区最佳实践**
   - [Cursor Rules Best Practices](https://medium.com/elementor-engineers/cursor-rules-best-practices-for-developers-16a438a4935c)

## 🎯 核心原则

### 1. 简单优先 (Simplicity First)

**来自 cursor-task-sync 项目的核心理念：**

> "Focus on simplicity and practical value over premature optimization or overengineering. Build a clean, maintainable solution that solves the core problems effectively without unnecessary complexity."

**应用到 Docker Hub MCP Server：**

```markdown
# .cursorrules

## 开发哲学

### 简单性原则

- ✅ 优先选择直接实现而非复杂架构
- ✅ 只在有明确收益时才增加复杂度
- ✅ 记录技术决策的理由
- ✅ 考虑开发者体验和可维护性

### 避免过早优化

- 从简单的实现开始
- 在优化前先测量性能
- 只优化已证实的瓶颈
- 优先实用性而非理论完美
```

### 2. 项目文档化 (Project Documentation)

**来自 deep-research-mcp-server 的结构化文档方法：**

```markdown
# .cursorrules

@project-documentation(projectName: "Docker Hub MCP Server Configuration") {

@section(name: "Project Overview", level: 1) {
@project-overview {
@short-description: "**Docker Hub MCP Server: 您的 Docker 镜像管理助手。** 通过 MCP 协议连接 Cursor AI 与 Docker Hub，实现智能化的镜像搜索、仓库管理和标签操作。"

      @mcp-tool-availability: "**无缝集成 AI Agent。** 作为 Model Context Protocol (MCP) 工具，可轻松集成到 Cursor、Claude 等 AI 系统中。"

      @core-features: "**核心功能。** 镜像搜索、仓库列表、标签管理、镜像拉取/推送、自动化工作流。"

      @goal: "**保持简单，保持高效。** 提供最简单但最有效的 Docker Hub 管理实现，设计清晰易于扩展。"
    }

}

@section(name: "Key Features", level: 1) {
@features-section {
@feature(name: "MCP Integration", description: "**MCP 就绪：** 无缝集成为 Model Context Protocol 工具，提供即插即用的 Docker Hub 管理能力。")

      @feature(name: "Intelligent Search", description: "**智能搜索：** 通过 AI 驱动的查询生成，精准定位所需的 Docker 镜像。")

      @feature(name: "Repository Management", description: "**仓库管理：** 完整的仓库 CRUD 操作，包括创建、读取、更新和删除。")

      @feature(name: "Tag Operations", description: "**标签操作：** 查看、管理和操作 Docker 镜像标签。")

      @feature(name: "Automated Workflows", description: "**自动化工作流：** 支持镜像构建、测试和部署的自动化流程。")
    }

}
}
```

### 3. 配置管理 (Configuration Management)

**综合最佳实践的配置结构：**

````markdown
# .cursorrules

## 配置系统

### MCP Server 配置

```typescript
interface DockerHubMCPConfig {
  // 服务器设置
  server: {
    port: number;
    logLevel: "debug" | "info" | "warn" | "error";
    timeout: number;
  };

  // Docker Hub 认证
  dockerHub: {
    token: string; // Docker Hub 个人访问令牌
    username: string; // Docker Hub 用户名
    namespace: string; // 默认命名空间
  };

  // MCP 协议设置
  mcp: {
    protocol: "stdio" | "http";
    version: "1.0";
    capabilities: string[];
  };

  // 缓存策略
  cache: {
    enabled: boolean;
    ttl: number; // 缓存生存时间（秒）
    maxSize: number; // 最大缓存大小（MB）
    useEtags: boolean; // 使用 ETags 优化
  };

  // 响应设置
  response: {
    defaultLimit: number; // 默认返回数量
    maxLimit: number; // 最大返回数量
    includeMetadata: boolean; // 是否包含元数据
    defaultFields: string[]; // 默认返回字段
  };

  // 安全设置
  security: {
    rateLimit: {
      enabled: boolean;
      maxRequests: number; // 每分钟最大请求数
      windowMs: number; // 时间窗口（毫秒）
    };
    tokenRotation: {
      enabled: boolean;
      intervalDays: number; // 令牌轮换间隔（天）
    };
  };
}
```
````

### 环境变量配置

```bash
# .env.example

# Docker Hub 配置
DOCKER_HUB_PAT=dckr_pat_YOUR_TOKEN_HERE
DOCKER_HUB_USERNAME=your_username
DOCKER_HUB_NAMESPACE=your_namespace

# MCP Server 配置
MCP_SERVER_PORT=3000
MCP_LOG_LEVEL=info
MCP_TIMEOUT=30000

# 缓存配置
CACHE_ENABLED=true
CACHE_TTL=300
CACHE_MAX_SIZE=100
CACHE_USE_ETAGS=true

# 安全配置
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_REQUESTS=100
RATE_LIMIT_WINDOW_MS=60000
```

````

## 🔧 实战配置示例

### 示例 1: 基础 Docker Hub MCP Server 配置

```markdown
# .cursorrules

## Docker Hub MCP Server 规则

### 核心原则
1. **优先更新而非创建** - 避免创建重复文件
2. **使用 MCP 工具** - 优先使用 MCP 执行 Docker Hub 操作
3. **保持简单** - 避免过早优化
4. **安全第一** - 永不提交敏感信息

### MCP 工具使用指南

#### 搜索镜像
````

"Search for official nginx images on Docker Hub"
"Find the latest Python 3.11 images"
"Show me all Node.js LTS images"

```

#### 管理仓库
```

"List all my Docker Hub repositories"
"Show details for my-app repository"
"Create a new repository named my-service"

```

#### 标签操作
```

"Show all tags for nginx repository"
"Get the latest tag for my-app"
"List tags sorted by date"

```

#### 镜像操作
```

"Pull the latest postgres image"
"Push my-app:v1.0.0 to Docker Hub"
"Tag local image as my-app:latest"

````

### 开发规范

#### 文件操作
- ✅ 读取文件前先检查是否存在
- ✅ 更新现有文件而非创建新文件
- ✅ 使用版本控制跟踪变更
- ❌ 不要创建临时文件后不清理
- ❌ 不要随意创建重复配置文件

#### 错误处理
```typescript
try {
  // Docker Hub API 调用
  const result = await dockerHub.searchImages(query);
  return result;
} catch (error) {
  console.error("Docker Hub API Error:", error);
  // 提供有意义的错误信息
  throw new Error(`Failed to search images: ${error.message}`);
}
````

#### 日志记录

```typescript
// 使用结构化日志
logger.info("Searching Docker Hub", {
  query: searchQuery,
  filters: appliedFilters,
  timestamp: new Date().toISOString(),
});
```

### 安全最佳实践

#### 令牌管理

- ✅ 使用环境变量存储 Docker Hub PAT
- ✅ 定期轮换访问令牌（每 3-6 个月）
- ✅ 使用最小权限原则
- ❌ 永不在代码中硬编码令牌
- ❌ 永不提交 `.env` 文件到 Git

#### 配置文件保护

```gitignore
# .gitignore

# 环境变量
.env
.env.local
.env.*.local

# MCP 配置（包含令牌）
.cursor/mcp.json

# 敏感日志
*.log
logs/
```

### 性能优化

#### 缓存策略

```typescript
// 简单的内存缓存
class SimpleCache {
  private cache = new Map<string, { data: any; expiry: number }>();

  async get(key: string): Promise<any> {
    const entry = this.cache.get(key);
    if (entry && entry.expiry > Date.now()) {
      return entry.data;
    }
    return null;
  }

  set(key: string, data: any, ttlSeconds: number = 300): void {
    this.cache.set(key, {
      data,
      expiry: Date.now() + ttlSeconds * 1000,
    });
  }
}
```

#### API 调用优化

- ✅ 使用缓存减少 API 调用
- ✅ 批量操作而非单个请求
- ✅ 实现请求去重
- ✅ 遵守 Docker Hub API 速率限制

### 测试规范

#### 单元测试

```typescript
describe("Docker Hub MCP Server", () => {
  it("should search images successfully", async () => {
    const result = await dockerHub.searchImages("nginx");
    expect(result).toBeDefined();
    expect(result.length).toBeGreaterThan(0);
  });

  it("should handle API errors gracefully", async () => {
    await expect(dockerHub.searchImages("")).rejects.toThrow("Invalid search query");
  });
});
```

### Git 提交规范

使用 Conventional Commits：

```bash
# 功能
feat: 添加镜像搜索功能
feat: 🐳 支持多标签推送

# 修复
fix: 修复令牌过期问题
fix: 🐛 解决缓存失效 bug

# 文档
docs: 更新 MCP 配置说明
docs: 📝 添加安全最佳实践

# 重构
refactor: 优化 API 调用逻辑
refactor: ♻️ 简化错误处理流程

# 性能
perf: 实现请求缓存
perf: ⚡️ 优化镜像搜索速度

# 测试
test: 添加 API 集成测试
test: ✅ 完善错误处理测试
```

### 文档规范

#### 必需章节

1. **快速开始** - 5 分钟上手
2. **完整指南** - 详细配置说明
3. **API 参考** - 所有 MCP 工具说明
4. **故障排查** - 常见问题解决
5. **安全指南** - 安全配置和最佳实践

#### Markdown 格式

```markdown
## 🔧 配置 MCP Server

### 步骤 1: 获取 Docker Hub 令牌

访问 [Docker Hub Settings](https://hub.docker.com/settings/security)

### 步骤 2: 配置环境变量

\`\`\`bash

# 创建 .env 文件

DOCKER_HUB_PAT=your_token_here
\`\`\`

### 步骤 3: 启动 MCP Server

\`\`\`bash
npm run start
\`\`\`
```

### 故障排查

#### 常见问题

**问题 1: MCP Server 未加载**

```bash
# 检查配置文件
cat .cursor/mcp.json

# 检查日志
tail -f logs/mcp-server.log

# 重启 Cursor
```

**问题 2: Docker Hub 认证失败**

```bash
# 验证令牌
docker login -u username -p token

# 检查令牌权限
# 确保令牌有 repo:read 和 repo:write 权限
```

**问题 3: 缓存数据过期**

```bash
# 清除缓存
rm -rf .cache/

# 或在代码中手动清除
cache.clear();
```

### 监控和日志

#### 日志级别

```typescript
const logLevels = {
  debug: 0, // 详细调试信息
  info: 1, // 一般信息
  warn: 2, // 警告信息
  error: 3, // 错误信息
};

// 生产环境使用 info 或 warn
const LOG_LEVEL = process.env.LOG_LEVEL || "info";
```

#### 监控指标

- API 调用次数
- 响应时间
- 错误率
- 缓存命中率
- 令牌使用情况

### 扩展性设计

#### 插件系统

```typescript
interface MCPPlugin {
  name: string;
  version: string;
  init(config: any): Promise<void>;
  execute(command: string, args: any): Promise<any>;
}

class PluginManager {
  private plugins = new Map<string, MCPPlugin>();

  register(plugin: MCPPlugin): void {
    this.plugins.set(plugin.name, plugin);
  }

  async execute(pluginName: string, command: string, args: any): Promise<any> {
    const plugin = this.plugins.get(pluginName);
    if (!plugin) {
      throw new Error(`Plugin not found: ${pluginName}`);
    }
    return await plugin.execute(command, args);
  }
}
```

### 检查清单

#### 开发前

- [ ] 阅读项目文档
- [ ] 配置开发环境
- [ ] 获取 Docker Hub 令牌
- [ ] 配置 `.env` 文件
- [ ] 测试 MCP Server 连接

#### 代码提交前

- [ ] 代码格式化（Prettier/ESLint）
- [ ] 类型检查通过（TypeScript）
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 文档已更新
- [ ] Commit 消息符合规范
- [ ] 没有敏感信息
- [ ] 没有 TODO 注释

#### 部署前

- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 性能测试完成
- [ ] 安全扫描通过
- [ ] 文档完整
- [ ] 变更日志更新
- [ ] 备份现有配置

````

### 示例 2: 高级 MCP Server 配置（带 Webhook）

```markdown
# .cursorrules

## 高级 Docker Hub MCP Server 配置

### Webhook 集成

#### 配置 Webhook
```typescript
interface WebhookConfig {
  enabled: boolean;
  secret: string;
  events: string[];
  endpoint: string;
}

const webhookConfig: WebhookConfig = {
  enabled: true,
  secret: process.env.WEBHOOK_SECRET,
  events: ['push', 'build', 'tag'],
  endpoint: '/api/v1/docker/webhook'
};
````

#### Webhook 处理

```typescript
app.post("/api/v1/docker/webhook", async (req, res) => {
  // 验证 webhook 签名
  if (!verifyWebhookSignature(req, webhookConfig.secret)) {
    return res.status(401).send("Unauthorized");
  }

  const event = req.headers["x-dockerhub-event"] as string;
  const payload = req.body;

  // 处理事件
  await processDockerHubEvent(event, payload);

  res.status(200).send("Received");
});
```

### 实时同步

#### 缓存失效

```typescript
async function handlePushEvent(payload: any): Promise<void> {
  const { repository, tag } = payload;

  // 使缓存失效
  cache.invalidate(`repo:${repository.name}`);
  cache.invalidate(`tags:${repository.name}`);

  // 通知 AI Agent
  await notifyAgent({
    type: "image_updated",
    repository: repository.name,
    tag: tag.name,
  });
}
```

### 监控和告警

#### Prometheus 指标

```typescript
import { Counter, Histogram } from "prom-client";

const apiCallsTotal = new Counter({
  name: "dockerhub_api_calls_total",
  help: "Total number of Docker Hub API calls",
  labelNames: ["method", "status"],
});

const apiDuration = new Histogram({
  name: "dockerhub_api_duration_seconds",
  help: "Docker Hub API call duration in seconds",
  labelNames: ["method"],
});
```

#### 告警规则

```yaml
# alerts.yml

groups:
  - name: docker_hub_mcp
    rules:
      - alert: HighErrorRate
        expr: rate(dockerhub_api_calls_total{status="error"}[5m]) > 0.1
        annotations:
          summary: "High error rate detected"

      - alert: SlowAPIResponse
        expr: dockerhub_api_duration_seconds{quantile="0.99"} > 5
        annotations:
          summary: "API response time is slow"
```

```

## 📊 配置对比

### 基础配置 vs 高级配置

| 特性 | 基础配置 | 高级配置 |
|------|---------|---------|
| MCP 集成 | ✅ | ✅ |
| 缓存 | ✅ 内存缓存 | ✅ Redis 缓存 |
| Webhook | ❌ | ✅ |
| 监控 | ❌ | ✅ Prometheus |
| 告警 | ❌ | ✅ Alertmanager |
| 负载均衡 | ❌ | ✅ |
| 高可用 | ❌ | ✅ |

### 何时使用哪种配置

**使用基础配置：**
- 个人开发项目
- 小团队（< 5 人）
- API 调用量 < 1000/天
- 不需要实时同步

**使用高级配置：**
- 生产环境
- 大团队（> 10 人）
- API 调用量 > 10000/天
- 需要实时同步和监控

## 🎓 学习路径

### 新手入门（1-2 天）

1. **第 1 天：基础配置**
   - 阅读 `QUICK_START.md`
   - 配置 Docker Hub 令牌
   - 启动 MCP Server
   - 测试基本功能

2. **第 2 天：实战练习**
   - 搜索镜像
   - 管理仓库
   - 操作标签
   - 自动化工作流

### 进阶使用（3-5 天）

3. **第 3 天：高级功能**
   - 配置缓存策略
   - 实现错误重试
   - 优化性能

4. **第 4-5 天：集成和扩展**
   - Webhook 集成
   - 监控配置
   - 自定义插件

### 专家级（1-2 周）

5. **第 1 周：深度定制**
   - 自定义 MCP 工具
   - 实现高可用架构
   - 性能调优

6. **第 2 周：生产部署**
   - Docker 容器化
   - CI/CD 集成
   - 安全加固

## 🔗 相关资源

### 官方文档
- [Docker Hub API 文档](https://docs.docker.com/docker-hub/api/latest/)
- [MCP Protocol 规范](https://modelcontextprotocol.io/)
- [Cursor 文档](https://docs.cursor.com/)

### 社区资源
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)
- [Docker MCP Examples](https://github.com/docker/mcp-examples)
- [MCP Server 模板](https://github.com/modelcontextprotocol/servers)

### 工具和库
- [Docker SDK for Node.js](https://www.npmjs.com/package/dockerode)
- [MCP TypeScript SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- [Cursor MCP Client](https://www.npmjs.com/package/@cursor/mcp-client)

## ✅ 总结

### 核心要点

1. **简单优先** - 从简单实现开始，逐步优化
2. **安全第一** - 保护敏感信息，定期轮换令牌
3. **文档完善** - 清晰的文档是成功的关键
4. **测试充分** - 单元测试和集成测试都不可少
5. **监控到位** - 及时发现和解决问题

### 下一步行动

1. ✅ 阅读本指南
2. ✅ 配置基础 MCP Server
3. ✅ 测试核心功能
4. ⏭️ 根据需求选择高级功能
5. ⏭️ 持续优化和改进

---

**记住：优先更新现有文件，避免创建重复内容，使用 MCP 工具，参考项目文档！**

**立即开始使用 Docker Hub MCP Server 提升开发效率！🚀**

```
