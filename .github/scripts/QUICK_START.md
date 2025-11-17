# GitHub 配置快速开始指南

> **创建时间**: 2025-01-27
> **预计完成时间**: 15-20 分钟

本指南提供最快速的配置步骤，帮助你完成 GitHub 仓库的基础配置。

## 🚀 快速执行清单

### 步骤 1: 创建 GitHub 标签（5 分钟）

#### 方式一：使用脚本（推荐）

1. **获取 GitHub Personal Access Token**
   - 访问：https://github.com/settings/tokens
   - 点击 **Generate new token** > **Generate new token (classic)**
   - 设置权限：✅ `repo` (完整仓库访问权限)
   - 点击 **Generate token** 并复制 token

2. **运行脚本**
   ```bash
   # 设置 Token（临时，仅当前终端会话有效）
   export GITHUB_TOKEN=your_token_here

   # 运行脚本
   cd /Users/zhiledeng/Movies/Hawaiihub.net
   ./.github/scripts/create-labels.sh
   ```

3. **验证结果**
   - 访问：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/labels
   - 确认所有标签已创建

#### 方式二：手动创建（如果脚本失败）

访问：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/labels/new

按照以下列表逐个创建：

| 标签名称 | 描述 | 颜色代码 |
|---------|------|---------|
| `bug` | Bug 报告 | `#d73a4a` |
| `feature` | 新功能 | `#0e8a16` |
| `enhancement` | 功能增强 | `#0052cc` |
| `documentation` | 文档更新 | `#0075ca` |
| `question` | 问题咨询 | `#d876e3` |
| `priority: high` | 高优先级 | `#b60205` |
| `priority: medium` | 中优先级 | `#fbca04` |
| `priority: low` | 低优先级 | `#e4e669` |
| `status: in-progress` | 进行中 | `#1d76db` |
| `status: blocked` | 已阻塞 | `#ee0701` |
| `status: needs-review` | 需要审查 | `#fef2c0` |
| `status: ready` | 就绪 | `#0e8a16` |
| `python` | Python 相关 | `#0052cc` |
| `javascript` | JavaScript 相关 | `#d4c5f9` |
| `api` | API 相关 | `#7057ff` |
| `database` | 数据库相关 | `#ededed` |
| `dependencies` | 依赖更新 | `#0366d6` |
| `github-actions` | GitHub Actions | `#000000` |

### 步骤 2: 配置分支保护规则（5 分钟）

1. **访问分支设置**
   - 打开：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/settings/branches

2. **配置 main 分支保护**
   - 点击 **Add rule**
   - **Branch name pattern**: 输入 `main`
   - 勾选以下选项：
     - ✅ **Require a pull request before merging**
       - ✅ Require approvals: `1`
     - ✅ **Require status checks to pass before merging**
       - ✅ Require branches to be up to date before merging
       - 在状态检查中选择：`lint`, `test`, `docs`
     - ✅ **Require conversation resolution before merging**
     - ✅ **Do not allow bypassing the above settings**
     - ✅ **Restrict who can push to matching branches**（可选）
   - 点击 **Create** 保存

3. **配置 develop 分支保护**（可选）
   - 点击 **Add rule**
   - **Branch name pattern**: 输入 `develop`
   - 勾选：
     - ✅ **Require a pull request before merging**
     - ✅ **Require status checks to pass before merging**
   - 点击 **Create** 保存

### 步骤 3: 启用安全设置（3 分钟）

1. **访问安全设置**
   - 打开：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/settings/security_analysis

2. **启用功能**
   - ✅ **Dependency graph** - 点击 **Enable**
   - ✅ **Dependabot alerts** - 点击 **Enable**
   - ✅ **Dependabot security updates** - 点击 **Enable**
   - ✅ **Code scanning** - 点击 **Set up** > **Set up this workflow**
   - ✅ **Secret scanning** - 点击 **Enable**

### 步骤 4: 配置仓库基础设置（2 分钟）

1. **访问仓库设置**
   - 打开：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/settings

2. **更新仓库信息**
   - **Description**: 输入
     ```
     HawaiiHub Firecrawl × 火鸟门户 × n8n 的采集与自动化运营仓库
     ```
   - **Topics**: 添加以下标签（每行一个）
     ```
     firecrawl
     web-scraping
     automation
     n8n
     python
     javascript
     data-collection
     ```
   - 点击 **Save changes**

3. **启用功能**
   - 在 **Features** 部分，确保以下功能已启用：
     - ✅ Issues
     - ✅ Projects
     - ✅ Wiki（可选）
     - ✅ Discussions（可选）

### 步骤 5: 验证配置（5 分钟）

#### 5.1 验证 Issue 模板

1. 访问：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/issues/new
2. 确认可以看到模板选择器
3. 测试每个模板是否正常工作

#### 5.2 验证 PR 模板

1. 创建一个测试分支并提交更改
2. 创建 Pull Request
3. 确认模板自动填充

#### 5.3 验证 CI 工作流

1. 推送代码到仓库
2. 访问 **Actions** 标签页
3. 确认工作流正常运行

## ✅ 完成检查清单

完成所有步骤后，请确认：

- [ ] 所有标签已创建（18 个标签）
- [ ] main 分支保护规则已配置
- [ ] develop 分支保护规则已配置（可选）
- [ ] 安全功能已全部启用
- [ ] 仓库描述和主题已设置
- [ ] Issue 模板正常工作
- [ ] PR 模板正常工作
- [ ] CI 工作流正常运行

## 🆘 遇到问题？

### 脚本执行失败

如果标签创建脚本失败，请检查：

1. **Token 权限**
   - 确保 Token 有 `repo` 权限
   - 确保 Token 未过期

2. **网络连接**
   - 检查是否能访问 GitHub API
   - 尝试手动创建标签

3. **查看详细错误**
   - 脚本会显示详细的错误信息
   - 检查 HTTP 状态码

### 分支保护规则无法保存

1. **权限检查**
   - 确保你有仓库管理员权限
   - 检查组织设置是否允许配置分支保护

2. **状态检查名称**
   - 确保状态检查名称正确：`lint`, `test`, `docs`
   - 如果名称不同，需要先运行一次 CI 工作流

### 安全设置无法启用

1. **仓库类型**
   - 某些功能可能仅适用于公开仓库
   - 检查仓库可见性设置

2. **组织限制**
   - 如果是组织仓库，检查组织策略
   - 可能需要组织管理员权限

## 📚 相关文档

- [完整配置指南](./manual-config-guide.md) - 详细的配置说明
- [标签创建脚本](./create-labels.sh) - 自动创建标签的脚本
- [待办事项清单](../../../docs/Firecrawl工具/docs/project/pending-tasks.md) - 所有待办任务

## 🎯 下一步

完成基础配置后，建议：

1. **创建第一个 Issue** 测试模板
2. **创建第一个 PR** 测试工作流
3. **查看 CodeQL 扫描结果** 了解代码质量
4. **配置 Dependabot** 自动更新依赖

---

**最后更新**: 2025-01-27
**维护者**: AI Agent Team

