# Cursor Slash Commands 故障排查指南

## 🔍 问题描述

在 Cursor 聊天输入框中输入 `/` 后，没有显示任何命令选项。

## 📚 官方文档说明

根据 Cursor 官方文档（https://cursor.com/cn/docs/agent/chat/commands），Slash Commands（斜杠命令）是 Cursor 2.0 的新功能，用于创建可复用的工作流。

### 命令的工作方式

当你在聊天输入框中输入 `/` 时，Cursor 会自动检测并显示来自以下三个位置的可用命令：

1. **项目命令**：存放在项目的 `.cursor/commands` 目录
2. **全局命令**：存放在主目录的 `~/.cursor/commands` 目录
3. **团队命令**：由团队管理员在 Cursor Dashboard 中创建（需要 Team/Enterprise 方案）

## 🎯 问题根因

**你的 `/` 命令没有内容的原因：当前项目和全局目录中都没有创建任何自定义命令文件。**

Cursor 不会自动提供内置命令（除了 `Summarize`），需要你手动创建命令文件。

## ✅ 解决方案

### 方案 1：创建项目级命令（推荐）

为当前 Docker Hub MCP Server 项目创建专属命令：

```bash
# 1. 创建命令目录
mkdir -p /Users/zhiledeng/Downloads/docker/.cursor/commands

# 2. 创建示例命令文件
cd /Users/zhiledeng/Downloads/docker/.cursor/commands
```

### 方案 2：创建全局命令

创建可在所有项目中使用的命令：

```bash
# 1. 创建全局命令目录
mkdir -p ~/.cursor/commands

# 2. 创建示例命令文件
cd ~/.cursor/commands
```

## 📝 推荐命令示例

### 1. 代码审查清单 (`code-review-checklist.md`)

```markdown
# 代码审查清单

请对当前更改进行全面的代码审查，检查以下方面：

## 代码质量

- [ ] 代码是否遵循项目的编码规范？
- [ ] 是否有重复代码可以重构？
- [ ] 变量和函数命名是否清晰？
- [ ] 是否有适当的注释？

## 功能性

- [ ] 代码是否实现了预期功能？
- [ ] 是否处理了边界情况？
- [ ] 错误处理是否完善？

## 安全性

- [ ] 是否存在安全漏洞？
- [ ] 敏感信息是否被正确保护？
- [ ] 输入验证是否充分？

## 性能

- [ ] 是否存在性能瓶颈？
- [ ] 是否有不必要的计算或查询？

## 测试

- [ ] 是否需要添加或更新测试？
- [ ] 测试覆盖率是否足够？

请提供详细的审查结果和改进建议。
```

### 2. Docker Hub MCP 测试 (`test-docker-mcp.md`)

```markdown
# Docker Hub MCP Server 测试

请执行以下测试步骤：

1. **配置检查**

   - 验证 `.cursor/mcp.json` 配置是否正确
   - 检查 Docker Hub PAT 是否已设置
   - 确认环境变量配置

2. **功能测试**

   - 测试镜像搜索功能
   - 测试仓库列表功能
   - 测试标签查询功能

3. **错误处理**

   - 测试无效令牌的处理
   - 测试网络错误的处理
   - 测试 API 限流的处理

4. **性能测试**
   - 检查缓存是否生效
   - 测试并发请求处理
   - 验证响应时间

请报告所有测试结果，包括成功和失败的情况。
```

### 3. 创建 PR (`create-pr.md`)

```markdown
# 创建拉取请求

请为当前更改创建一个详细的 Pull Request 描述，包含：

## 📝 更改摘要

简要描述本次 PR 的主要更改内容。

## 🎯 目的

说明为什么需要这些更改，解决了什么问题。

## 🔧 技术细节

- 主要更改的文件和模块
- 使用的技术和方法
- 重要的实现细节

## ✅ 测试

- 已执行的测试
- 测试结果
- 测试覆盖率

## 📸 截图/演示

如果适用，提供截图或演示。

## ⚠️ 注意事项

- 破坏性更改
- 依赖更新
- 配置变更
- 迁移步骤

## 🔗 相关 Issue

Closes #xxx
Related to #xxx

请使用 Conventional Commits 格式生成标题。
```

### 4. 安全审计 (`security-audit.md`)

```markdown
# 安全审计

请对当前代码进行安全审计，重点检查：

## 🔐 认证和授权

- [ ] API 密钥和令牌是否安全存储？
- [ ] 是否使用环境变量而非硬编码？
- [ ] 权限控制是否正确？

## 🛡️ 数据保护

- [ ] 敏感数据是否加密？
- [ ] 日志中是否暴露敏感信息？
- [ ] 数据传输是否使用 HTTPS？

## 🚨 漏洞检查

- [ ] 是否存在 SQL 注入风险？
- [ ] 是否存在 XSS 风险？
- [ ] 是否存在 CSRF 风险？
- [ ] 依赖包是否有已知漏洞？

## 📋 合规性

- [ ] 是否符合 GDPR/CCPA 要求？
- [ ] 是否有适当的审计日志？
- [ ] 错误消息是否泄露敏感信息？

请提供详细的安全评估报告和修复建议。
```

### 5. 运行测试并修复 (`run-tests-and-fix.md`)

```markdown
# 运行测试并修复失败

请执行以下步骤：

1. **运行所有测试**

   - 执行完整的测试套件
   - 记录所有失败的测试

2. **分析失败原因**

   - 查看错误日志
   - 识别根本原因
   - 确定影响范围

3. **修复问题**

   - 实现修复方案
   - 确保不引入新问题
   - 遵循最佳实践

4. **验证修复**

   - 重新运行失败的测试
   - 确保所有测试通过
   - 检查是否有副作用

5. **更新文档**
   - 如果需要，更新相关文档
   - 添加必要的注释

请报告完整的测试结果和修复过程。
```

### 6. Docker Hub 故障排查 (`troubleshoot-docker-hub.md`)

```markdown
# Docker Hub MCP Server 故障排查

请帮我诊断和解决 Docker Hub MCP Server 的问题：

## 🔍 诊断步骤

1. **配置检查**

   - 验证 MCP 配置文件格式
   - 检查环境变量设置
   - 确认 Docker Hub PAT 有效性

2. **连接测试**

   - 测试网络连接
   - 验证 API 端点可访问性
   - 检查防火墙设置

3. **日志分析**

   - 查看 Cursor 日志
   - 检查 MCP Server 日志
   - 分析错误消息

4. **权限验证**
   - 确认 PAT 权限范围
   - 检查仓库访问权限
   - 验证命名空间权限

## 🛠️ 常见问题

- **认证失败**：检查 PAT 是否过期或无效
- **连接超时**：检查网络和代理设置
- **权限不足**：验证 PAT 权限范围
- **速率限制**：检查 API 调用频率

请提供详细的诊断报告和解决方案。
```

## 🚀 快速创建命令

使用以下脚本快速创建所有推荐命令：

```bash
#!/bin/bash

# 创建命令目录
mkdir -p /Users/zhiledeng/Downloads/docker/.cursor/commands

# 定义命令目录
COMMANDS_DIR="/Users/zhiledeng/Downloads/docker/.cursor/commands"

# 创建命令文件（内容见上面的示例）
# 你可以手动创建，或者使用脚本批量创建
```

## 📖 使用方法

1. **创建命令文件后**，在 Cursor 聊天输入框中输入 `/`
2. **选择命令**：使用方向键浏览，按 `Enter` 选择
3. **添加参数**（可选）：在命令后添加额外的上下文

示例：

```
/code-review-checklist
/test-docker-mcp 测试搜索功能
/create-pr 这是一个重要的安全修复
```

## 🎯 命令目录结构

推荐的项目命令结构：

```
/Users/zhiledeng/Downloads/docker/
└── .cursor/
    └── commands/
        ├── code-review-checklist.md
        ├── test-docker-mcp.md
        ├── create-pr.md
        ├── security-audit.md
        ├── run-tests-and-fix.md
        ├── troubleshoot-docker-hub.md
        ├── update-docs.md
        └── setup-new-feature.md
```

## 💡 最佳实践

1. **命名规范**

   - 使用小写字母和连字符
   - 使用描述性名称
   - 避免过长的名称

2. **内容编写**

   - 使用清晰的 Markdown 格式
   - 包含具体的指令和检查清单
   - 提供上下文和示例

3. **团队协作**

   - 将命令文件提交到 Git
   - 在 README 中记录可用命令
   - 定期更新和优化命令

4. **版本控制**
   - 将 `.cursor/commands/` 目录加入 Git
   - 记录命令的更改历史
   - 与团队成员同步

## 🔗 相关资源

- [Cursor 官方文档 - Commands](https://cursor.com/cn/docs/agent/chat/commands)
- [Cursor 官方文档 - @ Symbols](https://cursor.com/cn/docs/context/symbols)
- [项目配置文档](./README.md)

## 📝 注意事项

1. **命令目前为测试版**：功能和语法可能会发生变化
2. **团队命令**：需要 Team 或 Enterprise 方案
3. **文件格式**：必须使用 `.md` 扩展名
4. **自动检测**：创建文件后，Cursor 会自动检测并显示命令

## ✅ 验证步骤

创建命令后，请验证：

1. [ ] 命令文件已创建在正确的目录
2. [ ] 文件扩展名为 `.md`
3. [ ] 文件内容格式正确
4. [ ] 在 Cursor 中输入 `/` 可以看到命令
5. [ ] 命令可以正常执行

---

**更新时间**：2025-11-01
**版本**：v1.0
**状态**：已验证
