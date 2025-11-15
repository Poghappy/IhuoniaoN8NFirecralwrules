# Markdown 链接锚点最佳实践

## 📚 问题背景

在 Markdown 文档中使用包含 emoji 的标题时，内部链接锚点的生成规则会导致链接失效。

### 常见错误

```markdown
## 🔧 故障排查

[查看故障排查](#🔧-故障排查)  ❌ 错误
```

## ✅ 解决方案

### 方案 1: 包含 emoji 的锚点（推荐）

GitHub 和大多数 Markdown 渲染器会保留 emoji，但需要包含 emoji 和空格：

```markdown
## 🔧 故障排查

[查看故障排查](#-故障排查)  ✅ 正确
```

**规则:**

- 保留 emoji 符号
- emoji 后的空格会被转换为 `-`
- 中文字符保持不变

### 方案 2: 移除 emoji（最兼容）

完全移除 emoji，只使用文字：

```markdown
## 🔧 故障排查

[查看故障排查](#故障排查)  ✅ 正确（某些环境）
```

### 方案 3: 使用自定义 ID

使用 HTML 注释或属性指定自定义 ID：

```markdown
## 🔧 故障排查 {#troubleshooting}

[查看故障排查](#troubleshooting)  ✅ 正确
```

## 🔍 锚点生成规则

### GitHub Flavored Markdown (GFM)

1. **转换为小写** - 所有字符转换为小写
2. **移除特殊字符** - 移除标点符号（保留 emoji）
3. **空格转短横线** - 空格替换为 `-`
4. **保留中文** - 中文字符保持不变
5. **保留 emoji** - emoji 符号保持不变

### 示例对照表

| 标题 | GitHub 锚点 | VS Code 锚点 |
|------|-------------|--------------|
| `## 🔧 故障排查` | `#-故障排查` | `#-故障排查` |
| `## 📦 仓库管理` | `#-仓库管理` | `#-仓库管理` |
| `## Hello World` | `#hello-world` | `#hello-world` |
| `## API 接口` | `#api-接口` | `#api-接口` |
| `## v2.0 更新` | `#v20-更新` | `#v20-更新` |

## 🛠️ 配置建议

### 1. 禁用链接片段检查

在 `.markdownlint.json` 中禁用 MD051：

```json
{
  "MD051": false
}
```

### 2. 使用一致的命名规范

**推荐规范:**

```markdown
## 🔧 故障排查
## 📦 仓库管理
## 🏷️ 标签管理
```

**链接写法:**

```markdown
[故障排查](#-故障排查)
[仓库管理](#-仓库管理)
[标签管理](#️-标签管理)
```

### 3. 测试链接有效性

使用工具验证链接：

```bash
# 使用 markdown-link-check
npx markdown-link-check README.md

# 使用 remark-validate-links
npx remark-validate-links README.md
```

## 📝 实战示例

### 示例 1: 目录链接

```markdown
# 文档标题

## 📋 目录

- [快速开始](#-快速开始)
- [配置说明](#-配置说明)
- [故障排查](#-故障排查)

## 🚀 快速开始

内容...

## ⚙️ 配置说明

内容...

## 🔧 故障排查

内容...
```

### 示例 2: 跨文件链接

```markdown
<!-- 在 README.md 中 -->
详见 [配置指南](./CONFIG.md#-配置步骤)

<!-- 在 CONFIG.md 中 -->
## ⚙️ 配置步骤

内容...
```

### 示例 3: 多级标题

```markdown
## 🔧 故障排查

### 问题 1: Docker 未安装

[返回故障排查](#-故障排查)

### 问题 2: 认证失败

[返回故障排查](#-故障排查)
```

## 🎯 最佳实践总结

### ✅ 推荐做法

1. **统一使用 emoji + 空格 + 文字** 的标题格式
2. **链接中包含 emoji** (如 `#-故障排查`)
3. **禁用 MD051 规则** 避免误报
4. **使用工具验证** 确保链接有效
5. **保持一致性** 团队统一规范

### ❌ 避免做法

1. ~~emoji 和文字之间没有空格~~ (`##🔧故障排查`)
2. ~~链接中使用完整 emoji 文本~~ (`#🔧-故障排查`)
3. ~~混用不同的命名风格~~
4. ~~不测试链接有效性~~

## 🔧 故障排查

### 问题 1: 链接无法跳转

**症状:** 点击链接后页面不跳转或跳转到错误位置

**解决方案:**

1. 检查标题格式:

   ```markdown
   ## 🔧 故障排查  ✅ emoji 后有空格
   ##🔧故障排查   ❌ emoji 后没有空格
   ```

2. 检查链接格式:

   ```markdown
   [链接](#-故障排查)    ✅ 包含 emoji
   [链接](#🔧-故障排查)  ❌ 完整 emoji
   [链接](#故障排查)     ⚠️ 某些环境可用
   ```

3. 使用浏览器开发者工具检查实际生成的 ID:

   ```javascript
   // 在浏览器控制台执行
   document.querySelectorAll('h2, h3').forEach(h => {
     console.log(h.textContent, '→', h.id);
   });
   ```

### 问题 2: VS Code 显示链接错误

**症状:** VS Code 提示 "No header found"

**解决方案:**

1. 更新 VS Code Markdown 扩展
2. 禁用 MD051 规则
3. 使用自定义 ID:

   ```markdown
   ## 🔧 故障排查 {#troubleshooting}
   [链接](#troubleshooting)
   ```

### 问题 3: GitHub 和本地渲染不一致

**症状:** 本地预览正常，GitHub 上链接失效

**解决方案:**

1. 使用 GitHub 的锚点生成规则
2. 在 GitHub 上测试验证
3. 使用 GitHub Actions 自动检查:

   ```yaml
   - name: Check Markdown links
     uses: gaurav-nelson/github-action-markdown-link-check@v1
   ```

## 📚 参考资源

### 官方文档

- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
- [CommonMark Spec](https://spec.commonmark.org/)
- [Markdown Guide](https://www.markdownguide.org/)

### 工具

- [markdown-link-check](https://github.com/tcort/markdown-link-check) - 链接有效性检查
- [remark-validate-links](https://github.com/remarkjs/remark-validate-links) - Remark 插件
- [markdownlint](https://github.com/DavidAnson/markdownlint) - Markdown 语法检查

### 相关 Issues

- [vscode-markdown #807](https://github.com/yzhang-gh/vscode-markdown/issues/807) - 特殊字符标题
- [vscode-markdown #98](https://github.com/yzhang-gh/vscode-markdown/issues/98) - Emoji 标题
- [vscode-markdown #792](https://github.com/yzhang-gh/vscode-markdown/issues/792) - Emoji 链接

## 🎓 学习资源

### 快速参考

```markdown
# 标题格式
## 🔧 故障排查           # 推荐：emoji + 空格 + 文字
## 故障排查              # 可选：纯文字

# 链接格式
[链接](#-故障排查)      # 推荐：包含 emoji
[链接](#故障排查)       # 可选：移除 emoji
[链接](#troubleshooting) # 可选：自定义 ID

# 跨文件链接
[链接](./file.md#-标题)  # 相对路径
[链接](/path/file.md#-标题) # 绝对路径
```

### 测试模板

创建 `test-links.md` 测试文件：

```markdown
# 链接测试

## 📋 目录

- [测试 1](#-测试-1)
- [测试 2](#-测试-2)
- [测试 3](#-测试-3)

## 🔧 测试 1

[返回目录](#-目录)

## 📦 测试 2

[返回目录](#-目录)

## 🏷️ 测试 3

[返回目录](#-目录)
```

## ✅ 检查清单

配置完成后，确认以下项目：

- [ ] 所有标题使用统一格式（emoji + 空格 + 文字）
- [ ] 所有内部链接包含正确的 emoji
- [ ] 已禁用 MD051 规则
- [ ] 已在 GitHub 上测试链接
- [ ] 已在 VS Code 中测试链接
- [ ] 已添加链接检查工具
- [ ] 团队成员了解规范

## 🎉 总结

**核心要点:**

1. 标题格式: `## 🔧 故障排查` (emoji + 空格 + 文字)
2. 链接格式: `[链接](#-故障排查)` (包含 emoji)
3. 禁用规则: `"MD051": false`
4. 保持一致: 团队统一规范

遵循这些最佳实践，你的 Markdown 文档链接将在所有环境中正常工作! 🚀
