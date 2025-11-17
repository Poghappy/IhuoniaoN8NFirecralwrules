# GitHub 手动配置指南

> **创建时间**: 2025-01-27
> **版本**: v1.0

本指南提供在 GitHub 网页端手动完成配置的详细步骤。

## 📋 前置要求

- GitHub 账户管理员权限
- 访问仓库设置权限

## 🔧 配置步骤

### 1. 分支保护规则

#### 1.1 配置 main 分支保护

1. 访问仓库：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules
2. 点击 **Settings** > **Branches**
3. 在 **Branch protection rules** 部分，点击 **Add rule**
4. 在 **Branch name pattern** 中输入：`main`
5. 配置以下选项：

   ✅ **Require a pull request before merging**
   - ✅ Require approvals: `1`
   - ✅ Dismiss stale pull request approvals when new commits are pushed

   ✅ **Require status checks to pass before merging**
   - ✅ Require branches to be up to date before merging
   - 在 **Status checks that are required** 中选择：
     - `lint`
     - `test`
     - `docs`

   ✅ **Require conversation resolution before merging**

   ✅ **Do not allow bypassing the above settings**

   ✅ **Restrict who can push to matching branches**
   - 添加管理员账户

6. 点击 **Create** 保存

#### 1.2 配置 develop 分支保护（可选）

1. 在 **Branch protection rules** 部分，点击 **Add rule**
2. 在 **Branch name pattern** 中输入：`develop`
3. 配置以下选项：

   ✅ **Require a pull request before merging**
   - ✅ Require status checks to pass before merging

4. 点击 **Create** 保存

### 2. 创建标签

#### 2.1 使用脚本创建（推荐）

```bash
# 设置 GitHub Token
export GITHUB_TOKEN=your_github_token_here

# 运行脚本
chmod +x .github/scripts/create-labels.sh
./github/scripts/create-labels.sh
```

#### 2.2 手动创建标签

1. 访问：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/labels
2. 点击 **New label**
3. 按照以下列表创建标签：

**类型标签**:
- `bug` - Bug 报告 (颜色: `#d73a4a`)
- `feature` - 新功能 (颜色: `#0e8a16`)
- `enhancement` - 功能增强 (颜色: `#0052cc`)
- `documentation` - 文档更新 (颜色: `#0075ca`)
- `question` - 问题咨询 (颜色: `#d876e3`)

**优先级标签**:
- `priority: high` - 高优先级 (颜色: `#b60205`)
- `priority: medium` - 中优先级 (颜色: `#fbca04`)
- `priority: low` - 低优先级 (颜色: `#e4e669`)

**状态标签**:
- `status: in-progress` - 进行中 (颜色: `#1d76db`)
- `status: blocked` - 已阻塞 (颜色: `#ee0701`)
- `status: needs-review` - 需要审查 (颜色: `#fef2c0`)
- `status: ready` - 就绪 (颜色: `#0e8a16`)

**技术标签**:
- `python` - Python 相关 (颜色: `#0052cc`)
- `javascript` - JavaScript 相关 (颜色: `#d4c5f9`)
- `api` - API 相关 (颜色: `#7057ff`)
- `database` - 数据库相关 (颜色: `#ededed`)

**依赖标签**:
- `dependencies` - 依赖更新 (颜色: `#0366d6`)
- `github-actions` - GitHub Actions (颜色: `#000000`)

### 3. 仓库基础设置

1. 访问 **Settings** > **General**
2. 配置以下选项：

   **Repository name**: `IhuoniaoN8NFirecralwrules`

   **Description**: 添加项目描述，例如：
   ```
   HawaiiHub Firecrawl × 火鸟门户 × n8n 的采集与自动化运营仓库
   ```

   **Topics**: 添加以下主题标签：
   - `firecrawl`
   - `web-scraping`
   - `automation`
   - `n8n`
   - `python`
   - `javascript`
   - `data-collection`

   **Default branch**: `main`

   **Features**: 启用以下功能：
   - ✅ Issues
   - ✅ Projects
   - ✅ Wiki（可选）
   - ✅ Discussions（可选）

### 4. 安全设置

1. 访问 **Settings** > **Security**
2. 在 **Code security and analysis** 部分，启用以下功能：

   ✅ **Dependency graph**
   - 点击 **Enable** 启用依赖图

   ✅ **Dependabot alerts**
   - 点击 **Enable** 启用 Dependabot 警报

   ✅ **Dependabot security updates**
   - 点击 **Enable** 启用自动安全更新

   ✅ **Code scanning**
   - 点击 **Set up** 配置代码扫描
   - 选择 **Set up this workflow** 使用默认配置

   ✅ **Secret scanning**
   - 点击 **Enable** 启用密钥扫描

### 5. 验证配置

#### 5.1 验证 Issue 模板

1. 访问：https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/issues/new
2. 确认可以看到模板选择器
3. 测试每个模板：
   - Bug 报告
   - 功能请求
   - 问题咨询

#### 5.2 验证 PR 模板

1. 创建一个测试分支
2. 提交一些更改
3. 创建 Pull Request
4. 确认模板自动填充
5. 检查所有字段是否正确

#### 5.3 验证 CI 工作流

1. 推送代码到仓库
2. 访问 **Actions** 标签页
3. 确认工作流正常运行：
   - `lint` 任务
   - `test` 任务
   - `docs` 任务

#### 5.4 验证 CodeQL

1. 等待 CodeQL 分析完成（首次可能需要几分钟）
2. 访问 **Security** > **Code scanning alerts**
3. 查看扫描结果

#### 5.5 验证 Dependabot

1. 等待 Dependabot 创建第一个 PR（可能需要几天）
2. 确认依赖更新 PR 格式正确
3. 检查自动标签是否正确应用

## 🔐 GitHub Token 获取

如果需要使用脚本创建标签，需要获取 GitHub Personal Access Token：

1. 访问：https://github.com/settings/tokens
2. 点击 **Generate new token** > **Generate new token (classic)**
3. 设置以下权限：
   - ✅ `repo` (完整仓库访问权限)
4. 点击 **Generate token**
5. 复制生成的 token（只显示一次）

```bash
export GITHUB_TOKEN=your_token_here
```

## ✅ 配置检查清单

- [ ] main 分支保护规则已配置
- [ ] develop 分支保护规则已配置（可选）
- [ ] 所有标签已创建
- [ ] 仓库描述和主题已设置
- [ ] 安全功能已启用
- [ ] Issue 模板已验证
- [ ] PR 模板已验证
- [ ] CI 工作流已验证
- [ ] CodeQL 已验证
- [ ] Dependabot 已验证

## 📚 相关文档

- [GitHub 分支保护规则文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub 标签管理文档](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- [GitHub 安全功能文档](https://docs.github.com/en/code-security)

---

**最后更新**: 2025-01-27
**维护者**: AI Agent Team

