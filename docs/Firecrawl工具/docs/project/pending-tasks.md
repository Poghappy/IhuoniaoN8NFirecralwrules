# 待办事项清单

> **创建时间**: 2025-01-27  
> **版本**: v1.0  
> **状态**: 📋 待处理

## 📋 概述

本文档列出所有需要手动完成的配置和任务，这些任务无法通过自动化工具完成，需要在 GitHub 网页端或本地手动配置。

## ✅ 已完成的自动化配置

以下配置已通过代码自动创建：

- [x] Issue 模板（Bug 报告、功能请求、问题咨询）
- [x] PR 模板
- [x] Dependabot 配置
- [x] CodeQL 安全扫描工作流
- [x] CI 工作流（已更新路径配置）
- [x] SECURITY.md 安全策略文档
- [x] LICENSE 许可证文件
- [x] CODEOWNERS 代码所有者配置

## 🔧 需要手动完成的配置

### 1. GitHub 仓库配置

#### 1.1 更新占位符信息

以下文件包含占位符，需要替换为实际值：

**`.github/CODEOWNERS`**
- 将所有 `@YOUR_USERNAME` 替换为实际的 GitHub 用户名或团队名称
- 示例：`* @zhiledeng` 或 `* @your-org/team-name`

**`.github/ISSUE_TEMPLATE/config.yml`**
- 将 `YOUR_USERNAME/YOUR_REPO` 替换为实际的仓库路径
- 示例：`https://github.com/zhiledeng/Hawaiihub.net/discussions`

**`SECURITY.md`**
- 将 `security@example.com` 替换为实际的安全联系邮箱
- 将 `YOUR_USERNAME/YOUR_REPO` 替换为实际的仓库路径

#### 1.2 分支保护规则

1. 进入仓库 **Settings > Branches**
2. 为 `main` 分支添加保护规则：
   - ✅ Require a pull request before merging
   - ✅ Require approvals: 1
   - ✅ Require status checks to pass before merging
     - 选择：`lint`, `test`, `docs`
   - ✅ Require branches to be up to date before merging
   - ✅ Do not allow bypassing the above settings
   - ✅ Restrict who can push to matching branches

3. 为 `develop` 分支添加保护规则（可选）：
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging

#### 1.3 标签配置

1. 进入仓库 **Issues > Labels**
2. 创建以下标签：

**类型标签**:
- `bug` - Bug 报告 (红色 `#d73a4a`)
- `feature` - 新功能 (绿色 `#0e8a16`)
- `enhancement` - 功能增强 (蓝色 `#0052cc`)
- `documentation` - 文档更新 (浅蓝色 `#0075ca`)
- `question` - 问题咨询 (黄色 `#d876e3`)

**优先级标签**:
- `priority: high` - 高优先级 (红色 `#b60205`)
- `priority: medium` - 中优先级 (橙色 `#fbca04`)
- `priority: low` - 低优先级 (黄色 `#e4e669`)

**状态标签**:
- `status: in-progress` - 进行中 (蓝色 `#1d76db`)
- `status: blocked` - 已阻塞 (红色 `#ee0701`)
- `status: needs-review` - 需要审查 (黄色 `#fef2c0`)
- `status: ready` - 就绪 (绿色 `#0e8a16`)

**技术标签**:
- `python` - Python 相关 (蓝色 `#0052cc`)
- `javascript` - JavaScript 相关 (黄色 `#d4c5f9`)
- `api` - API 相关 (紫色 `#7057ff`)
- `database` - 数据库相关 (灰色 `#ededed`)

**依赖标签**:
- `dependencies` - 依赖更新 (灰色 `#0366d6`)
- `github-actions` - GitHub Actions (黑色 `#000000`)

#### 1.4 仓库基础设置

1. 进入仓库 **Settings > General**
2. 配置以下选项：
   - **Repository name**: 确认仓库名称
   - **Description**: 添加项目描述
   - **Topics**: 添加相关主题标签（如：`firecrawl`, `web-scraping`, `automation`, `n8n`）
   - **Default branch**: 设置为 `main`
   - **Features**: 启用 Issues, Projects, Wiki（如需要）

#### 1.5 安全设置

1. 进入仓库 **Settings > Security**
2. 启用以下功能：
   - ✅ Dependency graph
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates
   - ✅ Code scanning
   - ✅ Secret scanning

### 2. 本地配置

#### 2.1 环境变量配置

如果项目使用环境变量，需要创建 `.env` 文件（不要提交到 Git）：

```bash
# 创建 .env 文件
touch .env

# 添加必要的环境变量
# 例如：
# DOCKER_HUB_PAT=your-token-here
# FIRECRAWL_API_KEY=your-key-here
# GITHUB_PERSONAL_ACCESS_TOKEN=your-token-here
```

确保 `.env` 已在 `.gitignore` 中。

#### 2.2 依赖安装

如果项目有依赖，需要安装：

```bash
# Python 依赖
cd docs/Firecrawl工具
pip install -r requirements.txt

# 或使用 uv/poetry
uv pip install -r requirements.txt
```

### 3. 验证配置

#### 3.1 验证 Issue 模板

1. 创建新 Issue
2. 确认可以看到模板选择器
3. 测试每个模板是否正常工作

#### 3.2 验证 PR 模板

1. 创建新 PR
2. 确认模板自动填充
3. 检查所有字段是否正确

#### 3.3 验证 CI 工作流

1. 推送代码到仓库
2. 检查 **Actions** 标签页
3. 确认工作流正常运行：
   - `lint` 任务
   - `test` 任务
   - `docs` 任务

#### 3.4 验证 CodeQL

1. 等待 CodeQL 分析完成（首次可能需要几分钟）
2. 检查 **Security** 标签页
3. 查看扫描结果

#### 3.5 验证 Dependabot

1. 等待 Dependabot 创建第一个 PR（可能需要几天）
2. 确认依赖更新 PR 格式正确
3. 检查自动标签是否正确应用

## 📝 配置优先级

### 高优先级（立即完成）

1. ✅ 更新占位符信息（CODEOWNERS、SECURITY.md、config.yml）
2. ✅ 配置分支保护规则
3. ✅ 启用安全设置

### 中优先级（本周完成）

4. ✅ 创建标签
5. ✅ 配置仓库基础设置
6. ✅ 验证所有配置

### 低优先级（可选）

7. ⏭️ 配置环境变量（如需要）
8. ⏭️ 安装本地依赖（如需要）

## 🔗 相关文档

- [GitHub 配置完整清单](./github-configuration-checklist.md)
- [GitHub 配置完成总结](./github-configuration-summary.md)
- [项目规则](./project-rules.md)

## ✅ 完成检查清单

- [ ] 更新 CODEOWNERS 中的用户名
- [ ] 更新 ISSUE_TEMPLATE/config.yml 中的仓库路径
- [ ] 更新 SECURITY.md 中的联系信息
- [ ] 配置 main 分支保护规则
- [ ] 配置 develop 分支保护规则（可选）
- [ ] 创建所有标签
- [ ] 配置仓库基础设置
- [ ] 启用安全设置
- [ ] 验证 Issue 模板
- [ ] 验证 PR 模板
- [ ] 验证 CI 工作流
- [ ] 验证 CodeQL
- [ ] 验证 Dependabot

---

**最后更新**: 2025-01-27  
**维护者**: AI Agent Team

