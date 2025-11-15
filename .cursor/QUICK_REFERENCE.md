# Cursor 配置快速参考

> 一页纸速查手册 - 打印或保存到桌面

## 🎯 核心原则

**单一配置源**: 只在 `.cursor/` 维护配置，不要在其他地方创建

## 📁 目录结构

```text
.cursor/
├── rules/          # 规则文件 (.mdc)
├── prompts/        # 提示词模板
└── context/        # 项目上下文
```

## 🔧 常用命令

```bash
# 健康检查
./scripts/check-cursor-config.sh

# 查看规则列表
ls .cursor/rules/

# 添加新规则
touch .cursor/rules/new-rule.mdc

# 重新加载 Cursor
Cmd + Shift + P → "Reload Window"
```

## 📝 规则文件模板

```markdown
---
alwaysApply: true
description: 规则描述
---

# 规则标题

## 核心原则
- 原则1
- 原则2

## 示例

### ✅ 正确
\`\`\`
正确代码
\`\`\`

### ❌ 错误
\`\`\`
错误代码
\`\`\`
```

## 🤖 提示词技巧

```text
# 引用上下文
@context/architecture.md
请根据架构设计新功能

# 引用文件
@file:src/main.py
请优化这个文件

# 使用模板
@prompts/code-review.md
请审查以下代码
```

## ✅ 配置变更流程

1. 团队讨论 → 2. 本地测试 → 3. 提交 PR → 4. 审查合并

## 🚫 禁止事项

- ❌ 在子目录创建 `.cursor/`
- ❌ 复制配置到多个位置
- ❌ 不运行健康检查就提交

## 📚 文档导航

| 文档 | 用途 |
|------|------|
| `README.md` | 配置说明 |
| `STRUCTURE_GUIDE.md` | 详细指南 |
| `TEAM_GUIDE.md` | 团队协作 |
| `QUICK_REFERENCE.md` | 本文档 |

## 🐛 问题排查

**规则不生效？**
1. 检查文件在 `.cursor/rules/`
2. 重启 Cursor
3. 查看控制台错误

**配置冲突？**
1. 运行健康检查
2. 查看检查报告
3. 联系维护者

## 📞 获取帮助

- 💬 团队群: [配置讨论群]
- 📧 邮件: config-team@example.com
- 🐛 Issues: GitHub

---

**快速参考 v1.0** | 2025-11-02

