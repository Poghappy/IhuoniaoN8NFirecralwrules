# Cursor Markdown 配置完成

## ✅ 已完成的配置

### 1. Cursor 配置文件更新

已在 `.cursor/config.json` 中添加完整的 Markdown 配置：

```json
{
  "markdown": {
    "enabled": true,
    "formatOnSave": true,
    "defaultFormatter": "prettier",
    "linting": {
      "enabled": true,
      "tool": "markdownlint",
      "autoFix": true,
      "runOnSave": true
    },
    "rules": {
      "MD013": false, // 行长度限制
      "MD029": false, // 有序列表前缀
      "MD033": false, // HTML 标签
      "MD034": false, // 裸 URL
      "MD036": false, // 强调标题
      "MD040": false, // 代码块语言
      "MD041": false, // 首行标题
      "MD051": false // 链接片段
    },
    "prettier": {
      "printWidth": 100,
      "proseWrap": "preserve",
      "tabWidth": 2,
      "useTabs": false
    },
    "linkValidation": {
      "enabled": true,
      "checkAnchors": true,
      "emojiInAnchors": true
    },
    "codeBlocks": {
      "requireLanguage": false,
      "syntaxHighlighting": true
    }
  }
}
```

### 2. README 文档更新

已在 `.cursor/README.md` 中添加 Markdown 使用指南：

- ✅ 功能特性说明
- ✅ 已禁用规则列表
- ✅ 使用方法说明
- ✅ 手动格式化快捷键
- ✅ 链接锚点规范
- ✅ 参考文档链接

## 🎯 核心功能

### 自动格式化

**触发方式：**

- 保存文件时自动触发（`Cmd+S` / `Ctrl+S`）
- Prettier 格式化代码风格
- Markdownlint 修复语法问题

**格式化内容：**

- 统一缩进（2 个空格）
- 规范列表格式
- 优化代码块
- 调整行长度（100 字符）
- 保持中文排版（不自动换行）

### 语法检查

**自动修复：**

- 标题格式
- 列表缩进
- 代码块格式
- 链接格式
- 表格对齐

**已禁用的规则：**

- MD013 - 行长度限制（中文需要灵活性）
- MD029 - 有序列表前缀（允许不同风格）
- MD033 - HTML 标签（允许使用 HTML）
- MD034 - 裸 URL（允许显示完整 URL）
- MD036 - 强调标题（允许粗体强调）
- MD040 - 代码块语言（不强制指定）
- MD041 - 首行标题（不强制要求）
- MD051 - 链接片段（避免 emoji 误报）

### 链接验证

**支持的链接类型：**

- 内部锚点链接（支持 emoji）
- 相对路径链接
- 绝对路径链接
- 外部 URL

**Emoji 锚点规范：**

```markdown
## 🔧 故障排查

[查看故障排查](#-故障排查) ✅ 正确
[查看故障排查](#🔧-故障排查) ❌ 错误
```

## 🚀 使用方法

### 基础使用

1. **自动格式化**

   ```
   编辑 .md 文件 → 按 Cmd+S 保存 → 自动格式化
   ```

2. **手动格式化**

   ```
   Shift+Alt+F (Windows/Linux)
   Shift+Option+F (macOS)
   ```

3. **格式化选中部分**
   ```
   选中文本 → 右键 → Format Selection
   ```

### 高级功能

1. **查看所有问题**

   ```
   Cmd+Shift+M (macOS)
   Ctrl+Shift+M (Windows/Linux)
   ```

2. **忽略特定规则**

   ```markdown
   <!-- markdownlint-disable MD013 -->

   这是一个很长的行，不会触发警告

   <!-- markdownlint-enable MD013 -->
   ```

3. **忽略整个文件**
   ```markdown
   <!-- markdownlint-disable -->

   整个文件的内容...

   <!-- markdownlint-enable -->
   ```

## 📋 配置清单

### 必需的 VS Code/Cursor 扩展

- [ ] **Prettier - Code formatter** (`esbenp.prettier-vscode`)
- [ ] **markdownlint** (`DavidAnson.vscode-markdownlint`)

### 安装命令

```bash
# 方法 1: 使用命令行
code --install-extension esbenp.prettier-vscode
code --install-extension DavidAnson.vscode-markdownlint

# 方法 2: 在 Cursor 中
# 1. 打开 Extensions (Cmd+Shift+X)
# 2. 搜索并安装 "Prettier" 和 "markdownlint"
```

### 配置文件

- [x] `.cursor/config.json` - Cursor 主配置
- [x] `.markdownlint.json` - Markdownlint 规则
- [x] `.prettierrc.json` - Prettier 格式化规则
- [x] `.vscode/settings.json` - 项目级编辑器设置

## 🔧 故障排查

### 问题 1: 保存时没有自动格式化

**解决方案：**

1. 检查 `.cursor/config.json` 中 `markdown.formatOnSave` 是否为 `true`
2. 确认已安装 Prettier 扩展
3. 重启 Cursor

### 问题 2: Markdownlint 不工作

**解决方案：**

1. 确认已安装 markdownlint 扩展
2. 检查 `.cursor/config.json` 中 `markdown.linting.enabled` 是否为 `true`
3. 查看输出日志：View → Output → 选择 `markdownlint`

### 问题 3: 链接锚点失效

**解决方案：**

1. 使用正确的 emoji 锚点格式：`#-标题`
2. 确认 `.cursor/config.json` 中 `markdown.linkValidation.emojiInAnchors` 为 `true`
3. 参考 [MARKDOWN_BEST_PRACTICES.md](../MARKDOWN_BEST_PRACTICES.md)

### 问题 4: 中文排版异常

**解决方案：**

1. 确认 `.cursor/config.json` 中 `markdown.prettier.proseWrap` 为 `"preserve"`
2. 禁用 MD013 规则（行长度限制）
3. 使用 Prettier 的中文排版优化

## 📚 参考文档

### 项目文档

- [MARKDOWN_CONFIG.md](../MARKDOWN_CONFIG.md) - 详细配置说明
- [MARKDOWN_BEST_PRACTICES.md](../MARKDOWN_BEST_PRACTICES.md) - 最佳实践指南
- [.cursor/README.md](./README.md) - .cursor 目录说明

### 官方文档

- [Prettier 官方文档](https://prettier.io/docs/en/)
- [Markdownlint 规则列表](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [VS Code Markdown 支持](https://code.visualstudio.com/docs/languages/markdown)
- [Cursor 文档](https://docs.cursor.com/)

### 工具

- [markdown-link-check](https://github.com/tcort/markdown-link-check) - 链接有效性检查
- [remark-validate-links](https://github.com/remarkjs/remark-validate-links) - Remark 插件
- [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) - 命令行工具

## ✅ 验证配置

### 1. 检查扩展

```
Cmd+Shift+P → Extensions: Show Installed Extensions
```

确认已安装：

- ✅ Prettier - Code formatter
- ✅ markdownlint

### 2. 测试自动格式化

1. 创建测试文件 `test.md`
2. 添加格式问题：

   ```markdown
   #标题没有空格
   这是一个很长很长很长很长很长很长很长很长很长很长的行
   ```

3. 按 `Cmd+S` 保存
4. 检查是否自动修复

### 3. 测试链接锚点

1. 创建测试文件：

   ```markdown
   ## 🔧 测试标题

   [链接](#-测试标题)
   ```

2. 点击链接验证跳转
3. 在 GitHub 上测试

## 🎉 配置完成

现在你的 Markdown 文件将会：

✅ 保存时自动格式化
✅ 自动修复语法问题
✅ 验证链接有效性
✅ 支持 emoji 锚点
✅ 优化中文排版
✅ 统一代码风格

开始编写高质量的 Markdown 文档吧！🚀

---

**更新时间：** 2025-11-01
**版本：** v1.0.0
