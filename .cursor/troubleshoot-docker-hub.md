# Docker Hub MCP Server 故障排查

请帮我诊断和解决 Docker Hub MCP Server 的问题。

## 🔍 诊断步骤

### 1. 配置检查

- 验证 `.cursor/mcp.json` 文件格式是否正确
- 检查 JSON 语法是否有错误
- 确认 MCP Server 路径是否存在
- 验证环境变量设置（DOCKER_HUB_PAT）
- 检查配置文件权限

### 2. 连接测试

- 测试网络连接到 Docker Hub API
- 验证 API 端点可访问性（https://hub.docker.com/v2/）
- 检查防火墙和代理设置
- 测试 DNS 解析

### 3. 认证验证

- 确认 Docker Hub PAT 有效性
- 检查 PAT 是否过期
- 验证 PAT 权限范围
- 测试 PAT 是否被撤销

### 4. 日志分析

- 查看 Cursor 日志（帮助 > 显示日志）
- 检查 MCP Server 日志
- 分析错误消息和堆栈跟踪
- 查找警告和异常

### 5. 权限验证

- 确认 PAT 具有必要的权限
- 检查仓库访问权限
- 验证命名空间权限
- 测试读写权限

## 🛠️ 常见问题和解决方案

### 问题 1：认证失败

**症状**：401 Unauthorized 错误

**可能原因**：

- PAT 过期或无效
- PAT 权限不足
- 环境变量未设置

**解决方案**：

1. 重新生成 Docker Hub PAT
2. 更新 `.cursor/mcp.json` 中的配置
3. 重启 Cursor

### 问题 2：连接超时

**症状**：请求超时或无响应

**可能原因**：

- 网络问题
- 代理配置错误
- Docker Hub API 故障

**解决方案**：

1. 检查网络连接
2. 配置代理设置
3. 查看 Docker Hub 状态页面

### 问题 3：权限不足

**症状**：403 Forbidden 错误

**可能原因**：

- PAT 权限范围不足
- 尝试访问私有仓库
- 组织权限限制

**解决方案**：

1. 更新 PAT 权限
2. 验证仓库访问权限
3. 联系组织管理员

### 问题 4：速率限制

**症状**：429 Too Many Requests 错误

**可能原因**：

- API 调用频率过高
- 超过 Docker Hub 限制

**解决方案**：

1. 实现请求缓存
2. 增加请求间隔
3. 升级 Docker Hub 计划

### 问题 5：MCP Server 未启动

**症状**：命令不可用或无响应

**可能原因**：

- MCP Server 路径错误
- 依赖未安装
- 配置文件错误

**解决方案**：

1. 验证 MCP Server 路径
2. 安装必要依赖
3. 检查配置文件语法

## 📊 诊断命令

运行以下命令收集诊断信息：

```bash
# 检查配置文件
cat .cursor/mcp.json

# 测试 Docker Hub API
curl -H "Authorization: Bearer YOUR_PAT" https://hub.docker.com/v2/users/YOUR_USERNAME

# 检查环境变量
echo $DOCKER_HUB_PAT

# 查看 Cursor 日志
# 在 Cursor 中：帮助 > 显示日志
```

## 🔧 修复验证

修复后，请验证：

1. [ ] MCP Server 可以正常启动
2. [ ] 认证成功
3. [ ] 可以搜索镜像
4. [ ] 可以列出仓库
5. [ ] 可以查看标签
6. [ ] 错误日志清空

## 📝 报告要求

请提供以下信息：

1. **问题描述**：详细说明遇到的问题
2. **错误信息**：完整的错误消息和堆栈跟踪
3. **配置信息**：相关配置（隐藏敏感信息）
4. **环境信息**：操作系统、Cursor 版本
5. **重现步骤**：如何重现问题
6. **已尝试的解决方案**：已经尝试过的修复方法

请提供详细的诊断报告和具体的解决方案。
