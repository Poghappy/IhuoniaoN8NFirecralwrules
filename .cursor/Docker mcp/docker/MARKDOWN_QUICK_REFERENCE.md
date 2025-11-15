# Markdown 快速参考卡片

## ⚡ 快捷键

| 操作               | macOS            | Windows/Linux  |
| ------------------ | ---------------- | -------------- |
| 保存并自动格式化   | `Cmd+S`          | `Ctrl+S`       |
| 手动格式化整个文档 | `Shift+Option+F` | `Shift+Alt+F`  |
| 查看所有问题       | `Cmd+Shift+M`    | `Ctrl+Shift+M` |
| 打开命令面板       | `Cmd+Shift+P`    | `Ctrl+Shift+P` |

## 📝 链接锚点规范

```markdown
## 🔧 故障排查

✅ [查看故障排查](#-故障排查)
❌ [查看故障排查](#🔧-故障排查)
⚠️ [查看故障排查](#故障排查)
```

## 🔧 禁用的规则

| 规则  | 说明         |
| ----- | ------------ |
| MD013 | 行长度限制   |
| MD029 | 有序列表前缀 |
| MD033 | HTML 标签    |
| MD034 | 裸 URL       |
| MD036 | 强调标题     |
| MD040 | 代码块语言   |
| MD041 | 首行标题     |
| MD051 | 链接片段     |

## 🎯 常用操作

### 忽略特定规则

```markdown
<!-- markdownlint-disable MD013 -->

很长的一行文本

<!-- markdownlint-enable MD013 -->
```

### 忽略整个文件

```markdown
<!-- markdownlint-disable -->

文件内容...

<!-- markdownlint-enable -->
```

## 📦 必需扩展

- Prettier - Code formatter (`esbenp.prettier-vscode`)
- markdownlint (`DavidAnson.vscode-markdownlint`)

## 🔍 故障排查

### 保存时没有自动格式化？

1. 检查 Prettier 扩展是否安装
2. 重启 Cursor
3. 检查 `.cursor/config.json` 中 `markdown.formatOnSave` 是否为 `true`

### Markdownlint 不工作？

1. 检查 markdownlint 扩展是否安装
2. 查看输出日志：View → Output → markdownlint
3. 重启 Cursor

### 链接锚点失效？

1. 使用格式：`#-标题`（包含 emoji）
2. 在 GitHub 上测试验证
3. 参考 [MARKDOWN_BEST_PRACTICES.md](../MARKDOWN_BEST_PRACTICES.md)

## 📚 详细文档

- [MARKDOWN_SETUP.md](./MARKDOWN_SETUP.md) - 完整配置说明
- [CURSOR_MARKDOWN_CONFIG_SUMMARY.md](../CURSOR_MARKDOWN_CONFIG_SUMMARY.md) - 配置总结
- [MARKDOWN_CONFIG.md](../MARKDOWN_CONFIG.md) - 自动修复配置
- [MARKDOWN_BEST_PRACTICES.md](../MARKDOWN_BEST_PRACTICES.md) - 最佳实践

---

**提示：** 按 `Cmd+S` 保存此文件，查看自动格式化效果！
